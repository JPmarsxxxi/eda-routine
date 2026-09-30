import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from scipy import stats
from panel import build, COINS
from plotstyle import plt, save, PAL, GRAY
P = build("EXPLORE", "p0_01")
rows = []
for c in COINS:
    r = P["r"][c].dropna(); a = r.abs().sort_values(ascending=False)
    k = max(int(0.01 * len(a)), 10); top = a.iloc[:k + 1].values
    hill = 1.0 / np.mean(np.log(top[:k] / top[k]))
    v = P["vol"][c].dropna(); n = P["n"][c].dropna()
    bs = (P["buy_vol"][c] / P["vol"][c]).replace([np.inf, -np.inf], np.nan).dropna()
    lv = np.log(v[v > 0]); ln = np.log(n[n > 0])
    rows.append(dict(coin=c, n_r=len(r), mean_bp=r.mean() * 1e4, sd_bp=r.std() * 1e4, skew=stats.skew(r),
                     exkurt=stats.kurtosis(r), hill_top1pct=hill, zero_r_pct=100 * (r == 0).mean(),
                     zero_vol_pct=100 * (v == 0).mean(), med_absr_bp=r.abs().median() * 1e4,
                     logvol_med=lv.median(), logvol_iqr=lv.quantile(.75) - lv.quantile(.25),
                     logn_iqr=ln.quantile(.75) - ln.quantile(.25),
                     buyshare_med=bs.median(), buyshare_iqr=bs.quantile(.75) - bs.quantile(.25)))
T = pd.DataFrame(rows).set_index("coin")
T["fat_tailed"] = (T.exkurt > 3) & (T.hill_top1pct < 4)
T["zero_r_material"] = T.zero_r_pct > 1; T["zero_vol_material"] = T.zero_vol_pct > 0.5
T.round(4).to_csv(os.path.join(os.path.dirname(__file__), "..", "tables", "p0_01_distributions.csv"))
print(T.round(3).to_string())
# plot: standardized return density vs normal on log y for 4 coins
fig, ax = plt.subplots(figsize=(8, 4))
bins = np.linspace(-10, 10, 161)
for i, c in enumerate(["BTCUSD", "ETHUSD", "DOGEUSD", "DOTUSD"]):
    r = P["r"][c].dropna(); z = (r - r.mean()) / r.std()
    h, e = np.histogram(z, bins=bins, density=True); ax.semilogy((e[1:] + e[:-1]) / 2, h, color=PAL[i], label=c)
x = (bins[1:] + bins[:-1]) / 2; ax.semilogy(x, stats.norm.pdf(x), color=GRAY, ls="--", label="normal")
ax.set_ylim(1e-6, 1); ax.set_xlabel("1h log return, standardized"); ax.set_ylabel("density (log)")
ax.set_title(f"1h returns are fat-tailed in all 10 coins: excess kurtosis {T.exkurt.min():.0f}-{T.exkurt.max():.0f} (EXPLORE)")
ax.legend(); save(fig, "00_distributions")
