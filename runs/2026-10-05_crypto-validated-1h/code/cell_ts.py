"""H2 / H3 test cells: market-wide feature known at d+1 00:00 vs equal-weight panel 24h return over day d+1, ONE slice.
usage: cell_ts.py <NN> <H2|H3> <slice> <kind>"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from hyp import *
setup()
nn, hy, sl, kind = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
CELL = f"cell_{nn:02d}"
idx = pd.date_range(ts("2015-01-01"), ts("2023-12-01"), freq="D")
if hy == "H2":
    fg = load("attention/fear_greed.parquet", CELL).set_index("_t").value.astype(float).sort_index()
    feat = fg.reindex(idx).ffill(limit=2)          # stamped <= d (published ~00:00 of its own day)
    fname = "Fear & Greed level"
else:
    y = load("macro/yahoo_GSPC.parquet", CELL)
    y = y.set_index(pd.to_datetime(y.local_date).dt.tz_localize("UTC")).close.sort_index()
    feat = np.log(y).diff().reindex(idx).shift(1)  # session local_date <= d-1 (lag one session)
    fname = "S&P 500 prior-session return"
z = ts_daily(CELL, feat, sl)
coins_present = primary_daily(CELL, sl)["r24"]
coins = sorted(coins_present.columns[coins_present.notna().any()].tolist())
T = ts_threshold(coins)
r = ts_stat(z); br = branch(r["t"], r["spread_bp"], T, +1)
res = dict(cell=nn, hyp=hy, slice=sl, T_bp=T, coins=coins, branch=br, first=str(z.index.min().date()), last=str(z.index.max().date()), **r)
json.dump(res, open(os.path.join(RUN, "tables", f"cell_{nn:02d}_result.json"), "w"), indent=1, default=str)
z.to_csv(os.path.join(RUN, "tables", f"cell_{nn:02d}_days.csv"))
print(json.dumps(res, indent=1, default=str))
q = z.f.rank(pct=True); grp = np.where(q > 2 / 3, "top", np.where(q <= 1 / 3, "bottom", "middle"))
m = z.groupby(grp).r.mean() * 1e4
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.bar(["bottom", "middle", "top"], [m.get("bottom", np.nan), m.get("middle", np.nan), m.get("top", np.nan)], color=[PAL[0], GRAY, PAL[1]])
ax.axhline(0, color=GRAY, lw=0.8)
ax.set_ylabel("mean next-day panel return (bp)"); ax.set_xlabel(f"tercile of {fname}")
ax.set_title(f"{hy} on {sl}: top-minus-bottom {r['spread_bp']:+.0f} bp (t {r['t']:+.2f}, n {r['n']}) vs +{T:.0f} needed -> {br}")
save(fig, f"cell_{nn:02d}_{hy.lower()}_{sl.lower()}.png")
