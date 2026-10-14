import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_30"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
r = lr.diff(); mk = r.mean(axis=1); btc = r["BTC"]
b_btc = r.rolling(720, min_periods=360).cov(btc).div(btc.rolling(720, min_periods=360).var(), axis=0).shift(1)
b_mkt = r.rolling(720, min_periods=360).cov(mk).div(mk.rolling(720, min_periods=360).var(), axis=0).shift(1)
V = {}
for k in (1, 3, 6, 24):
    bk = lr["BTC"] - lr["BTC"].shift(k); mkk = (lr - lr.shift(k)).mean(axis=1)
    V[f"lead_btc_{k}"] = b_btc.mul(bk, axis=0); V[f"lead_mkt_{k}"] = b_mkt.mul(mkk, axis=0)
rows = []
for name, x in V.items():
    for h in HORIZONS:
        ic = xs_ic(x[tr], B.R[h][tr]); rep = slice_report(ic, h + 5)
        rows.append(dict(variant=name, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" for k in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_30_table.csv", index=False)
print(T.drop(columns=["tr", "t"]).to_string(index=False))
tc = kit.tcrit_for(24); b = T.sort_values("tr", ascending=False).iloc[0]
print("\nbest (positive sign):", b.variant, b.h, round(b.tr, 4), round(b.t, 2), "tcrit", round(tc, 2), "supported:", bool(b.tr >= .02 and b.t >= tc))
print("largest negative:", T.sort_values("tr").iloc[0][["variant", "h", "tr", "t"]].to_dict())
print("mean cross-coin beta dispersion (std of beta_btc across coins):", round(float(b_btc[tr].std(axis=1).mean()), 3))
fig, ax = plt.subplots(figsize=(9, 4))
piv = T.pivot(index="variant", columns="h", values="tr"); piv.plot.barh(ax=ax); ax.axvline(0.02, color="#e34948", ls="--", lw=.8); ax.axvline(-0.02, color="#e34948", ls="--", lw=.8); ax.axvline(0, color="#9b9a94")
ax.set_title("H12 beta x market-move features, pooled TRAIN IC"); fig.savefig("plots/cell_30_lead.png", bbox_inches="tight")
