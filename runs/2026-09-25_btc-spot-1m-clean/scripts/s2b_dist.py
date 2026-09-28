"""Sweep rows 4-6: 06 fat tails, 07 heteroskedasticity, 08 regime changes. Plus ACF-lag p-values for row 2. TRAIN only."""
import warnings; warnings.filterwarnings("ignore")
from lib import *
from scipy import stats
from statsmodels.stats.diagnostic import het_arch, breaks_cusumolsresid
from statsmodels.tsa.stattools import acf
import statsmodels.api as sm

g = grid(load_train(["open", "high", "low", "close", "vol", "buy_vol", "n", "gap_min"]))
r = g["r"]; E = pd.Series(era(g.index), index=g.index)

# row-2 follow-up p-values (HAC) for the ACF lags flagged in 05, pooled
for lag in json.load(open(os.path.join(RUN, "tables", "05_acf_candidates.json")))["acf_candidates"]:
    b, se, t, p, n = nw_slope(r, r.shift(lag), 20)
    reg_p(f"05_acf_lag{lag}", "ACF (HAC slope)", "1-min r pooled", "t_HAC", p, f"beta={b:.4f}")
    print("lag", lag, b, t, p)

# ---------- 06 fat tails
r1 = r.dropna()
r60 = r.resample("60min").sum(min_count=60).dropna()
def hill(x, frac=0.01):
    x = np.sort(x[x > 0])[::-1]; k = max(int(len(x) * frac), 10)
    return 1 / np.mean(np.log(x[:k] / x[k]))
rng = np.random.default_rng(0)
rows = []
for lab, s in [("1-min", r1), ("60-min", r60)]:
    k2, pn = stats.normaltest(s)
    hl, hr = hill(-s.values), hill(s.values)
    # daily-block bootstrap CI for the Hill indexes
    days = s.index.floor("D"); ud = days.unique(); idx = pd.Series(np.arange(len(s)), index=days)
    groups = [idx.loc[d].values if np.ndim(idx.loc[d]) else np.array([idx.loc[d]]) for d in ud] if lab == "60-min" else None
    bl, br = [], []
    for b in range(200):
        if lab == "1-min":
            pick = rng.choice(len(s), size=len(s) // 10, replace=True)  # subsample bootstrap (speed); CI widened accordingly below
            x = s.values[pick]
        else:
            pick = np.concatenate([groups[i] for i in rng.integers(0, len(groups), len(groups))]); x = s.values[pick]
        bl.append(hill(-x)); br.append(hill(x))
    sc = np.sqrt(0.1) if lab == "1-min" else 1.0
    ql = np.percentile(bl, [2.5, 97.5]); qr = np.percentile(br, [2.5, 97.5])
    ql = hl + (ql - np.mean(bl)) * sc; qr = hr + (qr - np.mean(br)) * sc
    rows.append(dict(series=lab, n=len(s), skew=stats.skew(s), excess_kurt=stats.kurtosis(s), dagostino_p=pn,
                     hill_left=hl, hill_left_lo=ql[0], hill_left_hi=ql[1], hill_right=hr, hill_right_lo=qr[0], hill_right_hi=qr[1]))
    reg_p(f"06_normaltest_{lab}", "D'Agostino-Pearson", f"{lab} r", "K2", pn)
t06 = pd.DataFrame(rows); table(t06, 6, "fat_tails"); print(t06.round(3).T)
qs = np.array([0.0001, 0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.975, 0.99, 0.995, 0.999, 0.9999])
var_emp = stats.scoreatpercentile(r60.values, qs * 100); var_norm = stats.norm.ppf(qs, r60.mean(), r60.std())
table(pd.DataFrame({"q": qs, "empirical_bp": var_emp * 1e4, "normal_bp": var_norm * 1e4}), 6, "var_curve_60min")
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
(osm, osr), _ = stats.probplot(r60.values, dist="norm")
ax[0].scatter(osm, osr * 1e4, s=3, color=PAL[0]); ax[0].plot(osm, (r60.mean() + r60.std() * osm) * 1e4, color=GRAY)
ax[0].set_xlabel("normal quantile"); ax[0].set_ylabel("60-min r (bp)"); ax[0].set_title("Q-Q 60-min r vs normal", fontsize=10)
ax[1].plot(qs, var_emp * 1e4, marker="o", color=PAL[0], label="empirical"); ax[1].plot(qs, var_norm * 1e4, marker="s", color=GRAY, label="fitted normal")
ax[1].set_xscale("logit"); ax[1].set_xlabel("quantile"); ax[1].set_ylabel("bp"); ax[1].legend(); ax[1].set_title("VaR curve, 60-min r", fontsize=10)
a = t06.set_index("series")
fig.suptitle(f"06: fat tails everywhere (1-min excess kurt {a.loc['1-min','excess_kurt']:.0f}); Hill left {a.loc['60-min','hill_left']:.2f} vs right {a.loc['60-min','hill_right']:.2f} (60-min)", fontweight="bold")
save(fig, 6, "fat_tails")

# ---------- 07 heteroskedasticity
lm = []
for e in ERAS:
    x = r[E == e].dropna().values[:200000]
    st, p, _, _ = het_arch(x, nlags=60); lm.append(dict(era=e, arch_lm=st, p=p))
t07a = pd.DataFrame(lm); reg_p("07_archlm_2021", "ARCH-LM", "1-min r 2021", "LM", t07a.set_index("era").loc["2021", "p"])
ac = {}
for e in ERAS:
    x = r[E == e].abs(); x0 = (x - x.mean()).fillna(0)
    ac[e] = acf(x0, nlags=1440, fft=True)[1:]
A = pd.DataFrame(ac, index=range(1, 1441)); A.index.name = "lag"
table(t07a, 7, "arch_lm"); table(A.iloc[[0, 4, 14, 59, 239, 359, 719, 1079, 1439]], 7, "acf_absr_selected_lags")
diff1440 = A.loc[1440] - A.loc[720]
print(t07a); print("ACF|r| 1440 - 720:", diff1440.round(3).to_dict())
json.dump({"acf_absr_1440_minus_720": diff1440.to_dict()}, open(os.path.join(RUN, "tables", "07_daily_periodicity.json"), "w"))
fig, ax = plt.subplots(figsize=(10, 4))
for i, e in enumerate(ERAS):
    ax.plot(A.index, A[e], lw=0.8, color=(PAL + [GRAY])[i], label=e)
for v in (720, 1440): ax.axvline(v, color="k", lw=0.5, ls="--")
ax.set_xlabel("lag (min)"); ax.set_ylabel("ACF of |r|"); ax.legend(ncol=4, fontsize=8)
ax.set_title(f"07: |r| ACF at lag 1 = {A.loc[1].min():.2f}..{A.loc[1].max():.2f}, still {A.loc[1440].min():.2f}..{A.loc[1440].max():.2f} at 1 day; ACF(1440)-ACF(720) > 0.02 in {(diff1440 > 0.02).sum()} of 7 eras", fontsize=10)
save(fig, 7, "vol_clustering")

# ---------- 08 regime changes on daily r
rd = r.resample("1D").sum(min_count=1).dropna()  # sum of available 1-min r (gap moves excluded)
roll_m = rd.rolling(30).mean() * 1e4; roll_s = rd.rolling(30).std() * 1e4
cus_stat, cus_p, _ = breaks_cusumolsresid(sm.OLS(rd.values, np.ones(len(rd))).fit().resid)
def chow(y, brk):
    y1, y2 = y[y.index < brk], y[y.index >= brk]
    rss = lambda z: np.sum((z - z.mean()) ** 2)
    k = 1; n = len(y)
    F = ((rss(y) - rss(y1) - rss(y2)) / k) / ((rss(y1) + rss(y2)) / (n - 2 * k))
    return F, stats.f.sf(F, k, n - 2 * k)
F, pF = chow(rd, pd.Timestamp("2020-01-01", tz="UTC"))
w1, pw = stats.ttest_ind(rd[rd.index < "2020-01-01"], rd[rd.index >= "2020-01-01"], equal_var=False)
from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression
mr = MarkovRegression(rd.values * 100, k_regimes=2, trend="c", switching_variance=True).fit(disp=False)
pr = mr.params; bs = mr.bse
names = mr.model.param_names
mu0, mu1 = pr[names.index("const[0]")], pr[names.index("const[1]")]
se0, se1 = bs[names.index("const[0]")], bs[names.index("const[1]")]
s0, s1 = pr[names.index("sigma2[0]")], pr[names.index("sigma2[1]")]
tdiff = (mu0 - mu1) / np.sqrt(se0 ** 2 + se1 ** 2)
t08 = pd.DataFrame([dict(cusum_stat=cus_stat, cusum_p=cus_p, chow_F_2020=F, chow_p=pF, welch_p=pw,
                         ms_mean_state0_pct=mu0, ms_mean_state1_pct=mu1, ms_var0=s0, ms_var1=s1, ms_t_meandiff=tdiff)])
table(t08, 8, "regime_tests"); print(t08.T)
reg_p("08_cusum", "OLS-CUSUM", "daily r", "sup", cus_p); reg_p("08_chow2020", "Chow", "daily r mean at 2020-01-01", "F", pF)
reg_p("08_markov_meandiff", "Markov switching", "daily r state means", "t", 2 * stats.norm.sf(abs(tdiff)))
smp = mr.smoothed_marginal_probabilities
hv = 1 if s1 > s0 else 0
fig, ax = plt.subplots(2, 1, figsize=(10, 5.5), sharex=True)
ax[0].plot(roll_s.index, roll_s, color=PAL[0], label="30-day std of daily r (bp)"); ax[0].legend(fontsize=8)
ax[0].fill_between(rd.index, 0, smp[:, hv] * roll_s.max(), color=GRAY, alpha=0.25, step="mid")
ax[1].plot(roll_m.index, roll_m, color=PAL[1], label="30-day mean of daily r (bp)"); ax[1].axhline(0, color="k", lw=0.6); ax[1].legend(fontsize=8)
fig.suptitle(f"08: volatility regimes clear, mean regimes not: CUSUM p={cus_p:.2f}, Chow(2020) p={pF:.2f}, MS mean-diff t={tdiff:.1f}", fontweight="bold")
save(fig, 8, "regimes")
