import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_11"); S = B.S; C = S["close"]; lr = np.log(C); tr = train_mask(C.index)
Fu, W = funding("cell_11"); K = perp_hourly("cell_11", "klines"); PR = perp_hourly("cell_11", "premium"); M = metrics_hourly("cell_11")
oiv = M["sum_open_interest_value"].where(M["sum_open_interest_value"] > 0)
base = {"prem_lvl": PR["close"], "basis_lvl": K["close"] / C - 1, "funding_lvl": Fu, "ls_acct_lvl": M["count_long_short_ratio"], "oi_val_chg_24": np.log(oiv / oiv.shift(24))}
r3s = -(lr.shift(1) - lr.shift(4)); r24 = -(lr - lr.shift(24))
rows = []
for nm, x in base.items():
    dt = x - x.shift(1).rolling(720, min_periods=360).mean()
    dt_tr = dt[tr]
    res = residual_rank(dt_tr, [r3s[tr], r24[tr]])
    for h in HORIZONS:
        Rh = B.R[h][tr]
        for form, FF in (("raw", x[tr]), ("detrend", dt_tr), ("detrend+resid", res)):
            ic = xs_ic(FF, Rh); rep = slice_report(ic, h + 5)
            rows.append(dict(feat=nm, form=form, h=h, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" if rep[k]["n"] > 30 else "n/a" for k in rep},
                             tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], c2=rep["C2"]["mean"], c3=rep["C3"]["mean"], n=rep["TRAIN"]["n"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_11_table.csv", index=False)
print(T.drop(columns=["tr", "t", "c2", "c3", "n"]).to_string(index=False))
print("\nshare of raw IC kept (TRAIN):")
for nm in base:
    for h in HORIZONS:
        raw = T[(T.feat == nm) & (T.form == "raw") & (T.h == h)].tr.iloc[0]
        print(nm, h, {f: round(T[(T.feat == nm) & (T.form == f) & (T.h == h)].tr.iloc[0] / raw, 2) for f in ("detrend", "detrend+resid")})
c = T[T.form == "detrend+resid"].copy(); c["score"] = -c.tr; c["ts"] = -c.t
b = c.sort_values("score", ascending=False).iloc[0]
tc = kit.tcrit_for(30)
print("\nBEST form (c):", b.feat, b.h, "score", round(b.score, 4), "t", round(b.ts, 2), "C2", round(b.c2, 4), "C3", round(b.c3, 4), "tcrit", round(tc, 2))
print("supported:", bool(b.score >= 0.02 and b.ts >= tc and b.c2 < 0 and b.c3 < 0), " refuted:", bool((c.score <= 0.01).all()))
print(c[["feat", "h", "score", "ts", "c2", "c3", "n"]].round(4).sort_values("score", ascending=False).head(8).to_string(index=False))
fig, ax = plt.subplots(figsize=(10, 4))
piv = T.pivot_table(index=["feat", "form"], columns="h", values="tr"); (-piv).plot.barh(ax=ax); ax.axvline(0.02, color="#e34948", ls="--", lw=.8); ax.set_title("H5 crowding score (-IC): raw vs detrended vs detrended+residual; red = min_useful")
fig.savefig("plots/cell_11_h5_controls.png", bbox_inches="tight")
