# cell_10 - H2 VAL check, opened once. Rule: cells/cell_10_rule.md (written first).
from kit import *
HI = VAL_HI - pd.Timedelta("25h")
CRIT, REF = 0.1213, 0.05
F, b30, c30 = hourly("cell_10", VAL_LO, HI, warm_days=31)
F = F.loc[VAL_LO:HI].replace([np.inf, -np.inf], np.nan)
ctrl = ["rv24b", "rv7d", "rv30d"]
def partial(df, c):
    ex, ey = resid_ranks(df, "dvol", "rv24f", c); return float(np.corrcoef(ex, ey)[0, 1]), ex, ey
rho, ex, ey = partial(F, ctrl)
boot = block_boot_corr(ex.values, ey.values, 240, 2000, 71); se = float(boot.std())
branch = "PASS" if rho > CRIT else ("FAIL" if rho < REF else "INCONCLUSIVE")
res = dict(n=len(ex), partial_rho=rho, boot_se=se, branch=branch, crit=CRIT, ref=REF,
           raw_spearman=float(F[["dvol", "rv24f"]].dropna().corr(method="spearman").iloc[0, 1]))
F["r24b"] = np.log(F["close"] / F["close"].shift(24)); res["plus_signed24h"] = partial(F, ctrl + ["r24b"])[0]
F["ewma_lrv"] = 0.5 * np.log(((F["r"] ** 2).ewm(halflife=72, min_periods=72).mean()).replace(0, np.nan)); res["plus_ewma"] = partial(F, ctrl + ["ewma_lrv"])[0]
F["seg"] = np.where(F.index < pd.Timestamp("2023-07-01"), "2023Q2 hours", "2023H2 hours")
res["by_segment"] = {k: dict(n=len(g), partial_rho=partial(g, ctrl)[0]) for k, g in F.groupby("seg")}
json.dump(res, open("tables/10_result.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float))
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(boot - boot.mean() + rho, bins=40, color=PAL[0], alpha=.8); ax[0].axvline(rho, color="k"); ax[0].axvline(CRIT, color=PAL[7], ls=":", label=f"crit {CRIT}")
ax[0].axvline(REF, color=GRAY, ls=":", label=f"fail {REF}"); ax[0].legend(fontsize=8); ax[0].set_title(f"VAL partial rho={rho:.3f} (SE {se:.3f}) -> {branch}")
sg = res["by_segment"]; ax[1].bar(range(len(sg)), [v["partial_rho"] for v in sg.values()], color=PAL[3]); ax[1].set_xticks(range(len(sg))); ax[1].set_xticklabels(list(sg), fontsize=8)
ax[1].axhline(0, color=GRAY); ax[1].axhline(CRIT, color=PAL[7], ls=":"); ax[1].set_title("VAL partial rho by segment")
save(fig, "10_h2_val")
