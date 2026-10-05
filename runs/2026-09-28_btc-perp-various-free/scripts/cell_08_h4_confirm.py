# cell_08 - H4 CONFIRM opening. Rule: cells/cell_08_rule.md (written first).
from kit import *
from scipy import stats
HI = TRAIN_HI - pd.Timedelta("25h")
CRIT, REF = 0.0669, 0.025
F, b30, c30 = hourly("cell_08", CONFIRM_LO, HI, warm_days=2)
F = F.loc[CONFIRM_LO:HI].replace([np.inf, -np.inf], np.nan)
F["r24b"] = np.log(F["close"] / F["close"].shift(24))
D = F[["dvol", "r24f", "r24b"]].dropna()
rho = float(stats.spearmanr(D["dvol"], D["r24f"])[0])
ra, rb = D["dvol"].rank(), D["r24f"].rank(); ra = ((ra - ra.mean()) / ra.std()).values; rb = ((rb - rb.mean()) / rb.std()).values
boot = block_boot_corr(ra, rb, 240, 2000, 51); se = float(boot.std())
branch = "SUPPORTED" if rho > CRIT else ("REFUTED" if rho < REF else "INCONCLUSIVE")
res = dict(n=len(D), spearman=rho, boot_se=se, branch=branch, crit=CRIT, ref=REF)
a, b = resid_ranks(D, "dvol", "r24f", ["r24b"]); res["partial_on_r24b"] = float(np.corrcoef(a, b)[0, 1])
qs = [(str(q), len(g), float(stats.spearmanr(g["dvol"], g["r24f"])[0])) for q, g in D.groupby(D.index.to_period("Q"))]
qt = pd.DataFrame(qs, columns=["quarter", "n", "spearman"]); qt.to_csv("tables/08_by_quarter.csv", index=False)
best = qt.loc[qt["spearman"].abs().idxmax(), "quarter"]
Dk = D[D.index.to_period("Q").astype(str) != best]; res["best_quarter_removed"] = best; res["spearman_ex_best"] = float(stats.spearmanr(Dk["dvol"], Dk["r24f"])[0])
terc = pd.qcut(D["dvol"], 3, labels=["low", "mid", "high"])
tm = D.groupby(terc, observed=True)["r24f"].agg(["count", "mean"]); tm["mean_bp"] = tm["mean"] * 1e4; tm.to_csv("tables/08_tercile_means.csv")
res["tercile_mean_bp"] = tm["mean_bp"].to_dict()
json.dump(res, open("tables/08_result.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float)); print(qt.round(4))
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].hist(boot - boot.mean() + rho, bins=40, color=PAL[0], alpha=.8); ax[0].axvline(rho, color="k"); ax[0].axvline(CRIT, color=PAL[7], ls=":", label=f"crit {CRIT}")
ax[0].axvline(REF, color=PAL[3], ls=":", label=f"refute {REF}"); ax[0].legend(fontsize=8); ax[0].set_title(f"CONFIRM Spearman={rho:.4f} (SE {se:.4f}) -> {branch}")
ax[1].bar(range(len(qt)), qt["spearman"], color=PAL[3]); ax[1].set_xticks(range(len(qt))); ax[1].set_xticklabels(qt["quarter"], fontsize=8)
ax[1].axhline(0, color=GRAY); ax[1].axhline(CRIT, color=PAL[7], ls=":"); ax[1].set_title("Spearman by quarter (decay-first)")
save(fig, "08_h4_confirm")
