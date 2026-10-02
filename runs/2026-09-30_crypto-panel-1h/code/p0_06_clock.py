import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build, COINS
from plotstyle import plt, save, PAL
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("EXPLORE", "p0_06"); r = P["r"]
def norm(X):  # each coin divided by its own 30-day rolling median (trailing)
    return X / X.rolling(720, min_periods=240).median()
V = norm(P["vol"].where(P["vol"] > 0)); A = norm(r.abs().where(r.abs() > 0))
hr = r.index.hour; wd = r.index.dayofweek
out = {}
for name, X in [("vol", V), ("absr", A)]:
    out[f"{name}_by_hour"] = X.groupby(hr).mean().median(axis=1)
    out[f"{name}_by_wday"] = X.groupby(wd).mean().median(axis=1)
H = pd.DataFrame({k: v for k, v in out.items() if "hour" in k}); D = pd.DataFrame({k: v for k, v in out.items() if "wday" in k})
H.round(3).to_csv(os.path.join(TB, "p0_06_clock.csv")); D.round(3).to_csv(os.path.join(TB, "p0_06_weekday.csv"))
print(H.round(3).to_string()); print(D.round(3).to_string())
for k in H: print(k, "max/min", round(H[k].max() / H[k].min(), 2), "peak", H[k].idxmax(), "trough", H[k].idxmin())
for k in D: print(k, "max/min", round(D[k].max() / D[k].min(), 2), "peak", D[k].idxmax(), "trough", D[k].idxmin())
fig, ax = plt.subplots(figsize=(8.5, 3.8))
ax.plot(H.index, H.vol_by_hour, marker="o", color=PAL[0], label="volume / 30d median")
ax.plot(H.index, H.absr_by_hour, marker="o", color=PAL[1], label="|r| / 30d median")
ax.axhline(1, color="#9b9a94", lw=1); ax.set_xticks(range(0, 24, 2)); ax.set_xlabel("UTC hour (bar open)")
ax.set_title("Volume peaks at 16 UTC, troughs at 21 UTC (%.2fx); |r| shape is flatter (%.2fx) (EXPLORE)" % (H.vol_by_hour.max() / H.vol_by_hour.min(), H.absr_by_hour.max() / H.absr_by_hour.min())); ax.legend()
save(fig, "00_clock")
