# cell_09 - H4 redirect (EXPLORE only). Rule: cells/cell_09_rule.md (written first).
from kit import *
from scipy import stats
E_LO = pd.Timestamp("2020-09-01"); HI = EXPLORE_HI - pd.Timedelta("170h")
F, b30, c30 = hourly("cell_09", E_LO, HI, warm_days=31)
F = F.loc[E_LO:HI].replace([np.inf, -np.inf], np.nan)
cl = F["close"]
F["r72f"] = np.log(cl.shift(-73) / cl.shift(-1)); F["r168f"] = np.log(cl.shift(-169) / cl.shift(-1))
F["rel"] = F["dvol"] - F["dvol"].rolling(720, min_periods=500).median()
def sp(x, y, seed):
    D = F[[x, y]].dropna(); rho = float(stats.spearmanr(D[x], D[y])[0])
    a, b = D[x].rank(), D[y].rank(); a = ((a - a.mean()) / a.std()).values; b = ((b - b.mean()) / b.std()).values
    se = float(block_boot_corr(a, b, 240, 1000, seed).std()); return dict(n=len(D), rho=rho, se=se, z=rho / se)
res = {"T_relative_24h": sp("rel", "r24f", 61), "Hz_72h": sp("dvol", "r72f", 62), "Hz_168h": sp("dvol", "r168f", 63), "raw_24h_pooled": sp("dvol", "r24f", 64)}
D = F[["dvol", "r24f"]].dropna()
qs = [(str(q), len(g), float(stats.spearmanr(g["dvol"], g["r24f"])[0])) for q, g in D.groupby(D.index.to_period("Q")) if len(g) >= 300]
qt = pd.DataFrame(qs, columns=["quarter", "n", "spearman"]); qt.to_csv("tables/09_by_quarter.csv", index=False)
full = qt[qt["quarter"] >= "2021Q2"]; best = full.loc[full["spearman"].abs().idxmax(), "quarter"]
Dk = D[D.index.to_period("Q").astype(str) != best]
res["best_quarter"] = best; res["best_quarter_rho"] = float(full.set_index("quarter").loc[best, "spearman"])
res["others_pooled_rho"] = float(stats.spearmanr(Dk["dvol"], Dk["r24f"])[0])
B1 = res["best_quarter_rho"] >= 0.15 and res["others_pooled_rho"] < 0.0669
B2 = [k for k in ("T_relative_24h", "Hz_72h", "Hz_168h") if res[k]["rho"] >= 0.08 and res[k]["z"] >= 2]
B3 = [k for k in ("T_relative_24h", "Hz_72h", "Hz_168h") if res[k]["rho"] <= -0.08 and res[k]["z"] <= -2]
res["branches"] = dict(B1_one_era=B1, B2_transform_or_horizon=B2, B3_opposite=B3, B4_absent=(not B1 and not B2 and not B3))
json.dump(res, open("tables/09_result.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float)); print(qt.round(4))
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].bar(range(len(qt)), qt["spearman"], color=PAL[3]); ax[0].set_xticks(range(len(qt))); ax[0].set_xticklabels(qt["quarter"], fontsize=8); ax[0].axhline(0, color=GRAY); ax[0].set_title("EXPLORE raw DVOL vs next-24h return by quarter")
ks = ["raw_24h_pooled", "T_relative_24h", "Hz_72h", "Hz_168h"]
ax[1].bar(range(4), [res[k]["rho"] for k in ks], yerr=[2 * res[k]["se"] for k in ks], color=PAL[0], capsize=4); ax[1].set_xticks(range(4)); ax[1].set_xticklabels(["raw 24h", "relative 24h", "raw 72h", "raw 168h"], fontsize=8)
ax[1].axhline(0.08, color=PAL[7], ls=":"); ax[1].axhline(-0.08, color=PAL[7], ls=":"); ax[1].axhline(0, color=GRAY); ax[1].set_title("Spearman (bars +-2 SE)")
save(fig, "09_h4_redirect")
