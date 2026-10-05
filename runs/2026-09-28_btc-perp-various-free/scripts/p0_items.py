# Phase 0 items 1-6 on EXPLORE (<= 2021-12-31). Rules are pre-committed in DATA_PROFILE.md section headers
# (written into this file's comments before the numbers were printed).
from common import *
from scipy import stats

P = pd.read_parquet("tables/p0_panel_EXPLORE.parquet")
r1 = pd.read_parquet("tables/p0_r1_EXPLORE.parquet")["r1"].dropna()
fu = pd.read_parquet("tables/p0_funding_EXPLORE.parquet")["funding"]
res = {}

# impossible values (rule 11): OI == 0, quote volume == 0 hours -> NaN with counts
res["oi_zero_hours"] = int((P["oi"] == 0).sum()); res["qvol_zero_hours"] = int((P["qvol"] == 0).sum())
for c in ["oi", "oi_val"]:
    P.loc[P[c] <= 0, c] = np.nan
P.loc[P["qvol"] <= 0, "qvol"] = np.nan
for col in ["oi", "oi_val", "qvol"]:
    P[f"d_{col}"] = np.log(P[col]).diff()
P["abs_r"] = P["r"].abs(); P["log_qvol"] = np.log(P["qvol"]); P["log_rv"] = np.log(P["rv_1m"])
P["d_log_rv"] = P["log_rv"].diff()

# ---------------- item 1: distributions. Rule: fat-tailed if excess kurtosis > 3 AND D'Agostino p < 0.01;
# zero-mass notable if share of exact zeros > 5%.
cols1 = ["r", "d_qvol", "d_log_rv", "buy_share", "perp_taker_buy_share", "log_taker", "d_oi", "d_ls_top_cnt",
         "d_ls_top_sum", "d_ls_all", "basis_bp", "d_basis", "d_dvol", "half_bp", "d_half_bp"]
rows = []
def dstat(name, s):
    s = s.replace([np.inf, -np.inf], np.nan).dropna()
    nt = stats.normaltest(s) if len(s) > 20 else (np.nan, np.nan)
    return dict(col=name, n=len(s), mean=s.mean(), std=s.std(), skew=stats.skew(s), exkurt=stats.kurtosis(s),
                zero_share=float((s == 0).mean()), p01=s.quantile(.01), p99=s.quantile(.99), normaltest_p=nt[1])
rows = [dstat(c, P[c]) for c in cols1] + [dstat("r1 (1m)", r1), dstat("funding (8h)", fu)]
T1 = pd.DataFrame(rows); T1["fat"] = (T1.exkurt > 3) & (T1.normaltest_p < 0.01); T1["zero_notable"] = T1.zero_share > .05
T1.to_csv("tables/p0_1_distributions.csv", index=False); print(T1.round(4).to_string())
res["funding_cap_hits"] = int((fu.abs() >= 0.003 - 1e-12).sum()); res["funding_n"] = int(len(fu))
res["funding_eq_0.0001_share"] = float(np.isclose(fu, 1e-4).mean())
fig, axs = plt.subplots(4, 5, figsize=(16, 11)); axs = axs.ravel()
for i, (c, s) in enumerate([(c, P[c]) for c in cols1] + [("r1 (1m)", r1), ("funding (8h)", fu)]):
    s = s.replace([np.inf, -np.inf], np.nan).dropna(); lo, hi = s.quantile([.001, .999])
    axs[i].hist(s.clip(lo, hi), bins=120, color=PAL[0]); axs[i].set_yscale("log"); axs[i].set_title(c, fontsize=9)
for a in axs[len(cols1) + 2:]: a.axis("off")
fig.suptitle("Phase 0 item 1 - distributions (EXPLORE, clipped to p0.1-p99.9, log count)"); save(fig, "00_1_distributions")

# ---------------- item 2: missingness. Rule: a month is notable if coverage of the hourly grid < 95%; a gap is notable if
# >= 24 consecutive missing hours inside a series' own coverage span.
cov_cols = {"spot close": "close", "1m minutes (n_min=60)": None, "metrics (oi)": "oi", "ls_all": "ls_all",
            "dvol": "dvol", "half_bp": "half_bp", "basis": "basis_bp"}
cov = {}
for lab, c in cov_cols.items():
    s = (P["n_min"] == 60) if c is None else P[c].notna()
    first = s[s].index.min()
    s = s.loc[first:]
    cov[lab] = s.groupby(s.index.to_period("M")).mean() * 100
    runs = (~s).astype(int).groupby((s != s.shift()).cumsum()).sum()
    res[f"gap_max_hours::{lab}"] = int(runs.max()); res[f"gaps_ge_24h::{lab}"] = int((runs >= 24).sum())
    res[f"months_lt95::{lab}"] = int((cov[lab] < 95).sum()); res[f"first::{lab}"] = str(first)
fc = fu.index.to_series().diff().dt.total_seconds().div(3600)
res["funding_steps_ne_8h"] = int((fc.dropna() != 8).sum())
C = pd.DataFrame(cov).T; C.to_csv("tables/p0_2_coverage_by_month.csv")
hs_year = P["half_bp"].notna().groupby(P.index.year).mean().round(3).to_dict(); res["half_bp_coverage_by_year"] = hs_year
fig, ax = plt.subplots(figsize=(15, 3.6))
im = ax.imshow(C.values, aspect="auto", cmap="Blues", vmin=0, vmax=100)
ax.set_yticks(range(len(C))); ax.set_yticklabels(C.index); xt = list(range(0, C.shape[1], 6))
ax.set_xticks(xt); ax.set_xticklabels([str(C.columns[i]) for i in xt], rotation=45, fontsize=8)
fig.colorbar(im, ax=ax, label="% of hours present"); ax.set_title("Phase 0 item 2 - coverage by month (EXPLORE)")
save(fig, "00_2_missingness")
print({k: v for k, v in res.items()})

# ---------------- item 3: autocorrelation. Rule: significant if |ACF(k)| > 2/sqrt(n).
def acf(s, lags):
    s = s.replace([np.inf, -np.inf], np.nan)
    return {k: s.corr(s.shift(k)) for k in lags}
L = [1, 2, 3, 6, 12, 24]
acf_rows = []
for c in ["r", "abs_r", "log_qvol", "d_qvol", "log_rv", "basis_bp", "d_basis", "d_oi", "d_ls_all", "d_ls_top_cnt",
          "log_taker", "half_bp", "d_half_bp", "d_dvol", "buy_share"]:
    s = P[c]; n = s.replace([np.inf, -np.inf], np.nan).notna().sum()
    a = acf(s, L); acf_rows.append(dict(col=c, n=int(n), band=2 / np.sqrt(n), **{f"lag{k}": v for k, v in a.items()}))
a1 = acf(r1, [1, 2, 3, 5]); acf_rows.append(dict(col="r1 (1m)", n=len(r1), band=2 / np.sqrt(len(r1)), **{f"lag{k}": v for k, v in a1.items()}))
fa = acf(fu.reset_index(drop=True), [1, 2, 3]); acf_rows.append(dict(col="funding (8h lags)", n=len(fu), band=2 / np.sqrt(len(fu)), **{f"lag{k}": v for k, v in fa.items()}))
T3 = pd.DataFrame(acf_rows); T3.to_csv("tables/p0_3_acf.csv", index=False); print(T3.round(3).to_string())
roll_c = np.sqrt(max(-r1.cov(r1.shift(1)), 0)) * 1e4
res["roll_halfspread_bp_1m"] = float(roll_c); res["half_bp_median_explore"] = float(P["half_bp"].median())
fig, ax = plt.subplots(1, 2, figsize=(13, 4))
for c, col in (("r", PAL[0]), ("abs_r", PAL[5]), ("log_qvol", PAL[1]), ("basis_bp", PAL[3]), ("d_oi", PAL[6])):
    s = P[c]; ax[0].plot(range(1, 49), [s.corr(s.shift(k)) for k in range(1, 49)], label=c, color=col)
ax[0].axhline(0, color=GRAY); ax[0].set_xlabel("lag (h)"); ax[0].legend(fontsize=8); ax[0].set_title("hourly ACF, EXPLORE")
ax[1].bar(range(1, 11), [r1.corr(r1.shift(k)) for k in range(1, 11)], color=PAL[0]); ax[1].axhline(0, color=GRAY)
ax[1].set_title("1-minute spot return ACF"); ax[1].set_xlabel("lag (min)")
save(fig, "00_3_acf")

# ---------------- item 4: cross-column. Rule: impostor/twin if |Spearman| > 0.9 on changes; lead-lag screen notable if
# |corr(X_t, Y_{t+k})| > 2/sqrt(n) (reported, K counted as Phase-0 looks, not scored as findings).
cols4 = ["r", "d_qvol", "d_log_rv", "buy_share", "perp_taker_buy_share", "log_taker", "d_oi", "d_oi_val", "d_ls_top_cnt",
         "d_ls_top_sum", "d_ls_all", "d_basis", "basis_bp", "d_dvol", "d_half_bp"]
X = P[cols4].replace([np.inf, -np.inf], np.nan)
Cm = X.loc["2020-09-01":].corr(method="spearman"); Cm.to_csv("tables/p0_4_corr_spearman.csv")
tw = [(a, b, Cm.loc[a, b]) for i, a in enumerate(cols4) for b in cols4[i + 1:] if abs(Cm.loc[a, b]) > .5]
res["pairs_abs_spearman_gt_0.5"] = [(a, b, round(v, 3)) for a, b, v in tw]
fig, ax = plt.subplots(figsize=(9, 8))
im = ax.imshow(Cm.values, cmap="RdBu_r", vmin=-1, vmax=1); ax.set_xticks(range(len(cols4))); ax.set_yticks(range(len(cols4)))
ax.set_xticklabels(cols4, rotation=90, fontsize=8); ax.set_yticklabels(cols4, fontsize=8)
for i in range(len(cols4)):
    for j in range(len(cols4)):
        ax.text(j, i, f"{Cm.values[i, j]:.2f}", ha="center", va="center", fontsize=6)
fig.colorbar(im); ax.set_title("Phase 0 item 4 - Spearman on changes, 2020-09..2021-12 (EXPLORE)"); save(fig, "00_4_corr")
# lead-lag screen vs next-hour and next-24h spot return, and next-24h realized vol
fwd = {"r_next1": P["r"].shift(-1), "r_next24": P["r"].rolling(24).sum().shift(-24),
       "absr_next24": P["abs_r"].rolling(24).sum().shift(-24), "logrv_next24": np.log((P["rv_1m"] ** 2).rolling(24).sum().shift(-24)) / 2}
ll = []
for c in ["r", "d_qvol", "buy_share", "log_taker", "d_oi", "d_ls_all", "d_ls_top_cnt", "basis_bp", "d_basis", "d_dvol",
          "dvol", "half_bp", "d_half_bp", "log_rv"]:
    for fk, fy in fwd.items():
        j = pd.concat([X[c] if c in X else P[c], fy], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
        ll.append(dict(x=c, y=fk, n=len(j), rho=j.corr(method="spearman").iloc[0, 1], band=2 / np.sqrt(len(j))))
LL = pd.DataFrame(ll); LL["notable"] = LL.rho.abs() > LL.band; LL.to_csv("tables/p0_4_leadlag_screen.csv", index=False)
print(LL.round(4).to_string())
# funding (8h cadence): funding at settlement t vs spot return over the next 8h / 24h, and vs basis
f8 = fu.to_frame("funding")
cl = P["close"]
f8["r_next8"] = np.log(cl.reindex(f8.index + pd.Timedelta("8h")).values / cl.reindex(f8.index).values)
f8["r_next24"] = np.log(cl.reindex(f8.index + pd.Timedelta("24h")).values / cl.reindex(f8.index).values)
f8["r_prev24"] = np.log(cl.reindex(f8.index).values / cl.reindex(f8.index - pd.Timedelta("24h")).values)
f8["basis_prev8"] = P["basis_bp"].rolling(8).mean().shift(1).reindex(f8.index)
res["funding_spearman"] = f8.corr(method="spearman").round(3)["funding"].to_dict(); res["funding_n_rows"] = int(f8.dropna().shape[0])

# ---------------- item 5: regimes by era. Rule: a structural break is noted when an era's statistic differs from the
# adjacent era's by more than 2x (ratio) or flips sign for signed statistics.
P["era"] = np.select([P.index.year <= 2018, P.index.year == 2019, P.index.year == 2020, P.index.year == 2021],
                     ["2017-18", "2019", "2020", "2021"], "other")
def era_stats(g):
    return pd.Series(dict(std_r=g["r"].std(), exkurt_r=stats.kurtosis(g["r"].dropna()), acf1_r=g["r"].autocorr(1),
                          acf1_absr=g["abs_r"].autocorr(1), med_qvol=g["qvol"].median(), med_ntrades=g["ntrades"].median(),
                          med_half_bp=g["half_bp"].median(), cov_half_bp=g["half_bp"].notna().mean(),
                          basis_mean=g["basis_bp"].mean(), basis_std=g["basis_bp"].std(),
                          ls_all_zero_chg=(g["d_ls_all"] == 0).mean() if g["d_ls_all"].notna().any() else np.nan,
                          buy_share_std=g["buy_share"].std()))
E5 = P.groupby("era").apply(era_stats); r1e = r1.groupby(np.select([r1.index.year <= 2018, r1.index.year == 2019, r1.index.year == 2020], ["2017-18", "2019", "2020"], "2021"))
E5["acf1_r1m"] = r1e.apply(lambda s: s.autocorr(1)); E5.to_csv("tables/p0_5_eras.csv"); print(E5.round(4).T.to_string())
q = P.loc["2020-09":].copy(); q["half"] = np.where(q.index < "2021-01-01", "2020-09..12", np.where(q.index < "2021-07-01", "2021H1", "2021H2"))
E5b = q.groupby("half").agg(basis_mean=("basis_bp", "mean"), basis_std=("basis_bp", "std"), oi_med=("oi", "median"),
                            ls_all_med=("ls_all", "median"), ls_top_med=("ls_top_cnt", "median"), dvol_med=("dvol", "median"),
                            ls_all_zero=("d_ls_all", lambda s: (s == 0).mean()))
E5b.to_csv("tables/p0_5_eras_derivs.csv"); print(E5b.round(3).to_string())
fig, axs = plt.subplots(3, 2, figsize=(14, 9), sharex=False); axs = axs.ravel()
axs[0].plot(P["r"].rolling(24 * 30).std(), color=PAL[0]); axs[0].set_title("30d rolling std of hourly r")
axs[1].plot(P["qvol"].rolling(24 * 30).median(), color=PAL[1]); axs[1].set_yscale("log"); axs[1].set_title("30d median hourly quote volume (spot)")
axs[2].plot(P["half_bp"].rolling(24 * 30, min_periods=24).median(), color=PAL[5]); axs[2].set_title("30d median half_bp")
axs[3].plot(P["basis_bp"].rolling(24 * 7, min_periods=24).mean(), color=PAL[3]); axs[3].axhline(0, color=GRAY); axs[3].set_title("7d mean basis_bp (perp - spot)")
axs[4].plot(P["ls_all"], color=PAL[6], lw=.6, label="ls_all"); axs[4].plot(P["ls_top_cnt"], color=PAL[2], lw=.6, label="ls_top_cnt"); axs[4].legend(fontsize=8); axs[4].set_title("long/short ratios (levels)")
axs[5].plot(P["dvol"], color=PAL[7], lw=.7); axs[5].set_title("DVOL")
fig.suptitle("Phase 0 item 5 - regime structure (EXPLORE)"); save(fig, "00_5_regimes")

# ---------------- item 6: intraday / weekly shape (descriptive). Rule: a shape is noted if max/min across hours > 1.5.
P["hod"] = P.index.hour; P["dow"] = P.index.dayofweek
s6 = P.loc["2019-01-01":]
H6 = s6.groupby("hod").agg(qvol_med=("qvol", "median"), absr_mean=("abs_r", "mean"), rv_med=("rv_1m", "median"),
                             half_bp_med=("half_bp", "median"), basis_mean=("basis_bp", "mean"), d_oi_absmean=("d_oi", lambda s: s.abs().mean()))
W6 = s6.groupby("dow").agg(qvol_med=("qvol", "median"), absr_mean=("abs_r", "mean"), rv_med=("rv_1m", "median"),
                             half_bp_med=("half_bp", "median"))
H6.to_csv("tables/p0_6_hour_of_day.csv"); W6.to_csv("tables/p0_6_day_of_week.csv")
res["hod_max_min_ratio"] = (H6.max() / H6.min()).round(2).to_dict(); res["dow_max_min_ratio"] = (W6.max() / W6.min()).round(2).to_dict()
print(H6.round(4).to_string()); print(W6.round(4).to_string())
fig, axs = plt.subplots(1, 3, figsize=(15, 4))
axs[0].bar(H6.index, H6.qvol_med / H6.qvol_med.mean(), color=PAL[1]); axs[0].set_title("median quote vol by UTC hour (rel.)")
axs[1].bar(H6.index, H6.rv_med / H6.rv_med.mean(), color=PAL[0]); axs[1].set_title("median 1m-RV by UTC hour (rel.)")
axs[2].bar(H6.index, H6.half_bp_med, color=PAL[5]); axs[2].set_title("median half_bp by UTC hour")
for a in axs: a.set_xlabel("UTC hour (open stamp)")
for h in (0, 8, 16):
    for a in axs: a.axvline(h, color=GRAY, ls=":", lw=1)
fig.suptitle("Phase 0 item 6 - intraday shape 2019-2021 (EXPLORE); dotted = funding settlement hours"); save(fig, "00_6_intraday")

json.dump(res, open("tables/p0_summary.json", "w"), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
