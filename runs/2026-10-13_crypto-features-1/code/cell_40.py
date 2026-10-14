import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code"); sys.path.insert(0, r"C:\Users\User\eda-routine")
from fx import *
import importlib
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_40"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
Fu, W = funding("cell_40"); K = perp_hourly("cell_40", "klines"); PR = perp_hourly("cell_40", "premium")
L = make_long(B, PR["close"]); f004 = unstack_feature(importlib.import_module("features.f004").compute(L), ix)
r3s = -(lr.shift(1) - lr.shift(4)); r24 = -(lr - lr.shift(24))
base = {"basis_dtr": (K["close"] / C - 1), "funding_dtr": Fu}
rows = []
for nm, x in base.items():
    dt = (x - x.shift(1).rolling(720, min_periods=360).mean())[tr]
    ra = residual_rank(dt, [r3s[tr], r24[tr]]); rc = residual_rank(dt, [r3s[tr], r24[tr], f004[tr]])
    for h in HORIZONS:
        for form, FF in (("a:rank", dt), ("b:resid(r3s,r24)", ra), ("c:resid(r3s,r24,f004)", rc)):
            ic = -xs_ic(FF, B.R[h][tr]); rep = slice_report(ic, h + 5)
            rows.append(dict(feat=nm, form=form, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" for k in rep}, sc=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], c2=rep["C2"]["mean"], c3=rep["C3"]["mean"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_40_table.csv", index=False)
print("score = -IC:"); print(T.drop(columns=["sc", "t", "c2", "c3"]).to_string(index=False))
c = T[T.form.str.startswith("c")]; b = c.sort_values("sc", ascending=False).iloc[0]; tc = kit.tcrit_for(6)
print("\nBEST form (c):", b.feat, b.h, round(b.sc, 4), round(b.t * -1, 2), "C2", round(-b.c2, 4), "C3", round(-b.c3, 4), "tcrit", round(tc, 2))
print("supported:", bool(b.sc >= .015 and -b.t >= tc and b.c2 < 0 and b.c3 < 0), " refuted:", bool((c.sc < 0.01).all()))
print("mean XS corr of basis_dtr, funding_dtr with f004:", {nm: round(float(xs_ic((x - x.shift(1).rolling(720, min_periods=360).mean())[tr], f004[tr]).mean()), 3) for nm, x in base.items()})
fig, ax = plt.subplots(figsize=(9, 4)); piv = T.pivot_table(index=["feat", "form"], columns="h", values="sc"); piv.plot.barh(ax=ax); ax.axvline(0.015, color="#e34948", ls="--", lw=.8); ax.set_title("basis / funding crowding score (-IC) by form")
fig.savefig("plots/cell_40_basis_funding.png", bbox_inches="tight")
