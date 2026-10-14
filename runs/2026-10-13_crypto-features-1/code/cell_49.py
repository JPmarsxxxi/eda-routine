import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code"); sys.path.insert(0, r"C:\Users\User\eda-routine")
from fx import *
import importlib
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_49"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
L = make_long(B, None); f1 = unstack_feature(importlib.import_module("features.f001").compute(L), ix)
r = lr.diff(); mk = r.mean(axis=1)
beta = r.rolling(720, min_periods=360).cov(mk).div(mk.rolling(720, min_periods=360).var(), axis=0)
b_l = beta.shift(2)                       # beta ending at t-2 (lagged-feature convention of cell 48)
beta_dt = beta - beta.rolling(2160, min_periods=720).mean(); b_dt_l = beta_dt.shift(2)
r3_i = lr.shift(1) - lr.shift(4); r3_m = r3_i.mean(axis=1); mres = -(r3_i.sub(beta.shift(1).mul(r3_m, axis=0)))
sg = np.sign((lr - lr.shift(6)).mean(axis=1)).shift(1)
F = {"s_static": -b_l, "g_rev": (-b_l).mul(sg, axis=0), "g_rev_dt": (-b_dt_l).mul(sg, axis=0)}
rows = []
for nm, x in F.items():
    xt = x[tr]; res = residual_rank(xt, [f1[tr], mres[tr]])
    for h in (1, 6):
        for form, FF in (("raw", xt), ("resid(f001,mres)", res)):
            if nm == "s_static" and form != "raw": continue
            ic = xs_ic(FF, B.R[h][tr]); rep = slice_report(ic, h + 5)
            rows.append(dict(feat=nm, form=form, h=h, **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}, sc=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], c2=rep["C2"]["mean"], c3=rep["C3"]["mean"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_49_table.csv", index=False)
print(T.drop(columns=["sc", "t", "c2", "c3"]).to_string(index=False))
# state split of the static ranking
up = (sg > 0)
for h in (1, 6):
    ic = xs_ic((-b_l)[tr], B.R[h][tr]); print(f"static -beta IC h{h}: UP", fmt_rep({"TRAIN": nw(ic[up.reindex(ic.index).fillna(False).values], h + 5)}), " DOWN", fmt_rep({"TRAIN": nw(ic[(~up).reindex(ic.index).fillna(False).values], h + 5)}))
tc = kit.tcrit_for(2); c = T[(T.feat == "g_rev") & (T.form != "raw")]; b = c.sort_values("sc", ascending=False).iloc[0]
print("\nPRIMARY g_rev resid:", c[["h", "sc", "t"]].round(4).values.tolist(), "best h", b.h, round(b.sc, 4), round(b.t, 2), "C2", round(b.c2, 4), "C3", round(b.c3, 4), "tcrit", round(tc, 2))
print("supported:", bool(b.sc >= .015 and b.t >= tc and b.c2 > 0 and b.c3 > 0), " refuted:", bool((c.sc < .01).all()))
fig, ax = plt.subplots(figsize=(9, 4)); piv = T.pivot_table(index=["feat", "form"], columns="h", values="sc"); piv.plot.barh(ax=ax); ax.axvline(0.015, color="#e34948", ls="--", lw=.8); ax.axvline(0, color="#9b9a94"); ax.set_title("beta features: static vs reversal-only (IC)")
fig.savefig("plots/cell_49_beta.png", bbox_inches="tight")
