"""Shared helpers for features/f*.py. df is a LONG hourly frame with columns t (UTC bar open), coin and the carded columns below.
Every feature is point-in-time: row t uses bars <= t only (bar t is knowable at the END of bar t), trailing-only scaling."""
import numpy as np
import pandas as pd

CARDED = ["open", "high", "low", "close", "vol", "quote_vol", "n", "buy_vol", "prem_close"]


def wide(df, col):
    """pivot to a full hourly grid spanning the whole frame (same index and columns for every column of df)"""
    w = df.pivot_table(index="t", columns="coin", values=col, aggfunc="last", dropna=False)
    w.index = pd.to_datetime(w.index)
    t = pd.to_datetime(df["t"])
    full = pd.date_range(t.min(), t.max(), freq="h")
    return w.reindex(index=full, columns=sorted(df["coin"].unique()))


def stack(w, name):
    s = w.stack(future_stack=True) if hasattr(w, "stack") else w
    s.index.names = ["t", "coin"]
    return s.rename(name)


def residual_rank(F, Gs):
    """per row: cross-sectional rank of F residualised (OLS) on the cross-sectional ranks of every panel in Gs; rows with < 6 valid coins -> NaN"""
    m = F.notna()
    for g in Gs:
        m &= g.notna()
    A = F.where(m).rank(axis=1).values
    B = np.stack([g.where(m).rank(axis=1).values for g in Gs], axis=2)
    out = np.full(A.shape, np.nan)
    for i in range(A.shape[0]):
        a = A[i]; ok = ~np.isnan(a)
        if ok.sum() < 6:
            continue
        X = np.column_stack([np.ones(ok.sum()), B[i][ok]])
        beta, *_ = np.linalg.lstsq(X, a[ok], rcond=None)
        out[i, np.where(ok)[0]] = a[ok] - X @ beta
    return pd.DataFrame(out, index=F.index, columns=F.columns)
