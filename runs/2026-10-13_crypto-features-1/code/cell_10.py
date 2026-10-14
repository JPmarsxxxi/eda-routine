import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_10"); S = B.S; C = S["close"]
Fu, W = funding("cell_10"); K = perp_hourly("cell_10", "klines"); PR = perp_hourly("cell_10", "premium"); M = metrics_hourly("cell_10")
oi = M["sum_open_interest"].where(M["sum_open_interest"] > 0); oiv = M["sum_open_interest_value"].where(M["sum_open_interest_value"] > 0)
lg = np.log
F = {
 "funding_lvl": (Fu, -1), "funding_chg_24": (Fu - Fu.shift(24), -1),
 "prem_lvl": (PR["close"], -1), "prem_chg_6": (PR["close"] - PR["close"].shift(6), -1),
 "basis_lvl": (K["close"] / C - 1, -1), "basis_chg_6": ((K["close"] / C - 1) - (K["close"] / C - 1).shift(6), -1),
 "oi_chg_6": (lg(oi / oi.shift(6)), -1), "oi_chg_24": (lg(oi / oi.shift(24)), -1), "oi_val_chg_24": (lg(oiv / oiv.shift(24)), -1),
 "ls_acct_lvl": (M["count_long_short_ratio"], -1), "ls_chg_24": (lg(M["count_long_short_ratio"] / M["count_long_short_ratio"].shift(24)), -1),
 "ls_top_lvl": (M["count_toptrader_long_short_ratio"], -1), "taker_ls_lvl": (lg(M["sum_taker_long_short_vol_ratio"].where(M["sum_taker_long_short_vol_ratio"] > 0)), +1),
}
df, ics = sweep({k: (v, "h") for k, (v, d) in F.items()}, B)
df["dir"] = df.variant.map({k: d for k, (v, d) in F.items()})
df.to_csv("cells/cell_10_table.csv", index=False)
pd.set_option("display.width", 250)
out = df[["variant", "h", "dir"]].copy()
for nm in ("EXPLORE", "C1", "C2", "C3", "TRAIN"):
    out[nm] = [f"{a:+.4f}({b:+.1f})" if b == b else "n/a" for a, b in zip(df[f"{nm}_ic"], df[f"{nm}_t"])]
print(out.to_string(index=False))
print("\ncoverage (hours with >=6 coins and an IC) by fold, per feature:")
for k, (v, d) in F.items():
    ic = ics[(k, 6)]
    print(k, {nm: int(ic[in_slice(ic.index, nm)].notna().sum()) for nm in SLICES})
d2 = df.copy(); d2["TRAIN_ic"] = d2["TRAIN_ic"] * d2["dir"]; d2["TRAIN_t"] = d2["TRAIN_t"] * d2["dir"]
d2["C2s"] = d2["C2_ic"] * d2["dir"]; d2["C3s"] = d2["C3_ic"] * d2["dir"]
d2 = d2.dropna(subset=["TRAIN_ic"])
best = d2.sort_values("TRAIN_ic", ascending=False).head(10)
print("\nbest by pre-stated-sign pooled score:"); print(best[["variant", "h", "dir", "C2s", "C3s", "TRAIN_ic", "TRAIN_t", "n_train"]].round(4).to_string(index=False))
d2["ok"] = (d2.TRAIN_ic >= 0.02) & (d2.TRAIN_t >= kit.tcrit_for(39)) & (d2.C2s > 0) & (d2.C3s > 0)
print("variants passing the rule:", d2[d2.ok][["variant", "h"]].values.tolist())
fig, ax = plt.subplots(figsize=(10, 4))
piv = df.assign(s=df.TRAIN_ic * df.dir).pivot(index="variant", columns="h", values="s"); piv.plot.barh(ax=ax); ax.axvline(0, color="#9b9a94"); ax.axvline(0.02, color="#e34948", ls="--", lw=.8)
ax.set_title("H5 positioning: pooled score (pre-stated direction); red = min_useful"); fig.savefig("plots/cell_10_positioning.png", bbox_inches="tight")
