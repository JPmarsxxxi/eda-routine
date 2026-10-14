"""supplementary (not a cell): TRAIN top-3 minus bottom-3 forward 24h return of features/f009 for the cost line of candidate F10 and its correlations with the other candidates"""
import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code"); sys.path.insert(0, r"C:\Users\User\eda-routine")
from fx import *
import importlib, json
B = Base("supp_f009"); S = B.S; C = S["close"]; ix = C.index; tr = train_mask(ix)
PR = perp_hourly("supp_f009", "premium"); Fu = funding("supp_f009")[0]
L = make_long(B, PR["close"]); L = L.merge(pd.DataFrame({"t": ix.repeat(len(COINS)), "coin": list(COINS) * len(ix), "funding": Fu.values.ravel()}), on=["t", "coin"], how="left")
f9 = unstack_feature(importlib.import_module("features.f009").compute(L), ix)
ic = xs_ic(f9[tr], B.R[24][tr]); print("f009 h24:", fmt_rep(slice_report(ic, 29)))
RT = {"BTC": 18.9, "ETH": 25.4, "LTC": 36.5, "ADA": 46, "DOGE": 46, "DOT": 46, "BNB": 46, "SOL": 46, "BCH": 65.5, "XRP": 68.6}
Fs, Rs = f9[tr], B.R[24][tr]; m = Fs.notna() & Rs.notna(); keep = m.sum(axis=1) >= 6
Fv, Rv, mv = Fs[keep], Rs[keep], m[keep]; rk = Fv.where(mv).rank(axis=1, ascending=False); nn = mv.sum(axis=1); top = rk.le(3); bot = rk.gt(nn - 3, axis=0)
spread = (Rv.where(top).mean(axis=1) - Rv.where(bot).mean(axis=1)) * 1e4; rtc = pd.Series(RT)[COINS]; tc_ = ((top | bot) * rtc.values).sum(axis=1) / (top | bot).sum(axis=1)
print("gross top3-bottom3 %.2f bp (n %d); cost %.1f bp" % (spread.mean(), len(spread), 2 * tc_.mean()))
others = {}
for i in range(1, 9):
    o = unstack_feature(importlib.import_module(f"features.f00{i}").compute(L), ix); others[f"f00{i}"] = float(xs_ic(f9[tr], o[tr]).mean())
print({k: round(v, 3) for k, v in others.items()}); json.dump({"spread": float(spread.mean()), "n": len(spread), "cost": float(2 * tc_.mean()), "corr": others}, open("work/supp_f009.json", "w"))
