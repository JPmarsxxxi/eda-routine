import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_08"); S = B.S
q, n, bv, v = S["quote_vol"].where(S["quote_vol"] > 0), S["n"].where(S["n"] > 0), S["buy_vol"], S["vol"].where(S["vol"] > 0)


def surp(x, w):
    num = x.rolling(w, min_periods=max(1, int(.8 * w))).sum()
    base = x.shift(w).rolling(720, min_periods=360).mean()
    return np.log(num / (w * base))


def sizesurp(w):
    s = (q.rolling(w, min_periods=int(.8 * w)).sum() / n.rolling(w, min_periods=int(.8 * w)).sum())
    return np.log(s) - np.log(s).shift(w).rolling(720, min_periods=360).mean()


V = {}
for w in (1, 6, 24):
    V[f"volsurp_{w}"] = (surp(q, w), "h", -1); V[f"nsurp_{w}"] = (surp(n, w), "h", -1); V[f"sizesurp_{w}"] = (sizesurp(w), "h", -1)
    V[f"taker_{w}"] = (bv.rolling(w, min_periods=int(.8 * w)).sum() / v.rolling(w, min_periods=int(.8 * w)).sum() - 0.5, "h", +1)
V["volratio_d"] = (np.log(q.rolling(120, min_periods=100).sum() / q.rolling(480, min_periods=400).sum()), "h", -1)
dirs = {k: d for k, (_, _, d) in V.items()}
df, ics = sweep({k: (F, m) for k, (F, m, d) in V.items()}, B)
df["dir"] = df.variant.map(dirs)
for c in df.columns:
    if c.endswith("_ic"):
        df[c.replace("_ic", "_sc")] = df[c] * df["dir"]
df.to_csv("cells/cell_08_table.csv", index=False)
pd.set_option("display.width", 250)
out = df[["variant", "h", "dir"]].copy()
for nm in ("EXPLORE", "C1", "C2", "C3", "TRAIN"):
    out[nm] = [f"{a:+.4f}({b:+.1f})" for a, b in zip(df[f"{nm}_ic"], df[f"{nm}_t"])]
print(out.to_string(index=False))
d2 = df.copy(); d2["TRAIN_ic"] = d2["TRAIN_sc"]; d2["TRAIN_t"] = d2["TRAIN_t"] * d2["dir"]
vd = verdict(d2, 0.02, +1.0, V=39); print(vd)
print("best 8 by pre-stated-sign score:"); print(d2.sort_values("TRAIN_sc", ascending=False)[["variant", "h", "dir", "EXPLORE_sc", "C1_sc", "C2_sc", "C3_sc", "TRAIN_sc", "TRAIN_t"]].head(8).round(4).to_string(index=False))
print("\nbest 8 by absolute IC regardless of sign:"); print(df.assign(a=df.TRAIN_ic.abs()).sort_values("a", ascending=False)[["variant", "h", "EXPLORE_ic", "C1_ic", "C2_ic", "C3_ic", "TRAIN_ic", "TRAIN_t"]].head(8).round(4).to_string(index=False))
fig, ax = plt.subplots(figsize=(10, 4))
piv = df.pivot(index="variant", columns="h", values="TRAIN_ic"); ax.barh(piv.index, piv[6].values, color="#2a78d6"); ax.axvline(0, color="#9b9a94"); ax.set_title("H4 features: pooled-TRAIN IC at h=6")
fig.savefig("plots/cell_08_flow_ic.png", bbox_inches="tight")
