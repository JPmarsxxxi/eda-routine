# Cell 03 - C8 decay-first gate. TRAIN only. No pooled slope is printed in this cell.
from common import *
from scipy import stats
from statsmodels.stats.diagnostic import breaks_cusumolsresid
setup()
d = pd.read_parquet("tables/01_daily_legs_TRAIN.parquet").dropna(subset=["r_first", "r_last"])
rows = []
for n, a, b in ERAS:
    s = d.loc[a:b]; f = nw_ols(s["r_last"], s["r_first"])
    rows.append({"era": n, "n": len(s), "slope": f.params["r_first"], "nw_t": f.tvalues["r_first"],
                 "spearman_ic": stats.spearmanr(s["r_first"], s["r_last"]).statistic,
                 "hit_rate": float((np.sign(s["r_first"]) == np.sign(s["r_last"])).mean()),
                 "mean_signed_bp": 1e4 * float((np.sign(s["r_first"]) * s["r_last"]).mean())})
E = pd.DataFrame(rows).set_index("era"); print(E.round(4)); E.to_csv("tables/03_era_slopes.csv")
b, t = E["slope"].values, E["nw_t"].values
rho = stats.spearmanr(range(5), b).statistic
flips = int((np.diff(np.sign(b)) != 0).sum())
if t[0] >= 2 and rho <= -0.8 and t[4] < 1: shape = "MONOTONE DECAY (KILL)"
elif flips >= 2 and (t[b > 0] >= 1.5).any() and (np.abs(t[b < 0]) >= 1.5).any(): shape = "ALTERNATING (KILL)"
elif b[4] == b.max() or rho >= 0.8: shape = "STRONGEST-RECENT (PASS)"
elif len(set(np.sign(b))) == 1: shape = "FLAT (PASS)"
else: shape = "MIXED (INCONCLUSIVE)"
print("spearman(era,b)=%.2f flips=%d -> %s" % (rho, flips, shape))
# Chow at era boundaries
def ssr(s):
    return sm.OLS(s["r_last"], sm.add_constant(s["r_first"])).fit().ssr
chow = []
for i in range(1, 5):
    cut = ERAS[i][1]; s1, s2 = d.loc[:cut].iloc[:-1], d.loc[cut:]
    S, S1, S2, k = ssr(d), ssr(s1), ssr(s2), 2
    F = ((S - S1 - S2) / k) / ((S1 + S2) / (len(d) - 2 * k))
    chow.append({"boundary": cut, "F": F, "p": 1 - stats.f.cdf(F, k, len(d) - 2 * k)})
C = pd.DataFrame(chow); print(C.round(4)); C.to_csv("tables/03_chow.csv", index=False)
res = sm.OLS(d["r_last"], sm.add_constant(d["r_first"])).fit().resid
cus = breaks_cusumolsresid(res.values, ddof=2); print("CUSUM stat %.3f p %.4f" % (cus[0], cus[1]))
pd.Series({"cusum_stat": cus[0], "cusum_p": cus[1], "spearman_era_b": rho, "sign_flips": flips, "shape": shape}).to_csv("tables/03_shape.csv")
# rolling 365-day slope (cov/var over trailing 365 usable days)
x, y = d["r_first"], d["r_last"]
roll = (x.rolling(365).cov(y) / x.rolling(365).var()).dropna(); roll.to_csv("tables/03_rolling_slope.csv")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(roll.index, roll.values, color=PAL[0], label="rolling 365-day slope")
for (n, a, bb), sl in zip(ERAS, b):
    ax.hlines(sl, pd.Timestamp(a), pd.Timestamp(bb), color=PAL[3], lw=3, label="era slope" if n == ERAS[0][0] else None)
ax.axhline(0, color=GRAY, lw=1, ls="--")
ax.set_ylabel("slope of r_last on r_first"); ax.legend(frameon=False)
ax.set_title(f"C8 decay-first: {shape}; era slopes " + ", ".join(f"{v:+.3f}" for v in b) + f" (t " + ", ".join(f"{v:+.1f}" for v in t) + ")")
save(fig, "03_decay_first")
