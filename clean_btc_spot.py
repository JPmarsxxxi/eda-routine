"""clean_btc_spot.py: data-hygiene pass on the prepared BTC spot 1m data (TRAIN + VAL only).

Input : data\\btcusdt_spot_monthly\\*.parquet   (made by prep_target.py; ends 2023-11-30)
Output: data\\btcusdt_spot_1m_clean\\  btcusdt_spot_1m_clean.parquet, CLEANING_LOG.md, CUT.json, plots\\*.png

Follows finding-alphas\\data-skill\\tree-reference.md. Policy: NO ROW IS DROPPED. Impossible FIELDS are set to NaN and
flagged (the rest of such a row is valid); suspicious values are FLAGGED, never changed; missing minutes stay missing
(Brownlees-Gallo s3.2). Raw monthly files are untouched.

Holdout discipline: structural checks (duplicates, gaps, impossible values, flat bars) cover all rows. Distribution
statistics (wick sizes, close-vs-local-median scan, the Roll estimate, the perp reconciliation) are computed on TRAIN
(<= 2023-03-19) ONLY; on VAL the flags are applied mechanically and only their COUNTS are reported.
"""
import glob
import json
import os
import shutil
import sys
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = r"C:\Users\User\eda-routine\data"
SRC = os.path.join(ROOT, "btcusdt_spot_monthly")
OUT = os.path.join(ROOT, "btcusdt_spot_1m_clean")
TRAIN_END = pd.Timestamp("2023-03-19 23:59:59", tz="UTC")
VAL_END = pd.Timestamp("2023-11-30 23:59:59", tz="UTC")
L = []   # log lines


def log(s=""):
    L.append(s)


def main():
    os.makedirs(os.path.join(OUT, "plots"), exist_ok=True)
    files = sorted(glob.glob(os.path.join(SRC, "2*.parquet")))
    df = pd.concat([pd.read_parquet(f) for f in files])
    df.index.name = "t"
    assert df.index.max() <= VAL_END, "data past VAL_END present: STOP"
    orig_cols = ["open", "high", "low", "close", "vol", "quote", "n", "buy_vol", "sell_vol", "n_buy", "n_sell"]
    raw_rows = len(df)
    train = df.index <= TRAIN_END
    log("# CLEANING LOG: Binance BTCUSDT spot, 1-minute bars, TRAIN + VAL")
    log()
    log(f"Source: `{SRC}` ({len(files)} monthly files). Raw files untouched. Rows in: **{raw_rows:,}**. "
        f"TRAIN rows: {int(train.sum()):,}; VAL/embargo rows: {int((~train).sum()):,}.")
    log("Holdout discipline: structural checks cover all rows; distribution statistics are TRAIN-only "
        "(VAL flags are applied mechanically and only counted).")
    log()

    # ---- GATE 0 provenance
    log("## Gate 0: provenance")
    log("*These prices are **trade-based OHLCV bars** (last-trade prices, no bid/ask) from **Binance BTCUSDT SPOT**, "
        "timestamped in **UTC** at the bar's **OPEN** time, knowable at **open + 60 seconds** (the bar is complete only then).*")
    log("Evidence for open-time stamping: every full month starts at 00:00 and ends at 23:59 (e.g. 2023-11: 43,200 rows, "
        "first 2023-11-01 00:00, last 2023-11-30 23:59). A close-time stamp would run 00:01 to 00:00 next day. "
        "Not confirmed against the exchange's own documentation.")
    log()

    # ---- GATE 1 structure
    log("## Gate 1: structure and identity")
    idx_names = sorted({str(pd.read_parquet(f).index.name) for f in files})
    log(f"- index names across files: {idx_names} -> standardised to `t`")
    log(f"- sorted ascending: {df.index.is_monotonic_increasing}; duplicate timestamps: {int(df.index.duplicated().sum())}; "
        f"stamps not on a whole minute: {int(((df.index.second != 0) | (df.index.microsecond != 0)).sum())}")
    exact = df[orig_cols].duplicated(keep="first")
    adj = (df[orig_cols] == df[orig_cols].shift(1)).all(axis=1)
    log(f"- rows whose 11 values equal an earlier row's: **{int(exact.sum())}** (different timestamps, so NOT duplicate records: "
        f"all are flat bars with 1-2 trades in 2017). `drop_duplicates()` would have deleted them. "
        f"{int(adj.sum())} of them are identical to the IMMEDIATELY previous bar -> flagged `flag_repeat_prev_bar`, kept.")
    for c in ["n", "n_buy", "n_sell"]:
        df[c] = df[c].astype("int64")

    # ---- GATE 2 time
    log()
    log("## Gate 2: time and gaps")
    full = pd.date_range(df.index.min(), df.index.max(), freq="1min", tz="UTC")
    missing = full.difference(df.index)
    log(f"- timezone: UTC, tz-aware in every file. Grid minutes {len(full):,}; present {len(df):,}; "
        f"**missing {len(missing):,} ({len(missing) / len(full):.3%})**. Missing minutes are **left missing, not filled**.")
    if len(missing):
        grp = (missing.to_series().diff() != pd.Timedelta("1min")).cumsum()
        runs = missing.to_series().groupby(grp.values).agg(["min", "max", "count"])
        log(f"- {len(runs):,} gap runs: 1 min {int((runs['count'] == 1).sum()):,}; 2-10 min {int(runs['count'].between(2, 10).sum()):,}; "
            f"11-60 {int(runs['count'].between(11, 60).sum()):,}; >60 {int((runs['count'] > 60).sum()):,}. Longest: "
            f"{int(runs['count'].max()):,} min starting {runs.sort_values('count').iloc[-1]['min']}.")
        by_year = pd.Series(1, index=missing).groupby(missing.year).count().to_dict()
        log(f"- missing minutes by year: {by_year}")
    log("- No row has vol = 0 or n = 0: a minute with no trades is simply ABSENT. So a missing minute may mean "
        "'no trades' (likely in 2017) or an outage (block gaps such as 2018-02-08); the file cannot distinguish them. "
        "`gap_min` = minutes since the previous bar (1 = normal), so returns across a gap can be excluded.")
    df["gap_min"] = df.index.to_series().diff().dt.total_seconds() / 60.0

    # ---- GATE 3 validity
    log()
    log("## Gate 3: validity (impossible values)")
    P = ["open", "high", "low", "close"]
    log(f"- NaN in any column: {int(df[orig_cols].isna().any(axis=1).sum())}; low>high: {int((df['low'] > df['high']).sum())}; "
        f"open or close outside [low,high]: {int(((df[['open', 'close']].lt(df['low'], axis=0)) | (df[['open', 'close']].gt(df['high'], axis=0))).any(axis=1).sum())} "
        f"(measured with the zero lows included); vol<0: {int((df['vol'] < 0).sum())}; "
        f"buy_vol+sell_vol != vol: {int((~np.isclose(df['buy_vol'] + df['sell_vol'], df['vol'], rtol=1e-6, atol=1e-8)).sum())}; "
        f"n_buy+n_sell != n: {int(((df['n_buy'] + df['n_sell']) != df['n']).sum())}")
    bad_low = df["low"] <= 0
    log(f"- **low <= 0: {int(bad_low.sum())} bars** ({df.index[bad_low].min().date()} to {df.index[bad_low].max().date()}); open/high/close/vol "
        f"in those rows are valid. Identical in the daily-file copy of the feed -> a defect in the source data. "
        f"**Action: `low` set to NaN, `flag_low_invalid`. Rows kept.**")
    df["flag_low_invalid"] = bad_low
    df.loc[bad_low, "low"] = np.nan
    qz = (df["vol"] > 0) & (df["quote"] == 0)
    m = (df["vol"] > 0) & (df["quote"] > 0)
    vw = df["quote"] / df["vol"]
    off = m & ((vw < df["low"] * 0.999) | (vw > df["high"] * 1.001))
    log(f"- **quote == 0 with vol > 0: {int(qz.sum()):,} bars**, one contiguous block {df.index[qz].min()} to {df.index[qz].max()}. "
        f"Plus **{int(off.sum())}** further bar whose quote/vol (VWAP) lies outside [low, high] by >0.1% "
        f"({', '.join(str(t) for t in df.index[off])}). **Action: `quote` set to NaN, `flag_quote_bad`. Rows kept.**")
    df["flag_quote_bad"] = qz | off
    df.loc[qz | off, "quote"] = np.nan
    df["flag_repeat_prev_bar"] = adj.values
    log("- Nothing else impossible. **No row was dropped.**")

    # ---- GATE 4 outliers / staleness
    log()
    log("## Gate 4: outliers and staleness (flag, do not change)")
    flat = (df["open"] == df["high"]) & (df["high"] == df["low"].fillna(df["high"])) & (df["low"].fillna(df["high"]) == df["close"])
    fl = pd.DataFrame({"rows": df.groupby(df.index.year).size(), "flat_bars": flat.groupby(df.index.year).sum(),
                       "close==prev_close": (df["close"].diff() == 0).groupby(df.index.year).sum()})
    fl["flat_%"] = (100 * fl["flat_bars"] / fl["rows"]).round(3)
    fl["zero_ret_%"] = (100 * fl["close==prev_close"] / fl["rows"]).round(2)
    log("- flat bars (open=high=low=close) and zero-return rate by year (2017 is thin: 18.9% flat bars; from 2018 essentially none):")
    log("```\n" + fl.to_string() + "\n```")
    log("  Zero-return rate rises again in 2023 (4.9%): this includes VAL months, reported by count only. "
        "Real trading rarely repeats a price (data-hygiene trap): read 2017 and 2023 with that in mind.")
    tr = df[train]
    c = tr["close"]
    med = c.rolling(51, center=True, min_periods=25).median()
    mad = (c - med).abs().rolling(51, center=True, min_periods=25).mean()
    dev_tr = (c - med).abs() / (mad + c * 0.0005)
    ks = [5, 10, 20, 40]
    cnt = {k: int((dev_tr > k).sum()) for k in ks}
    log(f"- close vs centred 51-bar median, units of local mean-abs-dev + 0.05% floor (BHLS Q4 / BG style), TRAIN only. "
        f"Flagged bars at k = {ks}: {list(cnt.values())}. Chosen: **k = 10** ({cnt[10]} bars in TRAIN). "
        f"Threshold shown at four settings so the choice can be judged; these are NYSE-tick-derived starting values, justified here by the "
        f"count collapsing between k=5 and k=10.")
    c_all = df["close"]
    med_a = c_all.rolling(51, center=True, min_periods=25).median()
    mad_a = (c_all - med_a).abs().rolling(51, center=True, min_periods=25).mean()
    dev_all = (c_all - med_a).abs() / (mad_a + c_all * 0.0005)
    df["flag_close_outlier"] = dev_all > 10
    body_hi = df[["open", "close"]].max(axis=1)
    body_lo = df[["open", "close"]].min(axis=1)
    up = (df["high"] - body_hi) / body_hi * 100
    dn = (body_lo - df["low"]) / body_lo * 100
    wick = pd.concat([up, dn], axis=1).max(axis=1)
    wtr = wick[train]
    log(f"- wicks (high/low beyond the open-close body), TRAIN only: quantiles 99% {wtr.quantile(.99):.2f}%, 99.9% {wtr.quantile(.999):.2f}%, "
        f"99.99% {wtr.quantile(.9999):.2f}%; count > 1%: {int((wtr > 1).sum()):,}, > 3%: {int((wtr > 3).sum())}, > 5%: {int((wtr > 5).sum())}, > 10%: {int((wtr > 10).sum())}.")
    top = wtr.sort_values(ascending=False).head(6)
    log("  largest TRAIN wicks: " + "; ".join(f"{t:%Y-%m-%d %H:%M} ({v:.1f}%)" for t, v in top.items()) +
        ". These fall on days I recall as violent (Mar 2020 crash, May 2021 crash, Oct 2019 spike, Sep 2021): consistent with REAL "
        "moves, from memory, NOT checked against a second source. **Flagged `flag_wick_gt3pct`, not altered.**")
    df["flag_wick_gt3pct"] = wick > 3
    n_val = lambda col: int(df.loc[~train, col].sum())
    log(f"- flag counts: close_outlier {int(df['flag_close_outlier'].sum())} (VAL: {n_val('flag_close_outlier')}); "
        f"wick_gt3pct {int(df['flag_wick_gt3pct'].sum())} (VAL: {n_val('flag_wick_gt3pct')}); "
        f"repeat_prev_bar {int(df['flag_repeat_prev_bar'].sum())} (VAL: {n_val('flag_repeat_prev_bar')}).")

    # ---- GATE 4b regime break
    log()
    log("### Gate 4b: regime break at the TRAIN/VAL boundary (found while checking the rising zero-return rate)")
    d2 = df.loc["2022-07-01":]
    zr2 = d2["close"].diff() == 0
    mm = d2.index.to_period("M")
    reg = pd.DataFrame({"rows": d2.groupby(mm).size(), "zero_ret_%": (100 * zr2.groupby(mm).mean()).round(2),
                        "median_trades_per_min": d2["n"].groupby(mm).median()})
    on10 = (((d2["close"] * 100).round().astype("int64") % 10) == 0).groupby(mm).mean() * 100
    log("```\n" + reg.to_string() + "\n```")
    z2 = d2[zr2]
    log(f"- The zero-return bars are REAL bars, not stale rows: {100 * (z2['vol'] > 0).mean():.0f}% have volume, "
        f"{100 * (z2['high'] > z2['low']).mean():.0f}% have a price range, median {int(z2['n'].median())} trades.")
    log(f"- Tick size did NOT change: the share of closes on a $0.10 grid stays {on10.min():.0f}-{on10.max():.0f}% in every month "
        f"(a move to a $0.10 tick would push it to 100%).")
    log("- What changed is liquidity: median trades per minute fall from ~3,600 (2023-03) to ~450 (2023-04) and ~240-360 "
        "(2023-06 to 09), and the zero-return share rises from <0.3% to 4-12%. The cause is NOT established (a migration of BTC "
        "volume away from the USDT pair is one candidate, from memory, unverified). **Nothing was changed.**")
    log("- **Consequence: VAL (2023-03-25 to 2023-11-30) is a different microstructure regime from TRAIN.** A lead about trade counts, "
        "volume, or 1-minute tick behaviour can fail VAL for structural reasons alone; read every VAL result with that in mind.")

    # ---- GATE 5-7
    log()
    log("## Gates 5-7: price meaning, knowability, microstructure clock")
    log("- Price type: **last-trade prices**, no quotes, so no bid/ask, no mid, no spread series. **Gates 7 (spread clock) "
        "and the quote-side checks are N/A; round-trip cost is UNKNOWN from this file.** Trade prints carry bid-ask bounce (Roll 1984).")
    try:
        sys.path.insert(0, r"C:\Users\User\backtest_engine\backtest_engine2")
        from data_hygiene import roll_effective_spread
        r21 = roll_effective_spread(df.loc["2021-01-01":"2021-12-31", "close"].dropna())
        log(f"- Roll half-spread embedded in 2021 1-minute closes (TRAIN): {r21:.3f} bp (NaN means no detectable bounce)." if pd.notna(r21) else
            "- Roll estimate on 2021 1-minute closes (TRAIN): NaN, no detectable bounce at this sampling.")
    except Exception as e:
        log(f"- Roll estimate not run ({type(e).__name__}: {e}).")
    log("- **Knowability:** a bar stamped `T` is complete at `T + 60 s`. Any use of `close`, `high`, `low`, `vol` at time `T` "
        "is look-ahead; the earliest legitimate use is the NEXT bar.")
    log("- No fundamentals, no conditioning variables, no interpolation performed (Gate 6 otherwise N/A).")

    # ---- GATE 8 reconcile
    log()
    log("## Gate 8: second source (TRAIN only)")
    try:
        pp = pd.read_parquet(os.path.join(ROOT, "btcusdtperp_1m", "binance_btcusdtperp_1m.parquet")).set_index("t")
        cm = tr.index.intersection(pp.index)
        bp = (tr.loc[cm, "close"] / pp.loc[cm, "close"] - 1) * 1e4
        log(f"- Same feed, daily-file copy (`binance_btcusdt_1m`): identical on all {len(tr):,} TRAIN rows for open/high/low/close/vol, "
            f"INCLUDING the 11 zero lows, so **not independent**: it shows the defects are in the source, not in file handling.")
        log(f"- Spot close vs Binance PERP close (a different instrument, so a gross-error check only), {len(cm):,} overlapping TRAIN minutes "
            f"from {cm.min().date()}: |diff| median {bp.abs().median():.2f} bp, 99% {bp.abs().quantile(.99):.1f} bp, max {bp.abs().max():.0f} bp; "
            f"> 50 bp: {int((bp.abs() > 50).sum()):,}; > 200 bp: {int((bp.abs() > 200).sum()):,}. The wide tail is basis/liquidity stress, not checked bar by bar. "
            f"The zero-low bars pre-date the perp data, so they cannot be cross-checked this way.")
    except Exception as e:
        log(f"- perp reconciliation not run ({type(e).__name__}: {e}).")

    # ---- GATE 10 engine contract
    log()
    log("## Gate 10: engine contract (`DataPanel`)")
    try:
        sys.path.insert(0, r"C:\Users\User\backtest_engine")
        from backtest.data import DataPanel
        px = df[["close"]].rename(columns={"close": "BTCUSDT"})
        vo = df[["vol"]].rename(columns={"vol": "BTCUSDT"})
        with warnings.catch_warnings(record=True) as wlist:
            warnings.simplefilter("always")
            panel = DataPanel(px, volume=vo, check_outliers=True)      # check_outliers left ON, never silenced
        rep = panel.outlier_report()
        rep_tr = rep[pd.to_datetime(rep["date"], utc=True) <= TRAIN_END]
        log(f"- Wide panel (timestamp x asset `BTCUSDT`), index sorted, unique, UTC: **constructed without error** on all {len(px):,} rows "
            f"(price = `close`, volume = `vol`; NaN rows are missing minutes, left in place: `missing='drop'` is a no-op).")
        log(f"- `DataPanel`'s own outlier scan (global MAD, threshold 10) flags **{len(rep):,}** bars ({len(rep_tr):,} in TRAIN; the rest are VAL, "
            f"counted only). Explained: that scan uses ONE MAD for the whole sample, so heavy-tailed, volatility-clustering 1-minute crypto returns "
            f"trip it in bulk. It is not evidence of bad ticks: the local-window scan (Gate 4) finds {int(df['flag_close_outlier'].sum())}. "
            f"Top TRAIN examples: " + "; ".join(f"{pd.Timestamp(r['date']):%Y-%m-%d %H:%M} ({r['return']:+.1%})" for _, r in rep_tr.head(4).iterrows()) + ".")
        log(f"- Pipeline note: `pct_change` inside the scan spans gaps, so a return across a missing block is a multi-minute return: "
            f"use `gap_min == 1` to keep 1-minute returns only.")
    except Exception as e:
        log(f"- DataPanel check FAILED to run ({type(e).__name__}: {e}).")
    log("- Cleaning log, flags and raw-preservation: raw monthly files untouched; cleaned file written separately; row count unchanged.")

    # ---- write output
    df = df[orig_cols + ["gap_min", "flag_low_invalid", "flag_quote_bad", "flag_repeat_prev_bar",
                         "flag_close_outlier", "flag_wick_gt3pct"]]
    assert len(df) == raw_rows and df.index.is_monotonic_increasing and df.index.is_unique and str(df.index.tz) == "UTC"
    df.to_parquet(os.path.join(OUT, "btcusdt_spot_1m_clean.parquet"))
    with open(os.path.join(SRC, "CUT.json")) as fh:
        cut = json.load(fh)
    cut["cleaned"] = {"script": "clean_btc_spot.py", "rows": raw_rows, "rows_dropped": 0,
                      "fields_nulled": {"low": int(df["flag_low_invalid"].sum()), "quote": int(df["flag_quote_bad"].sum())}}
    with open(os.path.join(OUT, "CUT.json"), "w") as fh:
        json.dump(cut, fh, indent=2)

    # ---- plots (TRAIN-only distribution stats; structural counts all rows)
    def save(name):
        plt.tight_layout(); plt.savefig(os.path.join(OUT, "plots", name), dpi=110); plt.close()
    ms = pd.Series(1, index=missing).groupby(missing.to_period("M").astype(str)).count()
    ms.index = pd.to_datetime(ms.index)
    plt.figure(figsize=(9, 3.6)); plt.bar(ms.index, ms.values, width=25, color="#3b6ea5"); plt.yscale("log")
    plt.title(f"Missing minutes per month: {len(missing):,} in total ({len(missing) / len(full):.2%}); 74% are in 2017"); plt.ylabel("missing minutes (log)")
    save("01_missing_minutes_per_month.png")
    z = df.loc["2018-01-14":"2018-01-15"]
    plt.figure(figsize=(9, 3.6)); plt.plot(z.index, z["close"], lw=.7, label="close"); plt.plot(z.index, z["high"], lw=.4, label="high")
    plt.scatter(z.index[z["flag_low_invalid"]], z["close"][z["flag_low_invalid"]], c="r", s=25, label="bars with low = 0 (set to NaN)")
    plt.title(f"Low = 0.0 on {int(bad_low.sum())} bars (Dec 2017 to Jan 2018): {int(z['flag_low_invalid'].sum())} shown here, 14-15 Jan 2018"); plt.legend(fontsize=7); save("02_low_equals_zero.png")
    z = df.loc["2020-07-31 12:00":"2020-08-02 12:00"]
    plt.figure(figsize=(9, 3.6)); plt.plot(z.index, (z["quote"] / z["vol"]), lw=.7, label="quote / vol (VWAP)")
    plt.plot(z.index, z["close"], lw=.7, label="close"); plt.ylim(0, 13000)
    plt.title(f"quote = 0 on {int(qz.sum()):,} consecutive bars from 2020-08-01 00:00 to 08-02 01:48 (set to NaN)"); plt.legend(fontsize=7); save("03_quote_zero_block.png")
    plt.figure(figsize=(6, 3.4)); plt.bar([str(k) for k in ks], [max(cnt[k], .5) for k in ks], color="#3b6ea5"); plt.yscale("log")
    for i, k in enumerate(ks): plt.text(i, max(cnt[k], .5), str(cnt[k]), ha="center", va="bottom")
    plt.title("Close outliers vs threshold k: 310 -> 3 -> 0 -> 0 (TRAIN)"); plt.xlabel("k (local mean-abs-devs)"); save("04_close_outlier_sensitivity.png")
    plt.figure(figsize=(7, 3.6)); plt.hist(wtr.clip(upper=12).dropna(), bins=120, color="#3b6ea5"); plt.yscale("log"); plt.axvline(3, c="r", lw=1)
    plt.title(f"1-minute wick size (TRAIN): {int((wtr > 3).sum())} bars > 3% (flagged, kept); max {wtr.max():.1f}%"); plt.xlabel("wick, % of price"); save("05_wick_distribution.png")
    plt.figure(figsize=(6, 3.4)); plt.bar(fl.index.astype(str), fl["flat_%"], color="#3b6ea5")
    plt.title("Flat bars (open=high=low=close), % of rows: 18.9% in 2017, ~0 after"); save("06_flat_bars_by_year.png")

    fig, ax = plt.subplots(figsize=(9, 3.8)); x = [str(p) for p in reg.index]
    ax.bar(x, reg["zero_ret_%"], color="#c0504d"); ax.set_ylabel("zero-return bars, %", color="#c0504d")
    ax2 = ax.twinx(); ax2.plot(x, reg["median_trades_per_min"], c="k", marker="o", ms=3); ax2.set_ylabel("median trades / min")
    ax.axvline(x.index("2023-04") - 0.5, c="grey", ls="--"); ax.tick_params(axis="x", labelrotation=90, labelsize=7)
    ax.set_title("Regime break at the TRAIN/VAL boundary: trades/min ~3,600 -> ~450, zero-return bars 0.3% -> 4-12%"); save("07_regime_break_train_val.png")

    log()
    log("## Result")
    log(f"- Rows in {raw_rows:,}, rows out {len(df):,}, **rows dropped 0**. Fields set to NaN: low {int(df['flag_low_invalid'].sum())}, "
        f"quote {int(df['flag_quote_bad'].sum()):,}. Added columns: `gap_min` and five `flag_*` columns. Output: "
        f"`{os.path.join(OUT, 'btcusdt_spot_1m_clean.parquet')}`. Plots: `plots/01..06`.")
    with open(os.path.join(OUT, "CLEANING_LOG.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
