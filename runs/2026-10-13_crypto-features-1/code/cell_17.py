import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code"); sys.path.insert(0, r"C:\Users\User\eda-routine")
from fx import *
import importlib
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_17"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index
PR = perp_hourly("cell_17", "premium")
L = make_long(B, PR["close"])
mods = {f"f00{i}": importlib.import_module(f"features.f00{i}") for i in range(1, 8)}
F = {k: unstack_feature(m.compute(L), ix) for k, m in mods.items()}
# equality with the search-cell versions
r3s_search = -(lr.shift(1) - lr.shift(4)); f54_search = a54_roll(S)
print("max abs diff f001 vs search:", float((F["f001"] - r3s_search).abs().max().max()), " f005 vs search:", float((F["f005"] - f54_search).abs().max().max()))
# baselines
ret1 = lr.diff()
BL = {"b_rev1": -(lr - lr.shift(1)), "b_rev24": -(lr - lr.shift(24)), "b_mom168": (lr - lr.shift(168)), "b_lowvol": -ret1.rolling(168, min_periods=84).std(), "b_liq": np.log(S["quote_vol"].where(S["quote_vol"] > 0).rolling(720, min_periods=360).mean())}
ALL = {**F, **BL}
PRIM = {"f001": 6, "f002": 6, "f003": 24, "f004": 24, "f005": 24, "f006": 6, "f007": 24}
tr = train_mask(ix)
# IC table all horizons
rows = []
for k in F:
    mode = "d" if k in ("f006", "f007") else "h"
    for h in HORIZONS:
        ic = xs_ic(sample(F[k], mode), sample(B.R[h], mode)); rep = slice_report(ic, hl(h, mode))
        rows.append(dict(f=k, h=h, prim="*" if PRIM[k] == h else "", **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}))
print(pd.DataFrame(rows).to_string(index=False))
# pairwise corr on shared timestamps (train rows)
names = list(ALL)
M = pd.DataFrame(index=names, columns=names, dtype=float)
for a in names:
    for b in names:
        if a <= b:
            x = xs_ic(ALL[a][tr], ALL[b][tr], min_n=6).mean()
            M.loc[a, b] = M.loc[b, a] = x
pd.set_option("display.width", 250)
print("\nmean XS Spearman correlation (shared timestamps, TRAIN):"); print(M.round(2).to_string())
M.to_csv("cells/cell_17_corr.csv")
maxc = {}
for k in F:
    o = M.loc[k].drop(k); o_lib = o.drop([b for b in BL]); o_base = o[[b for b in BL]]
    maxc[k] = (o.abs().idxmax(), float(o.abs().max()))
    print(k, "max |corr| overall:", maxc[k], "| vs candidates:", (o_lib.abs().idxmax(), round(float(o_lib.abs().max()), 2)), "| vs baselines:", (o_base.abs().idxmax(), round(float(o_base.abs().max()), 2)))
# incremental IC
inc = {}
for k in F:
    o = M.loc[k].drop(k).abs().sort_values(ascending=False)
    top2 = list(o.index[:2]); h = PRIM[k]; mode = "d" if k in ("f006", "f007") else "h"
    res = residual_rank(F[k][tr], [ALL[t][tr] for t in top2])
    ic0 = xs_ic(sample(F[k][tr], mode), sample(B.R[h][tr], mode)); ic1 = xs_ic(sample(res, mode), sample(B.R[h][tr], mode))
    r0, r1 = nw(ic0, hl(h, mode)), nw(ic1, hl(h, mode)); inc[k] = (top2, r0["mean"], r1["mean"], r1["t"])
    print(f"{k} h{h}: top2 corr {top2} ({o.iloc[0]:.2f},{o.iloc[1]:.2f}); IC {r0['mean']:+.4f} -> residual IC {r1['mean']:+.4f} (t {r1['t']:+.1f})")
# cost line: top-3 minus bottom-3 forward return, bp
RT = {"BTC": 18.9, "ETH": 25.4, "LTC": 36.5, "ADA": 46, "DOGE": 46, "DOT": 46, "BNB": 46, "SOL": 46, "BCH": 65.5, "XRP": 68.6}
print("\ncost line (TRAIN): top3-bottom3 spread (bp) per signal at primary h vs 2 x mean RT of traded names")
cost = {}
for k in F:
    h = PRIM[k]; mode = "d" if k in ("f006", "f007") else "h"
    Fs, Rs = sample(F[k][tr], mode), sample(B.R[h][tr], mode)
    m = Fs.notna() & Rs.notna(); keep = m.sum(axis=1) >= 6
    Fv, Rv, mv = Fs[keep], Rs[keep], m[keep]
    rk = Fv.where(mv).rank(axis=1, ascending=False); nn = mv.sum(axis=1)
    top = rk.le(3); bot = rk.gt(nn - 3, axis=0)
    spread = (Rv.where(top).mean(axis=1) - Rv.where(bot).mean(axis=1)) * 1e4
    rtc = pd.Series(RT)[COINS]
    traded_cost = ((top | bot) * rtc.values).sum(axis=1) / (top | bot).sum(axis=1)
    net = spread - 2 * traded_cost
    cost[k] = (float(spread.mean()), float(2 * traded_cost.mean()), float(net.mean()), len(spread))
    print(f"{k}: h{h} gross top3-bottom3 {spread.mean():+.2f} bp (n {len(spread)}) cost {2*traded_cost.mean():.1f} bp -> net {net.mean():+.1f} bp  ->", "STANDALONE" if net.mean() > 0 else "COMBINE-ONLY")
import json
json.dump({"max_corr": maxc, "inc": {k: v for k, v in inc.items()}, "cost": cost}, open("work/cell17_stats.json", "w"), indent=1, default=float)
fig, ax = plt.subplots(figsize=(8, 6)); im = ax.imshow(M.values.astype(float), cmap="RdBu_r", vmin=-1, vmax=1); ax.set_xticks(range(len(names))); ax.set_xticklabels(names, rotation=90); ax.set_yticks(range(len(names))); ax.set_yticklabels(names); plt.colorbar(im)
ax.set_title("mean XS Spearman correlation, candidates + baselines"); fig.savefig("plots/cell_17_corr.png", bbox_inches="tight")
