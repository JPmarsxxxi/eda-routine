"""Phase 0 profile, sections 1-7, EXPLORE only. Rules are in DATA_PROFILE.md (written first)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import common as C

C.setup_plot()
T = lambda n: os.path.join(C.RUN, "tables", n)
F, R = C.cached()
ex = C.in_slice(R.index, "EXPLORE")
RE = C.response_in_slice(R, "EXPLORE")
out = {}

# alpha values on EXPLORE signal days (inputs may use the 40-day buffer, D6)
A = {k: f(F) for k, f in C.ALPHAS.items()}
AE = {k: v.loc[C.in_slice(v.index, "EXPLORE")] for k, v in A.items()}

# ---- 1. distributions
rows = []
for c in C.COINS:
    r = RE[c].dropna()
    if len(r) < 30:
        continue
    rows.append({"coin": c, "n": len(r), "mean_bp": r.mean() * 1e4, "sd_bp": r.std() * 1e4,
                 "skew": stats.skew(r), "exkurt": stats.kurtosis(r), "zero_share": (r == 0).mean()})
d1 = pd.DataFrame(rows)
d1.to_csv(T("p0_01_returns.csv"), index=False)
arows = []
for k, v in AE.items():
    live = F["close"].loc[v.index].notna() & F["high"].loc[v.index].notna()
    nan_div = (v.isna() & live).sum().sum() / max(live.sum().sum(), 1)
    distinct = v.apply(lambda s: s.dropna().nunique(), axis=1)
    present = v.notna().sum(axis=1)
    degen = ((distinct < 3) & (present >= C.MIN_COINS)).sum() / max((present >= C.MIN_COINS).sum(), 1)
    flat = v.stack().dropna()
    arows.append({"alpha": k, "coin_days": int(flat.size), "nan_share_live": nan_div, "degenerate_day_share": degen,
                  "p01": flat.quantile(.01), "median": flat.median(), "p99": flat.quantile(.99),
                  "exkurt": stats.kurtosis(flat)})
d1a = pd.DataFrame(arows)
d1a.to_csv(T("p0_01_alphas.csv"), index=False)
fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
for i, c in enumerate(d1["coin"]):
    ax[0].hist(RE[c].dropna() * 1e2, bins=80, histtype="step", color=C.PAL[i % 8], label=c)
ax[0].set_xlabel("daily log return (%)"); ax[0].legend(fontsize=6, ncol=2)
ax[0].set_title(f"Daily returns fat-tailed: median excess kurtosis {d1.exkurt.median():.1f}")
ax[1].bar(d1a.alpha, d1a.nan_share_live * 100, color=C.PAL[0], label="NaN from division guard (%)")
ax[1].bar(d1a.alpha, d1a.degenerate_day_share * 100, bottom=d1a.nan_share_live * 100, color=C.PAL[3],
          label="days < 3 distinct values (%)")
ax[1].legend(fontsize=7); ax[1].set_title("Alpha hazards on EXPLORE (D9)")
C.savefig(fig, "00_distributions.png")
out["1"] = {"fat_tailed_coins": int((d1.exkurt > 3).sum()), "coins": len(d1), "max_zero_share": d1.zero_share.max(),
            "alphas": d1a.set_index("alpha")[["nan_share_live", "degenerate_day_share"]].round(4).to_dict()}

# ---- 2. missingness
valid = RE.notna()
live_coins = [c for c in C.COINS if valid[c].any()]
vm = valid[live_coins].copy(); vm.index = pd.to_datetime(vm.index)
monthly = vm.resample("ME").mean()
monthly.to_csv(T("p0_02_valid_by_month.csv"))
ncoin = valid.sum(axis=1)
short = (ncoin < C.MIN_COINS).mean()
thin = (monthly < 0.8) & (monthly > 0)
fig, ax = plt.subplots(figsize=(11, 3.2))
im = ax.imshow(monthly.T.values, aspect="auto", cmap="Blues", vmin=0, vmax=1)
ax.set_yticks(range(len(live_coins))); ax.set_yticklabels(live_coins, fontsize=7)
ax.set_xticks(range(0, len(monthly), 3)); ax.set_xticklabels([d.strftime("%Y-%m") for d in monthly.index[::3]], fontsize=7)
ax.set_title(f"Valid response days by coin-month; {short:.1%} of EXPLORE days have < 5 coins")
fig.colorbar(im, ax=ax, fraction=0.02)
C.savefig(fig, "00_missingness.png")
out["2"] = {"short_day_share": short, "thin_coin_months": int(thin.sum().sum()),
            "coins_per_day_median": float(ncoin.median()), "coins_per_day_min": int(ncoin.min())}

# ---- 3. autocorrelation
def pooled_acf(df, lags=5):
    res = {}
    for k in range(1, lags + 1):
        xs, ys = [], []
        for c in df.columns:
            s = df[c].astype(float)
            a, b = s.values[k:], s.values[:-k]
            m = ~np.isnan(a) & ~np.isnan(b)
            z = lambda x: (x - np.nanmean(s)) / np.nanstd(s)
            xs.append(z(a[m])); ys.append(z(b[m]))
        x, y = np.concatenate(xs), np.concatenate(ys)
        res[k] = (float(np.mean(x * y)), len(x))
    return res
lv = np.log(F["volume"].loc[C.in_slice(F["volume"].index, "EXPLORE")].replace(0, np.nan))
lv = lv - lv.rolling(20, min_periods=10).mean()
acf = {"return": pooled_acf(RE[live_coins]), "abs_return": pooled_acf(RE[live_coins].abs()),
       "log_volume_detrended": pooled_acf(lv[live_coins])}
d3 = pd.DataFrame({k: {lag: v[0] for lag, v in d.items()} for k, d in acf.items()})
nmin = min(v[1] for d in acf.values() for v in d.values())
d3["band_2_over_sqrt_n"] = 2 / np.sqrt(nmin)
d3.to_csv(T("p0_03_acf.csv"))
fig, ax = plt.subplots(figsize=(8, 3.4))
for i, k in enumerate(["return", "abs_return", "log_volume_detrended"]):
    ax.plot(d3.index, d3[k], marker="o", color=C.PAL[i], label=k)
ax.axhline(2 / np.sqrt(nmin), color=C.GRAY, ls="--"); ax.axhline(-2 / np.sqrt(nmin), color=C.GRAY, ls="--")
ax.set_xlabel("lag (days)"); ax.legend(fontsize=7)
ax.set_title(f"Returns: lag-1 ACF {d3.loc[1,'return']:+.3f}; |returns| and volume persist")
C.savefig(fig, "00_acf.png")
out["3"] = d3.round(4).to_dict()

# ---- 4. cross-column, impostors
cm = RE[live_coins].corr()
cm.to_csv(T("p0_04_return_corr.csv"))
c_close = F["close"]
r_bin = np.log(c_close / c_close.shift(1))
base = {"b_rev1": -r_bin, "b_mom20": np.log(c_close / c_close.shift(20)),
        "b_vol20": r_bin.rolling(20, min_periods=15).std(),
        "b_volu": np.log(F["volume"]) - np.log(F["volume"]).rolling(20, min_periods=15).mean()}
allsig = {**A, **base}
names = list(allsig)
def xs_corr(a, b):
    a = a.loc[C.in_slice(a.index, "EXPLORE")]; b = b.loc[a.index]
    v = []
    for d in a.index:
        x, y = a.loc[d], b.loc[d]
        m = x.notna() & y.notna()
        if m.sum() >= C.MIN_COINS and x[m].nunique() > 1 and y[m].nunique() > 1:
            v.append(x[m].rank().corr(y[m].rank()))
    return float(np.mean(v)) if v else np.nan
M = pd.DataFrame(index=names, columns=names, dtype=float)
for i, a in enumerate(names):
    for b in names[i:]:
        M.loc[a, b] = M.loc[b, a] = 1.0 if a == b else xs_corr(allsig[a], allsig[b])
M.to_csv(T("p0_04_signal_xs_corr.csv"))
# twin: Binance daily close return (d -> d+1, same window as response) vs primary response
rb_fwd = np.log(c_close.shift(-1) / c_close)
tw = pd.concat([rb_fwd.loc[RE.index].stack(), RE.stack()], axis=1, join="inner").dropna()
twin = float(tw.corr().iloc[0, 1])
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
im = ax[0].imshow(cm.values, cmap="Blues", vmin=0, vmax=1)
ax[0].set_xticks(range(len(live_coins))); ax[0].set_xticklabels(live_coins, rotation=90, fontsize=7)
ax[0].set_yticks(range(len(live_coins))); ax[0].set_yticklabels(live_coins, fontsize=7)
ax[0].set_title(f"Coin returns co-move: mean pairwise r {cm.values[np.triu_indices(len(cm),1)].mean():.2f}")
im2 = ax[1].imshow(M.values.astype(float), cmap="RdBu_r", vmin=-1, vmax=1)
ax[1].set_xticks(range(len(names))); ax[1].set_xticklabels(names, rotation=90, fontsize=7)
ax[1].set_yticks(range(len(names))); ax[1].set_yticklabels(names, fontsize=7)
for i in range(len(names)):
    for j in range(len(names)):
        ax[1].text(j, i, f"{M.values[i,j]:.2f}", ha="center", va="center", fontsize=5)
ax[1].set_title("Alpha / baseline cross-sectional rank corr (EXPLORE)")
fig.colorbar(im2, ax=ax[1], fraction=0.04)
C.savefig(fig, "00_crosscorr.png")
pairs = []
for i, a in enumerate(names):
    for b in names[i + 1:]:
        if abs(M.loc[a, b]) > 0.4 and (a in A or b in A):
            pairs.append((a, b, round(float(M.loc[a, b]), 3)))
out["4"] = {"mean_pairwise_return_corr": float(cm.values[np.triu_indices(len(cm), 1)].mean()),
            "binance_vs_primary_return_corr": twin, "related_or_impostor_pairs": pairs}

# ---- 5. regimes
q = pd.Series(pd.to_datetime(list(RE.index))).dt.to_period("Q").values
absr = RE[live_coins].abs().median(axis=1).groupby(q).median()
disp = RE[live_coins].std(axis=1).groupby(q).median()
pc = []
for p in sorted(set(q)):
    sub = RE[live_coins][q == p]
    cc = sub.corr().values
    pc.append(np.nanmean(cc[np.triu_indices(len(cc), 1)]))
d5 = pd.DataFrame({"median_abs_ret": absr, "median_dispersion": disp, "mean_pair_corr": pc})
d5.to_csv(T("p0_05_regimes.csv"))
fig, ax = plt.subplots(figsize=(9, 3.4))
ax.plot(d5.index.astype(str), d5.median_abs_ret * 1e4, marker="o", label="median |daily return| (bp)", color=C.PAL[0])
ax.plot(d5.index.astype(str), d5.median_dispersion * 1e4, marker="o", label="median cross-sectional sd (bp)", color=C.PAL[1])
ax2 = ax.twinx(); ax2.grid(False)
ax2.plot(d5.index.astype(str), d5.mean_pair_corr, marker="s", color=C.PAL[3], label="mean pairwise corr (right)")
ax.legend(fontsize=7, loc="upper left"); ax2.legend(fontsize=7, loc="upper right")
ax.set_title("EXPLORE quarters: 2020Q1 (the March crash) is the volatility outlier")
C.savefig(fig, "00_regimes.png")
med = d5.median()
shift_q = [str(i) for i in d5.index if (d5.loc[i, "median_abs_ret"] > 2 * med.median_abs_ret or
           d5.loc[i, "median_abs_ret"] < med.median_abs_ret / 2 or abs(d5.loc[i, "mean_pair_corr"] - med.mean_pair_corr) > 0.2)]
out["5"] = {"table": d5.round(4).reset_index().astype(str).values.tolist(), "shift_quarters": shift_q}

# ---- 6. intraday / weekly
hv, hr = [], []
for c in live_coins:
    h = C.load(f"spot/binance_{c}.parquet", "p0_profile")
    h = h[(h.t >= "2019-01-01") & (h.t < "2020-06-02")]
    h["ret"] = np.log(h.close / h.open).abs()
    h["share"] = h.quote_vol / h.groupby(h.t.dt.floor("D")).quote_vol.transform("sum")
    hv.append(h.groupby(h.t.dt.hour)["share"].mean()); hr.append(h.groupby(h.t.dt.hour)["ret"].mean())
hv = pd.concat(hv, axis=1).mean(axis=1); hr = pd.concat(hr, axis=1).mean(axis=1)
wd = RE[live_coins].abs().mean(axis=1).groupby(pd.to_datetime(list(RE.index)).dayofweek).mean()
pd.DataFrame({"vol_share": hv, "mean_abs_hourly_ret": hr}).to_csv(T("p0_06_hour.csv"))
wd.to_csv(T("p0_06_weekday.csv"))
fig, ax = plt.subplots(1, 2, figsize=(11, 3.4))
ax[0].bar(hv.index, hv * 100, color=C.PAL[0]); ax[0].set_xlabel("UTC hour"); ax[0].set_ylabel("% of daily volume")
ax[0].set_title(f"Volume share peaks at hour {hv.idxmax()} ({hv.max()/hv.median():.2f}x median)")
ax[1].bar(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], wd * 1e4, color=C.PAL[1])
ax[1].set_title(f"|daily return| by weekday of the RESPONSE's signal day (max/median {wd.max()/wd.median():.2f}x)")
C.savefig(fig, "00_clock.png")
out["6"] = {"hour_vol_max_over_median": float(hv.max() / hv.median()), "peak_hour": int(hv.idxmax()),
            "hour_absret_max_over_median": float(hr.max() / hr.median()), "weekday_max_over_median": float(wd.max() / wd.median())}

# ---- 7. what a row is
zg = []
for c in live_coins:
    h = C.load(f"spot/binance_{c}.parquet", "p0_profile").sort_values("t")
    h = h[(h.t >= "2019-01-01") & (h.t < "2020-06-02")]
    cont = h.t.diff().eq(pd.Timedelta(hours=1))
    zg.append({"coin": c, "zero_gap_rate": float((h.open == h.close.shift(1))[cont].mean()),
               "month_first_hour_is_00": bool(h.groupby(h.t.dt.to_period("M")).t.min().dt.hour.eq(0).all())})
d7 = pd.DataFrame(zg)
cb = F["close"]
gaps = []
for c in live_coins:
    p = C.load(f"primary/validated_{c}.parquet", "p0_profile")
    p = p[(p.t >= "2019-01-01") & (p.t < "2020-06-02") & (p.t.dt.hour == 23)]
    pe = pd.Series(p.price.values, index=p.t.dt.floor("D").dt.date)
    j = pd.concat([pe, cb[c]], axis=1, join="inner").dropna()
    gaps.append((np.abs(np.log(j.iloc[:, 0] / j.iloc[:, 1])) * 1e4).median())
d7["primary_vs_binance_close_median_gap_bp"] = gaps
d7.to_csv(T("p0_07_row.csv"), index=False)
fig, ax = plt.subplots(figsize=(8, 3.2))
ax.bar(d7.coin, d7.zero_gap_rate, color=C.PAL[0], label="zero-gap rate (open == prev close)")
ax.set_ylim(0, 1); ax.legend(fontsize=7)
ax.set_title(f"Binance 1h bars: zero-gap {d7.zero_gap_rate.median():.2f}; primary = Binance close (gap {np.median(gaps):.2f} bp)")
C.savefig(fig, "00_row.png")
out["7"] = d7.round(4).to_dict(orient="list")

json.dump(out, open(T("p0_profile_summary.json"), "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
