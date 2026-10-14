import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_12"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
Fu, W = funding("cell_12"); PR = perp_hourly("cell_12", "premium")
prem = PR["close"]
dt = prem - prem.shift(1).rolling(720, min_periods=360).mean()
r3s = -(lr.shift(1) - lr.shift(4)); r24 = -(lr - lr.shift(24))
res = residual_rank(dt[tr], [r3s[tr], r24[tr]])
mprem = prem.mean(axis=1); regime = (mprem > mprem.rolling(720, min_periods=360).median()).where(mprem.rolling(720, min_periods=360).median().notna())
hrs = pd.Series(ix.hour, index=ix); since = (hrs % 8)  # hours since 00/08/16 settlement (stamp hour of bar open)
bucket = pd.Series(np.where(since <= 2, "0-2", np.where(since <= 5, "3-5", "6-7")), index=ix)
sess = pd.Series("other", index=ix); sess[np.isin(ix.hour, [21, 22, 23, 0, 1])] = "ASIA"; sess[np.isin(ix.hour, [7, 8, 9, 10, 11])] = "EU"; sess[np.isin(ix.hour, [13, 14, 15, 16])] = "US"
floor_share = ((Fu.round(6) == 0.0001).where(Fu.notna()).mean(axis=1)); floorhi = (floor_share > 0.5).where(floor_share.notna())
conds = {"mkt_prem_above": regime == True, "mkt_prem_below": regime == False, "settle_0-2": bucket == "0-2", "settle_3-5": bucket == "3-5", "settle_6-7": bucket == "6-7",
         "ASIA": sess == "ASIA", "EU": sess == "EU", "US": sess == "US", "other": sess == "other", "floor_hi": floorhi == True, "floor_lo": floorhi == False}
rows = []; store = {}
for h in HORIZONS:
    ic = -xs_ic(res, B.R[h][tr])
    for cn, m in conds.items():
        x = ic[m.reindex(ic.index).fillna(False).values]; store[(cn, h)] = x
        rep = slice_report(x, h + 5)
        rows.append(dict(cond=cn, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" if rep[k]["n"] > 30 else "n/a" for k in rep}, sc=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], n=rep["TRAIN"]["n"]))
    rows.append(dict(cond="ALL", h=h, **{k: f"{(v:=slice_report(ic, h+5)[k])['mean']:+.4f}({v['t']:+.1f})" for k in ("EXPLORE", "C1", "C2", "C3", "TRAIN")}, sc=slice_report(ic, h + 5)["TRAIN"]["mean"], t=slice_report(ic, h + 5)["TRAIN"]["t"], n=slice_report(ic, h + 5)["TRAIN"]["n"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_12_table.csv", index=False)
print("score = -IC (positive = crowding works):"); print(T.drop(columns=["sc", "t"]).to_string(index=False))
tc = kit.tcrit_for(2)
a = T[(T.h == 6) & (T.cond == "mkt_prem_above")].iloc[0]; b = T[(T.h == 6) & (T.cond == "mkt_prem_below")].iloc[0]
print("\nPRIMARY h6: above", round(a.sc, 4), round(a.t, 2), " below", round(b.sc, 4), round(b.t, 2), " tcrit", round(tc, 2))
print("supported:", bool(a.sc >= .015 and a.t >= tc and b.sc >= .015 and b.t >= tc), " refuted:", bool((a.sc <= 0 and a.t <= -1.65) or (b.sc <= 0 and b.t <= -1.65)))
fig, ax = plt.subplots(figsize=(9, 4))
piv = T[T.cond != "ALL"].pivot(index="cond", columns="h", values="sc"); piv.plot.barh(ax=ax); ax.axvline(0.015, color="#e34948", ls="--", lw=.8); ax.set_title("prem_dtr crowding score by condition (red = 0.015)")
fig.savefig("plots/cell_12_prem_conditions.png", bbox_inches="tight")
