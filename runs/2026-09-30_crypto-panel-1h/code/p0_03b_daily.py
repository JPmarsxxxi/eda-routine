import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build, COINS
from daily import daily
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("EXPLORE", "p0_03b"); R, REL, V, QV = daily(P)
rows = []
for name, S in [("raw", R), ("rel", REL)]:
    for c in COINS:
        for k in [1, 2, 3, 7]:
            x, y = S[c], S[c].shift(k); m = x.notna() & y.notna(); n = int(m.sum())
            a = np.corrcoef(x[m], y[m])[0, 1]; rows.append(dict(series=name, coin=c, lag=k, acf=a, n=n, sig=abs(a) > 2 / np.sqrt(n)))
A = pd.DataFrame(rows); A.to_csv(os.path.join(TB, "p0_03b_daily.csv"), index=False)
s = A.groupby(["series", "lag"]).apply(lambda g: pd.Series(dict(median=g.acf.median(), sig_pos=int(((g.acf > 0) & g.sig).sum()), sig_neg=int(((g.acf < 0) & g.sig).sum()), n_med=g.n.median())), include_groups=False)
print(s.round(4).to_string())
# quintile sort, per day
nxt = REL.shift(-1); q = REL.rank(axis=1, pct=True)
qb = np.ceil(q * 5).clip(1, 5)
res = {k: nxt.where(qb == k).mean(axis=1) for k in range(1, 6)}
Q = pd.DataFrame(res).dropna(); spread = Q[5] - Q[1]
t = spread.mean() / spread.std() * np.sqrt(len(spread))
from scipy.stats import spearmanr
rho = spearmanr(range(1, 6), Q.mean().values).statistic
print("quintile mean next-day rel ret (bp):", (Q.mean() * 1e4).round(1).to_dict(), "rho", round(rho, 2), "Q5-Q1 bp", round(spread.mean() * 1e4, 1), "t", round(t, 2), "days", len(Q))
pd.DataFrame({"q_mean_next_rel_bp": Q.mean() * 1e4}).assign(rho=rho, q5_q1_bp=spread.mean() * 1e4, t=t, days=len(Q)).to_csv(os.path.join(TB, "p0_03b_quintiles.csv"))
# by era
for a, b in [("2017", "2018"), ("2019", "2019"), ("2020", "2020"), ("2021", "2021")]:
    sp = spread.loc[a:b]; print("era", a, b, "Q5-Q1 bp", round(sp.mean() * 1e4, 1), "t", round(sp.mean() / sp.std() * np.sqrt(len(sp)), 2), len(sp))
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.bar([f"Q{k}" for k in range(1, 6)], Q.mean().values * 1e4, color=PAL[0]); ax.axhline(0, color=GRAY, lw=1)
ax.set_xlabel("today's return relative to panel, quintile (Q5 = best)"); ax.set_ylabel("next-day relative return, bp")
ax.set_title("Daily cross-section: next-day relative return by today's quintile, Q5-Q1 %.0f bp, t %.1f (EXPLORE)" % (spread.mean() * 1e4, t))
save(fig, "00_daily_acf")
