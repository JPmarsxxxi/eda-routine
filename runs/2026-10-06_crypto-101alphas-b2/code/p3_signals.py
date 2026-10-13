"""Phase 3 SIGNALS.md inputs (TRAIN only = EXPLORE + C1..C3; VAL never touched): baseline correlations, market share,
signal-vs-signal correlation and IC-series correlation, for every hypothesis supported on >= 1 CONFIRM fold (H1, H6)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import common as C

F, R = C.cached()
c = F["close"]
rb = np.log(c / c.shift(1))
base = {"reversal_1d": -rb, "momentum_20d": np.log(c / c.shift(20)),
        "volatility_20d": rb.rolling(20, min_periods=15).std(),
        "volume_vs_20d": np.log(F["volume"]) - np.log(F["volume"]).rolling(20, min_periods=15).mean()}
SIG = {"S1": C.alpha30(F), "S2": -1 * C.alpha54(F)}
train = lambda df: df.loc[[(d >= C.SLICES["EXPLORE"][0]) and (d < C.SLICES["C3"][1]) for d in df.index]]
def xs(a, b):
    a, b = train(a), train(b).reindex(train(a).index)
    v = []
    for d in a.index:
        x, y = a.loc[d], b.loc[d]
        m = x.notna() & y.notna()
        if m.sum() >= C.MIN_COINS and x[m].nunique() > 1 and y[m].nunique() > 1:
            v.append(x[m].rank().corr(y[m].rank()))
    return float(np.mean(v))
out = {}
for k, S in SIG.items():
    z = train(C.trailing_z(S))
    r = train(rb)
    mk = pd.concat([z.mean(axis=1), r.mean(axis=1), r["BTCUSD"]], axis=1).dropna()
    out[k] = {"market": float(mk.iloc[:, 0].corr(mk.iloc[:, 1])), "btc": float(mk.iloc[:, 0].corr(mk.iloc[:, 2]))}
    out[k].update({b: xs(S, v) for b, v in base.items()})
    ics = []
    for sl in ["EXPLORE", "C1", "C2", "C3"]:
        Ss = S.loc[C.in_slice(S.index, sl)]
        ics.append(C.daily_rank_ic(Ss, C.response_in_slice(R, sl)))
    out[k]["_ic"] = pd.concat(ics)
pair = {"signal_corr": xs(SIG["S1"], SIG["S2"]),
        "ic_series_corr": float(pd.concat([out["S1"]["_ic"], out["S2"]["_ic"]], axis=1).dropna().corr().iloc[0, 1])}
for k in SIG:
    out[k].pop("_ic")
res = {"signals": out, "S1_vs_S2": pair}
json.dump(res, open(os.path.join(C.RUN, "tables", "p3_signals.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
