"""Phase 1 assumption check, SIGNAL INPUTS ONLY (Binance OHLCV; no response is loaded): on how many days per slice does
each alpha vary across >= 5 coins (a degenerate all-tied cross-section cannot be sorted into halves)?"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import run_lib as L
S = L.slices()
win = (S["EXPLORE"][0] - pd.Timedelta(days=40), S["C3"][1])
F = {k: {} for k in ["open", "high", "low", "close", "volume", "vwap"]}
for c in L.COINS:
    db = L.daily_bars(L.load_binance(c, "Phase 1 signal-coverage check (signal inputs only, no response)", win))
    for k in F: F[k][c] = db[k]
P = {k: pd.DataFrame(v) for k, v in F.items()}
rows = []
for a in ["A101", "A42", "A2", "A6", "A4"]:
    sig = L.alpha(a, P)
    r = [a]
    for name in ["EXPLORE", "C1", "C2", "C3"]:
        lo, hi = S[name]
        s = sig[(sig.index >= lo) & (sig.index < hi)]
        ok = (s.notna().sum(axis=1) >= L.MIN_COINS)
        nondeg = ok & (s.round(12).nunique(axis=1) >= 2)
        r += [f"{int(nondeg.sum())}/{int(ok.sum())}"]
    rows.append(r)
t = pd.DataFrame(rows, columns=["alpha", "EXPLORE", "C1", "C2", "C3"])
print("non-degenerate days / days with >= 5 coins having a signal")
print(L.md(t))
open(os.path.join(L.RUN, "code", "signal_coverage.md"), "w").write("non-degenerate days / days with >= 5 coins having a signal (signal inputs only)\n\n" + L.md(t) + "\n")
