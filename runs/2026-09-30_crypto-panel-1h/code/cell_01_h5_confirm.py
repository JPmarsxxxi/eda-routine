import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build, COINS
from tests import lag_ic, nscore
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("CONFIRM", "cell_01"); r = P["r"]
g = r.index.floor("6h"); cnt = r.notna().groupby(g).sum(); B = r.groupby(g).sum(min_count=1).where(cnt == 6)
B = B.reindex(pd.date_range(B.index.min(), B.index.max(), freq="6h", tz="UTC"))
day = B.index.floor("D")
ic, se, z, n = lag_ic(B, 1, cluster=day)
icp, sep, zp, _ = lag_ic(B, 1, cluster=day, transform=False)
branch = "inconclusive" if n < 400 or (z < -1.645 and zp > 1.645) else ("supported" if z < -1.645 else "refuted")
print(f"PRIMARY normal-score IC {ic:.4f} se {se:.4f} z {z:.2f} day-clusters {n} | Pearson IC {icp:.4f} z {zp:.2f} -> {branch}")
desc = {}
for L in [1, 2, 3, 4]:
    a = lag_ic(B, L, cluster=day); desc[f"lag{L}_{6*L}h"] = a[:3]
mid = pd.Timestamp("2022-05-14", tz="UTC")
for nm, m in [("half1", B.index < mid), ("half2", B.index >= mid)]:
    Bh = B[m]; desc[nm] = lag_ic(Bh, 1, cluster=Bh.index.floor("D"))[:3]
per = {c: lag_ic(B[[c]], 1, cluster=day)[:3] for c in COINS}
D = pd.DataFrame(desc, index=["ic", "se", "z"]).T; PC = pd.DataFrame(per, index=["ic", "se", "z"]).T
print(D.round(4).to_string()); print(PC.round(4).to_string())
# gross move by decile of current block (pooled, per-coin deciles)
nx = B.shift(-1); dec = B.rank(pct=True); lo = nx.where(dec <= .1).stack().mean() * 1e4; hi = nx.where(dec > .9).stack().mean() * 1e4
sd6 = (B.std() * 1e4).median()
print(f"next-block mean after bottom decile {lo:.1f} bp, after top decile {hi:.1f} bp; median 6h sd {sd6:.0f} bp; implied 1-sd move {abs(ic)*sd6:.1f} bp vs RT 19.8 bp")
out = pd.concat([D.assign(kind="desc"), PC.assign(kind="per_coin")]); out.loc["PRIMARY"] = [ic, se, z, "primary"]
out.to_csv(os.path.join(TB, "cell_01_h5.csv"))
pd.Series(dict(ic=ic, se=se, z=z, n=n, pearson_ic=icp, pearson_z=zp, branch=branch, bottom_dec_next_bp=lo, top_dec_next_bp=hi, sd6_bp=sd6)).to_csv(os.path.join(TB, "cell_01_h5_primary.csv"))
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.bar(range(1, 5), [desc[f"lag{L}_{6*L}h"][0] for L in range(1, 5)], color=[PAL[0]] + [GRAY] * 3)
ax.errorbar(range(1, 5), [desc[f"lag{L}_{6*L}h"][0] for L in range(1, 5)], yerr=[1.645 * desc[f"lag{L}_{6*L}h"][1] for L in range(1, 5)], fmt="none", ecolor="#52514e")
ax.axhline(0, color=GRAY, lw=1); ax.axhline(-0.065, color=PAL[7], ls="--", lw=1, label="smallest meaningful effect -0.065")
ax.set_xticks(range(1, 5)); ax.set_xticklabels(["6h", "12h", "18h", "24h"]); ax.set_xlabel("lag between 6h blocks"); ax.set_ylabel("normal-score IC")
ax.set_title(f"H5 on CONFIRM: 6h->next-6h IC {ic:.3f} (z {z:.1f}) -> {branch}"); ax.legend()
save(fig, "cell_01_h5_6h_reversal")
