import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_01")
Dd = B.D
v = {
 "seed_daily":      (to_hourly(a30_daily(Dd, 3, 5, 20, True), B.P.index), "d"),
 "streak_daily":    (to_hourly(a30_daily(Dd, 3, 5, 20, False), B.P.index), "d"),
 "seed_roll24":     (a30_roll(B.S, 3, 5, 20, True), "h"),
 "streak_roll24":   (a30_roll(B.S, 3, 5, 20, False), "h"),
}
df, ics = sweep(v, B)
print(show(df)); df.to_csv("cells/cell_01_table.csv", index=False)
vd = verdict(df, 0.02, +1.0, V=12); print(vd)
print("market corr (seed_roll24, h24):", mkt_corr(v["seed_roll24"][0], B, 24, "h"), " daily:", mkt_corr(v["seed_daily"][0], B, 24, "d"))
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
for i, nm in enumerate(["seed_daily", "seed_roll24"]):
    ic = ics[(nm, 24)]; s = ic.dropna().rolling(90 if nm == "seed_daily" else 24*60).mean()
    ax[i].plot(s.index, s.values); ax[i].axhline(0, color="#9b9a94", lw=.8); ax[i].set_title(f"{nm}: rolling mean rank IC, h=24")
fig.savefig("plots/cell_01_seed30_ic.png", bbox_inches="tight")
