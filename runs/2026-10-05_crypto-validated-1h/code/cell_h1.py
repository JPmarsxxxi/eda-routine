"""H1 test / val cell: XS perp-premium sort, 72h primary returns, ONE slice. usage: cell_h1.py <NN> <slice> <kind>"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from hyp import *
setup()
nn, sl, kind = int(sys.argv[1]), sys.argv[2], sys.argv[3]
CELL = f"cell_{nn:02d}"
B, R3 = h1_blocks(CELL, sl)
B.to_csv(os.path.join(RUN, "tables", f"cell_{nn:02d}_blocks.csv"))
v = B.dropna(subset=["spread"])
coins = sorted(R3.columns[R3.notna().any()].tolist())
T = h1_threshold(coins)
n = len(v); m = v.spread.mean(); sd = v.spread.std(ddof=1); t = m / sd * np.sqrt(n)
br = branch(t, m * 1e4, T, -1)
res = dict(cell=nn, slice=sl, n_blocks=n, blocks_dropped=int(B.spread.isna().sum()), coins=coins, T_bp=T,
           spread_bp=m * 1e4, sd_bp=sd * 1e4, t=t, mean_ic=v.ic.mean(), ic_t=v.ic.mean() / v.ic.std() * np.sqrt(n),
           share_negative=(v.spread < 0).mean(), first=str(v.index.min().date()), last=str(v.index.max().date()), branch=br)
json.dump(res, open(os.path.join(RUN, "tables", f"cell_{nn:02d}_result.json"), "w"), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
fig, ax = plt.subplots(figsize=(10, 3.8))
cs = v.spread.cumsum() * 1e4
ax.plot(cs.index, cs, color=PAL[0], label="cumulative top-minus-bottom 72h spread (bp)")
ax.plot(cs.index, -T * np.arange(1, n + 1), color=GRAY, ls="--", lw=1, label=f"cost-sized path (-{T:.0f} bp per block)")
ax.axhline(0, color=GRAY, lw=0.8)
ax.set_title(f"H1 on {sl}: mean spread {m*1e4:+.0f} bp per 72h (t {t:+.2f}, n {n}) vs -{T:.0f} bp needed -> {br}")
ax.legend(loc="lower left"); save(fig, f"cell_{nn:02d}_h1_{sl.lower()}.png")
