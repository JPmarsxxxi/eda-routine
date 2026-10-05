import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build, COINS
from guarded_load import load
from plotstyle import plt, save, PAL, DIV
from matplotlib.colors import LinearSegmentedColormap
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("EXPLORE", "p0_04"); r = P["r"]
C = r.corr(min_periods=2000); C.round(3).to_csv(os.path.join(TB, "p0_04_corr.csv"))
iu = np.triu_indices(10, 1); pairs = [(C.index[i], C.columns[j], C.values[i, j]) for i, j in zip(*iu)]
print(C.round(2).to_string()); print("max pair", max(pairs, key=lambda x: x[2]), "median", np.median([p[2] for p in pairs]))
rows = []
for c in COINS:
    d = pd.DataFrame({k: np.log(P[k][c].where(P[k][c] > 0)).diff() for k in ["vol", "quote_vol", "n"]}).dropna()
    cc = d.corr()
    lv = np.log(P["vol"][c].where(P["vol"][c] > 0)); det = lv - lv.rolling(720, min_periods=240).median()
    sp = pd.concat([r[c].abs(), det], axis=1).dropna().corr(method="spearman").iloc[0, 1]
    rows.append(dict(coin=c, corr_dvol_dquotevol=cc.loc["vol", "quote_vol"], corr_dvol_dn=cc.loc["vol", "n"],
                     spearman_absr_detrended_logvol=sp))
W = pd.DataFrame(rows).set_index("coin"); W["twin_vol_quotevol"] = W.corr_dvol_dquotevol > .95; W["vol_is_vol_proxy"] = W.spearman_absr_detrended_logvol > .5
W.round(3).to_csv(os.path.join(TB, "p0_04_within.csv")); print(W.round(3).to_string())
# venue twin: coinbase BTC
cb = load("spot/coinbase_BTCUSD.parquet", "p0_04", "EXPLORE", columns=["close"]).set_index("t")["close"]
cb = cb.reindex(r.index); rcb = np.log(cb).diff()
vt = pd.concat([r["BTCUSD"], rcb], axis=1).dropna().corr().iloc[0, 1]
print("binance vs coinbase BTC 1h return corr", round(vt, 4), "n", pd.concat([r["BTCUSD"], rcb], axis=1).dropna().shape[0])
pd.Series({"binance_vs_coinbase_BTC_1h_corr": vt}).to_csv(os.path.join(TB, "p0_04_venue.csv"))
fig, ax = plt.subplots(figsize=(6.4, 5.4))
cm = LinearSegmentedColormap.from_list("div", DIV)
im = ax.imshow(C.values, cmap=cm, vmin=-1, vmax=1); ax.grid(False)
ax.set_xticks(range(10)); ax.set_xticklabels([c[:-3] for c in C.columns], rotation=45); ax.set_yticks(range(10)); ax.set_yticklabels([c[:-3] for c in C.index])
for i in range(10):
    for j in range(10): ax.text(j, i, f"{C.values[i,j]:.2f}", ha="center", va="center", fontsize=7)
ax.set_title("No twin coins: 1h return correlations %.2f-%.2f, none > 0.95 (EXPLORE)" % (min(p[2] for p in pairs), max(p[2] for p in pairs)))
fig.colorbar(im, ax=ax, shrink=.7); save(fig, "00_crosscorr")
