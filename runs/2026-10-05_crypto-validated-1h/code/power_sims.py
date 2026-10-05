"""Power simulations, run BEFORE any CONFIRM fold is opened. Inputs: EXPLORE statistics only (already seen; birth slice)
and each fold's sample size from coverage/new_source flags only (no fold return is computed here)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from hyp import *
rng = np.random.default_rng(20261005)
NSIM = 20000
CELL = "power_sims"
H = hourly(CELL)
D = daily(H)
# ---- fold sample sizes from validity flags only: a window is valid iff its daily r24 entries are non-NaN; r24 validity is
# decided by new_source/holes. We count VALID WINDOWS using notna() only (values are never read).
valid1 = D["r24"].notna()
def n_blocks(slice_name, h, need=5):
    v = sum(valid1.shift(-k).fillna(False).astype(bool).astype(int) for k in range(1, h + 1)) == h  # all h days valid
    m = in_slice(v.index, slice_name, h)
    v = v[m]
    cnt = v.sum(1)
    if h == 3:
        cnt = cnt.iloc[::3]
    return int((cnt >= need).sum()), sorted(v.columns[v.any()].tolist())
sizes = {}
for s in ["C1", "C2", "C3", "VAL"]:
    sizes[(s, 3)] = n_blocks(s, 3); sizes[(s, 1)] = n_blocks(s, 1)
    print(s, "72h blocks:", sizes[(s, 3)][0], "| 24h days:", sizes[(s, 1)][0], "| coins:", [c[:-3] for c in sizes[(s, 3)][1]])
rows = []
# ---- H1: bootstrap EXPLORE block spreads (de-meaned), shift to -T (true) or 0 (null)
B, _ = h1_blocks(CELL, "EXPLORE", D)
e = B.spread.dropna().values; e = e - e.mean()
print("EXPLORE H1 block spread sd (bp):", e.std() * 1e4, "n", len(e))
for s in ["C1", "C2", "C3", "VAL"]:
    n, coins = sizes[(s, 3)]
    T = h1_threshold(coins) / 1e4
    for truth, mu in (("true", -T), ("null", 0.0)):
        x = rng.choice(e, size=(NSIM, n)) + mu
        m, sd = x.mean(1), x.std(1, ddof=1); t = m / sd * np.sqrt(n)
        sup = ((t <= -Z) & (m <= -T)).mean(); inc = ((t <= -Z) & (m > -T)).mean(); ref = (t > -Z).mean()
        rows.append(dict(hyp="H1", slice=s, n=n, T_bp=T * 1e4, truth=truth, p_sup=sup, p_inc=inc, p_ref=ref))
# ---- H2 / H3: bootstrap EXPLORE panel daily returns (de-meaned), random tercile labels, add +T/2 top, -T/2 bottom
z0 = ts_daily(CELL, pd.Series(0.0, index=D["r24"].index), "EXPLORE", D)
r = z0.r.values - z0.r.mean()
print("EXPLORE panel daily sd (bp):", r.std() * 1e4, "n", len(r))
for hyp, frac in (("H2", 1.0), ("H3", 250 / 365)):  # H3 feature exists on equity-session days only
    for s in ["C1", "C2", "C3", "VAL"]:
        n0, coins = sizes[(s, 1)]
        n = int(round(n0 * frac)); T = ts_threshold(coins) / 1e4
        nt = n // 3
        for truth, eff in (("true", T), ("null", 0.0)):
            top = rng.choice(r, size=(NSIM, nt)) + eff / 2; bot = rng.choice(r, size=(NSIM, nt)) - eff / 2
            sp = top.mean(1) - bot.mean(1); se = np.sqrt(top.var(1, ddof=1) / nt + bot.var(1, ddof=1) / nt); t = sp / se
            sup = ((t >= Z) & (sp >= T)).mean(); inc = ((t >= Z) & (sp < T)).mean(); ref = (t < Z).mean()
            rows.append(dict(hyp=hyp, slice=s, n=n, T_bp=T * 1e4, truth=truth, p_sup=sup, p_inc=inc, p_ref=ref))
P = pd.DataFrame(rows).round(4)
P.to_csv(os.path.join(RUN, "tables", "power.csv"), index=False)
print(P.to_string())
