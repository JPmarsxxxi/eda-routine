import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_03"); Dd = B.D; ix = B.P.index
feats = {
 "seed": to_hourly(a30_daily(Dd, 3, 5, 20, True), ix),
 "streak": to_hourly(a30_daily(Dd, 3, 5, 20, False), ix),
 "volratio": to_hourly(Dd["V"].rolling(5).sum() / Dd["V"].rolling(20).sum(), ix),
 "volratio_neg": to_hourly(-(Dd["V"].rolling(5).sum() / Dd["V"].rolling(20).sum()), ix),
 "r24": -np.log(B.S["close"] / B.S["close"].shift(24)),
}
ics = {}
rows = []
for name, F in feats.items():
    for resp, RR in (("prim", B.R), ("binance", B.RB)):
        for h in HORIZONS:
            ic = xs_ic(sample(F, "d"), sample(RR[h], "d")); ics[(name, resp, h)] = ic
            rep = slice_report(ic, h // 24 + 3)
            rows.append(dict(feature=name, resp=resp, h=h, **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}))
print(pd.DataFrame(rows).to_string(index=False))
print("\nPRIMARY: IC(seed)-IC(streak) paired per-day (primary response):")
for h in (6, 24):
    d = (ics[("seed", "prim", h)] - ics[("streak", "prim", h)]); d = d[train_mask(d.index)]
    r = nw(d, h // 24 + 3); print(h, round(r["mean"], 4), round(r["t"], 2), r["n"])
print("\nSECONDARY response switch: IC(Binance resp) - IC(primary resp), C2+C3 only:")
c23 = lambda s: s[in_slice(s.index, "C2") | in_slice(s.index, "C3")]
for name in ("streak", "r24", "seed"):
    for h in (1, 6, 24):
        d = c23(ics[(name, "binance", h)] - ics[(name, "prim", h)]); r = nw(d, h // 24 + 3)
        print(name, h, round(r["mean"], 4), round(r["t"], 2), r["n"])
print("\nresponse correlation: share of C2/C3 days where Binance-close and primary 6h returns agree in cross-sectional rank (mean XS Spearman):")
for h in (6, 24):
    x = xs_ic(sample(B.R[h], "d"), sample(B.RB[h], "d")); print(h, {nm: round(float(x[in_slice(x.index, nm)].mean()), 4) for nm in SLICES})
