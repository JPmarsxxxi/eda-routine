# cell_01 - H1 CONFIRM opening. Rule: cells/cell_01_rule.md (written first).
from kit import *
import statsmodels.api as sm
from scipy import stats

F, b30, c30 = hourly("cell_01", CONFIRM_LO, TRAIN_HI, warm_days=1)
fu = load(FUNDING, "cell_01", use=["funding"], lo=CONFIRM_LO, hi=TRAIN_HI)["funding"]; fu.index = fu.index.round("h")
hs = load(HSPREAD, "cell_01", use=["half_bp"], lo=CONFIRM_LO, hi=TRAIN_HI)["half_bp"]
S = pd.date_range(CONFIRM_LO, TRAIN_HI, freq="8h")
S = S[(S - pd.Timedelta("30min") >= CONFIRM_LO) & (S + pd.Timedelta("4h30min") <= TRAIN_HI)]
jump = b30.reindex(S + pd.Timedelta("30min")).values - b30.reindex(S - pd.Timedelta("30min")).values
plac = b30.reindex(S + pd.Timedelta("4h30min")).values - b30.reindex(S + pd.Timedelta("3h30min")).values
T = pd.DataFrame({"jump": jump, "plac": plac, "funding": fu.reindex(S).values, "half_bp": hs.reindex(S).values}, index=S)
T["D"] = T["jump"] - T["plac"]
T = T.dropna(subset=["D"])
m = sm.OLS(T["D"].values, np.ones(len(T))).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
meanD, t = float(m.params[0]), float(m.tvalues[0])
branch = "SUPPORTED" if t >= 2.326 else ("REFUTED" if meanD < 0.25 else "INCONCLUSIVE")
res = dict(n=len(T), mean_D=meanD, nw_t=t, mean_jump=float(T.jump.mean()), mean_placebo=float(T.plac.mean()), branch=branch)
# side bets (unweighted)
res["spearman_jump_funding"] = float(stats.spearmanr(T["jump"], T["funding"], nan_policy="omit")[0])
bins = pd.cut(T["funding"], [-1, 0.0000999, 0.0001001, 0.0003, 1], labels=["<0.01%", "=0.01%", "0.01-0.03%", ">0.03%"])
byf = T.groupby(bins, observed=True).agg(n=("D", "size"), D=("D", "mean"), jump=("jump", "mean"),
                                          se=("D", lambda s: s.std() / np.sqrt(len(s))))
byh = T.groupby(T.index.hour).agg(n=("D", "size"), D=("D", "mean"), se=("D", lambda s: s.std() / np.sqrt(len(s))))
byq = T.groupby(T.index.to_period("Q")).agg(n=("D", "size"), D=("D", "mean"), se=("D", lambda s: s.std() / np.sqrt(len(s))))
cov = T["half_bp"].notna()
res["cost_events_covered"] = int(cov.sum())
res["median_roundtrip_2leg_bp"] = float((4 * T.loc[cov, "half_bp"]).median()) if cov.any() else None
res["funding_share_eq_default"] = float(np.isclose(T["funding"], 1e-4).mean())
for nm, tb in (("by_funding", byf), ("by_hour", byh), ("by_quarter", byq)):
    tb.to_csv(f"tables/01_{nm}.csv"); print(nm); print(tb.round(3).to_string())
T.to_csv("tables/01_per_settlement.csv")
json.dump(res, open("tables/01_result.json", "w"), indent=1); print(json.dumps(res, indent=1))
fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
ax[0].bar(["settlement jump", "mid-cycle placebo", "D"], [T.jump.mean(), T.plac.mean(), meanD],
          yerr=[2 * T.jump.std() / np.sqrt(len(T)), 2 * T.plac.std() / np.sqrt(len(T)), 2 * meanD / t if t else 0],
          color=[PAL[3], GRAY, PAL[0]]); ax[0].axhline(0, color=GRAY); ax[0].axhline(0.5, color=PAL[7], ls=":", label="min effect 0.5bp")
ax[0].legend(fontsize=8); ax[0].set_ylabel("bp"); ax[0].set_title(f"CONFIRM: D={meanD:.2f}bp, NW t={t:.2f} -> {branch}")
ax[1].bar(range(len(byf)), byf["jump"], color=PAL[3]); ax[1].set_xticks(range(len(byf))); ax[1].set_xticklabels([f"{i}\nn={n}" for i, n in zip(byf.index, byf.n)], fontsize=8)
ax[1].axhline(0, color=GRAY); ax[1].set_title("settlement jump by funding settled")
ax[2].errorbar(range(len(byq)), byq["D"], yerr=2 * byq["se"], fmt="o", color=PAL[0]); ax[2].set_xticks(range(len(byq))); ax[2].set_xticklabels([str(i) for i in byq.index], fontsize=8)
ax[2].axhline(0, color=GRAY); ax[2].set_title("D by quarter (decay-first)")
save(fig, "01_h1_confirm")
