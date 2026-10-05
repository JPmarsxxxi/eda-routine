# cell_02 - redirect after H1 refutation. Rule: cells/cell_02_rule.md (written first). EXPLORE only.
from kit import *
import statsmodels.api as sm

LO = pd.Timestamp("2020-09-01")
F, b30, c30 = hourly("cell_02", LO, EXPLORE_HI, warm_days=1)
fu = load(FUNDING, "cell_02", use=["funding"], lo=LO, hi=EXPLORE_HI)["funding"]; fu.index = fu.index.round("h")
S = pd.date_range(LO.ceil("8h"), EXPLORE_HI, freq="8h")
S = S[(S - pd.Timedelta("30min") >= LO) & (S + pd.Timedelta("4h30min") <= EXPLORE_HI)]
jump = b30.reindex(S + pd.Timedelta("30min")).values - b30.reindex(S - pd.Timedelta("30min")).values
plac = b30.reindex(S + pd.Timedelta("4h30min")).values - b30.reindex(S + pd.Timedelta("3h30min")).values
T = pd.DataFrame({"jump": jump, "plac": plac, "funding": fu.reindex(S).values}, index=S)
T["D"] = T["jump"] - T["plac"]
T = T.dropna(subset=["D", "funding"]).copy()
T["HI"] = (T["funding"] > 1.0001e-4).astype(int)
T["NEG"] = (T["funding"] < 0.9999e-4).astype(int)
def nw_mean(x):
    m = sm.OLS(np.asarray(x), np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": 3}); return float(m.params[0]), float(m.tvalues[0])
X = sm.add_constant(T[["HI"]].astype(float))
fit = sm.OLS(T["D"].values, X.values).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
res = dict(n=len(T), meanD_all=float(T.D.mean()), n_HI=int(T.HI.sum()), n_LE=int((1 - T.HI).sum()),
           meanD_HI=float(T.loc[T.HI == 1, "D"].mean()), meanD_LE=float(T.loc[T.HI == 0, "D"].mean()),
           diff_HI_minus_LE=float(fit.params[1]), t_HI=float(fit.tvalues[1]))
mn, tn = nw_mean(T.loc[T.NEG == 1, "D"]); res.update(n_NEG=int(T.NEG.sum()), meanD_NEG=mn, t_NEG=tn)
q = T.groupby(T.index.to_period("Q"))["D"].agg(["size", "sum", "mean"]); q["share_of_sum"] = q["sum"] / T["D"].sum()
res["max_quarter_share"] = float(q["share_of_sum"].max()); res["max_quarter"] = str(q["share_of_sum"].idxmax())
fbins = pd.cut(T["funding"], [-1, 0.0000999, 0.0001001, 0.0003, 1], labels=["<0.01%", "=0.01%", "0.01-0.03%", ">0.03%"])
byf = T.groupby(fbins, observed=True).agg(n=("D", "size"), D=("D", "mean"), se=("D", lambda s: s.std() / np.sqrt(len(s))))
b1 = res["diff_HI_minus_LE"] >= 1.0 and res["t_HI"] > 3 and res["meanD_LE"] < 0.5
b2 = res["meanD_NEG"] <= -0.5 and res["t_NEG"] < -2
b3 = res["max_quarter_share"] > 0.60
res["B1"], res["B2"], res["B3"] = bool(b1), bool(b2), bool(b3)
res["branch"] = "B1" if b1 else "B2" if b2 else "B3" if b3 else "B4"
q.to_csv("tables/02_by_quarter.csv"); byf.to_csv("tables/02_by_funding.csv"); T.to_csv("tables/02_per_settlement.csv")
json.dump(res, open("tables/02_result.json", "w"), indent=1); print(json.dumps(res, indent=1)); print(q.round(3)); print(byf.round(3))
fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
ax[0].bar(range(len(byf)), byf["D"], yerr=2 * byf["se"], color=PAL[0]); ax[0].set_xticks(range(len(byf))); ax[0].set_xticklabels([f"{i}\nn={n}" for i, n in zip(byf.index, byf.n)], fontsize=8)
ax[0].axhline(0, color=GRAY); ax[0].axhline(0.5, color=PAL[7], ls=":"); ax[0].set_ylabel("bp"); ax[0].set_title("EXPLORE D by funding settled")
ax[1].bar(range(len(q)), q["mean"], color=PAL[3]); ax[1].set_xticks(range(len(q))); ax[1].set_xticklabels([str(i) for i in q.index], fontsize=7, rotation=45)
ax[1].axhline(0, color=GRAY); ax[1].set_title("EXPLORE mean D by quarter")
ax[2].scatter(T["funding"] * 1e4, T["D"], s=4, alpha=.4, color=PAL[0]); ax[2].axhline(0, color=GRAY); ax[2].set_xlabel("funding settled (bp)"); ax[2].set_ylabel("D (bp)")
ax[2].set_title(f"branch fired: {res['branch']}")
save(fig, "02_h1_redirect")
