import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from scipy import stats
from panel import build, COINS
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("EXPLORE", "p0_05"); r = P["r"]
rel = r.sub(r.mean(axis=1), axis=0); rel[r.notna().sum(axis=1) < 4] = np.nan
ERAS = {"2017H2-2018": ("2017-08-01", "2019-01-01"), "2019": ("2019-01-01", "2020-01-01"), "2020": ("2020-01-01", "2021-01-01"), "2021H1": ("2021-01-01", "2021-07-01")}
def ac(x, k):
    m = x.notna() & x.shift(k).notna(); return np.corrcoef(x[m], x.shift(k)[m])[0, 1] if m.sum() > 200 else np.nan
rows = []
for e, (a, b) in ERAS.items():
    R = r.loc[a:b].iloc[:-1] if b <= "2021-07-01" else r.loc[a:b]
    RL = rel.loc[R.index]
    live = [c for c in COINS if R[c].count() > 2000]
    C = R[live].corr(); iu = np.triu_indices(len(live), 1)
    lv = np.log(P["vol"].loc[R.index].where(P["vol"].loc[R.index] > 0))
    per = []
    for c in live:
        x = R[c].dropna(); xs = R[c].rolling(24, min_periods=24).sum()
        per.append(dict(sd_bp=x.std() * 1e4, exkurt=stats.kurtosis(x), acf1=ac(R[c], 1), acf24=ac(R[c], 24),
                        vr24=xs.var() / (24 * x.var()), rel_acf1=ac(RL[c], 1), rel_acf24=ac(RL[c], 24),
                        absr_acf24=ac(R[c].abs(), 24), logvol_acf24=ac(lv[c], 24)))
    d = pd.DataFrame(per).median(); d["avg_crosscorr"] = C.values[iu].mean() if len(live) > 1 else np.nan
    d["n_coins"] = len(live); d.name = e; rows.append(d)
T = pd.DataFrame(rows); T.round(4).to_csv(os.path.join(TB, "p0_05_regimes.csv")); print(T.round(3).to_string())
flags = []
for s in T.columns:
    if s == "n_coins": continue
    for i in range(len(T) - 1):
        a, b = T[s].iloc[i], T[s].iloc[i + 1]
        if s in ("sd_bp", "exkurt"): hit = max(a, b) / min(a, b) > 2 if min(a, b) > 0 else False
        else: hit = abs(b - a) > .15
        if hit: flags.append((s, T.index[i], T.index[i + 1], round(a, 3), round(b, 3)))
print("STRUCTURAL CHANGES:", flags)
# OLS-CUSUM on equal-weight |r| (demeaned), 5% band 1.358*sigma*sqrt(n)
ew = r.abs().mean(axis=1).dropna(); e = ew - ew.mean(); cs = e.cumsum() / (ew.std() * np.sqrt(len(ew)))
brk = cs.abs().idxmax(); print("CUSUM max |stat|", round(cs.abs().max(), 2), "at", brk, "band 1.358")
pd.DataFrame(flags, columns=["stat", "from", "to", "a", "b"]).to_csv(os.path.join(TB, "p0_05_breaks.csv"), index=False)
fig, ax = plt.subplots(figsize=(8.5, 3.8))
ax.plot(cs.index, cs.values, color=PAL[0], label="OLS-CUSUM of panel mean |r|")
ax.axhline(1.358, color=GRAY, ls="--", label="5% band"); ax.axhline(-1.358, color=GRAY, ls="--")
ax.set_title("Panel volatility level shifts: CUSUM peaks %.1f (band 1.36) at %s (EXPLORE)" % (cs.abs().max(), brk.date())); ax.legend()
save(fig, "00_regimes")
