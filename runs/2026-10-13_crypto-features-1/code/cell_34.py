import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code"); sys.path.insert(0, r"C:\Users\User\eda-routine")
from fx import *
import importlib, json
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_34"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
PR = perp_hourly("cell_34", "premium"); L = make_long(B, PR["close"])
F = {f"f00{i}": unstack_feature(importlib.import_module(f"features.f00{i}").compute(L), ix) for i in range(1, 9)}
ret1 = lr.diff()
BL = {"b_rev1": -(lr - lr.shift(1)), "b_rev24": -(lr - lr.shift(24)), "b_mom168": (lr - lr.shift(168)), "b_lowvol": -ret1.rolling(168, min_periods=84).std(), "b_liq": np.log(S["quote_vol"].where(S["quote_vol"] > 0).rolling(720, min_periods=360).mean())}
ALL = {**F, **BL}
# f008 at three horizons by fold
for h in HORIZONS:
    ic = xs_ic(F["f008"], B.R[h]); print("f008 h%d:" % h, fmt_rep(slice_report(ic, h + 5)))
# correlation rows
for k in ("f008", "f004"):
    row = {}
    for b in ALL:
        if b == k: continue
        row[b] = float(xs_ic(ALL[k][tr], ALL[b][tr]).mean())
    s = pd.Series(row); print(f"\n{k} mean XS Spearman with others:", s.round(2).to_dict()); print("   max |corr|:", s.abs().idxmax(), round(float(s.abs().max()), 3))
    if k == "f008": mx = float(s.abs().max()); top2 = list(s.abs().sort_values(ascending=False).index[:2])
    if k == "f004": top2b = list(s.abs().sort_values(ascending=False).index[:2])
# incremental
res = {}
for k, t2 in (("f008", top2), ("f004", top2b)):
    r = residual_rank(F[k][tr], [ALL[t][tr] for t in t2])
    ic0 = xs_ic(F[k][tr], B.R[1][tr]); ic1 = xs_ic(r, B.R[1][tr])
    a, b = nw(ic0, 6), nw(ic1, 6); res[k] = (t2, a["mean"], b["mean"], b["t"])
    print(f"{k} h1: top2 {t2}; IC {a['mean']:+.4f} -> residual {b['mean']:+.4f} (t {b['t']:+.1f}); residual by fold:", fmt_rep(slice_report(ic1, 6)))
# cost line h1
RT = {"BTC": 18.9, "ETH": 25.4, "LTC": 36.5, "ADA": 46, "DOGE": 46, "DOT": 46, "BNB": 46, "SOL": 46, "BCH": 65.5, "XRP": 68.6}
cost = {}
for k in ("f008", "f004"):
    for h in (1,):
        Fs, Rs = F[k][tr], B.R[h][tr]; m = Fs.notna() & Rs.notna(); keep = m.sum(axis=1) >= 6
        Fv, Rv, mv = Fs[keep], Rs[keep], m[keep]
        rk = Fv.where(mv).rank(axis=1, ascending=False); nn = mv.sum(axis=1); top = rk.le(3); bot = rk.gt(nn - 3, axis=0)
        spread = (Rv.where(top).mean(axis=1) - Rv.where(bot).mean(axis=1)) * 1e4
        rtc = pd.Series(RT)[COINS]; tc_ = ((top | bot) * rtc.values).sum(axis=1) / (top | bot).sum(axis=1)
        cost[k] = (float(spread.mean()), float(2 * tc_.mean()), len(spread))
        print(f"{k} h{h}: gross top3-bottom3 {spread.mean():+.2f} bp (n {len(spread)}) cost {2*tc_.mean():.1f} bp -> net {spread.mean()-2*tc_.mean():+.1f} bp ->", "STANDALONE" if spread.mean() - 2 * tc_.mean() > 0 else "COMBINE-ONLY")
json.dump({"f008": {"max_corr": mx, "top2": top2, "inc": res["f008"], "cost": cost["f008"]}, "f004_h1": {"top2": top2b, "inc": res["f004"], "cost": cost["f004"]}}, open("work/cell34_stats.json", "w"), indent=1, default=float)
print("\nPRIMARY: max|corr| f008 =", round(mx, 3), " incremental h1 =", round(res["f008"][2], 4), "t", round(res["f008"][3], 2), " supported:", bool(mx < .5 and res["f008"][2] >= .015 and res["f008"][3] >= 1.96))
fig, ax = plt.subplots(figsize=(8, 4)); s = pd.Series({b: float(xs_ic(ALL["f008"][tr], ALL[b][tr]).mean()) for b in ALL if b != "f008"}); s.plot.barh(ax=ax); ax.set_title("f008 mean XS correlation with candidates and baselines")
fig.savefig("plots/cell_34_f008_corr.png", bbox_inches="tight")
