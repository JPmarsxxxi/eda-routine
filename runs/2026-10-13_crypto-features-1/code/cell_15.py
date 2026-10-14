import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_15"); S = B.S; Dd = B.D; ix = B.P.index; C = S["close"]; tr = train_mask(ix)
O, H, L, Cd = Dd["O"], Dd["H"], Dd["L"], Dd["C"]
rng = (H - L).where((H - L) > 0)
clv_d = to_hourly((Cd - L) / rng, ix); oc5_d = to_hourly((O / Cd) ** 5, ix)
rngh = (S["high"].rolling(24, min_periods=22).max() - S["low"].rolling(24, min_periods=22).min()); rngh = rngh.where(rngh > 0)
clv_r = (C - S["low"].rolling(24, min_periods=22).min()) / rngh; oc5_r = (S["open"].shift(23) / C) ** 5
r24p = np.log(C / C.shift(24))
V = {"f54_daily": (to_hourly(a54_daily(Dd), ix), "d"), "f54_roll": (a54_roll(S), "h"), "clv_daily": (clv_d, "d"), "clv_roll": (clv_r, "h"),
     "oc5_daily": (oc5_d, "d"), "oc5_roll": (oc5_r, "h"), "r24_cont": (r24p, "h")}
df, ics = sweep(V, B)
# residual form
res = residual_rank(V["f54_roll"][0][tr], [r24p[tr]])
rows = []
for h in HORIZONS:
    ic = xs_ic(res, B.R[h][tr]); rep = slice_report(ic, h + 5)
    rows.append(dict(variant="f54_roll|r24", mode="h", h=h, **{f"{n}_ic": rep[n]["mean"] for n in rep}, **{f"{n}_t": rep[n]["t"] for n in rep}, n_train=rep["TRAIN"]["n"]))
df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
df.to_csv("cells/cell_15_table.csv", index=False)
print(show(df))
prim = df[df.variant.isin(["f54_daily", "f54_roll"])]
vd = verdict(prim, 0.02, +1.0, V=6); print(vd)
print("market corr f54_roll h24:", mkt_corr(V["f54_roll"][0], B, 24, "h"))
print("mean XS corr f54_roll vs r24_cont:", round(float(xs_ic(V["f54_roll"][0], r24p).mean()), 3), " vs clv_roll:", round(float(xs_ic(V["f54_roll"][0], clv_r).mean()), 3))
fig, ax = plt.subplots(figsize=(9, 4))
piv = df.pivot(index="variant", columns="h", values="TRAIN_ic"); piv.plot.barh(ax=ax); ax.axvline(0.02, color="#e34948", ls="--", lw=.8); ax.axvline(0, color="#9b9a94"); ax.set_title("H2 f54 family, pooled TRAIN IC (red = min_useful)")
fig.savefig("plots/cell_15_f54.png", bbox_inches="tight")
