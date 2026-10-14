import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_09"); S = B.S; C = S["close"]; lr = np.log(C)
q, n, bv, v = S["quote_vol"].where(S["quote_vol"] > 0), S["n"].where(S["n"] > 0), S["buy_vol"], S["vol"].where(S["vol"] > 0)
tr = train_mask(C.index)


def surp(x, w):
    num = x.rolling(w, min_periods=max(1, int(.8 * w))).sum()
    base = x.shift(w).rolling(720, min_periods=360).mean()
    return np.log(num / (w * base))


def trim(F):  # TRAIN rows only, to keep the residual loop short
    return F[tr]


rows = []
for fam, X in (("nsurp", n), ("volsurp", q)):
    for w in (1, 6, 24):
        F = surp(X, w); r = lr - lr.shift(w)
        res = residual_rank(trim(F), [trim(r), trim(r.abs())])
        for h in (6, 24):
            for nm, FF in (("raw", trim(F)), ("resid", res)):
                ic = xs_ic(FF, trim(B.R[h])); rep = slice_report(ic, h + 5)
                rows.append(dict(feat=f"{fam}_{w}", kind=nm, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" for k in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"]))
# taker_1 residual on rev1 at h1
tk = bv / v - 0.5; rev1 = -(lr - lr.shift(1))
res = residual_rank(trim(tk), [trim(rev1)])
for nm, FF in (("raw", trim(tk)), ("resid_on_rev1", res), ("rev1 itself", trim(rev1))):
    ic = xs_ic(FF, trim(B.R[1])); rep = slice_report(ic, 6)
    rows.append(dict(feat="taker_1", kind=nm, h=1, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" for k in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250)
print(T.drop(columns=["tr", "t"]).to_string(index=False)); T.to_csv("cells/cell_09_table.csv", index=False)
r = T[(T.kind == "resid") & (T.feat != "taker_1")]
b = r.sort_values("tr", ascending=False).iloc[0]
tc = kit.tcrit_for(13)
print("\nbest residual variant:", b.feat, "h", b.h, "IC", round(b.tr, 4), "t", round(b.t, 2), "tcrit", round(tc, 2))
print("supported:", bool(b.tr >= 0.02 and b.t >= tc), " refuted (all <= 0.01):", bool((r.tr <= 0.01).all()))
fig, ax = plt.subplots(figsize=(9, 4))
piv = r.pivot_table(index="feat", columns="h", values="tr"); piv.plot.barh(ax=ax); ax.axvline(0, color="#9b9a94"); ax.axvline(0.02, color="#e34948", ls="--", lw=.8); ax.set_title("residual (return, |return| partialled out) IC; red = min_useful")
fig.savefig("plots/cell_09_resid.png", bbox_inches="tight")
