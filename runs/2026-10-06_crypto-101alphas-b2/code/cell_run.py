"""Run one Phase-2 cell's computation AFTER its rule file exists. Usage:
    python cell_run.py NN KIND ALPHA SLICE [SIGN]
KIND in {test, val, redirect}. SIGN = +1 (paper's direction, default) or -1 (a flipped child).
Writes tables/cell_NN.json and plots/cell_NN_<alpha>_<slice>.png. The decision is the D7 rule on the neutral statistic; every
other number is a pre-registered descriptive (DECISIONS D7, D11)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import common as C

nn, kind, alpha, sl = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
sign = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
rule = os.path.join(C.RUN, "cells", f"cell_{nn:02d}_rule.md")
assert os.path.exists(rule), "rule file must exist before the cell runs"
C.setup_plot()
F, R = C.cached()
S = sign * C.ALPHAS[alpha](F)
Ss = S.loc[C.in_slice(S.index, sl)]
Rs = C.response_in_slice(R, sl)
Ss, Rs = Ss.align(Rs, join="inner")

ic = C.daily_rank_ic(Ss, Rs)
st = C.summarize(ic)
br = C.branch(st, 1.0) if st["n"] >= 150 else "inconclusive"

# raw version: own-return prediction incl. market (trailing scaling only)
raw = C.summarize(C.daily_ts_ic(S, Rs, R))

# net of 1-day reversal: residualise the alpha's ranks on b_rev1's ranks each day
c = F["close"]
brev = -np.log(c / c.shift(1))
net = {}
for d in Ss.index:
    s, b, r = Ss.loc[d], brev.loc[d], Rs.loc[d]
    m = s.notna() & b.notna() & r.notna()
    if m.sum() < C.MIN_COINS or s[m].nunique() < 2:
        continue
    x, z = s[m].rank().values, b[m].rank().values
    z1 = np.c_[np.ones(len(z)), z]
    res = x - z1 @ np.linalg.lstsq(z1, x, rcond=None)[0]
    if np.std(res) > 0:
        net[d] = pd.Series(res).rank().corr(r[m].rank().reset_index(drop=True))
net = C.summarize(pd.Series(net, dtype=float))
ic_rev = C.summarize(C.daily_rank_ic(brev.loc[Ss.index], Rs))  # the impostor's own IC on this slice

spr, turn = C.ls_spread_bp(Ss, Rs)
sp = C.summarize(spr)
RT, ROLL = 45.0, 8.2   # TARGET.md median-coin round trip incl. one rollover night; rollover part (DECISIONS D11)
cost_day = 2 * (turn * (RT - ROLL) + ROLL) if np.isfinite(turn) else np.nan

# market share: cross-sectional mean of the trailing-z signal vs the same-day panel / BTC return (Binance, day d)
zS = C.trailing_z(S).loc[Ss.index]
rb = np.log(c / c.shift(1)).loc[Ss.index]
mk = pd.concat([zS.mean(axis=1), rb.mean(axis=1), rb["BTCUSD"]], axis=1).dropna()
mkt_corr = float(mk.iloc[:, 0].corr(mk.iloc[:, 1])) if len(mk) > 30 else np.nan
btc_corr = float(mk.iloc[:, 0].corr(mk.iloc[:, 2])) if len(mk) > 30 else np.nan

half = len(ic) // 2
h1, h2 = C.summarize(ic.iloc[:half]), C.summarize(ic.iloc[half:])
out = {"cell": nn, "kind": kind, "alpha": alpha, "slice": sl, "sign": sign,
       "neutral": st, "branch": br, "raw": raw, "net_of_rev1": net, "rev1_ic": ic_rev,
       "spread_bp": sp, "turnover": turn, "cost_bp_day": cost_day, "market_corr": mkt_corr, "btc_corr": btc_corr,
       "half1": h1, "half2": h2, "first_day": str(ic.index.min()), "last_day": str(ic.index.max())}
json.dump(out, open(os.path.join(C.RUN, "tables", f"cell_{nn:02d}.json"), "w"), indent=1, default=float)
ic.rename("ic").to_csv(os.path.join(C.RUN, "tables", f"cell_{nn:02d}_daily_ic.csv"))

fig, ax = plt.subplots(1, 2, figsize=(11, 3.6), gridspec_kw={"width_ratios": [2, 1]})
cum = ic.cumsum()
ax[0].plot(pd.to_datetime(list(cum.index)), cum.values, color=C.PAL[0], label="cumulative daily rank IC")
ax[0].plot(pd.to_datetime(list(cum.index)), np.arange(1, len(cum) + 1) * C.MIN_USEFUL_IC, color=C.GRAY, ls="--",
           label="pace of IC = 0.02 (minimum useful)")
ax[0].legend(fontsize=7)
lab = f"{'-' if sign < 0 else ''}{alpha} on {sl}: IC {st['mean']:+.4f} (t {st['t']:+.2f}, {st['n']} days) -> {br.upper()}"
ax[0].set_title(lab)
names = ["neutral", "raw", "net_of_rev1", "rev1_ic"]
vals = [st["mean"], raw["mean"], net["mean"], ic_rev["mean"]]
errs = [1.645 * x["se"] if x["se"] == x["se"] else 0 for x in (st, raw, net, ic_rev)]
ax[1].barh(names, vals, xerr=errs, color=[C.PAL[0], C.PAL[1], C.PAL[3], C.GRAY])
ax[1].axvline(C.MIN_USEFUL_IC, color=C.GRAY, ls="--"); ax[1].axvline(0, color="#52514e", lw=0.8)
ax[1].set_title("mean daily IC +- 1.645 se")
C.savefig(fig, f"cell_{nn:02d}_{alpha.lower()}_{sl.lower()}{'_flip' if sign < 0 else ''}.png")
print(json.dumps(out, indent=1, default=float))
