import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_29"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
r = lr.diff(); mk = r.mean(axis=1)
beta = r.rolling(720, min_periods=360).cov(mk).div(mk.rolling(720, min_periods=360).var(), axis=0)
resid = r - beta.shift(1).mul(mk, axis=0)
F = {
 "rv_168": r.rolling(168, min_periods=120).std(), "rv_24": r.rolling(24, min_periods=20).std(),
 "max_168": r.rolling(168, min_periods=120).max(), "min_168": r.rolling(168, min_periods=120).min(),
 "skew_168": r.rolling(168, min_periods=120).skew(), "rng_24": (S["high"].rolling(24, min_periods=20).max() - S["low"].rolling(24, min_periods=20).min()) / C,
 "idio_168": resid.rolling(168, min_periods=120).std(),
}
F["rv_ratio"] = np.log(F["rv_24"] / F["rv_168"])
V = {}
for k, x in F.items():
    V[f"{k}|level"] = x
    V[f"{k}|detrend"] = x - x.shift(1).rolling(2160, min_periods=720).mean()
rows = []
for name, x in V.items():
    xt = x[tr]
    for h in HORIZONS:
        ic = xs_ic(xt, B.R[h][tr]); rep = slice_report(ic, h + 5)
        rows.append(dict(variant=name, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" for k in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_29_table.csv", index=False)
print(T.drop(columns=["tr", "t"]).to_string(index=False))
one = ["rv_168", "rv_24", "max_168", "skew_168", "rng_24", "idio_168"]
d = T[T.variant.str.contains("detrend") & T.variant.str.split("|").str[0].isin(one)].copy()
d["score"] = -d.tr; d["st"] = -d.t
tc = kit.tcrit_for(36); b = d.sort_values("score", ascending=False).iloc[0]
print("\nBEST detrended one-sided:", b.variant, b.h, round(b.score, 4), round(b.st, 2), "tcrit", round(tc, 2), "supported:", bool(b.score >= 0.02 and b.st >= tc))
print("level-vs-detrend share of IC (TRAIN, h24):")
for k in F:
    lv = T[(T.variant == f"{k}|level") & (T.h == 24)].tr.iloc[0]; dt = T[(T.variant == f"{k}|detrend") & (T.h == 24)].tr.iloc[0]
    print(" ", k, round(lv, 4), round(dt, 4))
print("top |IC| detrended:"); print(T[T.variant.str.contains("detrend")].assign(a=lambda x: x.tr.abs()).sort_values("a", ascending=False).head(8)[["variant", "h", "tr", "t"]].round(4).to_string(index=False))
fig, ax = plt.subplots(figsize=(10, 5))
piv = T.pivot_table(index="variant", columns="h", values="tr"); piv.plot.barh(ax=ax); ax.axvline(0, color="#9b9a94"); ax.axvline(-0.02, color="#e34948", ls="--", lw=.8); ax.set_title("H11 risk features: IC (level vs detrended)")
fig.savefig("plots/cell_29_risk.png", bbox_inches="tight")
