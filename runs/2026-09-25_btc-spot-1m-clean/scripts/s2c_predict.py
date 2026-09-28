"""Sweep rows 7-11, 13: 09 relationship stability, 10 IC / lead-lag, 11 calendar, 12 monotone sorts,
13 group distributions, 14 outliers/runs. TRAIN only."""
import warnings; warnings.filterwarnings("ignore")
from lib import *
from scipy import stats
import statsmodels.api as sm

g = grid(load_train(["open", "high", "low", "close", "vol", "buy_vol", "n", "gap_min",
                     "flag_repeat_prev_bar", "flag_close_outlier", "flag_wick_gt3pct", "flag_low_invalid", "flag_quote_bad"]))
r = g["r"]; E = pd.Series(era(g.index), index=g.index)
g["tr5"] = trail(r, 5); g["imb5"] = g["imb"].rolling(5, min_periods=5).mean(); g["dlogn"] = g["logn"].diff()
for tau in (1, 5, 20, 60):
    g[f"f{tau}"] = fwd(r, tau)
g["absr5"] = r.abs().rolling(5, min_periods=5).sum(); g["absr60"] = r.abs().rolling(60, min_periods=60).sum()
g["fabs5"] = r.abs().rolling(5, min_periods=5).sum().shift(-6); g["fabs60"] = r.abs().rolling(60, min_periods=60).sum().shift(-61)
BRK = pd.Timestamp("2020-01-01", tz="UTC")

def chow_inter(y, x, lags):
    d = pd.concat([y, x], axis=1).dropna(); d.columns = ["y", "x"]
    D = (d.index >= BRK).astype(float)
    X = sm.add_constant(np.column_stack([d.x.values, D, d.x.values * D]))
    m = sm.OLS(d.y.values, X).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return m.params[1], m.params[1] + m.params[3], m.tvalues[3], m.pvalues[3]

# ---------- 09 relationship stability
mo = g.index.to_period("M")
rows = []
for p_, x in g.groupby(mo):
    d1 = pd.concat([x.r, x.r.shift(1)], axis=1).dropna()
    d2 = x[["f5", "imb"]].dropna()
    rows.append(dict(month=str(p_), ar1=np.polyfit(d1.iloc[:, 1], d1.iloc[:, 0], 1)[0] if len(d1) > 1000 else np.nan,
                     imb_slope_bp=np.polyfit(d2.imb, d2.f5 * 1e4, 1)[0] if len(d2) > 1000 else np.nan))
t09 = pd.DataFrame(rows).set_index("month")
a_pre, a_post, a_t, a_p = chow_inter(r, r.shift(1), 10)
b_pre, b_post, b_t, b_p = chow_inter(g.f5, g.imb, 10)
t09b = pd.DataFrame([dict(rel="AR(1) 1-min r", pre2020=a_pre, post2020=a_post, t_change=a_t, p_change=a_p),
                     dict(rel="fwd5 r on taker imbalance", pre2020=b_pre, post2020=b_post, t_change=b_t, p_change=b_p)])
table(t09, 9, "monthly_coefficients"); table(t09b, 9, "chow_2020"); print(t09b)
reg_p("09_chow_ar1", "Chow (HAC interaction)", "AR(1) 1-min r at 2020-01-01", "t", a_p)
reg_p("09_chow_imb", "Chow (HAC interaction)", "fwd5 on imbalance at 2020-01-01", "t", b_p)
fig, ax = plt.subplots(2, 1, figsize=(10, 5.5), sharex=True)
xi = pd.PeriodIndex(t09.index, freq="M").to_timestamp()
ax[0].plot(xi, t09.ar1, color=PAL[0], marker=".", label="monthly AR(1) of 1-min r"); ax[0].axhline(0, color="k", lw=0.6); ax[0].legend(fontsize=8); ax[0].set_ylim(-0.25, 0.1)
ax[1].plot(xi, t09.imb_slope_bp, color=PAL[1], marker=".", label="monthly slope: fwd 5-min r (bp) per unit imbalance"); ax[1].axhline(0, color="k", lw=0.6); ax[1].legend(fontsize=8)
fig.suptitle(f"09: AR(1) {a_pre:+.3f} before 2020 vs {a_post:+.3f} after (change t={a_t:.1f}); imbalance slope {b_pre:+.2f} vs {b_post:+.2f} bp (t={b_t:.1f})", fontweight="bold", fontsize=10)
save(fig, 9, "relationship_stability")

# ---------- 10 IC and lead-lag
def ic(xc, yc, sub=None, lags=10):
    d = g[[xc, yc]] if sub is None else g.loc[sub, [xc, yc]]
    d = d.dropna()
    rx = d[xc].rank().values; ry = d[yc].rank().values
    rx = (rx - rx.mean()) / rx.std(); ry = (ry - ry.mean()) / ry.std()
    m = sm.OLS(ry, rx).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return m.params[0], m.tvalues[0], m.pvalues[0], len(d)
rows = []
for xc in ["r", "tr5", "imb", "imb5", "dlogn"]:
    for tau in (1, 5, 20):
        v, t, p, n = ic(xc, f"f{tau}", lags=tau + 5)
        eras = {e: ic(xc, f"f{tau}", sub=(E == e).values, lags=tau + 5)[0] for e in ERAS}
        rows.append(dict(X=xc, Y=f"fwd{tau}", ic=v, t_hac=t, p=p, n=n, **{f"ic_{e}": eras[e] for e in ERAS}))
        reg_p(f"10_ic_{xc}_f{tau}", "Spearman IC (HAC)", f"{xc} -> fwd{tau} r", "t", p)
for xc, yc in [("absr5", "fabs5"), ("absr60", "fabs60")]:
    v, t, p, n = ic(xc, yc, lags=70)
    eras = {e: ic(xc, yc, sub=(E == e).values, lags=70)[0] for e in ERAS}
    rows.append(dict(X=xc, Y=yc, ic=v, t_hac=t, p=p, n=n, **{f"ic_{e}": eras[e] for e in ERAS}))
    reg_p(f"10_ic_{xc}_{yc}", "Spearman IC (HAC)", f"{xc} -> {yc}", "t", p)
t10 = pd.DataFrame(rows); table(t10, 10, "ic_table"); print(t10.round(4).to_string())
ll = {k: g["imb"].corr(r.shift(-k)) for k in range(-10, 11)}
table(pd.Series(ll, name="corr(imb_t, r_t+k)"), 10, "leadlag_imbalance")
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
dirn = t10[~t10.X.str.startswith("absr")]
lab = dirn.X + "->" + dirn.Y
ax[0].barh(lab, dirn.ic, color=[PAL[0] if abs(t) > 3 else GRAY for t in dirn.t_hac]); ax[0].axvline(0, color="k", lw=0.6)
ax[0].set_xlabel("pooled Spearman IC (blue: |t_HAC| > 3)"); ax[0].tick_params(axis="y", labelsize=7)
ax[1].bar(list(ll.keys()), list(ll.values()), color=[PAL[1] if k == 0 else GRAY for k in ll]); ax[1].set_yscale("symlog", linthresh=0.01)
ax[1].set_xlabel("k (min): corr(imbalance_t, r_t+k)"); ax[1].set_title(f"lead-lag: k=0 {ll[0]:.2f}, k=+1 {ll[1]:.3f}, k=+2 {ll[2]:.3f}", fontsize=10)
best = dirn.iloc[dirn.ic.abs().argmax()]
szs = t10[t10.X.str.startswith("absr")].ic
fig.suptitle(f"10: largest direction IC {best.X}->{best.Y} = {best.ic:+.3f}; size IC {szs.min():.2f}..{szs.max():.2f}", fontweight="bold")
save(fig, 10, "ic_leadlag")

# ---------- 11 calendar
hr = r.resample("60min").sum(min_count=1).dropna()
hh = hr.index.hour; Eh = pd.Series(era(hr.index), index=hr.index)
cal = pd.DataFrame({"mean_bp": hr.groupby(hh).mean() * 1e4, "mean_abs_bp": hr.abs().groupby(hh).mean() * 1e4, "n": hr.groupby(hh).size()})
cal.index.name = "hour_utc"
kw_m = stats.kruskal(*[hr[hh == h].values for h in range(24)]).pvalue
kw_a = stats.kruskal(*[hr[hh == h].abs().values for h in range(24)]).pvalue
per_era = pd.DataFrame({e: hr[Eh == e].groupby(hh[Eh.values == e]).mean() * 1e4 for e in ERAS})
per_era_a = pd.DataFrame({e: hr[Eh == e].abs().groupby(hh[Eh.values == e]).mean() * 1e4 for e in ERAS})
top_h, bot_h = cal.mean_bp.idxmax(), cal.mean_bp.idxmin()
dm = per_era.sub(per_era.mean())
top_keep = int((dm.loc[top_h] > 0).sum()); bot_keep = int((dm.loc[bot_h] < 0).sum())
da = per_era_a.div(per_era_a.mean())
topa = cal.mean_abs_bp.idxmax(); bota = cal.mean_abs_bp.idxmin()
topa_keep = int((da.loc[topa] > 1).sum()); bota_keep = int((da.loc[bota] < 1).sum())
dr = r.resample("1D").sum(min_count=1).dropna(); wd = dr.index.dayofweek; Ed = pd.Series(era(dr.index), index=dr.index)
wk = pd.DataFrame({"mean_bp": dr.groupby(wd).mean() * 1e4, "mean_abs_bp": dr.abs().groupby(wd).mean() * 1e4})
kw_wm = stats.kruskal(*[dr[wd == d].values for d in range(7)]).pvalue
kw_wa = stats.kruskal(*[dr[wd == d].abs().values for d in range(7)]).pvalue
per_era_wa = pd.DataFrame({e: dr[Ed == e].abs().groupby(wd[Ed.values == e]).mean() for e in ERAS})
per_era_wm = pd.DataFrame({e: dr[Ed == e].groupby(wd[Ed.values == e]).mean() for e in ERAS})
wtop, wbot = wk.mean_bp.idxmax(), wk.mean_bp.idxmin()
wtop_keep = int((per_era_wm.sub(per_era_wm.mean()).loc[wtop] > 0).sum()); wbot_keep = int((per_era_wm.sub(per_era_wm.mean()).loc[wbot] < 0).sum())
wabot = wk.mean_abs_bp.idxmin(); wabot_keep = int((per_era_wa.div(per_era_wa.mean()).loc[wabot] < 1).sum())
cal_s = dict(kw_hour_mean_p=kw_m, kw_hour_abs_p=kw_a, top_hour=int(top_h), top_hour_eras_above=top_keep, bottom_hour=int(bot_h), bottom_hour_eras_below=bot_keep,
             top_abs_hour=int(topa), top_abs_eras=topa_keep, bottom_abs_hour=int(bota), bottom_abs_eras=bota_keep,
             kw_weekday_mean_p=kw_wm, kw_weekday_abs_p=kw_wa, top_weekday=int(wtop), top_weekday_eras=wtop_keep, bottom_weekday=int(wbot), bottom_weekday_eras=wbot_keep,
             lowest_abs_weekday=int(wabot), lowest_abs_weekday_eras=wabot_keep)
table(cal, 11, "hour_of_day"); table(wk, 11, "weekday"); table(per_era, 11, "hour_mean_by_era"); table(per_era_a, 11, "hour_abs_by_era")
json.dump(cal_s, open(os.path.join(RUN, "tables", "11_calendar_summary.json"), "w"), indent=1); print(cal_s)
for k, p in [("hour_mean", kw_m), ("hour_abs", kw_a), ("weekday_mean", kw_wm), ("weekday_abs", kw_wa)]:
    reg_p(f"11_kw_{k}", "Kruskal-Wallis", k, "H", p)
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].bar(cal.index, cal.mean_bp, color=[PAL[0] if h in (top_h, bot_h) else GRAY for h in cal.index]); ax[0].axhline(0, color="k", lw=0.6)
ax[0].set_xlabel("UTC hour"); ax[0].set_ylabel("mean hourly r (bp)"); ax[0].set_title(f"mean: KW p={kw_m:.2g}; top h{top_h} above mean in {top_keep}/7 eras", fontsize=10)
ax[1].bar(cal.index, cal.mean_abs_bp, color=PAL[1]); ax[1].set_xlabel("UTC hour"); ax[1].set_ylabel("mean |hourly r| (bp)")
ax[1].set_title(f"size: KW p={kw_a:.2g}; peak h{topa} ({topa_keep}/7 eras), trough h{bota} ({bota_keep}/7)", fontsize=10)
fig.suptitle(f"11: |r| has a strong UTC-hour profile ({cal.mean_abs_bp.max()/cal.mean_abs_bp.min():.1f}x peak/trough); mean r by hour KW p={kw_m:.2g}", fontweight="bold")
save(fig, 11, "calendar")

# ---------- 12 monotone decile sorts
def decile_sort(xc, yc, lags):
    d = g[[xc, yc]].dropna()
    q = pd.qcut(d[xc].rank(method="first"), 10, labels=False)
    m = d[yc].groupby(q).mean()
    rho = stats.spearmanr(m.index, m.values)[0]
    tb = d[(q == 9) | (q == 0)]
    b, se, t, p, n = nw_slope(tb[yc], (q[(q == 9) | (q == 0)] == 9).astype(float), lags)
    # least squares on [1, x, x^3] vs [1, x]
    xs = (d[xc] - d[xc].mean()) / d[xc].std()
    X3 = np.column_stack([np.ones(len(xs)), xs, xs ** 3]); X1 = X3[:, :2]
    c3 = np.linalg.lstsq(X3, d[yc].values, rcond=None)[0]; c1 = np.linalg.lstsq(X1, d[yc].values, rcond=None)[0]
    mse3 = np.mean((d[yc].values - X3 @ c3) ** 2); mse1 = np.mean((d[yc].values - X1 @ c1) ** 2)
    return m, rho, b, t, p, mse1, mse3, c3
res12 = {}
rows = []
for xc, yc, L in [("imb", "f5", 10), ("tr5", "f5", 10), ("absr60", "fabs60", 70)]:
    m, rho, b, t, p, mse1, mse3, c3 = decile_sort(xc, yc, L)
    res12[(xc, yc)] = m
    rows.append(dict(X=xc, Y=yc, spearman_decile=rho, top_minus_bottom_bp=b * 1e4, t_hac=t, p=p, mse_linear=mse1, mse_cubic=mse3, cubic_coef=c3[2],
                     **{f"d{i}": m.iloc[i] * 1e4 for i in range(10)}))
    reg_p(f"12_decile_{xc}_{yc}", "decile sort top-bottom (HAC)", f"{xc} -> {yc}", "t", p)
t12 = pd.DataFrame(rows); table(t12, 12, "decile_sorts"); print(t12.round(4).T)
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
for i, ((xc, yc), m) in enumerate(res12.items()):
    ax[i].bar(range(1, 11), m.values * 1e4, color=PAL[i]); ax[i].axhline(0, color="k", lw=0.6)
    rr = t12.iloc[i]; ax[i].set_title(f"{xc}->{yc}: rho={rr.spearman_decile:.2f}, T-B {rr.top_minus_bottom_bp:+.2f}bp (t={rr.t_hac:.1f})", fontsize=9)
    ax[i].set_xlabel(f"decile of {xc}"); ax[i].set_ylabel(f"mean {yc} (bp)")
fig.suptitle(f"12: |r| sort monotone (T-B {t12.top_minus_bottom_bp[2]:.0f} bp); tr5 reversal monotone but T-B only {t12.top_minus_bottom_bp[1]:+.2f} bp; imbalance not monotone", fontweight="bold", fontsize=10)
save(fig, 12, "decile_sorts")

# ---------- 13 distributions differ
we = dr[wd >= 5]; wdd = dr[wd < 5]
rows = []
for lab, a_, b_ in [("daily r weekend vs weekday", we, wdd), ("daily |r| weekend vs weekday", we.abs(), wdd.abs())]:
    ks = stats.ks_2samp(a_, b_).pvalue; mw = stats.mannwhitneyu(a_, b_).pvalue; wt = stats.ttest_ind(a_, b_, equal_var=False).pvalue
    dir_eras = sum(np.sign(a_[Ed.loc[a_.index] == e].mean() - b_[Ed.loc[b_.index] == e].mean()) == np.sign(a_.mean() - b_.mean()) for e in ERAS)
    rows.append(dict(test=lab, mean_a_bp=a_.mean() * 1e4, mean_b_bp=b_.mean() * 1e4, ks_p=ks, mw_p=mw, welch_p=wt, eras_same_direction=dir_eras))
    reg_p(f"13_{lab[:12].replace(' ', '_')}_ks", "KS", lab, "D", ks); reg_p(f"13_{lab[:12].replace(' ', '_')}_mw", "Mann-Whitney", lab, "U", mw)
d = g[["imb", "f5"]].dropna(); d["E"] = E.loc[d.index].values
d["q"] = d.groupby("E")["imb"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
top = d[d.q == 9].f5; bot = d[d.q == 0].f5
ks = stats.ks_2samp(top, bot).pvalue; mw = stats.mannwhitneyu(top, bot).pvalue; wt = stats.ttest_ind(top, bot, equal_var=False).pvalue
dir_eras = sum(np.sign(d[(d.q == 9) & (d.E == e)].f5.mean() - d[(d.q == 0) & (d.E == e)].f5.mean()) == np.sign(top.mean() - bot.mean()) for e in ERAS)
rows.append(dict(test="fwd5 r after top vs bottom imbalance decile (per-era deciles)", mean_a_bp=top.mean() * 1e4, mean_b_bp=bot.mean() * 1e4, ks_p=ks, mw_p=mw, welch_p=wt, eras_same_direction=dir_eras))
reg_p("13_imb_topbot_ks", "KS", "fwd5 top vs bottom imbalance decile", "D", ks); reg_p("13_imb_topbot_mw", "Mann-Whitney", "fwd5 top vs bottom imbalance decile", "U", mw)
t13 = pd.DataFrame(rows); table(t13, 13, "group_tests"); print(t13.round(4).T)
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].hist(wdd.abs() * 1e4, bins=80, density=True, alpha=0.6, color=GRAY, label="weekday"); ax[0].hist(we.abs() * 1e4, bins=80, density=True, alpha=0.6, color=PAL[0], label="weekend")
ax[0].set_xlim(0, 1500); ax[0].set_xlabel("|daily r| (bp)"); ax[0].legend(); ax[0].set_title(f"|daily r|: weekend {we.abs().mean()*1e4:.0f} vs weekday {wdd.abs().mean()*1e4:.0f} bp (MW p={t13.mw_p[1]:.1g})", fontsize=10)
qq = np.linspace(0.01, 0.99, 99)
ax[1].plot(np.quantile(bot, qq) * 1e4, np.quantile(top, qq) * 1e4, color=PAL[1]); lim = np.quantile(bot, [0.01, 0.99]) * 1e4
ax[1].plot(lim, lim, color="k", lw=0.6); ax[1].set_xlabel("fwd5 r after bottom-decile imbalance (bp)"); ax[1].set_ylabel("after top decile (bp)")
ax[1].set_title(f"fwd5: top {top.mean()*1e4:+.2f} vs bottom {bot.mean()*1e4:+.2f} bp, same sign {dir_eras}/7 eras", fontsize=10)
fig.suptitle(f"13: weekend |daily r| {t13.mean_a_bp[1]:.0f} vs {t13.mean_b_bp[1]:.0f} bp weekday; imbalance top-bottom fwd5 gap {t13.mean_a_bp[2]-t13.mean_b_bp[2]:+.2f} bp", fontweight="bold", fontsize=10)
save(fig, 13, "group_tests")

# ---------- 14 outliers / runs (only new things count)
z = (r == 0).astype(float).where(r.notna())
runs = []
for e in ERAS:
    zz = z[E == e].fillna(0).values
    edges = np.diff(np.concatenate([[0], zz, [0]]))
    st = np.where(edges == 1)[0]; en = np.where(edges == -1)[0]; L = en - st
    runs.append(dict(era=e, zero_ret_share=np.nanmean(z[E == e]), runs=len(L), max_run=L.max() if len(L) else 0, runs_ge5=int((L >= 5).sum()),
                     flag_repeat=int(g.loc[E == e, "flag_repeat_prev_bar"].fillna(False).sum()), flag_outlier=int(g.loc[E == e, "flag_close_outlier"].fillna(False).sum()),
                     flag_wick=int(g.loc[E == e, "flag_wick_gt3pct"].fillna(False).sum()), missing=int(g.loc[E == e, "close"].isna().sum())))
t14 = pd.DataFrame(runs).set_index("era"); table(t14, 14, "runs_flags"); print(t14)
fig, ax = plt.subplots(figsize=(9, 3.6))
ax.bar(t14.index, t14.zero_ret_share * 100, color=PAL[0]); ax.set_ylabel("% zero-return 1-min bars")
for i, e in enumerate(t14.index): ax.text(i, t14.zero_ret_share.iloc[i] * 100, f"max run {t14.max_run.iloc[i]}", ha="center", va="bottom", fontsize=8)
ax.set_title(f"14: zero-return share and runs match CLEANING_LOG (2017 {t14.zero_ret_share['2017']*100:.1f}%, 2018+ <= {t14.zero_ret_share.drop('2017').max()*100:.1f}%): nothing new", fontsize=10)
save(fig, 14, "runs_flags")
