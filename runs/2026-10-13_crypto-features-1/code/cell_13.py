import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_13"); S = B.S; BN = np.log(S["close"])
CB = venue("cell_13", "coinbase"); UB = venue("cell_13", "upbit")
cb = np.log(CB["close"].reindex(columns=COINS)); ub = np.log(UB["close"].reindex(columns=COINS))
F = {}
gap = cb - BN
F["cb_gap_lvl"] = gap - gap.shift(1).rolling(720, min_periods=360).mean()
for k in (1, 3, 6):
    F[f"cb_gap_chg_{k}"] = gap - gap.shift(k)
    F[f"cb_retdiff_{k}"] = (cb - cb.shift(k)) - (BN - BN.shift(k))
ug = ub - BN
F["ub_gap_lvl"] = ug - ug.shift(1).rolling(720, min_periods=360).mean()
for k in (1, 3, 6):
    F[f"ub_retdiff_{k}"] = (ub - ub.shift(k)) - (BN - BN.shift(k))
rows = []; ics = {}
for name, Fx in F.items():
    for h in HORIZONS:
        ic = xs_ic(Fx, B.R[h], min_n=5); ics[(name, h)] = ic
        rep = slice_report(ic, h + 5)
        rows.append(dict(variant=name, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" if rep[k]["n"] > 30 else "n/a" for k in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], n=rep["TRAIN"]["n"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_13_table.csv", index=False)
print(T.drop(columns=["tr", "t"]).to_string(index=False))
tc = kit.tcrit_for(33)
b = T.sort_values("tr", ascending=False).iloc[0]
print("\nbest:", b.variant, b.h, round(b.tr, 4), round(b.t, 2), "n", b.n, "tcrit", round(tc, 2), " supported:", bool(b.tr >= .02 and b.t >= tc))
print("largest |IC|:"); print(T.assign(a=T.tr.abs()).sort_values("a", ascending=False).head(6)[["variant", "h", "tr", "t", "n"]].round(4).to_string(index=False))
print("\nmean coins per hour: coinbase", round(float(cb.notna().sum(axis=1)[train_mask(cb.index)].mean()), 1), " upbit", round(float(ub.notna().sum(axis=1)[train_mask(ub.index)].mean()), 1))
print("std of cb-bn log gap (bp, TRAIN, detrended pooled):", round(float((F['cb_gap_lvl'][train_mask(cb.index)]).stack().std() * 1e4), 1), " ub:", round(float((F['ub_gap_lvl'][train_mask(ub.index)]).stack().std() * 1e4), 1))
fig, ax = plt.subplots(figsize=(10, 4))
piv = T.pivot(index="variant", columns="h", values="tr"); piv.plot.barh(ax=ax); ax.axvline(0.02, color="#e34948", ls="--", lw=.8); ax.axvline(-0.02, color="#e34948", ls="--", lw=.8); ax.set_title("H6 venue features, pooled TRAIN IC")
fig.savefig("plots/cell_13_venue.png", bbox_inches="tight")
