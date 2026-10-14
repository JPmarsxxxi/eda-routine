import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_38"); S = B.S; C = S["close"]; ix = C.index; tr = train_mask(ix)
O, H, L = S["open"], S["high"], S["low"]
rng = np.log(H / L).where(np.log(H / L) > 0)
vwap = (S["quote_vol"] / S["vol"]).where(S["vol"] > 0)
F = {
 "clv1": (C - L) / (H - L).where((H - L) > 0), "body": np.log(C / O), "body_n": np.log(C / O) / rng,
 "upper_wick": np.log(H / np.maximum(O, C)) / rng, "lower_wick": np.log(np.minimum(O, C) / L) / rng,
 "gap": np.log(O / C.shift(1)), "vwap_dev": np.log(C / vwap),
}
rows = []
for name, x in F.items():
    xt = x[tr]
    for h in HORIZONS:
        for tm, d in (("undelayed", 0), ("delay1", 1)):
            ic = xs_ic(xt, B.R[h].shift(-d)[tr]); rep = slice_report(ic, h + 5 + d)
            rows.append(dict(variant=name, h=h, timing=tm, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" for k in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_38_table.csv", index=False)
print(T.drop(columns=["tr", "t"]).to_string(index=False))
tc = kit.tcrit_for(21); d = T[T.timing == "delay1"]; b = d.assign(a=d.tr.abs()).sort_values("a", ascending=False).iloc[0]
print("\nPRIMARY best delayed |IC|:", b.variant, b.h, round(b.tr, 4), round(b.t, 2), "tcrit", round(tc, 2), "supported:", bool(abs(b.tr) >= .02 and abs(b.t) >= tc))
print("corr of body with the 1h reversal rank (mean XS):", round(float(xs_ic(F["body"][tr], -(np.log(C) - np.log(C).shift(1))[tr]).mean()), 3), " clv1:", round(float(xs_ic(F["clv1"][tr], -(np.log(C) - np.log(C).shift(1))[tr]).mean()), 3))
fig, ax = plt.subplots(figsize=(10, 5))
piv = T.pivot_table(index=["variant", "timing"], columns="h", values="tr"); piv.plot.barh(ax=ax); ax.axvline(0.02, color="#e34948", ls="--", lw=.8); ax.axvline(-0.02, color="#e34948", ls="--", lw=.8); ax.axvline(0, color="#9b9a94")
ax.set_title("H15 within-bar shape: undelayed vs delay-1 IC"); fig.savefig("plots/cell_38_barshape.png", bbox_inches="tight")
