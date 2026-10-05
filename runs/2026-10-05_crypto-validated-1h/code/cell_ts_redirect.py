"""Fixed redirect menu for H2 / H3 on a slice the hypothesis already opened. usage: cell_ts_redirect.py <NN> <H2|H3> <slice>"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from hyp import *
setup()
NN, hy, SL = int(sys.argv[1]), sys.argv[2], sys.argv[3]; CELL = f"cell_{NN:02d}"
idx = pd.date_range(ts("2015-01-01"), ts("2023-12-01"), freq="D")
if hy == "H2":
    fg = load("attention/fear_greed.parquet", CELL).set_index("_t").value.astype(float).sort_index()
    feat = fg.reindex(idx).ffill(limit=2); chg = feat - feat.shift(7); lo, hi = 25, 75
else:
    y = load("macro/yahoo_GSPC.parquet", CELL); y = y.set_index(pd.to_datetime(y.local_date).dt.tz_localize("UTC")).close.sort_index()
    lr = np.log(y).diff()
    feat = lr.reindex(idx).shift(1); chg = np.log(y / y.shift(5)).reindex(idx).shift(1); lo, hi = -0.01, 0.01
D = primary_daily(CELL, SL)
coins = sorted(D["r24"].columns[D["r24"].notna().any()].tolist())
T24 = ts_threshold(coins); T72 = 2 * np.mean([rt_cost(c, 72) for c in coins]); TB = 2 * rt_cost("BTCUSD", 24)
def tstat(top, bot):
    top, bot = top.dropna(), bot.dropna()
    if len(top) < 2 or len(bot) < 2:
        return dict(n_top=len(top), n_bot=len(bot), spread_bp=np.nan, t=np.nan)
    sp = top.mean() - bot.mean(); se = np.sqrt(top.var() / len(top) + bot.var() / len(bot))
    return dict(n_top=len(top), n_bot=len(bot), spread_bp=sp * 1e4, t=sp / se)
def terc(f, r):
    z = pd.DataFrame({"f": f, "r": r}).dropna(); q = z.f.rank(pct=True); return tstat(z.r[q > 2 / 3], z.r[q <= 1 / 3])
z1 = ts_daily(CELL, feat, SL, D)
out = {}
out["R1_opposite_sign"] = dict(**terc(z1.f, z1.r), bar_bp=-T24)
R3 = fwd(D["r24"], 3); R3 = R3[in_slice(R3.index, SL, 3)]; p3 = R3.mean(1).where(R3.notna().sum(1) >= 5).iloc[::3]
out["R2_72h"] = dict(**terc(feat.reindex(p3.index), p3), bar_bp=T72)
out["R3_extremes"] = dict(**tstat(z1.r[z1.f >= hi], z1.r[z1.f <= lo]), bar_bp=T24)
out["R4_change"] = dict(**terc(chg.reindex(z1.index), z1.r), bar_bp=T24)
Rb = fwd(D["r24"], 1)["BTCUSD"]; Rb = Rb[in_slice(Rb.index, SL, 1)]
out["R5_btc_only"] = dict(**terc(feat.reindex(Rb.index), Rb), bar_bp=TB)
O = pd.DataFrame(out).T
O["qualifies"] = [bool(r.t == r.t) and ((r.t <= -2.5 and r.spread_bp <= r.bar_bp) if k == "R1_opposite_sign" else (r.t >= 2.5 and r.spread_bp >= r.bar_bp)) for k, r in O.iterrows()]
O.to_csv(os.path.join(RUN, "tables", f"cell_{NN:02d}_redirect.csv")); print(O.round(3).to_string())
fig, ax = plt.subplots(figsize=(9, 3.6))
ax.bar(O.index, O.spread_bp.astype(float).fillna(0), color=[PAL[7] if q else PAL[0] for q in O.qualifies])
for i, (k, r) in enumerate(O.iterrows()):
    ax.text(i, float(np.nan_to_num(r.spread_bp)), f"t {float(r.t):+.1f}", ha="center", va="bottom" if r.spread_bp > 0 else "top", fontsize=8)
ax.axhline(0, color=GRAY, lw=0.8); ax.set_ylabel("top-minus-bottom (bp)"); ax.tick_params(axis="x", labelsize=7)
ax.set_title(f"{hy} redirect on {SL}: {int(O.qualifies.sum())} of {len(O)} looks clear |t|>=2.5 and the cost bar")
save(fig, f"cell_{NN:02d}_{hy.lower()}_redirect_{SL.lower()}.png")
