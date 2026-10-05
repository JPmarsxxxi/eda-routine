"""REPORT cost line for H1 (signal inputs only, slices H1 already opened): daily turnover of top/bottom-half membership
by Alpha#101 and the implied cost per day at TARGET.md round-trip costs (24h hold incl. one rollover night)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import run_lib as L
RT = {"BTC": 18.9, "ETH": 25.4, "LTC": 36.5, "ADA": 46, "DOGE": 46, "DOT": 46, "BNB": 46, "SOL": 46, "BCH": 65.5, "XRP": 68.6}
S = L.slices()
for sl in ["EXPLORE", "C1", "C2", "VAL"]:
    win = S[sl]; F = {k: {} for k in ["open", "high", "low", "close", "volume", "vwap"]}
    for c in L.COINS:
        b = L.load_binance(c, f"REPORT cost line H1 on {sl} (signal inputs only, slice already opened by H1)", (win[0] - pd.Timedelta(days=5), win[1]))
        if not len(b): continue
        db = L.daily_bars(b)
        for k in F: F[k][c] = db[k]
    P = {k: pd.DataFrame(v) for k, v in F.items()}
    s = L.alpha("A101", P); s = s[(s.index >= win[0]) & (s.index < win[1])]
    w = []
    for d, row in s.iterrows():
        a = row.dropna()
        if len(a) < 5: w.append(None); continue
        rk = a.rank(); mid = (len(a) + 1) / 2
        x = pd.Series(0.0, index=a.index); x[rk > mid] = 1 / (rk > mid).sum(); x[rk < mid] = -1 / (rk < mid).sum()
        w.append(x)
    W = pd.DataFrame([x if x is not None else pd.Series(dtype=float) for x in w], index=s.index).fillna(0)
    traded = W.diff().abs()                                   # fraction of each leg's 1-unit book traded per day
    cost = (traded * pd.Series(RT) / 2).sum(axis=1)           # one-way = half a round trip, bp of one leg
    print(f"{sl}: mean one-way traded per day (both legs, units of one leg) {traded.sum(axis=1).mean():.2f}; implied cost {cost.mean():.1f} bp/day")
