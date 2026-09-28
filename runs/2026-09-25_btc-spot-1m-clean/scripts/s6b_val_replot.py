"""Re-draw plot 24 from tables/24_val_results.json (layout fix only; VAL data NOT re-read)."""
from lib import *
res = json.load(open(os.path.join(RUN, "tables", "24_val_results.json")))
train = {"L1": (0.407, 0.347, 0.467), "L2": (-0.400, -0.497, -0.302), "L3": (-2.061, -2.416, -1.706)}
fig, ax = plt.subplots(1, 3, figsize=(13, 4.2))
for i, (k, lab) in enumerate([("L1", "h00 - h05 |r| (day-means)"), ("L2", "weekend - weekday |r| (rel.)"), ("L3", "fwd5 top-bottom tr5 (bp)")]):
    tv = train[k]; vv = res[k]
    ax[i].errorbar([0], [tv[0]], yerr=[[tv[0] - tv[1]], [tv[2] - tv[0]]], fmt="o", color=GRAY, capsize=4)
    ax[i].errorbar([1], [vv["est"]], yerr=[[vv["est"] - vv["lo"]], [vv["hi"] - vv["est"]]], fmt="o", color=PAL[i], capsize=4)
    ax[i].axhline(0, color="k", lw=0.6); ax[i].set_xticks([0, 1]); ax[i].set_xticklabels(["TRAIN", "VAL"]); ax[i].set_xlim(-0.5, 1.5)
    ax[i].set_title(f"{k}: {lab}\nVAL {vv['est']:+.2f} [{vv['lo']:+.2f},{vv['hi']:+.2f}] {vv['verdict']}", fontsize=9)
fig.suptitle("24: VAL opened once: all 3 pass their rules; L3 is 72% smaller than TRAIN (SOFT-clean VAL, different regime)", fontweight="bold", y=1.03)
save(fig, 24, "val_results")
