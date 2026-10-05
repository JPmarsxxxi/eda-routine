import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build, COINS
from daily import daily
from tests import fm_interaction
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("CONFIRM", "cell_04"); R, REL, V, QV = daily(P)
shock = np.log(V / V.shift(1).rolling(30, min_periods=20).median())
Y = REL.shift(-1)
b3, se, z, n = fm_interaction(Y, REL, shock, min_n=8)
rk = lambda X: X.rank(axis=1)
b3r, ser, zr, _ = fm_interaction(Y, rk(REL.where(shock.notna())), rk(shock.where(REL.notna())), min_n=8)
branch = "inconclusive" if n < 400 or (z > 1.645 and zr < -1.645) else ("supported" if z > 1.645 else "refuted")
print(f"PRIMARY b3 {b3*1e4:.1f} bp se {se*1e4:.1f} z {z:.2f} days {n} | rank version z {zr:.2f} -> {branch}")
# descriptive: full coefficients
coefs = []
for t in Y.index:
    y, a, b = Y.loc[t], REL.loc[t], shock.loc[t]; m = y.notna() & a.notna() & b.notna()
    if m.sum() < 8: continue
    za = (a[m] - a[m].mean()) / a[m].std(); zb = (b[m] - b[m].mean()) / b[m].std()
    X = np.column_stack([np.ones(m.sum()), za, zb, za * zb]); coefs.append(pd.Series(np.linalg.lstsq(X, y[m].values, rcond=None)[0], index=["b0", "b1_rel", "b2_shock", "b3_int"], name=t))
Cf = pd.DataFrame(coefs) * 1e4
mid = pd.Timestamp("2022-05-14", tz="UTC")
D = pd.DataFrame({"all": Cf.mean(), "half1": Cf[Cf.index < mid].mean(), "half2": Cf[Cf.index >= mid].mean(), "t_all": Cf.mean() / Cf.std() * np.sqrt(len(Cf))})
print(D.round(2).to_string())
ok = REL.notna() & shock.notna() & Y.notna(); ter = np.ceil(shock.where(ok).rank(axis=1, pct=True) * 3).clip(1, 3); win = REL > 0
tab = pd.DataFrame({(t, s): [Y.where(ok & (ter == k) & m).stack().mean() * 1e4] for t, k in [("low", 1), ("mid", 2), ("high", 3)] for s, m in [("win", win), ("lose", ~win)]})
print(tab.round(1).to_string())
D.to_csv(os.path.join(TB, "cell_04_h4.csv")); pd.Series(dict(b3_bp=b3 * 1e4, se_bp=se * 1e4, z=z, days=n, rank_z=zr, branch=branch)).to_csv(os.path.join(TB, "cell_04_h4_primary.csv"))
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.bar(["b1 rel", "b2 shock", "b3 rel x shock"], [D.loc["b1_rel", "all"], D.loc["b2_shock", "all"], D.loc["b3_int", "all"]], color=[GRAY, GRAY, PAL[0]])
ax.errorbar(range(3), [D.loc[k, "all"] for k in ["b1_rel", "b2_shock", "b3_int"]], yerr=[1.645 * D.loc[k, "all"] / D.loc[k, "t_all"] for k in ["b1_rel", "b2_shock", "b3_int"]], fmt="none", ecolor="#52514e")
ax.axhline(0, color=GRAY, lw=1); ax.axhline(28, color=PAL[7], ls="--", lw=1, label="smallest meaningful b3 = 28 bp")
ax.set_ylabel("next-day relative return, bp per 1 sd"); ax.legend()
ax.set_title(f"H4 on CONFIRM: interaction b3 {b3*1e4:.1f} bp (z {z:.2f}) -> {branch}")
save(fig, "cell_04_h4_fm")
