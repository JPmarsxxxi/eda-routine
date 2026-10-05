# Phase 0 extras (EXPLORE only, descriptive). 6b: basis by hour-in-funding-cycle x funding sign.
# 4b: do dvol / half_bp / basis carry information about next-24h RV beyond trailing RV (partial Spearman)?
# Rules: 6b notable if the post-settlement hour's mean basis change differs from the other 7 cycle hours by > 2 SE.
#        4b notable if |partial rho| > 2/sqrt(n) after controlling log trailing 24h RV and 30d RV.
from common import *
from scipy import stats

P = pd.read_parquet("tables/p0_panel_EXPLORE.parquet")
fu = pd.read_parquet("tables/p0_funding_EXPLORE.parquet")["funding"]
res = {}
# ---- 6b
q = P.loc["2020-09-01":].copy()
q["cyc"] = q.index.hour % 8                       # 0 = the hour starting at settlement
# funding applying at the settlement that opened this cycle (known at settlement)
fset = fu.reindex(q.index.floor("8h"))
q["fsign"] = np.where(fset.values > 1e-4 + 1e-12, "funding > 0.01%", np.where(fset.values < 1e-4 - 1e-12, "funding < 0.01%", "funding = 0.01% (default)"))
# 5-minute basis path around settlement
mt = load(METRICS, "p0_extra", use=["c"], lo=pd.Timestamp("2020-09-01"), hi=EXPLORE_HI)
m1 = load(PERP_1M, "p0_extra", use=["close"], lo=pd.Timestamp("2020-09-01"), hi=EXPLORE_HI)
b5 = pd.Series(1e4 * np.log(mt["c"].values / m1["close"].reindex(mt.index + pd.Timedelta(minutes=4)).values), index=mt.index)
tb = b5.to_frame("b"); tb["m"] = ((tb.index - tb.index.floor("8h")) / pd.Timedelta("5min")).astype(int)   # 0..95 within cycle
tb["f"] = fu.reindex(tb.index.floor("8h")).values
tb["fs"] = np.where(tb["f"] > 1e-4 + 1e-12, "pos", np.where(tb["f"] < 1e-4 - 1e-12, "low/neg", "default"))
# demean within each 8h cycle so the profile is the within-cycle shape, not the level
tb["cycle"] = tb.index.floor("8h"); tb["bd"] = tb["b"] - tb.groupby("cycle")["b"].transform("mean")
prof = tb.groupby(["fs", "m"])["bd"].mean().unstack(0); prof.to_csv("tables/p0_6b_basis_cycle_profile.csv")
cnt = tb.groupby("fs")["cycle"].nunique().to_dict(); res["cycles_by_funding_state"] = cnt
# jump across settlement: mean basis in first 30 min after settlement minus last 30 min before, per cycle
tb["seg"] = np.where(tb["m"] < 6, "first30", np.where(tb["m"] >= 90, "last30", "mid"))
seg = tb.groupby(["cycle", "seg"])["b"].mean().unstack()
seg["prev_last30"] = seg["last30"].shift(1)
seg["jump"] = seg["first30"] - seg["prev_last30"]            # across the settlement at 'cycle' start
seg["drift"] = seg["last30"] - seg["first30"]                 # within the cycle
seg["f"] = fu.reindex(seg.index).values                       # funding settled AT this cycle start
seg["f_prev"] = fu.shift(1).reindex(seg.index).values
J = seg.dropna(subset=["jump"])
res["jump_mean_bp"] = float(J["jump"].mean()); res["jump_se"] = float(J["jump"].std() / np.sqrt(len(J))); res["jump_n"] = int(len(J))
res["drift_mean_bp"] = float(seg["drift"].mean()); res["drift_se"] = float(seg["drift"].std() / np.sqrt(seg["drift"].notna().sum()))
res["spearman_jump_vs_funding_settled"] = float(J[["jump", "f"]].corr(method="spearman").iloc[0, 1])
res["spearman_drift_vs_funding_settled"] = float(seg[["drift", "f"]].dropna().corr(method="spearman").iloc[0, 1])
bins = pd.cut(J["f"], [-1, 0.0000999, 0.0001001, 0.0003, 1], labels=["<0.01%", "=0.01%", "0.01-0.03%", ">0.03%"])
JT = J.groupby(bins, observed=True).agg(n=("jump", "size"), jump_mean=("jump", "mean"), jump_se=("jump", lambda s: s.std() / np.sqrt(len(s))),
                                        drift_mean=("drift", "mean"))
JT.to_csv("tables/p0_6b_jump_by_funding.csv"); print(JT.round(3).to_string())
# placebo: same jump measure at the 4h mid-cycle point (m=48) - not a settlement
tb["cyc4"] = tb.index.floor("4h"); mid = tb[(tb.index.floor("4h") != tb.index.floor("8h"))]
s4 = tb.assign(m4=((tb.index - tb.index.floor("4h")) / pd.Timedelta("5min")).astype(int))
s4["seg"] = np.where(s4["m4"] < 6, "first30", np.where(s4["m4"] >= 42, "last30", "mid"))
sg4 = s4.groupby(["cyc4", "seg"])["b"].mean().unstack(); sg4["jump"] = sg4["first30"] - sg4["last30"].shift(1)
sg4 = sg4[sg4.index.hour % 8 == 4]
res["placebo_midcycle_jump_mean_bp"] = float(sg4["jump"].mean()); res["placebo_se"] = float(sg4["jump"].std() / np.sqrt(sg4["jump"].notna().sum()))
fig, ax = plt.subplots(1, 2, figsize=(14, 4.5))
for i, c in enumerate(prof.columns):
    ax[0].plot(prof.index * 5 / 60, prof[c], label=f"{c} (n={cnt.get(c)})", color=PAL[i])
ax[0].axhline(0, color=GRAY); ax[0].set_xlabel("hours since funding settlement"); ax[0].set_ylabel("basis minus cycle mean (bp)")
ax[0].legend(fontsize=8); ax[0].set_title("within-cycle basis shape by funding state")
ax[1].bar(range(len(JT)), JT["jump_mean"], yerr=2 * JT["jump_se"], color=PAL[3]); ax[1].set_xticks(range(len(JT))); ax[1].set_xticklabels(JT.index)
ax[1].axhline(0, color=GRAY); ax[1].set_title(f"basis jump across settlement by funding settled (placebo mid-cycle {res['placebo_midcycle_jump_mean_bp']:.2f}bp)")
fig.suptitle("Phase 0 item 6b - basis around funding settlement, 2020-09..2021-12 (EXPLORE)"); save(fig, "00_6b_basis_cycle")

# ---- 4b partial Spearman for next-24h log RV
P["rv24_next"] = np.log((P["rv_1m"] ** 2).rolling(24).sum().shift(-24)) / 2
P["rv24_trail"] = np.log((P["rv_1m"] ** 2).rolling(24).sum()) / 2
P["rv30d_trail"] = np.log((P["rv_1m"] ** 2).rolling(24 * 30, min_periods=24 * 20).sum() / 30) / 2
def partial_spearman(df, x, y, ctrl):
    d = df[[x, y] + ctrl].replace([np.inf, -np.inf], np.nan).dropna().rank()
    import statsmodels.api as sm
    ex = sm.OLS(d[x], sm.add_constant(d[ctrl])).fit().resid; ey = sm.OLS(d[y], sm.add_constant(d[ctrl])).fit().resid
    return float(np.corrcoef(ex, ey)[0, 1]), int(len(d))
rows = []
for x in ["dvol", "half_bp", "basis_bp"]:
    for ctrl in (["rv24_trail"], ["rv24_trail", "rv30d_trail"]):
        rho, n = partial_spearman(P, x, "rv24_next", ctrl)
        rows.append(dict(x=x, ctrl="+".join(ctrl), partial_rho=rho, n=n, band=2 / np.sqrt(n)))
    rho, n = partial_spearman(P, x, "rv24_trail", [])  if False else (P[[x, "rv24_trail"]].corr(method="spearman").iloc[0, 1], 0)
    rows.append(dict(x=x, ctrl="contemporaneous corr with trailing RV", partial_rho=rho, n=np.nan, band=np.nan))
T4b = pd.DataFrame(rows); T4b.to_csv("tables/p0_4b_partial_rv.csv", index=False); print(T4b.round(4).to_string())
# dvol vs returns by era within EXPLORE (9 months) - monthly sign
P["r_next24"] = P["r"].rolling(24).sum().shift(-24)
m = P.dropna(subset=["dvol", "r_next24"]).groupby(pd.Grouper(freq="QE")).apply(lambda g: g[["dvol", "r_next24"]].corr(method="spearman").iloc[0, 1])
res["dvol_rnext24_spearman_by_quarter"] = {str(k.date()): v for k, v in m.round(3).items()}
json.dump(res, open("tables/p0_extra.json", "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str))
