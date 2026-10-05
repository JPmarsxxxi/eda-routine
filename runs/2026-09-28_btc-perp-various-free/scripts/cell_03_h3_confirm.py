# cell_03 - H3 CONFIRM opening. Rule: cells/cell_03_rule.md (written first).
from kit import *
from scipy import stats

HI = TRAIN_HI - pd.Timedelta("25h")            # forward window must end inside CONFIRM (SPLITS.md boundary rule)
F, b30, c30 = hourly("cell_03", CONFIRM_LO, HI, warm_days=31)
F = F.loc[CONFIRM_LO:HI].replace([np.inf, -np.inf], np.nan)
ctrl = ["rv24b", "rv7d", "rv30d"]

def partial(df, x, y, c):
    ex, ey = resid_ranks(df, x, y, c); return float(np.corrcoef(ex, ey)[0, 1]), ex, ey
rho, ex, ey = partial(F, "basis", "rv24f", ctrl)
n = len(ex); boot = block_boot_corr(ex.values, ey.values, 240, 2000, 11)
se = float(boot.std()); raw = float(F[["basis", "rv24f"]].dropna().corr(method="spearman").iloc[0, 1])
branch = "SUPPORTED" if rho > 0.0689 else ("REFUTED" if rho < 0.05 else "INCONCLUSIVE")
res = dict(n=n, partial_rho=rho, boot_se=se, raw_spearman=raw, branch=branch, crit=0.0689)
# reported rivals (unweighted)
F2 = F.copy(); F2["ldvol"] = np.log(F2["dvol"])
res["partial_rho_plus_dvol"] = partial(F2, "basis", "rv24f", ctrl + ["ldvol"])[0]
res["n_plus_dvol"] = int(F2[["basis", "rv24f", "ldvol"] + ctrl].dropna().shape[0])
mv = load(METRICS, "cell_03", use=["v"], lo=CONFIRM_LO - pd.Timedelta(days=2), hi=HI)["v"]
hv = mv.resample("1h").sum(min_count=12)                                       # hourly open-stamped base volume
lv24 = np.log(hv.rolling(24, min_periods=22).mean().shift(0)).reindex(F.index + pd.Timedelta("0h"))
F2["lvol24b"] = np.log(hv.rolling(24, min_periods=22).mean()).reindex(F2.index + pd.Timedelta("0h")).values
res["partial_rho_plus_volume"] = partial(F2, "basis", "rv24f", ctrl + ["lvol24b"])[0]
qs = []
for qn, g in F.groupby(F.index.to_period("Q")):
    r_, _, _ = partial(g, "basis", "rv24f", ctrl); qs.append((str(qn), len(g), r_))
qt = pd.DataFrame(qs, columns=["quarter", "n", "partial_rho"]); qt.to_csv("tables/03_by_quarter.csv", index=False)
json.dump(res, open("tables/03_result.json", "w"), indent=1); print(json.dumps(res, indent=1)); print(qt.round(3))
fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
ax[0].hist(boot - boot.mean() + rho, bins=40, color=PAL[0], alpha=.8); ax[0].axvline(rho, color="k"); ax[0].axvline(0.0689, color=PAL[7], ls=":", label="crit 0.0689")
ax[0].axvline(0.05, color=GRAY, ls=":", label="0.05"); ax[0].legend(fontsize=8); ax[0].set_title(f"CONFIRM partial rho={rho:.3f} (block-boot SE {se:.3f}) -> {branch}")
ax[1].bar(range(len(qt)), qt["partial_rho"], color=PAL[3]); ax[1].set_xticks(range(len(qt))); ax[1].set_xticklabels(qt["quarter"], fontsize=8); ax[1].axhline(0, color=GRAY); ax[1].axhline(0.0689, color=PAL[7], ls=":")
ax[1].set_title("partial rho by quarter (decay-first)")
ax[2].bar(["raw", "partial", "+dvol", "+volume"], [raw, rho, res["partial_rho_plus_dvol"], res["partial_rho_plus_volume"]], color=[GRAY, PAL[0], PAL[3], PAL[3]])
ax[2].axhline(0, color=GRAY); ax[2].axhline(0.0689, color=PAL[7], ls=":"); ax[2].set_title("controls ladder (rivals; unweighted)")
save(fig, "03_h3_confirm")
