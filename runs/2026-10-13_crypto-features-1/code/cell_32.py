import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_32"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
r = lr.diff()
# for the signal at the END of bar t, the next bar has the same hour-of-day as bars t+1-24j; r at those bars = r.shift(24j - 1)
def season(N):
    acc = sum(r.shift(24 * j - 1) for j in range(1, N + 1))
    cnt = sum(r.shift(24 * j - 1).notna().astype(int) for j in range(1, N + 1))
    return (acc / cnt).where(cnt >= int(0.8 * N))
V = {}
for N in (20, 60):
    s = season(N); drift = r.shift(0).rolling(24 * N, min_periods=int(24 * N * .6)).mean()
    V[f"season{N}_raw"] = s; V[f"season{N}_dm"] = s - drift; V[f"season{N}_sign"] = np.sign(s - drift)
V["lag24_ref"] = r.shift(23)   # return of the bar with the same hour-of-day as the next bar, one day earlier
rows = []
for name, x in V.items():
    for h in HORIZONS:
        ic = xs_ic(x[tr], B.R[h][tr]); rep = slice_report(ic, h + 5)
        rows.append(dict(variant=name, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" for k in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_32_table.csv", index=False)
print(T.drop(columns=["tr", "t"]).to_string(index=False))
tc = kit.tcrit_for(21)
d = T[T.variant.str.contains("_dm|_sign")]; b = d.sort_values("tr", ascending=False).iloc[0]
print("\nbest demeaned/sign:", b.variant, b.h, round(b.tr, 4), round(b.t, 2), "tcrit", round(tc, 2), "supported:", bool(b.tr >= .02 and b.t >= tc))
print("largest |IC| overall:"); print(T.assign(a=T.tr.abs()).sort_values("a", ascending=False).head(5)[["variant", "h", "tr", "t"]].round(4).to_string(index=False))
fig, ax = plt.subplots(figsize=(9, 4))
piv = T.pivot(index="variant", columns="h", values="tr"); piv.plot.barh(ax=ax); ax.axvline(0.02, color="#e34948", ls="--", lw=.8); ax.axvline(0, color="#9b9a94")
ax.set_title("H14 hour-of-day seasonality persistence, pooled TRAIN IC"); fig.savefig("plots/cell_32_season.png", bbox_inches="tight")
