import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_50"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
K = perp_hourly("cell_50", "klines")
pv, pq, pc, pb = K["volume"].where(K["volume"] > 0), K["quote_volume"].where(K["quote_volume"] > 0), K["count"].where(K["count"] > 0), K["taker_buy_volume"]
sv, sb, sq = S["vol"].where(S["vol"] > 0), S["buy_vol"], S["quote_vol"].where(S["quote_vol"] > 0)
def tk(b, v, w): return b.rolling(w, min_periods=int(.8 * w)).sum() / v.rolling(w, min_periods=int(.8 * w)).sum() - 0.5
def surp(x, w):
    num = x.rolling(w, min_periods=max(1, int(.8 * w))).sum(); base = x.shift(w).rolling(720, min_periods=360).mean(); return np.log(num / (w * base))
F = {}
for w in (1, 6, 24): F[f"ptaker_{w}"] = (tk(pb, pv, w), w)
for w in (6, 24): F[f"pgap_{w}"] = (tk(pb, pv, w) - tk(sb, sv, w), w)
ps = np.log(pq.rolling(24, min_periods=20).sum() / sq.rolling(24, min_periods=20).sum()); F["pshare"] = (ps - ps.shift(1).rolling(2160, min_periods=720).mean(), 24)
for w in (1, 6): F[f"pnsurp_{w}"] = (surp(pc, w), w)
rows = []
for nm, (x, w) in F.items():
    xd = x if nm in ("pshare", "pnsurp_1", "pnsurp_6") else x - x.shift(1).rolling(2160, min_periods=720).mean()
    r = lr - lr.shift(w); res = residual_rank(xd[tr], [r[tr], r.abs()[tr]])
    for h in HORIZONS:
        for form, FF in (("a:detrended", xd[tr]), ("b:resid(r,|r|)", res)):
            ic = xs_ic(FF, B.R[h][tr]); rep = slice_report(ic, h + 5)
            rows.append(dict(feat=nm, form=form, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" for k in rep}, ic=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], c2=rep["C2"]["mean"], c3=rep["C3"]["mean"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_50_table.csv", index=False)
print(T.drop(columns=["ic", "t", "c2", "c3"]).to_string(index=False))
tc = kit.tcrit_for(48); b = T[T.form.str.startswith("b")]; bb = b.assign(a=b.ic.abs()).sort_values("a", ascending=False).iloc[0]
print("\nPRIMARY best form (b):", bb.feat, bb.h, round(bb.ic, 4), round(bb.t, 2), "C2", round(bb.c2, 4), "C3", round(bb.c3, 4), "tcrit", round(tc, 2))
print("supported:", bool(abs(bb.ic) >= .02 and abs(bb.t) >= tc and np.sign(bb.c2) == np.sign(bb.ic) and np.sign(bb.c3) == np.sign(bb.ic)))
fig, ax = plt.subplots(figsize=(10, 5)); piv = T.pivot_table(index=["feat", "form"], columns="h", values="ic"); piv.plot.barh(ax=ax); ax.axvline(0.02, color="#e34948", ls="--", lw=.8); ax.axvline(-0.02, color="#e34948", ls="--", lw=.8); ax.axvline(0, color="#9b9a94")
ax.set_title("H17 perp flow features: IC (detrended vs residual)"); fig.savefig("plots/cell_50_perpflow.png", bbox_inches="tight")
