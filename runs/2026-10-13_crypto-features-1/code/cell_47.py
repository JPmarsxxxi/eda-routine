import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_47"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
r = lr.diff(); mk = r.mean(axis=1)
b_mkt = r.rolling(720, min_periods=360).cov(mk).div(mk.rolling(720, min_periods=360).var(), axis=0).shift(1)
rows = []
for k in (1, 3, 6):
    mkk = (lr - lr.shift(k)).mean(axis=1); lead = b_mkt.mul(mkk, axis=0); up = (mkk > 0)
    dt = lead - lead.shift(1).rolling(720, min_periods=360).mean()
    for form, x in (("level", lead), ("detrended", dt)):
        for tm, d in (("undelayed", 0), ("delay1", 1)):
            for h in ((1, 6) if tm == "delay1" else (1,)):
                ic = xs_ic(x[tr], B.R[h].shift(-d)[tr]); xx = ic[up.reindex(ic.index).fillna(False).values]; rep = slice_report(xx, h + 5 + d)
                rows.append(dict(k=k, form=form, timing=tm, h=h, **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], n=rep["TRAIN"]["n"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_47_table.csv", index=False)
print(T.drop(columns=["tr", "t"]).to_string(index=False))
tc = kit.tcrit_for(6); p = T[(T.form == "detrended") & (T.timing == "delay1") & (T.h == 1)]; b = p.sort_values("tr").iloc[0]
print("\nPRIMARY delayed+detrended UP-state h1:", p[["k", "tr", "t"]].round(4).values.tolist(), "best (most negative):", b.k, round(b.tr, 4), round(b.t, 2), "tcrit", round(tc, 2))
print("supported:", bool(b.tr <= -.015 and b.t <= -tc), " refuted:", bool((p.tr.abs() < .01).all()))
fig, ax = plt.subplots(figsize=(9, 4)); piv = T[T.h == 1].pivot_table(index=["k", "form"], columns="timing", values="tr"); piv.plot.barh(ax=ax); ax.axvline(0, color="#9b9a94"); ax.set_title("UP-state beta x market move, h1: undelayed vs delay1")
fig.savefig("plots/cell_47_up_delay.png", bbox_inches="tight")
