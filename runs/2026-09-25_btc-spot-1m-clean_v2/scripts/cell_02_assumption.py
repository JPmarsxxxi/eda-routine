# Cell 02 - C2 assumption: is 00:00 UTC a focal close? TRAIN only.
from common import *
from scipy import stats
setup()
hh = pd.read_parquet("tables/halfhour_TRAIN.parquet")
legs = pd.read_parquet("tables/01_daily_legs_TRAIN.parquet").dropna(subset=["r_first", "r_last"])
v = hh["vol"]
V = pd.DataFrame({"v": v.values, "d": v.index.floor("D"), "k": v.index.hour * 2 + v.index.minute // 30}).pivot(index="d", columns="k", values="v")
V = V.loc[V.index.isin(legs.index)]
S = V.div(V.sum(axis=1), axis=0)
mean_share = S.mean()
med = mean_share.median()
ratio = mean_share / med
day_med = S.median(axis=1)
res = {}
for k, name in [(47, "last 23:30-23:59"), (0, "first 00:00-00:29")]:
    a, b = S[k].dropna(), day_med.loc[S[k].dropna().index]
    res[name] = {"ratio_mean_share_to_median_halfhour": ratio[k], "rank_of_48": int(mean_share.rank(ascending=False)[k]),
                 "wilcoxon_p(two-sided)": stats.wilcoxon(a, b).pvalue, "median_diff_share_pp": 100 * float((a - b).median()),
                 "mannwhitney_p": stats.mannwhitneyu(a, b).pvalue, "welch_p": stats.ttest_ind(a, b, equal_var=False).pvalue,
                 "ks_p": stats.ks_2samp(a, b).pvalue}
R = pd.DataFrame(res).T
print(R.round(4)); R.to_csv("tables/02_boundary_volume_share.csv")
pd.DataFrame({"mean_share": mean_share, "ratio_to_median": ratio}).to_csv("tables/02_mean_share_by_halfhour.csv")
rl, rf = ratio[47], ratio[0]
pl, pf = R.iloc[0]["wilcoxon_p(two-sided)"], R.iloc[1]["wilcoxon_p(two-sided)"]
dl, df_ = R.iloc[0]["median_diff_share_pp"], R.iloc[1]["median_diff_share_pp"]
if (rl >= 1.2 and pl < 0.05 and dl > 0) or (rf >= 1.2 and pf < 0.05 and df_ > 0): verdict = "SUPPORTED"
elif rl <= 1.0 and rf <= 1.0: verdict = "REFUTED"
else: verdict = "INCONCLUSIVE"
print("C2 verdict:", verdict, rl, rf)
fig, ax = plt.subplots(figsize=(10, 4))
cols = [PAL[7] if k in (0, 47) else PAL[0] for k in ratio.index]
ax.bar(ratio.index, ratio.values, color=cols)
ax.axhline(1.0, color=GRAY, lw=1, ls="--", label="median half-hour = 1.0")
ax.axhline(1.2, color=GRAY, lw=1, ls=":", label="support threshold 1.2")
ax.set_xlabel("UTC half-hour index (0 = 00:00-00:29, 47 = 23:30-23:59)"); ax.set_ylabel("mean volume share / median half-hour")
ax.legend(frameon=False)
ax.set_title(f"C2 {verdict}: boundary half-hours trade {rl:.2f}x (last) and {rf:.2f}x (first) the median half-hour")
save(fig, "02_boundary_volume")
