import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_07"); C = B.S["close"]; lr = np.log(C); ix = C.index
rev3s = -(lr.shift(1) - lr.shift(4)); rev24s = -(lr.shift(1) - lr.shift(25))
ret1 = lr.diff(); mkt1 = ret1.mean(axis=1)
mvol = mkt1.rolling(168, min_periods=84).std()
cuts = mvol[in_slice(ix, "EXPLORE")].quantile([1 / 3, 2 / 3]).values
mvt = pd.Series(np.where(mvol <= cuts[0], 0, np.where(mvol <= cuts[1], 1, 2)), index=ix).where(mvol.notna())
sess = pd.Series("other", index=ix)
hr = ix.hour
sess[np.isin(hr, [21, 22, 23, 0, 1])] = "ASIA"; sess[np.isin(hr, [7, 8, 9, 10, 11])] = "EU"; sess[np.isin(hr, [13, 14, 15, 16])] = "US"
m3 = mkt1.rolling(3).sum(); move = pd.Series(np.where(m3 < -0.005, "down", np.where(m3 > 0.005, "up", "flat")), index=ix).where(m3.notna())
vol = ret1.rolling(168, min_periods=84).std(); hv = vol.gt(vol.median(axis=1), axis=0).where(vol.notna())
tr = train_mask(ix)


def cond_ic(F, R, mask_rows=None, coin_mask=None):
    """xs_ic restricted to rows in mask_rows (bool Series) and, if given, to coins in coin_mask (bool DataFrame)"""
    F2 = F.where(coin_mask) if coin_mask is not None else F
    R2 = R.where(coin_mask) if coin_mask is not None else R
    ic = xs_ic(F2, R2, min_n=4 if coin_mask is not None else 6)
    if mask_rows is not None:
        ic = ic[mask_rows.reindex(ic.index).fillna(False).values]
    return ic


rows = []; store = {}
for fn, F in (("rev3s", rev3s), ("rev24s", rev24s)):
    for h in HORIZONS:
        R = B.R[h]; L = h + 5
        conds = {"mvol_low": (mvt == 0), "mvol_mid": (mvt == 1), "mvol_high": (mvt == 2),
                 "ASIA": sess == "ASIA", "EU": sess == "EU", "US": sess == "US", "other": sess == "other",
                 "move_down": move == "down", "move_flat": move == "flat", "move_up": move == "up"}
        for cn, m in conds.items():
            ic = cond_ic(F, R, m); store[(fn, h, cn)] = ic
            rep = slice_report(ic, L); rows.append(dict(f=fn, h=h, cond=cn, **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}, n=rep["TRAIN"]["n"], tr=rep["TRAIN"]["mean"]))
        for cn, cm in (("ownvol_high", hv == True), ("ownvol_low", hv == False)):
            ic = cond_ic(F, R, None, cm); store[(fn, h, cn)] = ic
            rep = slice_report(ic, L); rows.append(dict(f=fn, h=h, cond=cn, **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}, n=rep["TRAIN"]["n"], tr=rep["TRAIN"]["mean"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_07_table.csv", index=False)
print(T.drop(columns="tr").to_string(index=False))
print("\nPRIMARY (rev3s): IC(mvol_high) - IC(mvol_low), paired by day, NW:")
for h in (1, 6):
    a = store[("rev3s", h, "mvol_high")]; b = store[("rev3s", h, "mvol_low")]
    da = a.groupby(a.index.floor("D")).mean(); db = b.groupby(b.index.floor("D")).mean()
    d = (da - db).dropna(); d = d[train_mask(d.index)]
    r = nw(d, 3); print(h, round(r["mean"], 4), round(r["t"], 2), r["n"])
print("\nauxiliary paired differences (rev3s h6): session ASIA-US, move_down-move_up, ownvol_high - low")
for (x, y) in (("ASIA", "US"), ("move_down", "move_up"), ("ownvol_high", "ownvol_low"), ("mvol_high", "mvol_mid")):
    for h in (1, 6):
        a = store[("rev3s", h, x)]; b = store[("rev3s", h, y)]
        da = a.groupby(a.index.floor("D")).mean(); db = b.groupby(b.index.floor("D")).mean()
        d = (da - db).dropna(); d = d[train_mask(d.index)]; r = nw(d, 3); print(x, "-", y, h, round(r["mean"], 4), round(r["t"], 2), r["n"])
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
for i, h in enumerate((1, 6)):
    sub = T[(T.f == "rev3s") & (T.h == h)]; ax[i].barh(sub.cond, sub.tr, color="#2a78d6"); ax[i].set_title(f"rev3s pooled-TRAIN IC by condition, h={h}"); ax[i].axvline(0, color="#9b9a94", lw=.8)
fig.savefig("plots/cell_07_conditions.png", bbox_inches="tight")
