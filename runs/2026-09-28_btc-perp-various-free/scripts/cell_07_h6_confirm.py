# cell_07 - H6 CONFIRM opening. Rule: cells/cell_07_rule.md (written first).
from kit import *
from scipy import stats
HI = TRAIN_HI - pd.Timedelta("2h")
CRIT, REF = -0.0168, -0.015
F, b30, c30 = hourly("cell_07", CONFIRM_LO, HI, warm_days=1)
F = F.loc[CONFIRM_LO:HI].replace([np.inf, -np.inf], np.nan)
hs = load(HSPREAD, "cell_07", use=["half_bp"], lo=CONFIRM_LO, hi=TRAIN_HI)["half_bp"]
F["d_basis"] = F["basis"].diff(); F["rn"] = F["r"].shift(-1); F["r_l1"] = F["r"].shift(1)
D = F[["d_basis", "rn", "r", "r_l1"]].dropna(); D = D[D.index <= HI - pd.Timedelta("1h")]
ex, ey = resid_ranks(D, "d_basis", "rn", ["r"]); rho = float(np.corrcoef(ex, ey)[0, 1])
se = float(block_boot_corr(ex.values, ey.values, 240, 2000, 41, len(D)).std())
branch = "SUPPORTED" if rho < CRIT else ("REFUTED" if rho > REF else "INCONCLUSIVE")
res = dict(n=len(D), partial_rho=rho, boot_se=se, branch=branch, crit=CRIT)
res["raw_spearman"] = float(stats.spearmanr(D["d_basis"], D["rn"])[0])
a, b = resid_ranks(D, "d_basis", "rn", ["r", "r_l1"]); res["partial_ctrl_r_and_rl1"] = float(np.corrcoef(a, b)[0, 1])
keep = D["d_basis"].abs() <= D["d_basis"].abs().quantile(0.99); Dk = D[keep]
a, b = resid_ranks(Dk, "d_basis", "rn", ["r"]); res["partial_trim99"] = float(np.corrcoef(a, b)[0, 1])
qs = []
for q, g in D.groupby(D.index.to_period("Q")):
    a, b = resid_ranks(g, "d_basis", "rn", ["r"]); qs.append((str(q), len(g), float(np.corrcoef(a, b)[0, 1])))
qt = pd.DataFrame(qs, columns=["quarter", "n", "partial_rho"]); qt.to_csv("tables/07_by_quarter.csv", index=False)
gross = -np.sign(D["d_basis"]) * D["rn"] * 1e4
res["mean_gross_bp_per_hour"] = float(gross.mean())
cost = 2 * hs.reindex(D.index + pd.Timedelta("1h")).values; cov = ~np.isnan(cost)
res["cost_events_covered"] = int(cov.sum())
res["median_roundtrip_bp"] = float(np.median(cost[cov])) if cov.any() else None
res["mean_gross_bp_covered"] = float(gross.values[cov].mean()) if cov.any() else None
res["mean_net_bp_covered"] = float((gross.values[cov] - cost[cov]).mean()) if cov.any() else None
json.dump(res, open("tables/07_result.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float)); print(qt.round(4))
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
bt = block_boot_corr(ex.values, ey.values, 240, 2000, 41, len(D))
ax[0].hist(bt - bt.mean() + rho, bins=40, color=PAL[0], alpha=.8); ax[0].axvline(rho, color="k"); ax[0].axvline(CRIT, color=PAL[7], ls=":", label=f"crit {CRIT}")
ax[0].legend(fontsize=8); ax[0].set_title(f"CONFIRM partial rho={rho:.4f} (SE {se:.4f}) -> {branch}")
ax[1].bar(range(len(qt)), qt["partial_rho"], color=PAL[3]); ax[1].set_xticks(range(len(qt))); ax[1].set_xticklabels(qt["quarter"], fontsize=8)
ax[1].axhline(0, color=GRAY); ax[1].axhline(CRIT, color=PAL[7], ls=":"); ax[1].set_title("partial rho by quarter (decay-first)")
save(fig, "07_h6_confirm")
