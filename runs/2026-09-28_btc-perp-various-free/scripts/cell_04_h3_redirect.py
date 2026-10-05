# cell_04 - redirect after H3 refutation. Rule: cells/cell_04_rule.md (written first). EXPLORE only.
from kit import *
E_LO = pd.Timestamp("2020-09-01")
HI = EXPLORE_HI - pd.Timedelta("25h")
F, b30, c30 = hourly("cell_04", E_LO, HI, warm_days=31)
F = F.loc[E_LO:HI].replace([np.inf, -np.inf], np.nan)
ctrl = ["rv24b", "rv7d", "rv30d"]
F["chg24"] = F["basis"] - F["basis"].shift(24)
F["ext"] = (F["basis"] - F["basis"].rolling(720, min_periods=500).median()).abs()
def partial(df, x):
    ex, ey = resid_ranks(df, x, "rv24f", ctrl); return float(np.corrcoef(ex, ey)[0, 1]), ex, ey
res = {}
rows = []
for qn, g in F.loc["2020-10-01":].groupby(F.loc["2020-10-01":].index.to_period("Q")):
    r_, _, _ = partial(g, "basis"); rows.append((str(qn), len(g), r_))
qt = pd.DataFrame(rows, columns=["quarter", "n", "partial_rho_level"]); qt.to_csv("tables/04_level_by_quarter.csv", index=False)
best = qt.loc[qt["partial_rho_level"].idxmax()]
others = F.loc["2020-10-01":]; others = others[others.index.to_period("Q").astype(str) != best["quarter"]]
res["best_quarter"] = best["quarter"]; res["best_quarter_rho"] = float(best["partial_rho_level"]); res["pooled_others_level_rho"] = partial(others, "basis")[0]
res["pooled_all_level_rho"] = partial(F, "basis")[0]
for nm in ("chg24", "ext"):
    r_, ex, ey = partial(F, nm); bs = block_boot_corr(ex.values, ey.values, 240, 1000, 5)
    res[f"{nm}_rho"] = r_; res[f"{nm}_se"] = float(bs.std()); res[f"{nm}_n"] = int(len(ex))
b1 = res["best_quarter_rho"] >= 0.25 and res["pooled_others_level_rho"] < 0.0689
def okc(nm): return res[f"{nm}_rho"] >= 0.10 and res[f"{nm}_rho"] >= 2 * res[f"{nm}_se"]
b2 = okc("chg24") or okc("ext")
res["B1"], res["B2"] = bool(b1), bool(b2)
res["B2_pick"] = (max(("chg24", "ext"), key=lambda k: res[f"{k}_rho"]) if b2 else None)
res["branch"] = "+".join([n for n, f in (("B1", b1), ("B2", b2)) if f]) or "B3"
json.dump(res, open("tables/04_result.json", "w"), indent=1); print(json.dumps(res, indent=1)); print(qt.round(3))
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].bar(range(len(qt)), qt["partial_rho_level"], color=PAL[3]); ax[0].set_xticks(range(len(qt))); ax[0].set_xticklabels(qt["quarter"], fontsize=8)
ax[0].axhline(0, color=GRAY); ax[0].axhline(0.25, color=PAL[7], ls=":"); ax[0].set_title("EXPLORE basis-level partial rho by quarter")
ax[1].bar(["level", "24h change", "extremity"], [res["pooled_all_level_rho"], res["chg24_rho"], res["ext_rho"]], yerr=[0, 2 * res["chg24_se"], 2 * res["ext_se"]], color=[GRAY, PAL[0], PAL[0]])
ax[1].axhline(0.10, color=PAL[7], ls=":"); ax[1].axhline(0, color=GRAY); ax[1].set_title(f"EXPLORE transforms -> {res['branch']}")
save(fig, "04_h3_redirect")
