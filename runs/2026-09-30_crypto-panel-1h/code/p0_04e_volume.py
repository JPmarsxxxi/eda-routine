import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build, COINS
from daily import daily
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("EXPLORE", "p0_04e"); R, REL, V, QV = daily(P)
shock = np.log(V / V.shift(1).rolling(30, min_periods=20).median())
nxt = REL.shift(-1)
ok = REL.notna() & shock.notna() & nxt.notna()
ter = shock.where(ok).rank(axis=1, pct=True); ter = np.ceil(ter * 3).clip(1, 3)
win = REL > 0
cells = {}
for tname, tv in [("low", 1), ("mid", 2), ("high", 3)]:
    for side, m in [("win", win), ("lose", ~win)]:
        cells[(tname, side)] = nxt.where(ok & (ter == tv) & m).mean(axis=1)
C = pd.DataFrame(cells)
wl = {t: C[(t, "win")] - C[(t, "lose")] for t in ["low", "mid", "high"]}
diff = (wl["high"] - wl["low"]).dropna(); t = diff.mean() / diff.std() * np.sqrt(len(diff))
tab = (C.mean() * 1e4).round(1).unstack(); print(tab.to_string())
print({k: round(v.mean() * 1e4, 1) for k, v in wl.items()}, "high-low W-L diff bp", round(diff.mean() * 1e4, 1), "t", round(t, 2), "days", len(diff))
tab.assign(high_minus_low_WL_bp=diff.mean() * 1e4, t=t, days=len(diff)).to_csv(os.path.join(TB, "p0_04e_volume.csv"))
# raw (not relative) version: panel-level volume shock vs next-day panel return, descriptive
ew = R.mean(axis=1); evs = shock.mean(axis=1)
d = pd.DataFrame({"ew": ew, "ewn": ew.shift(-1), "vs": evs}).dropna()
d["big"] = d.vs > d.vs.quantile(2 / 3)
for b in [False, True]:
    s = d[d.big == b]; print("panel", "high-vol-shock" if b else "other", "corr(ew_t, ew_t+1)", round(s.ew.corr(s.ewn), 3), "n", len(s))
fig, ax = plt.subplots(figsize=(7, 3.6))
x = np.arange(3); w = .38
ax.bar(x - w / 2, tab["win"].reindex(["low", "mid", "high"]).values, w, color=PAL[0], label="today's winners")
ax.bar(x + w / 2, tab["lose"].reindex(["low", "mid", "high"]).values, w, color=PAL[1], label="today's losers")
ax.set_xticks(x); ax.set_xticklabels(["low", "mid", "high"]); ax.set_xlabel("volume-shock tercile (cross-section)"); ax.axhline(0, color=GRAY, lw=1)
ax.set_ylabel("next-day relative return, bp"); ax.set_title("Volume shock x winners/losers: high-low W-L diff %.0f bp, t %.1f (EXPLORE)" % (diff.mean() * 1e4, t)); ax.legend()
save(fig, "00_volume_interaction")
