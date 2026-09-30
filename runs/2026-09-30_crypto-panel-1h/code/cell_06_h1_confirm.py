import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build, COINS
from daily import daily
from tests import lag_ic, nscore
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("CONFIRM", "cell_06"); R, REL, V, QV = daily(P)
ic, se, z, n = lag_ic(R, 1); icp, sep, zp, _ = lag_ic(R, 1, transform=False)
branch = "inconclusive" if n < 400 or (z < -1.645 and zp > 1.645) else ("supported" if z < -1.645 else "refuted")
print(f"PRIMARY daily IC {ic:.4f} se {se:.4f} z {z:.2f} days {n} | Pearson {icp:.4f} z {zp:.2f} -> {branch}")
D = {f"lag{L}d": lag_ic(R, L)[:3] for L in [1, 2, 3, 7]}
mid = pd.Timestamp("2022-05-14", tz="UTC")
D["half1"] = lag_ic(R[R.index < mid], 1)[:3]; D["half2"] = lag_ic(R[R.index >= mid], 1)[:3]
for c in COINS: D[c] = lag_ic(R[[c]], 1)[:3]
Z = nscore(R); prod = Z * Z.shift(-1)
big = R.abs().ge(R.abs().quantile(.9)); D["big10pct_days"] = (prod.where(big).stack().mean(), np.nan, np.nan); D["other_days"] = (prod.where(~big).stack().mean(), np.nan, np.nan)
for w, nm in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
    D[f"wd_{nm}"] = (prod[R.index.dayofweek == w].stack().mean(), np.nan, np.nan)
T = pd.DataFrame(D, index=["ic", "se", "z"]).T; print(T.round(4).to_string())
nx = R.shift(-1); dec = R.rank(pct=True); lo = nx.where(dec <= .1).stack().mean() * 1e4; hi = nx.where(dec > .9).stack().mean() * 1e4
sdd = (R.std() * 1e4).median()
print(f"next-day mean after bottom decile {lo:.1f} bp, after top decile {hi:.1f} bp; median daily sd {sdd:.0f} bp; implied 1-sd move {abs(ic)*sdd:.1f} bp vs 28 bp")
T.to_csv(os.path.join(TB, "cell_06_h1.csv"))
pd.Series(dict(ic=ic, se=se, z=z, days=n, pearson_ic=icp, pearson_z=zp, branch=branch, bottom_dec_next_bp=lo, top_dec_next_bp=hi, sd_day_bp=sdd)).to_csv(os.path.join(TB, "cell_06_h1_primary.csv"))
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ks = ["lag1d", "lag2d", "lag3d", "lag7d"]
ax.bar(["1d", "2d", "3d", "7d"], [D[k][0] for k in ks], color=[PAL[0], GRAY, GRAY, GRAY])
ax.errorbar(range(4), [D[k][0] for k in ks], yerr=[1.645 * D[k][1] for k in ks], fmt="none", ecolor="#52514e")
ax.axhline(0, color=GRAY, lw=1); ax.axhline(-0.045, color=PAL[7], ls="--", lw=1, label="smallest meaningful -0.045")
ax.set_xlabel("lag (days)"); ax.set_ylabel("daily normal-score IC"); ax.legend()
ax.set_title(f"H1 on CONFIRM: day->next-day IC {ic:.3f} (z {z:.2f}) -> {branch}")
save(fig, "cell_06_h1_daily")
