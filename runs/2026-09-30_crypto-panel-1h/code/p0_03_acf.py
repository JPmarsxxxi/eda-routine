import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build, COINS
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("EXPLORE", "p0_03"); r = P["r"]
LAGS = [1, 2, 3, 6, 12, 24, 48, 168]
rel = r.sub(r.mean(axis=1), axis=0); rel[r.notna().sum(axis=1) < 4] = np.nan   # relative to panel (>=4 coins live)
lv = np.log(P["vol"].where(P["vol"] > 0))
series = {"r": r, "absr": r.abs(), "logvol": lv, "rel": rel}
def acf(s, k):
    x, y = s, s.shift(k); m = x.notna() & y.notna(); n = int(m.sum())
    return (np.corrcoef(x[m], y[m])[0, 1] if n > 30 else np.nan), n
rows = []
for name, S in series.items():
    for c in COINS:
        for k in LAGS:
            a, n = acf(S[c], k); rows.append(dict(series=name, coin=c, lag=k, acf=a, n=n, sig=abs(a) > 2 / np.sqrt(n)))
A = pd.DataFrame(rows)
A.to_csv(os.path.join(TB, "p0_03_acf.csv"), index=False)
summ = A.groupby(["series", "lag"]).apply(lambda g: pd.Series(dict(median_acf=g.acf.median(), n_sig_pos=int(((g.acf > 0) & g.sig).sum()), n_sig_neg=int(((g.acf < 0) & g.sig).sum()))), include_groups=False)
summ["panel_fact"] = np.where(summ.n_sig_pos >= 7, "+", np.where(summ.n_sig_neg >= 7, "-", ""))
print(summ.round(4).to_string())
# variance ratios on r and rel
vr = []
for name in ["r", "rel"]:
    S = series[name]
    for c in COINS:
        x = S[c]; v1 = x.var()
        for q in [2, 6, 24, 72, 168]:
            xs = x.rolling(q, min_periods=q).sum().dropna(); n = x.count()
            V = xs.var() / (q * v1); se = np.sqrt(2 * (2 * q - 1) * (q - 1) / (3 * q * n))
            vr.append(dict(series=name, coin=c, q=q, VR=V, se=se, sig=abs(V - 1) > 2 * se))
VR = pd.DataFrame(vr); VR.to_csv(os.path.join(TB, "p0_03_vr.csv"), index=False)
vs = VR.groupby(["series", "q"]).apply(lambda g: pd.Series(dict(median_VR=g.VR.median(), n_sig_above=int(((g.VR > 1) & g.sig).sum()), n_sig_below=int(((g.VR < 1) & g.sig).sum()))), include_groups=False)
print(vs.round(3).to_string())
print(VR.pivot_table(index="coin", columns=["series", "q"], values="VR").round(2).to_string())
# Roll
roll = []
for c in COINS:
    cl = P["close"][c]; dp = cl.diff(); cov = (dp * dp.shift(1)).mean() - dp.mean() ** 2
    half = np.sqrt(-cov) / cl.mean() * 1e4 if cov < 0 else np.nan
    # scale-free version on log returns
    rr = r[c]; covr = rr.cov(rr.shift(1)); half_r = np.sqrt(-covr) * 1e4 if covr < 0 else np.nan
    roll.append(dict(coin=c, roll_half_bp_logret=half_r, med_absr_bp=r[c].abs().median() * 1e4))
R = pd.DataFrame(roll).set_index("coin"); R["ratio"] = R.roll_half_bp_logret / R.med_absr_bp; R["material"] = R.ratio > 0.25
R.to_csv(os.path.join(TB, "p0_03_roll.csv")); print(R.round(3).to_string())
fig, ax = plt.subplots(figsize=(8.5, 4))
for i, name in enumerate(["r", "rel", "absr"]):
    m = A[A.series == name].groupby("lag").acf.median()
    ax.plot(range(len(LAGS)), m.values, marker="o", color=PAL[i], label={"r": "1h return", "rel": "return minus panel mean", "absr": "|return|"}[name])
ax.axhline(0, color=GRAY, lw=1)
ax.set_xticks(range(len(LAGS))); ax.set_xticklabels(LAGS); ax.set_xlabel("lag (hours)"); ax.set_ylabel("median ACF across 10 coins")
ax.set_title("|r| clusters for a week; raw and relative 1h returns are near zero after lag 1 (EXPLORE)"); ax.legend()
save(fig, "00_acf")
