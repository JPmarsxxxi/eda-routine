# Test statistics shared by the power simulations and the real cells (same function both places, so the simulated power is
# the power of the exact statistic that is run).
import numpy as np, pandas as pd
from scipy import stats

def nscore(X):
    """per-column normal scores over the whole slice (robust to the fat tails in OBSERVATIONS #1)."""
    X = pd.DataFrame(X)
    R = X.rank(pct=True) * X.count() / (X.count() + 1)
    return pd.DataFrame(stats.norm.ppf(R), index=X.index, columns=X.columns)

def nw_se(c, lags=2):
    c = np.asarray(c, float); c = c[~np.isnan(c)]; n = len(c); d = c - c.mean()
    g0 = d @ d / n; s = g0
    for L in range(1, lags + 1):
        s += 2 * (1 - L / (lags + 1)) * (d[L:] @ d[:-L]) / n
    return np.sqrt(max(s, 1e-18) / n), n

def lag_ic(X, lag, cluster=None, transform=True):
    """Pooled IC between X_t and X_{t+lag} (per column), clustered: c_k = mean of x*y within cluster k (cluster labels
    indexed like X; default = each row its own cluster). Returns ic, se, z, n_clusters."""
    Z = nscore(X) if transform else (X - X.mean()) / X.std()
    Y = Z.shift(-lag)
    prod = (Z * Y)
    if cluster is None:
        c = prod.mean(axis=1)
    else:
        cl = np.asarray(cluster)
        c = prod.sum(axis=1, min_count=1).groupby(cl).sum(min_count=1) / prod.notna().sum(axis=1).groupby(cl).sum().replace(0, np.nan)
    c = c.dropna(); se, n = nw_se(c.values)
    return c.mean(), se, c.mean() / se, n

def diff_ic(X, lag, high_mask):
    """IC on 'high' rows minus IC on the other rows (row = time unit), Welch t on the per-row c_t."""
    Z = nscore(X); c = (Z * Z.shift(-lag)).mean(axis=1)
    hm = pd.Series(high_mask, index=X.index).reindex(c.index).fillna(False).astype(bool)
    a, b = c[hm].dropna(), c[~hm].dropna()
    d = a.mean() - b.mean(); se = np.sqrt(a.var() / len(a) + b.var() / len(b))
    return d, se, d / se, (len(a), len(b))

def fm_interaction(Y, A, B, min_n=8):
    """Daily Fama-MacBeth: cross-sectional OLS of Y on zA, zB, zA*zB (z = cross-sectional standardization); returns mean b3,
    NW se, z, n_days. Y in return units (e.g. log return), so b3 is in return units per 1sd x 1sd."""
    b3 = []
    for t in Y.index:
        y, a, b = Y.loc[t], A.loc[t], B.loc[t]
        m = y.notna() & a.notna() & b.notna()
        if m.sum() < min_n: b3.append(np.nan); continue
        za = (a[m] - a[m].mean()) / a[m].std(); zb = (b[m] - b[m].mean()) / b[m].std()
        Xm = np.column_stack([np.ones(m.sum()), za, zb, za * zb])
        coef = np.linalg.lstsq(Xm, y[m].values, rcond=None)[0]; b3.append(coef[3])
    s = pd.Series(b3, index=Y.index).dropna(); se, n = nw_se(s.values)
    return s.mean(), se, s.mean() / se, n

def diff_ic_clustered(X, lag, high_mask, cluster):
    """IC (normal-score, X_t vs X_{t+lag}) on clusters flagged high minus on the other clusters; one c per cluster; Welch t.
    high_mask is per ROW of X (known at the conditioning row); a cluster is 'high' if its rows are flagged (first row)."""
    Z = nscore(X); prod = Z * Z.shift(-lag); cl = np.asarray(cluster)
    c = prod.sum(axis=1, min_count=1).groupby(cl).sum(min_count=1) / prod.notna().sum(axis=1).groupby(cl).sum().replace(0, np.nan)
    hm = pd.Series(np.asarray(high_mask, bool)).groupby(cl).first().reindex(c.index)
    a, b = c[hm.values].dropna(), c[~hm.values].dropna()
    d = a.mean() - b.mean(); se = np.sqrt(a.var() / len(a) + b.var() / len(b))
    return d, se, d / se, (len(a), len(b))
