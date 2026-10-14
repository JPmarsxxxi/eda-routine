import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_43"); S = B.S; C = S["close"]; ix = C.index; tr = train_mask(ix); lc = np.log(C)
r3s = -(lc.shift(1) - lc.shift(4)); r24 = -(lc - lc.shift(24)); r72 = -(lc - lc.shift(72))
def mk(name, w):
    mp = int(.8 * w)
    x = {"dd": lc - np.log(C.rolling(w, min_periods=mp).max()), "madev": lc - np.log(C.rolling(w, min_periods=mp).mean())}[name]
    return x - x.shift(1).rolling(2160, min_periods=720).mean()
V = {"dd_72": mk("dd", 72), "madev_72": mk("madev", 72), "dd_168": mk("dd", 168), "dd_336": mk("dd", 336)}
rows = []
for nm, x in V.items():
    res = residual_rank(x[tr], [r3s[tr], r24[tr], r72[tr]])
    for h in (6, 24):
        for form, FF in (("raw detrended", x[tr]), ("resid(r3s,r24,r72)", res)):
            ic = -xs_ic(FF, B.R[h][tr]); rep = slice_report(ic, h + 5)
            rows.append(dict(variant=nm, form=form, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" for k in rep}, sc=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], c2=rep["C2"]["mean"], c3=rep["C3"]["mean"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_43_table.csv", index=False)
print("score = -IC:"); print(T.drop(columns=["sc", "t", "c2", "c3"]).to_string(index=False))
c = T[T.form.str.startswith("resid")]; b = c.sort_values("sc", ascending=False).iloc[0]; tc = kit.tcrit_for(8)
print("\nBEST residual:", b.variant, b.h, round(b.sc, 4), round(b.t, 2), "C2", round(b.c2, 4), "C3", round(b.c3, 4), "tcrit", round(tc, 2))
print("supported:", bool(b.sc >= .015 and b.t >= tc and b.c2 > 0 and b.c3 > 0), " refuted:", bool((c.sc < .01).all()))
print("mean XS corr dd_72(detr) vs r3s / r24 / r72:", [round(float(xs_ic(V['dd_72'][tr], g[tr]).mean()), 3) for g in (r3s, r24, r72)])
fig, ax = plt.subplots(figsize=(9, 4)); piv = T.pivot_table(index=["variant", "form"], columns="h", values="sc"); piv.plot.barh(ax=ax); ax.axvline(0.015, color="#e34948", ls="--", lw=.8); ax.set_title("H16 drawdown/MA features: raw vs residual on trailing returns (score -IC)")
fig.savefig("plots/cell_43_range_resid.png", bbox_inches="tight")
