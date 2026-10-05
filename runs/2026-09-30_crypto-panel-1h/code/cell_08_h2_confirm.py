import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build
from daily import daily
from tests import diff_ic, nscore, nw_se
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("CONFIRM", "cell_08"); R, REL, V, QV = daily(P)
shock = np.log(V / V.shift(1).rolling(30, min_periods=20).median()); ps = shock.mean(axis=1)
cut = ps.quantile(2 / 3); high = (ps > cut).values & ps.notna().values
d, se, z, (na, nb) = diff_ic(R, 1, high)
Rs = (R - R.mean()) / R.std(); c = (Rs * Rs.shift(-1)).mean(axis=1); hm = pd.Series(high, index=R.index)
a_, b_ = c[hm].dropna(), c[~hm].dropna(); dp = a_.mean() - b_.mean(); zp = dp / np.sqrt(a_.var() / len(a_) + b_.var() / len(b_))
branch = "inconclusive" if min(na, nb) < 150 or (z < -1.645 and zp > 1.645) else ("supported" if z < -1.645 else "refuted")
print(f"PRIMARY diff IC (high - other) {d:.4f} se {se:.4f} z {z:.2f} n_high {na} n_other {nb} | Pearson diff {dp:.4f} z {zp:.2f} -> {branch}")
Z = nscore(R); prod = Z * Z.shift(-1); cday = prod.mean(axis=1)
ter = pd.qcut(ps, 3, labels=["low", "mid", "high"])
desc = {}
for t in ["low", "mid", "high"]:
    x = cday[ter == t].dropna(); s_, n_ = nw_se(x.values); desc[f"tercile_{t}"] = (x.mean(), s_, x.mean() / s_)
mid = pd.Timestamp("2022-05-14", tz="UTC")
for nm, m in [("half1", R.index < mid), ("half2", R.index >= mid)]:
    hh = hm & m; x1, x2 = cday[hh].dropna(), cday[~hm & m].dropna(); desc[f"diff_{nm}"] = (x1.mean() - x2.mean(), np.sqrt(x1.var() / len(x1) + x2.var() / len(x2)), (x1.mean() - x2.mean()) / np.sqrt(x1.var() / len(x1) + x2.var() / len(x2)))
big = R.abs().ge(R.abs().quantile(.9)); cnb = prod.where(~big).mean(axis=1)
x1, x2 = cnb[hm].dropna(), cnb[~hm].dropna(); desc["diff_excl_big_moves"] = (x1.mean() - x2.mean(), np.sqrt(x1.var() / len(x1) + x2.var() / len(x2)), (x1.mean() - x2.mean()) / np.sqrt(x1.var() / len(x1) + x2.var() / len(x2)))
D = pd.DataFrame(desc, index=["ic", "se", "z"]).T; D.loc["PRIMARY_diff"] = [d, se, z]; print(D.round(4).to_string())
D.to_csv(os.path.join(TB, "cell_08_h2.csv"))
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ks = ["tercile_low", "tercile_mid", "tercile_high"]
ax.bar(["low", "mid", "high"], [desc[k][0] for k in ks], color=[GRAY, GRAY, PAL[0]])
ax.errorbar(range(3), [desc[k][0] for k in ks], yerr=[1.645 * desc[k][1] for k in ks], fmt="none", ecolor="#52514e")
ax.axhline(0, color=GRAY, lw=1); ax.set_xlabel("panel volume-shock tercile (day d)"); ax.set_ylabel("day->next-day normal-score IC")
ax.set_title(f"H2 on CONFIRM: high-minus-other IC {d:.3f} (z {z:.2f}) -> {branch}")
save(fig, "cell_08_h2_volume_shock")
