import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code"); sys.path.insert(0, r"C:\Users\User\eda-routine")
from fx import *
import importlib
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_45"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
L = make_long(B, None); f3 = unstack_feature(importlib.import_module("features.f003").compute(L), ix)
r1 = lr.diff(); mk1 = r1.mean(axis=1); mvol = mk1.rolling(168, min_periods=84).std(); cut = mvol[in_slice(ix, "EXPLORE")].median(); trend = mk1.rolling(720, min_periods=500).sum()
sess = pd.Series("other", index=ix); sess[np.isin(ix.hour, [21, 22, 23, 0, 1])] = "ASIA"; sess[np.isin(ix.hour, [7, 8, 9, 10, 11])] = "EU"; sess[np.isin(ix.hour, [13, 14, 15, 16])] = "US"
conds = {"ASIA": sess == "ASIA", "EU": sess == "EU", "US": sess == "US", "other": sess == "other", "trend_up": trend > 0, "trend_down": trend < 0, "mvol_high": mvol > cut, "mvol_low": mvol <= cut}
rows = []; store = {}
for h in (6, 24):
    ic = xs_ic(f3[tr], B.R[h][tr])
    rep = slice_report(ic, h + 5); rows.append(dict(cond="ALL", h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" for k in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], n=rep["TRAIN"]["n"]))
    for cn, m in conds.items():
        x = ic[m.reindex(ic.index).fillna(False).values]; store[(cn, h)] = x; rep = slice_report(x, h + 5)
        rows.append(dict(cond=cn, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" if rep[k]["n"] > 30 else "n/a" for k in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], n=rep["TRAIN"]["n"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_45_table.csv", index=False)
print(T.drop(columns=["tr", "t"]).to_string(index=False))
tc = kit.tcrit_for(2)
print("\nPRIMARY contrasts at h24 (paired by day, NW lag 3):")
dd = {}
for s in ("ASIA", "US"):
    a = store[(s, 24)]; b = store[("other", 24)]
    da = a.groupby(a.index.floor("D")).mean(); db = b.groupby(b.index.floor("D")).mean(); d = (da - db).dropna(); d = d[train_mask(d.index)]
    r = nw(d, 3); dd[s] = r; print(s, "-other:", round(r["mean"], 4), round(r["t"], 2), r["n"])
print("depends on session:", bool(any(dd[s]["mean"] <= -0.02 and dd[s]["t"] <= -tc for s in dd)), " refuted (both within +-0.01):", bool(all(abs(dd[s]["mean"]) <= 0.01 for s in dd)))
fig, ax = plt.subplots(figsize=(9, 4)); piv = T[T.cond != "ALL"].pivot(index="cond", columns="h", values="tr"); piv.plot.barh(ax=ax); ax.axvline(0, color="#9b9a94"); ax.set_title("f003 IC by condition")
fig.savefig("plots/cell_45_f003_cond.png", bbox_inches="tight")
