import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_42"); S = B.S; C = S["close"]; ix = C.index; tr = train_mask(ix); lc = np.log(C)
rows = []
for w in (72, 168, 336, 720):
    mp = int(.8 * w)
    Hh, Ll = S["high"].rolling(w, min_periods=mp).max(), S["low"].rolling(w, min_periods=mp).min()
    F = {"pos": (C - Ll) / (Hh - Ll).where((Hh - Ll) > 0), "dd": lc - np.log(C.rolling(w, min_periods=mp).max()), "ru": lc - np.log(C.rolling(w, min_periods=mp).min()), "madev": lc - np.log(C.rolling(w, min_periods=mp).mean())}
    for k, x in F.items():
        for form, xx in (("level", x), ("detrend", x - x.shift(1).rolling(2160, min_periods=720).mean())):
            xt = xx[tr]
            for h in HORIZONS:
                ic = xs_ic(xt, B.R[h][tr]); rep = slice_report(ic, h + 5)
                rows.append(dict(variant=f"{k}_{w}|{form}", h=h, **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_42_table.csv", index=False)
d = T[T.variant.str.contains("detrend") & T.h.isin([6, 24])].copy(); d["score"] = -d.tr; d["st"] = -d.t
tc = kit.tcrit_for(32); b = d.sort_values("score", ascending=False).iloc[0]
print("top 10 detrended by score (-IC), h6/h24:"); print(d.sort_values("score", ascending=False).head(10)[["variant", "h", "EXPLORE", "C1", "C2", "C3", "TRAIN", "score", "st"]].to_string(index=False))
print("\nPRIMARY best:", b.variant, b.h, round(b.score, 4), round(b.st, 2), "tcrit", round(tc, 2), "supported:", bool(b.score >= .02 and b.st >= tc))
print("largest |IC| overall (any form/h):"); print(T.assign(a=T.tr.abs()).sort_values("a", ascending=False).head(8)[["variant", "h", "TRAIN", "t"]].round(3).to_string(index=False))
lv = T[(T.variant.str.endswith("level")) & (T.h == 24)].assign(a=lambda x: x.tr.abs()).sort_values("a", ascending=False).head(4)
print("\nbiggest level ICs at h24:"); print(lv[["variant", "tr", "t"]].round(4).to_string(index=False))
fig, ax = plt.subplots(figsize=(10, 4))
piv = d.pivot_table(index="variant", columns="h", values="score"); piv.plot.bar(ax=ax, legend=True); ax.axhline(0.02, color="#e34948", ls="--", lw=.8); ax.set_xticklabels([]); ax.set_title("H16 detrended range features: score (-IC) at h6/h24")
fig.savefig("plots/cell_42_range.png", bbox_inches="tight")
