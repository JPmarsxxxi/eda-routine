import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build, COINS
from tests import lag_ic, diff_ic_clustered
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("EXPLORE", "cell_02"); r = P["r"]
g = r.index.floor("6h"); cnt = r.notna().groupby(g).sum(); B = r.groupby(g).sum(min_count=1).where(cnt == 6)
B = B.reindex(pd.date_range(B.index.min(), B.index.max(), freq="6h", tz="UTC")); day = B.index.floor("D")
ew = r.mean(axis=1)                                  # EW over live coins
tv = ew.pow(2).rolling(168, min_periods=150).sum()   # trailing 7d realized var up to and incl. hour t
tv_day = tv.shift(1).groupby(tv.index.floor("D")).first()   # value known at 00:00 of the day (uses hours < 00:00)
cut = tv_day.quantile(2 / 3); high_day = tv_day > cut
hm = pd.Series(day, index=B.index).map(high_day).fillna(False).astype(bool).values
d, se, z, (na, nb) = diff_ic_clustered(B, 1, hm, day)
from tests import nscore
Bp = (B - B.mean()) / B.std()
# Pearson variant: same function on standardized raw values (monkey: skip nscore by passing already-ranked-free data)
prod = Bp * Bp.shift(-1); cl = np.asarray(day)
c = prod.sum(axis=1, min_count=1).groupby(cl).sum(min_count=1) / prod.notna().sum(axis=1).groupby(cl).sum().replace(0, np.nan)
hmd = pd.Series(hm).groupby(cl).first().reindex(c.index).values
a_, b_ = c[hmd].dropna(), c[~hmd].dropna(); dp = a_.mean() - b_.mean(); zp = dp / np.sqrt(a_.var() / len(a_) + b_.var() / len(b_))
branch = "inconclusive" if min(na, nb) < 300 or (z < -1.645 and zp > 1.645) else ("supported" if z < -1.645 else "refuted")
print(f"PRIMARY diff IC (high - other) {d:.4f} se {se:.4f} z {z:.2f} n_high {na} n_other {nb} | Pearson diff {dp:.4f} z {zp:.2f} -> {branch}")
ter = pd.qcut(tv_day, 3, labels=["low", "mid", "high"])
desc = {}
for t in ["low", "mid", "high"]:
    days_t = set(ter[ter == t].index); m = np.array([x in days_t for x in day])
    Bt = B[m]; desc[f"tercile_{t}"] = lag_ic(Bt, 1, cluster=Bt.index.floor("D"))[:3]
for e, (a, b) in {"2017H2-18": ("2017", "2018"), "2019": ("2019", "2019"), "2020": ("2020", "2020"), "2021H1": ("2021", "2021")}.items():
    Bt = B.loc[a:b]; desc[e] = lag_ic(Bt, 1, cluster=Bt.index.floor("D"))[:3]
desc["ALL_EXPLORE"] = lag_ic(B, 1, cluster=day)[:3]
D = pd.DataFrame(desc, index=["ic", "se", "z"]).T; print(D.round(4).to_string())
D.loc["PRIMARY_diff"] = [d, se, z]; D.to_csv(os.path.join(TB, "cell_02_h6.csv"))
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ks = ["tercile_low", "tercile_mid", "tercile_high"]
ax.bar(["low", "mid", "high"], [desc[k][0] for k in ks], color=[GRAY, GRAY, PAL[0]])
ax.errorbar(range(3), [desc[k][0] for k in ks], yerr=[1.645 * desc[k][1] for k in ks], fmt="none", ecolor="#52514e")
ax.axhline(0, color=GRAY, lw=1); ax.set_xlabel("trailing 7-day panel volatility tercile (day start)"); ax.set_ylabel("6h->6h normal-score IC")
ax.set_title(f"H6 on EXPLORE: high-minus-other IC {d:.3f} (z {z:.1f}) -> {branch}")
save(fig, "cell_02_h6_vol_conditional")
