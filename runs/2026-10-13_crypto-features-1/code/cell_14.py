import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_14"); S = B.S; BN = np.log(S["close"]); tr = train_mask(BN.index)
CB = venue("cell_14", "coinbase"); UB = venue("cell_14", "upbit")
cb = np.log(CB["close"].reindex(columns=COINS)); ub = np.log(UB["close"].reindex(columns=COINS))
gap = cb - BN; ug = ub - BN
F = {"cb_gap_lvl": gap - gap.shift(1).rolling(720, min_periods=360).mean(), "ub_gap_lvl": ug - ug.shift(1).rolling(720, min_periods=360).mean(),
     "cb_retdiff_3": (cb - cb.shift(3)) - (BN - BN.shift(3)), "ub_retdiff_3": (ub - ub.shift(3)) - (BN - BN.shift(3)), "ub_retdiff_6": (ub - ub.shift(6)) - (BN - BN.shift(6))}
rev1 = -(BN - BN.shift(1)); rev3 = -(BN - BN.shift(3))
rows = []; store = {}
for nm, x in F.items():
    xt = x[tr]
    res = residual_rank(xt, [rev1[tr], rev3[tr]])
    for h in (1, 6):
        for form, FF, d in (("base", xt, 0), ("delay1", xt, 1), ("delay1+resid", res, 1)):
            ic = xs_ic(FF, B.R[h].shift(-d)[tr], min_n=5); store[(nm, form, h)] = ic
            rep = slice_report(ic, h + 6)
            rows.append(dict(feat=nm, form=form, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" if rep[k]["n"] > 30 else "n/a" for k in rep},
                             tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], c2=rep["C2"]["mean"], c3=rep["C3"]["mean"], n=rep["TRAIN"]["n"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_14_table.csv", index=False)
print(T.drop(columns=["tr", "t", "c2", "c3", "n"]).to_string(index=False))
print("\nshare of base IC kept (TRAIN):")
for nm in F:
    for h in (1, 6):
        b0 = T[(T.feat == nm) & (T.form == "base") & (T.h == h)].tr.iloc[0]
        print(nm, h, {f: round(T[(T.feat == nm) & (T.form == f) & (T.h == h)].tr.iloc[0] / b0, 2) for f in ("delay1", "delay1+resid")})
c = T[T.form == "delay1+resid"]; b = c.sort_values("tr", ascending=False).iloc[0]; tc = kit.tcrit_for(10)
print("\nBEST form (c):", b.feat, b.h, round(b.tr, 4), round(b.t, 2), "C2", round(b.c2, 4), "C3", round(b.c3, 4), "tcrit", round(tc, 2))
print("supported:", bool(b.tr >= .02 and b.t >= tc and b.c2 > 0 and b.c3 > 0), " refuted:", bool((c.tr <= 0.01).all()))
fig, ax = plt.subplots(figsize=(10, 4))
piv = T.pivot_table(index=["feat", "form"], columns="h", values="tr"); piv.plot.barh(ax=ax); ax.axvline(0.02, color="#e34948", ls="--", lw=.8); ax.set_title("H6 venue features: base vs delay vs delay+residual; red = min_useful")
fig.savefig("plots/cell_14_h6_controls.png", bbox_inches="tight")
