import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build, COINS
from tests import lag_ic
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("CONFIRM", "cell_03"); r = P["r"]; day = r.index.floor("D")
res = {L: lag_ic(r, L, cluster=day) for L in [1, 2, 12, 23, 24, 25, 48]}
ic24, se24, z24, n = res[24]; icp, sep, zp, _ = lag_ic(r, 24, cluster=day, transform=False)
cond2 = ic24 < min(res[23][0], res[25][0])
branch = "inconclusive" if n < 400 or (z24 < -1.645 and zp > 1.645) else ("supported" if (z24 < -1.645 and cond2) else "refuted")
print(f"PRIMARY lag24 IC {ic24:.4f} se {se24:.4f} z {z24:.2f} days {n}; lag23 {res[23][0]:.4f} lag25 {res[25][0]:.4f} cond2 {cond2} | Pearson {icp:.4f} z {zp:.2f} -> {branch}")
D = pd.DataFrame({f"lag{L}": v[:3] for L, v in res.items()}, index=["ic", "se", "z"]).T
mid = pd.Timestamp("2022-05-14", tz="UTC")
for nm, m in [("half1", r.index < mid), ("half2", r.index >= mid)]:
    rh = r[m]; D.loc[f"lag24_{nm}"] = lag_ic(rh, 24, cluster=rh.index.floor("D"))[:3]
for c in COINS: D.loc[f"lag24_{c}"] = lag_ic(r[[c]], 24, cluster=day)[:3]
# by hour of r(t): products of normal scores averaged per hour (descriptive, no SE)
from tests import nscore
Z = nscore(r); prod = (Z * Z.shift(-24)).mean(axis=1); byh = prod.groupby(r.index.hour).mean()
print(D.round(4).to_string()); print("lag24 IC by UTC hour:", byh.round(3).to_dict())
D.to_csv(os.path.join(TB, "cell_03_h3.csv")); byh.to_csv(os.path.join(TB, "cell_03_h3_byhour.csv"))
fig, ax = plt.subplots(figsize=(7.5, 3.8))
Ls = [1, 2, 12, 23, 24, 25, 48]
ax.bar([str(L) for L in Ls], [res[L][0] for L in Ls], color=[PAL[0] if L == 24 else GRAY for L in Ls])
ax.errorbar(range(len(Ls)), [res[L][0] for L in Ls], yerr=[1.645 * res[L][1] for L in Ls], fmt="none", ecolor="#52514e")
ax.axhline(0, color=GRAY, lw=1); ax.axhline(-0.05, color=PAL[7], ls="--", lw=1, label="smallest meaningful -0.05")
ax.set_xlabel("lag (hours)"); ax.set_ylabel("1h normal-score IC"); ax.legend()
ax.set_title(f"H3 on CONFIRM: lag-24 IC {ic24:.3f} (z {z24:.1f}), lag-24-specific={cond2} -> {branch}")
save(fig, "cell_03_h3_lag24")
