import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_44"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
q, n, bv, v = S["quote_vol"].where(S["quote_vol"] > 0), S["n"].where(S["n"] > 0), S["buy_vol"], S["vol"].where(S["vol"] > 0)
def surp(x, w):
    num = x.rolling(w, min_periods=max(1, int(.8 * w))).sum(); base = x.shift(w).rolling(720, min_periods=360).mean()
    return np.log(num / (w * base))
F = {"volsurp_6": (surp(q, 6), 6, -1), "nsurp_6": (surp(n, 6), 6, -1),
     "taker_6": (bv.rolling(6, min_periods=5).sum() / v.rolling(6, min_periods=5).sum() - 0.5, 6, +1), "taker_24": (bv.rolling(24, min_periods=20).sum() / v.rolling(24, min_periods=20).sum() - 0.5, 24, +1)}
r1 = lr.diff(); mk1 = r1.mean(axis=1); mvol = mk1.rolling(168, min_periods=84).std(); cut = mvol[in_slice(ix, "EXPLORE")].median()
trend = mk1.rolling(720, min_periods=500).sum()
sess = pd.Series("other", index=ix); sess[np.isin(ix.hour, [21, 22, 23, 0, 1])] = "ASIA"; sess[np.isin(ix.hour, [7, 8, 9, 10, 11])] = "EU"; sess[np.isin(ix.hour, [13, 14, 15, 16])] = "US"
conds = {"ASIA": sess == "ASIA", "EU": sess == "EU", "US": sess == "US", "other": sess == "other", "trend_up": trend > 0, "trend_down": trend < 0, "mvol_high": mvol > cut, "mvol_low": mvol <= cut}
rows = []
for nm, (x, w, d) in F.items():
    r = lr - lr.shift(w); res = residual_rank(x[tr], [r[tr], r.abs()[tr]])
    for h in (6, 24):
        ic = d * xs_ic(res, B.R[h][tr])
        for cn, m in conds.items():
            xx = ic[m.reindex(ic.index).fillna(False).values]; rep = slice_report(xx, h + 5)
            rows.append(dict(feat=nm, cond=cn, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" if rep[k]["n"] > 30 else "n/a" for k in rep}, sc=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], n=rep["TRAIN"]["n"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_44_table.csv", index=False)
tc = kit.tcrit_for(64)
print("score = pre-stated-sign IC; top 12:"); print(T.sort_values("sc", ascending=False).head(12)[["feat", "cond", "h", "EXPLORE", "C1", "C2", "C3", "TRAIN", "n"]].to_string(index=False))
print("\nmost negative (wrong-sign leads):"); print(T.sort_values("sc").head(6)[["feat", "cond", "h", "TRAIN", "t", "n"]].round(4).to_string(index=False))
b = T.sort_values("sc", ascending=False).iloc[0]
print("\nPRIMARY best:", b.feat, b.cond, b.h, round(b.sc, 4), round(b.t, 2), "tcrit", round(tc, 2), "supported:", bool(b.sc >= .02 and b.t >= tc))
fig, ax = plt.subplots(figsize=(10, 4)); piv = T[T.h == 24].pivot(index="cond", columns="feat", values="sc"); piv.plot.bar(ax=ax); ax.axhline(0.02, color="#e34948", ls="--", lw=.8); ax.axhline(0, color="#9b9a94"); ax.set_title("H4 residual surprise scores (pre-stated sign) by condition, h24")
fig.savefig("plots/cell_44_h4_cond.png", bbox_inches="tight")
