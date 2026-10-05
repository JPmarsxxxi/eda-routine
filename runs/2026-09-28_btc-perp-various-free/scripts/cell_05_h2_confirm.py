# cell_05 - H2 CONFIRM opening. Rule: cells/cell_05_rule.md (written first).
from kit import *
HI = TRAIN_HI - pd.Timedelta("25h")
F, b30, c30 = hourly("cell_05", CONFIRM_LO, HI, warm_days=31)
F = F.loc[CONFIRM_LO:HI].replace([np.inf, -np.inf], np.nan)
ctrl = ["rv24b", "rv7d", "rv30d"]
def partial(df, x, c):
    ex, ey = resid_ranks(df, x, "rv24f", c); return float(np.corrcoef(ex, ey)[0, 1]), ex, ey
rho, ex, ey = partial(F, "dvol", ctrl)
boot = block_boot_corr(ex.values, ey.values, 240, 2000, 21); se = float(boot.std())
raw = float(F[["dvol", "rv24f"]].dropna().corr(method="spearman").iloc[0, 1])
branch = "SUPPORTED" if rho > 0.0869 else ("REFUTED" if rho < 0.05 else "INCONCLUSIVE")
res = dict(n=len(ex), partial_rho=rho, boot_se=se, raw_spearman=raw, branch=branch, crit=0.0869)
F["r24b"] = np.log(F["close"] / F["close"].shift(24))
res["partial_rho_plus_signed24h_return"] = partial(F, "dvol", ctrl + ["r24b"])[0]
F["ewma_lrv"] = 0.5 * np.log(((F["r"] ** 2).ewm(halflife=72, min_periods=72).mean()).replace(0, np.nan))
res["partial_rho_plus_ewma"] = partial(F, "dvol", ctrl + ["ewma_lrv"])[0]
qs = [(str(qn), len(g), partial(g, "dvol", ctrl)[0]) for qn, g in F.groupby(F.index.to_period("Q"))]
qt = pd.DataFrame(qs, columns=["quarter", "n", "partial_rho"]); qt.to_csv("tables/05_by_quarter.csv", index=False)
json.dump(res, open("tables/05_result.json", "w"), indent=1); print(json.dumps(res, indent=1)); print(qt.round(3))
fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
ax[0].hist(boot - boot.mean() + rho, bins=40, color=PAL[0], alpha=.8); ax[0].axvline(rho, color="k"); ax[0].axvline(0.0869, color=PAL[7], ls=":", label="crit 0.0869")
ax[0].axvline(0.05, color=GRAY, ls=":", label="0.05"); ax[0].legend(fontsize=8); ax[0].set_title(f"CONFIRM partial rho={rho:.3f} (SE {se:.3f}) -> {branch}")
ax[1].bar(range(len(qt)), qt["partial_rho"], color=PAL[3]); ax[1].set_xticks(range(len(qt))); ax[1].set_xticklabels(qt["quarter"], fontsize=8); ax[1].axhline(0, color=GRAY); ax[1].axhline(0.0869, color=PAL[7], ls=":")
ax[1].set_title("partial rho by quarter (decay-first)")
ax[2].bar(["raw", "partial", "+signed 24h ret", "+EWMA RV"], [raw, rho, res["partial_rho_plus_signed24h_return"], res["partial_rho_plus_ewma"]], color=[GRAY, PAL[0], PAL[3], PAL[3]])
ax[2].axhline(0, color=GRAY); ax[2].axhline(0.0869, color=PAL[7], ls=":"); ax[2].set_title("controls ladder (rivals; unweighted)")
save(fig, "05_h2_confirm")
