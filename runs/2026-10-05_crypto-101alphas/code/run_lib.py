"""Run-specific helpers for runs/2026-10-05_crypto-101alphas (NOT a generic eda.py).

What lives here, and only this:
  * the guarded loaders (assert no row later than VAL_END at every load; every load logged to ACCESS_LOG.md)
  * the TARGET.md translation of a "day" (UTC calendar day built from Binance 1h bars) and of the response
    (primary/validated_<COIN> `price`, end of day d -> end of day d+1, never across a new_source=True row)
  * the five Kakushadze (2015) Appendix-A formulas named in TARGET.md (#101, #42, #2, #6, #4), verbatim
  * the slice table (parsed from SPLITS.md) and the one pre-registered test statistic every test cell uses
  * plotting palette copied from backtest_engine2/cellplot.py (seaborn is not installed / not pre-approved,
    so cellplot itself cannot be imported; matplotlib only, same colours)
"""
from __future__ import annotations

import datetime as _dt
import os
import re

import numpy as np
import pandas as pd

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(RUN))                      # /home/user/eda-routine
DATA = os.path.join(ROOT, "data", "crypto_panel_validated_2026-10-05")
VAL_END = pd.Timestamp("2023-11-30 23:59:59", tz="UTC")
TRAIN_END = pd.Timestamp("2023-03-19", tz="UTC")
COINS = ["BTC", "ETH", "BNB", "LTC", "XRP", "BCH", "ADA", "DOT", "SOL", "DOGE"]
MIN_COINS = 5            # a day enters a cross-sectional statistic only with >= 5 coins (DECISIONS D5)
MIN_HOURS = 20           # a Binance daily bar needs >= 20 of 24 hours, incl. hour 00 and hour 23 (DECISIONS D4)
ECON_BP = 20.0           # smallest economically meaningful top-minus-bottom spread, bp/day (DECISIONS D7)

# cellplot.py palette (light mode), copied verbatim
PAL = ["#2a78d6", "#008300", "#e87ba4", "#eda100", "#1baf7a", "#eb6834", "#4a3aa7", "#e34948"]
SURFACE, TEXT, TEXT2, GRID, GRAY = "#fcfcfb", "#0b0b0b", "#52514e", "#e5e4e0", "#9b9a94"


# ------------------------------------------------------------------ guard + access log

def _log(path, rows, tmax, purpose):
    line = (f"| {_dt.datetime.utcnow():%Y-%m-%d %H:%M:%S} | {os.path.relpath(path, ROOT)} | {rows} | {tmax} | "
            f"{purpose} | guard PASS (max t <= {VAL_END}) |\n")
    p = os.path.join(RUN, "ACCESS_LOG.md")
    if not os.path.exists(p):
        with open(p, "w") as fh:
            fh.write("# ACCESS_LOG — every data load, with the VAL_END guard result\n\n"
                     "Guard = an assertion at every load that no row is later than VAL_END 2023-11-30 23:59:59 UTC "
                     "(TARGET.md NOTES: no eda_guard.py in this checkout). A failing assertion would raise and the "
                     "run would write STOPPED.md.\n\n| utc | file | rows | max t | purpose / window used | guard |\n"
                     "|---|---|---:|---|---|---|\n")
    with open(p, "a") as fh:
        fh.write(line)


def guarded_read(rel, purpose, time_col="t"):
    path = os.path.join(DATA, rel)
    assert os.path.abspath(path).startswith(DATA), "load outside the prepared data folder"
    df = pd.read_parquet(path)
    tmax = pd.to_datetime(df[time_col], utc=True).max()
    assert tmax <= VAL_END, f"GUARD FAIL: {rel} has a row at {tmax} > VAL_END {VAL_END}"
    _log(path, len(df), tmax, purpose)
    df[time_col] = pd.to_datetime(df[time_col], utc=True)
    return df


# ------------------------------------------------------------------ slices

def slices():
    """Parse SPLITS.md's machine-readable block -> {name: (from, to)} (from incl., to excl., UTC)."""
    txt = open(os.path.join(RUN, "SPLITS.md")).read()
    rows = re.findall(r"(?m)^\s*-\s*(EXPLORE|C\d+|VAL)\s+(\d{4}-\d{2}-\d{2})\s+(\d{4}-\d{2}-\d{2})\s*$", txt)
    return {n: (pd.Timestamp(a, tz="UTC"), pd.Timestamp(b, tz="UTC")) for n, a, b in rows}


# ------------------------------------------------------------------ panels

def load_primary(coin, purpose, window):
    """Hourly validated price for one coin, cut to window=(start, end) right after the guard."""
    df = guarded_read(f"primary/validated_{coin}USD.parquet", f"{purpose}; window {window[0].date()}..{window[1].date()}")
    return df[(df.t >= window[0]) & (df.t < window[1])].reset_index(drop=True)


def load_binance(coin, purpose, window):
    df = guarded_read(f"spot/binance_{coin}USD.parquet", f"{purpose}; window {window[0].date()}..{window[1].date()}")
    return df[(df.t >= window[0]) & (df.t < window[1])].reset_index(drop=True)


def daily_response(prim):
    """Per UTC day d: r_next[d] = P(end of d+1)/P(end of d) - 1, using the bar stamped d+1 23:00 (price at
    00:00 d+2) and d 23:00. Valid only if all 24 bars of day d+1 exist and none has new_source=True
    (TARGET.md: never take a return across a new_source row)."""
    p = prim.set_index("t")
    day = p.index.floor("D")
    g = pd.DataFrame({"n": p.groupby(day).size(),
                      "ns": p["new_source"].groupby(day).sum()})
    end = p[p.index.hour == 23]["price"]
    end.index = end.index.floor("D")
    g["p_end"] = end
    g = g.asfreq("D")
    ok_next = (g["n"].shift(-1) == 24) & (g["ns"].shift(-1) == 0)
    r = g["p_end"].shift(-1) / g["p_end"] - 1
    return r.where(ok_next & g["p_end"].notna() & g["p_end"].shift(-1).notna())


def daily_bars(b):
    """UTC daily OHLCV + vwap from Binance 1h bars (TARGET.md HYPOTHESIS translation)."""
    b = b.set_index("t").sort_index()
    day = b.index.floor("D")
    g = b.groupby(day)
    d = pd.DataFrame({
        "open": g["open"].first(), "high": g["high"].max(), "low": g["low"].min(), "close": g["close"].last(),
        "volume": g["vol"].sum(), "quote": g["quote_vol"].sum(), "nh": g.size(),
        "h0": g.apply(lambda x: (x.index.hour == 0).any()), "h23": g.apply(lambda x: (x.index.hour == 23).any()),
    })
    d["vwap"] = d["quote"] / d["volume"]
    bad = (d["nh"] < MIN_HOURS) | (~d["h0"]) | (~d["h23"]) | (d["volume"] <= 0)
    d.loc[bad, ["open", "high", "low", "close", "volume", "vwap"]] = np.nan
    return d.asfreq("D")


def build_panel(purpose, window, lookback_days=40, coins=COINS):
    """Signal inputs from Binance with a lookback buffer before window start (signal inputs only), and the
    response from primary/ strictly inside window. Returns dict of date x coin frames."""
    sig_win = (window[0] - pd.Timedelta(days=lookback_days), window[1])
    fields = {k: {} for k in ["open", "high", "low", "close", "volume", "vwap"]}
    resp = {}
    for c in coins:
        b = load_binance(c, purpose + " (signal inputs, incl. lookback buffer)", sig_win)
        db = daily_bars(b)
        for k in fields:
            fields[k][c] = db[k]
        pr = load_primary(c, purpose + " (response)", window)
        resp[c] = daily_response(pr) if len(pr) else pd.Series(dtype=float)
    out = {k: pd.DataFrame(v) for k, v in fields.items()}
    R = pd.DataFrame(resp).reindex(out["close"].index)
    # response must END inside the window: signal day d needs d+2 00:00 <= window end
    keep = (R.index >= window[0]) & (R.index + pd.Timedelta(days=2) <= window[1])
    R.loc[~keep] = np.nan
    out["fwd"] = R
    return out


# ------------------------------------------------------------------ Appendix-A operators (paper A.1 definitions)

def cs_rank(x):
    return x.rank(axis=1, pct=True)


def ts_corr(x, y, d):
    return x.rolling(d, min_periods=d).corr(y)


def ts_rank(x, d):
    return x.rolling(d, min_periods=d).apply(lambda a: (pd.Series(a).rank(pct=True).iloc[-1]), raw=True)


def delta(x, d):
    return x - x.shift(d)


def alpha(name, P):
    o, h, l, c, v, w = P["open"], P["high"], P["low"], P["close"], P["volume"], P["vwap"]
    if name == "A101":
        return (c - o) / ((h - l) + 0.001)
    if name == "A42":
        return cs_rank(w - c) / cs_rank(w + c)
    if name == "A2":
        return -1 * ts_corr(cs_rank(delta(np.log(v), 2)), cs_rank((c - o) / o), 6)
    if name == "A6":
        return -1 * ts_corr(o, v, 10)
    if name == "A4":
        return -1 * ts_rank(cs_rank(l), 9)
    raise KeyError(name)


# ------------------------------------------------------------------ the pre-registered test statistic

def half_spread_series(sig, fwd, min_coins=MIN_COINS):
    """Per day: mean fwd return of the top half by signal minus the bottom half (bp). Average ranks for ties;
    with an odd count the middle coin is left out. Days with < min_coins usable coins, or a degenerate split
    (one side empty because of ties), are skipped."""
    out = {}
    s, f = sig.where(fwd.notna()), fwd.where(sig.notna())
    for d in s.index:
        a, r = s.loc[d].dropna(), f.loc[d].dropna()
        if len(a) < min_coins:
            continue
        rk = a.rank()
        mid = (len(a) + 1) / 2
        top, bot = rk[rk > mid].index, rk[rk < mid].index
        if len(top) == 0 or len(bot) == 0:
            continue
        out[d] = (r[top].mean() - r[bot].mean()) * 1e4
    return pd.Series(out, dtype=float)


def nw_se(x, lags=5):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    n = len(x)
    e = x - x.mean()
    g0 = (e @ e) / n
    s = g0
    for k in range(1, lags + 1):
        if k >= n:
            break
        gk = (e[k:] @ e[:-k]) / n
        s += 2 * (1 - k / (lags + 1)) * gk
    return float(np.sqrt(max(s, 1e-12) / n))


def decide(mean_bp, se_bp, econ=ECON_BP, z=1.645):
    """Pre-registered three-branch rule (identical in every test rule file).
    supported    : mean >= econ AND t >= z
    refuted      : mean + z*se < econ AND t < z   (the economic effect is excluded and there is no significant
                   positive effect)
    inconclusive : anything else (incl. significant-but-below-econ)."""
    t = mean_bp / se_bp if se_bp > 0 else 0.0
    if mean_bp >= econ and t >= z:
        return "supported"
    if mean_bp + z * se_bp < econ and t < z:
        return "refuted"
    return "inconclusive"


def daily_ic(sig, fwd, min_coins=MIN_COINS):
    out = {}
    s, f = sig.where(fwd.notna()), fwd.where(sig.notna())
    for d in s.index:
        a, r = s.loc[d].dropna(), f.loc[d].dropna()
        if len(a) < min_coins or a.nunique() < 2:
            continue
        out[d] = a.rank().corr(r.rank())
    return pd.Series(out, dtype=float)


# ------------------------------------------------------------------ belief arithmetic

def odds(p):
    return p / (1 - p)


def prob(o):
    return o / (1 + o)


def capped(w, cap=10.0):
    return min(max(w, 1 / cap), cap)


def setup_mpl():
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "text.color": TEXT, "axes.labelcolor": TEXT2, "xtick.color": TEXT2, "ytick.color": TEXT2,
        "axes.edgecolor": GRID, "grid.color": GRID, "grid.linewidth": 0.6, "axes.grid": True,
        "axes.spines.top": False, "axes.spines.right": False, "axes.prop_cycle": matplotlib.cycler(color=PAL),
        "axes.titlesize": 11, "axes.titleweight": "bold", "figure.dpi": 110, "lines.linewidth": 1.6,
        "font.size": 9,
    })
    import matplotlib.pyplot as plt
    return plt


def save(fig, name):
    path = os.path.join(RUN, "plots", f"{name}.png")
    fig.savefig(path, bbox_inches="tight")
    import matplotlib.pyplot as plt
    plt.close(fig)
    print(f"[plot] plots/{name}.png")
    return path


def md(df, index=False):
    """Markdown table without the optional `tabulate` dependency."""
    d = df.reset_index() if index else df
    cols = [str(c) for c in d.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in d.iterrows():
        lines.append("| " + " | ".join(str(v) for v in r.values) + " |")
    return "\n".join(lines)
