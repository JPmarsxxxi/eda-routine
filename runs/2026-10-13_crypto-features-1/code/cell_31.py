import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_31"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
r = lr.diff(); mk = r.mean(axis=1)
b_mkt = r.rolling(720, min_periods=360).cov(mk).div(mk.rolling(720, min_periods=360).var(), axis=0).shift(1)
rows = []; store = {}
for k in (1, 3, 6, 24):
    mkk = (lr - lr.shift(k)).mean(axis=1); lead = b_mkt.mul(mkk, axis=0)
    for h in HORIZONS:
        ic_all = xs_ic(lead[tr], B.R[h][tr])
        for st, m in (("UP", mkk > 0), ("DOWN", mkk < 0)):
            x = ic_all[m.reindex(ic_all.index).fillna(False).values]; store[(k, st, h)] = x
            rep = slice_report(x, h + 5)
            rows.append(dict(form="lead", k=k, state=st, h=h, **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], n=rep["TRAIN"]["n"]))
for k in (1, 6):
    mkk = (lr - lr.shift(k)).mean(axis=1); lead = b_mkt.mul(mkk, axis=0)
    dt = lead - lead.shift(1).rolling(720, min_periods=360).mean()
    for h in HORIZONS:
        ic = xs_ic(dt[tr], B.R[h][tr]); rep = slice_report(ic, h + 5)
        rows.append(dict(form="lead-detrended", k=k, state="ALL", h=h, **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}, tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], n=rep["TRAIN"]["n"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_31_table.csv", index=False)
print(T.drop(columns=["tr", "t"]).to_string(index=False))
tc = kit.tcrit_for(2)
print("\nPRIMARY pairs:")
ok = []
for k, h in ((6, 6), (24, 24)):
    u = T[(T.form == "lead") & (T.k == k) & (T.h == h) & (T.state == "UP")].iloc[0]; d = T[(T.form == "lead") & (T.k == k) & (T.h == h) & (T.state == "DOWN")].iloc[0]
    print(k, h, "UP", round(u.tr, 4), round(u.t, 2), "DOWN", round(d.tr, 4), round(d.t, 2))
    ok.append(bool(u.tr <= -0.015 and u.t <= -tc and d.tr <= -0.015 and d.t <= -tc))
    print("   same-sign reversal passes:", ok[-1], " opposite signs with |IC|>=0.01:", bool(u.tr * d.tr < 0 and abs(u.tr) >= .01 and abs(d.tr) >= .01))
print("supported:", any(ok))
fig, ax = plt.subplots(figsize=(9, 4))
L = T[T.form == "lead"]; piv = L.pivot_table(index=["k", "state"], columns="h", values="tr"); piv.plot.barh(ax=ax); ax.axvline(0, color="#9b9a94"); ax.set_title("beta x market move: IC in UP vs DOWN states")
fig.savefig("plots/cell_31_updown.png", bbox_inches="tight")
