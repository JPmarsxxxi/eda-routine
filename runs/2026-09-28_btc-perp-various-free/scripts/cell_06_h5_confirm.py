# cell_06 - H5 CONFIRM opening. Rule: cells/cell_06_rule.md (written first).
from kit import *
from scipy import stats
HI = TRAIN_HI - pd.Timedelta("2h")
F, b30, c30 = hourly("cell_06", CONFIRM_LO, HI, warm_days=1)
F = F.loc[CONFIRM_LO:HI]
hs = load(HSPREAD, "cell_06", use=["half_bp"], lo=CONFIRM_LO, hi=TRAIN_HI)["half_bp"]
D = pd.DataFrame({"r": F["r"], "rn": F["r"].shift(-1)}); D = D.replace([np.inf, -np.inf], np.nan).dropna()
D = D[D.index <= HI - pd.Timedelta("1h")]
rho = float(stats.spearmanr(D["r"], D["rn"])[0])
ra, rb = D["r"].rank(), D["rn"].rank()
ra = ((ra - ra.mean()) / ra.std()).values; rb = ((rb - rb.mean()) / rb.std()).values
boot = block_boot_corr(ra, rb, 240, 2000, 31); se = float(boot.std())
branch = "SUPPORTED" if rho < -0.01526 else ("REFUTED" if rho > -0.015 else "INCONCLUSIVE")
res = dict(n=len(D), spearman=rho, boot_se=se, pearson=float(D.corr().iloc[0, 1]), branch=branch, crit=-0.01526)
keep = D["r"].abs() <= D["r"].abs().quantile(0.99)
res["spearman_trim99"] = float(stats.spearmanr(D.loc[keep, "r"], D.loc[keep, "rn"])[0]); res["n_trim99"] = int(keep.sum())
qs = [(str(q), len(g), float(stats.spearmanr(g["r"], g["rn"])[0])) for q, g in D.groupby(D.index.to_period("Q"))]
qt = pd.DataFrame(qs, columns=["quarter", "n", "spearman"]); qt.to_csv("tables/06_by_quarter.csv", index=False)
terc = pd.qcut(D["r"].abs(), 3, labels=["low|r|", "mid|r|", "high|r|"])
tt = pd.DataFrame({k: {"n": int((terc == k).sum()), "spearman": float(stats.spearmanr(D.loc[terc == k, "r"], D.loc[terc == k, "rn"])[0])} for k in ["low|r|", "mid|r|", "high|r|"]}).T
tt.to_csv("tables/06_by_abs_tercile.csv"); res["tercile"] = tt.to_dict()
gross = -np.sign(D["r"]) * D["rn"] * 1e4
res["mean_gross_bp_per_hour"] = float(gross.mean())
cost = 2 * hs.reindex(D.index + pd.Timedelta("1h")).values          # round trip = 2 x half spread at the trade hour
cov = ~np.isnan(cost)
res["cost_events_covered"] = int(cov.sum()); res["median_roundtrip_bp"] = float(np.median(cost[cov])) if cov.any() else None
res["mean_gross_bp_covered"] = float(gross.values[cov].mean()) if cov.any() else None
res["mean_net_bp_covered"] = float((gross.values[cov] - cost[cov]).mean()) if cov.any() else None
json.dump(res, open("tables/06_result.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float)); print(qt.round(4)); print(tt.round(4))
fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
ax[0].hist(boot - boot.mean() + rho, bins=40, color=PAL[0], alpha=.8); ax[0].axvline(rho, color="k"); ax[0].axvline(-0.01526, color=PAL[7], ls=":", label="crit -0.01526")
ax[0].legend(fontsize=8); ax[0].set_title(f"CONFIRM Spearman={rho:.4f} (SE {se:.4f}) -> {branch}")
ax[1].bar(range(len(qt)), qt["spearman"], color=PAL[3]); ax[1].set_xticks(range(len(qt))); ax[1].set_xticklabels(qt["quarter"], fontsize=8); ax[1].axhline(0, color=GRAY); ax[1].axhline(-0.01526, color=PAL[7], ls=":")
ax[1].set_title("Spearman by quarter (decay-first)")
ax[2].bar(range(3), tt["spearman"], color=PAL[0]); ax[2].set_xticks(range(3)); ax[2].set_xticklabels(tt.index); ax[2].axhline(0, color=GRAY); ax[2].set_title("by |r_t| tercile (mechanism side bet)")
save(fig, "06_h5_confirm")
