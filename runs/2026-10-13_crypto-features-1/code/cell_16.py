import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_16"); S = B.S; ix = B.P.index; C = S["close"]; tr = train_mask(ix); lr = np.log(C)
f54 = a54_roll(S); r24p = np.log(C / C.shift(24))
mk = lr.diff().mean(axis=1).rolling(720, min_periods=500).sum()
trend = pd.Series(np.where(mk > 0, "up", "down"), index=ix).where(mk.notna())
sess = pd.Series("other", index=ix); sess[np.isin(ix.hour, [21, 22, 23, 0, 1])] = "ASIA"; sess[np.isin(ix.hour, [7, 8, 9, 10, 11])] = "EU"; sess[np.isin(ix.hour, [13, 14, 15, 16])] = "US"
res = residual_rank(f54[tr], [r24p[tr]])
rows = []; store = {}
for fn, FF in (("f54", f54[tr]), ("f54|r24", res)):
    for h in HORIZONS:
        ic = xs_ic(FF, B.R[h][tr])
        for cn, m in (("trend_up", trend == "up"), ("trend_down", trend == "down"), ("ASIA", sess == "ASIA"), ("EU", sess == "EU"), ("US", sess == "US"), ("other", sess == "other")):
            if fn == "f54|r24" and cn not in ("trend_up", "trend_down"):
                continue
            x = ic[m.reindex(ic.index).fillna(False).values]; store[(fn, cn, h)] = x
            rep = slice_report(x, h + 5)
            rows.append(dict(f=fn, cond=cn, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" if rep[k]["n"] > 30 else "n/a" for k in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], n=rep["TRAIN"]["n"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_16_table.csv", index=False)
print(T.drop(columns=["tr", "t"]).to_string(index=False))
print("\nshare of TRAIN hours in the up state, by fold:", {nm: round(float((trend[in_slice(ix, nm)] == "up").mean()), 2) for nm in SLICES})
d = T[(T.f == "f54") & (T.h == 24) & (T.cond == "trend_down")].iloc[0]; u = T[(T.f == "f54") & (T.h == 24) & (T.cond == "trend_up")].iloc[0]
print("PRIMARY h24: down", round(d.tr, 4), round(d.t, 2), "n", d.n, " up", round(u.tr, 4), round(u.t, 2))
print("not an impostor:", bool(d.tr >= 0.02 and d.t >= 1.96), " impostor:", bool(d.tr <= 0.01 and u.tr >= 0.02))
fig, ax = plt.subplots(figsize=(9, 4))
piv = T[T.f == "f54"].pivot(index="cond", columns="h", values="tr"); piv.plot.barh(ax=ax); ax.axvline(0.02, color="#e34948", ls="--", lw=.8); ax.axvline(0, color="#9b9a94"); ax.set_title("f54_roll IC by trend state and session")
fig.savefig("plots/cell_16_f54_conditions.png", bbox_inches="tight")
