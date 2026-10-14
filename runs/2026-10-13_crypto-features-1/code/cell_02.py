import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_02")
S = B.S; C = S["close"]
tr = train_mask(C.index)
streak = {k: a30_roll(S, k, 5, 20, False) for k in (1, 2, 3, 5, 7)}
r24 = -np.log(C / C.shift(24))   # fade direction: low past return -> high rank
res = {}
heat = {}
for h in HORIZONS:
    ic = xs_ic(streak[3], B.R[h]); ic = ic[tr]
    heat[h] = ic.groupby(ic.index.hour).apply(lambda x: nw(x, h // 24 + 3))
tab = pd.DataFrame({h: [heat[h][a]["mean"] for a in range(24)] for h in HORIZONS}); tabt = pd.DataFrame({h: [heat[h][a]["t"] for a in range(24)] for h in HORIZONS})
print("streak-3 IC by anchor hour (rows) x horizon (cols), TRAIN:"); print(pd.concat([tab.round(4), tabt.round(1).add_prefix("t")], axis=1).to_string())
# paired contrast anchor 23 vs others at each horizon
con = {}
for h in HORIZONS:
    ic = xs_ic(streak[3], B.R[h])[tr]
    d = ic.groupby(ic.index.floor("D"))
    a23 = ic[ic.index.hour == 23]; a23.index = a23.index.floor("D")
    oth = ic[ic.index.hour != 23].groupby(ic[ic.index.hour != 23].index.floor("D")).mean()
    diff = (a23 - oth).dropna()
    con[h] = nw(diff, h // 24 + 3)
print("paired diff IC(anchor23) - mean IC(other anchors):", {h: (round(v["mean"], 4), round(v["t"], 2)) for h, v in con.items()})
# streak-length sweep at anchor 23 (daily sampling)
rows = []
for k, F in streak.items():
    for h in HORIZONS:
        ic = xs_ic(sample(F, "d"), sample(B.R[h], "d")); rep = slice_report(ic, h // 24 + 3)
        rows.append(dict(k=k, h=h, **{nm: round(rep[nm]["mean"], 4) for nm in rep}, tr_t=round(rep["TRAIN"]["t"], 2)))
print("\nstreak length sweep at anchor 23:"); print(pd.DataFrame(rows).to_string(index=False))
# rival control: residualise on trailing-24h return rank (anchor 23 only, to keep it fast)
F23 = sample(streak[3], "d"); r23 = sample(r24, "d")
res_rank = residual_rank(F23[train_mask(F23.index)], [r23.reindex(F23.index)[train_mask(F23.index)]])
rows2 = []
for h in HORIZONS:
    R23 = sample(B.R[h], "d")
    for nm, F in (("streak3", F23), ("r24 only", r23), ("streak3 | r24", res_rank)):
        ic = xs_ic(F.reindex(R23.index), R23); rep = slice_report(ic, h // 24 + 3)
        rows2.append(dict(feature=nm, h=h, **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}))
print("\nrival control (anchor 23):"); print(pd.DataFrame(rows2).to_string(index=False))
print("corr streak3 vs r24 (mean XS Spearman, anchor 23):", round(float(xs_ic(F23, r23.reindex(F23.index)).mean()), 3))
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
for i, h in enumerate(HORIZONS):
    ax[i].bar(range(24), tab[h].values, color=["#e34948" if a == 23 else "#2a78d6" for a in range(24)]); ax[i].axhline(0, color="#9b9a94", lw=.8); ax[i].set_title(f"streak-3 rank IC by anchor hour, h={h}")
fig.savefig("plots/cell_02_anchor_hour.png", bbox_inches="tight")
a23h6 = heat[6][23]
print("PRIMARY: IC anchor23 h6 =", round(a23h6["mean"], 4), "diff =", round(con[6]["mean"], 4), "t =", round(con[6]["t"], 2))
