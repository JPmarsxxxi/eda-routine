import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_46"); S = B.S; BN = np.log(S["close"]); ix = BN.index; tr = train_mask(ix)
CB = venue("cell_46", "coinbase"); UB = venue("cell_46", "upbit")
cb = np.log(CB["close"].reindex(columns=COINS)); ub = np.log(UB["close"].reindex(columns=COINS))
gap = cb - BN; ug = ub - BN
F = {"cb_gap_lvl": gap - gap.shift(1).rolling(720, min_periods=360).mean(), "cb_retdiff_3": (cb - cb.shift(3)) - (BN - BN.shift(3)),
     "ub_gap_lvl": ug - ug.shift(1).rolling(720, min_periods=360).mean(), "ub_retdiff_6": (ub - ub.shift(6)) - (BN - BN.shift(6))}
rev1 = -(BN - BN.shift(1)); rev3 = -(BN - BN.shift(3))
sess = pd.Series("other", index=ix); sess[np.isin(ix.hour, [21, 22, 23, 0, 1])] = "ASIA"; sess[np.isin(ix.hour, [13, 14, 15, 16])] = "US"
rows = []
for nm, x in F.items():
    res = residual_rank(x[tr], [rev1[tr], rev3[tr]])
    home = "US" if nm.startswith("cb") else "ASIA"
    for h in (1, 6):
        ic = xs_ic(res, B.R[h].shift(-1)[tr], min_n=5)
        for cn, m in (("home(" + home + ")", sess == home), ("other", sess == "other")):
            xx = ic[m.reindex(ic.index).fillna(False).values]; rep = slice_report(xx, h + 6)
            rows.append(dict(feat=nm, cond=cn, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" if rep[k]["n"] > 30 else "n/a" for k in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], c2=rep["C2"]["mean"], c3=rep["C3"]["mean"], n=rep["TRAIN"]["n"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_46_table.csv", index=False)
print(T.drop(columns=["tr", "t", "c2", "c3"]).to_string(index=False))
h_ = T[T.cond.str.startswith("home")]; b = h_.sort_values("tr", ascending=False).iloc[0]; tc = kit.tcrit_for(8)
print("\nPRIMARY best home-session:", b.feat, b.cond, b.h, round(b.tr, 4), round(b.t, 2), "C2", round(b.c2, 4), "C3", round(b.c3, 4), "n", b.n, "tcrit", round(tc, 2))
print("supported:", bool(b.tr >= .02 and b.t >= tc and b.c2 > 0 and b.c3 > 0), " refuted:", bool((h_.tr < .01).all()))
fig, ax = plt.subplots(figsize=(9, 4)); piv = T.pivot_table(index=["feat", "cond"], columns="h", values="tr"); piv.plot.barh(ax=ax); ax.axvline(0.02, color="#e34948", ls="--", lw=.8); ax.axvline(0, color="#9b9a94"); ax.set_title("H6 residual venue gaps: home session vs other (entry delay 1)")
fig.savefig("plots/cell_46_venue_sessions.png", bbox_inches="tight")
