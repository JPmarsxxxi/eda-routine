import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_05"); C = B.S["close"]
lr = np.log(C)
ret1 = lr.diff()
mkt1 = ret1.mean(axis=1)
beta = ret1.rolling(720, min_periods=360).cov(mkt1).div(mkt1.rolling(720, min_periods=360).var(), axis=0)
sig = ret1.rolling(168, min_periods=84).std()
KS = (1, 2, 3, 6, 12, 24, 48, 72, 168)
V = {}
for k in KS:
    rk = -(lr - lr.shift(k))
    mk = -(lr - lr.shift(k)).mean(axis=1)  # -(EW-market k-hour return) = market part in the same (reversal) sign
    res = rk - beta.mul(mk, axis=0)
    V[f"k{k}_raw"] = (rk, "h"); V[f"k{k}_vs"] = (rk / sig, "h"); V[f"k{k}_mres"] = (res, "h"); V[f"k{k}_mres_vs"] = (res / sig, "h")
df, ics = sweep(V, B)
df.to_csv("cells/cell_05_table.csv", index=False)
pd.set_option("display.width", 250)
for h in HORIZONS:
    sub = df[df.h == h].copy()
    sub["tf"] = sub.variant.str.split("_", n=1).str[1]; sub["k"] = sub.variant.str.extract(r"k(\d+)")[0].astype(int)
    print(f"\nh={h}: TRAIN IC (t) by lookback k (rows) x transform (cols)")
    print(sub.pivot(index="k", columns="tf", values="TRAIN_ic").round(4).join(sub.pivot(index="k", columns="tf", values="TRAIN_t").round(1).add_prefix("t_")).to_string())
vd = verdict(df, 0.02, +1.0, V=108); print(vd)
best = df.sort_values("TRAIN_ic", ascending=False).head(12); print(show(best))
print("\nper-slice IC for the best raw/vs/mres_vs variants at each horizon:")
for h in HORIZONS:
    for tf in ("raw", "vs", "mres", "mres_vs"):
        s = df[(df.h == h) & df.variant.str.endswith("_" + tf)].sort_values("TRAIN_ic", ascending=False).iloc[0]
        print(h, tf, s.variant, " ".join(f"{n}:{s[n+'_ic']:+.4f}({s[n+'_t']:+.1f})" for n in ("EXPLORE", "C1", "C2", "C3", "TRAIN")))
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
for i, h in enumerate(HORIZONS):
    for j, tf in enumerate(("raw", "vs", "mres", "mres_vs")):
        s = df[(df.h == h) & df.variant.str.endswith("_" + tf)]; s = s.assign(k=s.variant.str.extract(r"k(\d+)")[0].astype(int)).sort_values("k")
        ax[i].plot(range(len(s)), s.TRAIN_ic.values, marker="o", label=tf)
    ax[i].set_xticks(range(len(KS))); ax[i].set_xticklabels(KS); ax[i].axhline(0, color="#9b9a94", lw=.8); ax[i].set_title(f"reversal IC vs lookback k, h={h}")
ax[0].legend(); fig.savefig("plots/cell_05_reversal_profile.png", bbox_inches="tight")
