# Daily (UTC day) aggregation of the 1h panel, per slice. A day counts only if all 24 hourly returns exist.
import numpy as np, pandas as pd
def daily(P):
    r = P["r"]; g = r.index.floor("D")
    cnt = r.notna().groupby(g).sum(); R = r.groupby(g).sum(min_count=1).where(cnt == 24)
    V = P["vol"].groupby(g).sum(min_count=1).where(cnt == 24)
    QV = P["quote_vol"].groupby(g).sum(min_count=1).where(cnt == 24)
    live = R.notna().sum(axis=1)
    REL = R.sub(R.mean(axis=1), axis=0); REL[live < 5] = np.nan
    return R, REL, V, QV
