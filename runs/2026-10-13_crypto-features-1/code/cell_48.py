import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code"); sys.path.insert(0, r"C:\Users\User\eda-routine")
from fx import *
import importlib
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_48"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
L = make_long(B, None)
f1 = unstack_feature(importlib.import_module("features.f001").compute(L), ix); f2 = unstack_feature(importlib.import_module("features.f002").compute(L), ix)
r = lr.diff(); mk = r.mean(axis=1)
b_mkt = r.rolling(720, min_periods=360).cov(mk).div(mk.rolling(720, min_periods=360).var(), axis=0).shift(1)
# market-residual 3h reversal, lag 1: -(r_i - beta_i * m) over bars t-3..t-1
r3_i = lr.shift(1) - lr.shift(4); r3_m = r3_i.mean(axis=1)
mres = -(r3_i.sub(b_mkt.mul(r3_m, axis=0)))
rows = []
for k in (1, 3, 6):
    mkk = (lr - lr.shift(k)).mean(axis=1); up = (mkk > 0)
    bup = (-b_mkt).shift(1).where(up.shift(1).fillna(False).values[:, None]) if False else None
    # lagged feature: stamped at t, built from information at t-1 (bar t-1 end): -beta(t-1) if market return over the k hours ending t-1 is > 0
    upl = up.shift(1).fillna(False).astype(bool)
    bupk = (-b_mkt.shift(1)).mul(np.where(upl.values, 1.0, np.nan), axis=0)
    xt = bupk[tr]
    res = residual_rank(xt, [f1[tr], mres[tr]])
    for h in (1, 6):
        for form, FF in (("raw", xt), ("resid(f001,mres)", res)):
            ic = xs_ic(FF, B.R[h][tr]); rep = slice_report(ic, h + 5)
            rows.append(dict(k=k, form=form, h=h, **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}, sc=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], c2=rep["C2"]["mean"], c3=rep["C3"]["mean"], n=rep["TRAIN"]["n"]))
    print(f"k={k}: mean XS corr of bup with f001 {float(xs_ic(xt, f1[tr]).mean()):+.3f}, f002 {float(xs_ic(xt, f2[tr]).mean()):+.3f}, mres {float(xs_ic(xt, mres[tr]).mean()):+.3f}")
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_48_table.csv", index=False)
print(T.drop(columns=["sc", "t", "c2", "c3"]).to_string(index=False))
tc = kit.tcrit_for(6); c = T[(T.form != "raw") & (T.h == 6)]; b = c.sort_values("sc", ascending=False).iloc[0]
print("\nPRIMARY residual h6:", c[["k", "sc", "t"]].round(4).values.tolist(), "best k", b.k, round(b.sc, 4), round(b.t, 2), "C2", round(b.c2, 4), "C3", round(b.c3, 4), "tcrit", round(tc, 2))
print("supported:", bool(b.sc >= .015 and b.t >= tc and b.c2 > 0 and b.c3 > 0), " refuted:", bool((c.sc < .01).all()))
fig, ax = plt.subplots(figsize=(9, 4)); piv = T.pivot_table(index=["k", "form"], columns="h", values="sc"); piv.plot.barh(ax=ax); ax.axvline(0.015, color="#e34948", ls="--", lw=.8); ax.set_title("UP-state -beta feature: raw vs residual on f001 and market-residual reversal")
fig.savefig("plots/cell_48_bup.png", bbox_inches="tight")
