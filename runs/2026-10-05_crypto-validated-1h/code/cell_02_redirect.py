import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from hyp import *
setup()
CELL, SL = "cell_02", "C1"
D = primary_daily(CELL, SL)
P = feat_premium(CELL)
B, R3 = h1_blocks(CELL, SL, D)
coins = sorted(R3.columns[R3.notna().any()].tolist()); T72 = h1_threshold(coins); T24 = ts_threshold(coins)
def tt(x): x = pd.Series(x).dropna(); return dict(n=len(x), mean_bp=x.mean() * 1e4, t=x.mean() / x.std() * np.sqrt(len(x)))
out = {}
v = B.dropna(subset=["spread"])
out["R1_sign_72h"] = tt(v.spread)
# R2 24h
R1 = fwd(D["r24"], 1); R1 = R1[in_slice(R1.index, SL, 1)]
sp24 = []
for d in R1.index:
    a = pd.DataFrame({"p": P.reindex(index=[d], columns=R1.columns).iloc[0], "f": R1.loc[d]}).dropna()
    if len(a) < 5: continue
    q = a.p.rank(pct=True); sp24.append(a.f[q > 2 / 3].mean() - a.f[q <= 1 / 3].mean())
out["R2_24h"] = tt(sp24)
# R3 dispersion, R4 extremes
rng_, ext = {}, {}
for d in v.index:
    a = pd.DataFrame({"p": P.reindex(index=[d], columns=R3.columns).iloc[0], "f": R3.loc[d]}).dropna()
    rng_[d] = a.p.max() - a.p.min(); ext[d] = a.f[a.p.idxmax()] - a.f[a.p.idxmin()]
rg = pd.Series(rng_); hi = rg > rg.median()
out["R3_high_dispersion"] = tt(v.spread[hi]); out["R3_low_dispersion"] = tt(v.spread[~hi])
out["R4_extremes"] = tt(pd.Series(ext))
half = len(v) // 2
out["R5_first_half"] = tt(v.spread.iloc[:half]); out["R5_second_half"] = tt(v.spread.iloc[half:])
bars = {"R1_sign_72h": T72, "R2_24h": T24, "R3_high_dispersion": T72, "R3_low_dispersion": T72, "R4_extremes": T72, "R5_first_half": T72, "R5_second_half": T72}
for k, r in out.items():
    r["bar_bp"] = bars[k]
    if k == "R1_sign_72h":
        r["qualifies"] = bool(r["t"] >= 2.5 and r["mean_bp"] >= bars[k])
    else:
        r["qualifies"] = bool(r["t"] <= -2.5 and r["mean_bp"] <= -bars[k])
O = pd.DataFrame(out).T; O.to_csv(os.path.join(RUN, "tables", "cell_02_redirect.csv")); print(O.round(3).to_string())
fig, ax = plt.subplots(figsize=(10, 3.6))
ax.bar(O.index, O.mean_bp.astype(float), color=[PAL[7] if q else PAL[0] for q in O.qualifies])
for i, (k, r) in enumerate(O.iterrows()):
    ax.text(i, float(r.mean_bp), f"t {float(r.t):+.1f}", ha="center", va="bottom" if r.mean_bp > 0 else "top", fontsize=8)
ax.axhline(-T72, color=GRAY, ls="--", lw=1); ax.axhline(0, color=GRAY, lw=0.8)
ax.set_ylabel("mean spread (bp)"); ax.tick_params(axis="x", labelsize=7)
ax.set_title(f"H1 redirect on C1: {int(O.qualifies.sum())} of {len(O)} looks clear |t|>=2.5 and the cost bar")
save(fig, "cell_02_h1_redirect_c1.png")
