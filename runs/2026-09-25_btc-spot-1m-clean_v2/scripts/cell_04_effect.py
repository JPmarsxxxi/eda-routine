# Cell 04 - C5 the effect, pooled TRAIN.
from common import *
from scipy import stats
setup()
legs, M = daily("TRAIN")
d = pd.read_parquet("tables/01_daily_legs_TRAIN.parquet").dropna(subset=["r_first", "r_last"])
M = M.loc[d.index]
f = nw_ols(d["r_last"], d["r_first"]); b, t = f.params["r_first"], f.tvalues["r_first"]
sp = stats.spearmanr(d["r_first"], d["r_last"]); pe = stats.pearsonr(d["r_first"], d["r_last"])
hits = int((np.sign(d["r_first"]) == np.sign(d["r_last"])).sum()); n = len(d)
bt = stats.binomtest(hits, n, 0.5)
out = {"n": n, "slope": b, "nw_t": t, "pearson": pe.statistic, "pearson_p": pe.pvalue, "spearman": sp.statistic, "spearman_p": sp.pvalue,
       "hit_rate": hits / n, "binom_p": bt.pvalue, "mean_signed_bp": 1e4 * float((np.sign(d.r_first) * d.r_last).mean())}
taus = []
for tau in (1, 5, 20):
    y = (M[47] - M[47 - tau]).loc[d.index]
    ok = y.notna()
    taus.append({"tau_halfhours": tau, "window_utc": f"{(48 - tau) // 2:02d}:{30 * ((48 - tau) % 2):02d}-24:00",
                 "pearson": stats.pearsonr(d.r_first[ok], y[ok]).statistic, "spearman": stats.spearmanr(d.r_first[ok], y[ok]).statistic,
                 "spearman_p": stats.spearmanr(d.r_first[ok], y[ok]).pvalue, "n": int(ok.sum())})
T = pd.DataFrame(taus); print(T.round(4)); T.to_csv("tables/04_ic_by_tau.csv", index=False)
ll = []
for k in range(1, 48):
    y = (M[k] - M[k - 1]).loc[d.index]; ok = y.notna()
    ll.append({"halfhour": k, "start_utc": f"{k // 2:02d}:{30 * (k % 2):02d}", "spearman": stats.spearmanr(d.r_first[ok], y[ok]).statistic,
               "pearson": stats.pearsonr(d.r_first[ok], y[ok]).statistic})
L = pd.DataFrame(ll); L.to_csv("tables/04_leadlag_profile.csv", index=False)
pd.Series(out).to_csv("tables/04_effect.csv"); print(pd.Series(out).round(5))
if b > 0 and t >= 2 and sp.pvalue < 0.05: verdict = "SUPPORTED"
elif b <= 0 or t < 1: verdict = "REFUTED"
else: verdict = "INCONCLUSIVE"
print("C5 verdict:", verdict)
se = 1 / np.sqrt(n)
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(L["halfhour"], L["spearman"], color=[PAL[7] if k == 47 else PAL[0] for k in L["halfhour"]])
ax.axhline(0, color=GRAY, lw=1); ax.axhline(2 * se, color=GRAY, ls=":", lw=1, label="+/-2/sqrt(n)"); ax.axhline(-2 * se, color=GRAY, ls=":", lw=1)
ax.set_xlabel("later half-hour of the same UTC day (47 = 23:30-23:59, the claim)"); ax.set_ylabel("Spearman IC with r_first"); ax.legend(frameon=False)
ax.set_title(f"C5 {verdict}: r_first -> r_last slope {b:+.3f} (NW t {t:+.2f}), Spearman {sp.statistic:+.3f}, hit {hits/n:.1%}, n={n}")
save(fig, "04_effect")
