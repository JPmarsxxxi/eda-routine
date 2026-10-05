# Claim-specific helpers for THIS session's tests (H1-H5). Built only from files that also exist in VAL
# (spot 30m, perp metrics, DVOL, funding, half_bp) so a CONFIRM rule can be re-run unchanged on VAL.
from common import *

def hourly(cell, lo, hi, warm_days=31):
    """Hourly open-stamped frame on [lo, hi] plus warm-up history (for trailing controls only).
    Row t = hour [t, t+1h), knowable at t+1h. Columns:
      r      spot log return of hour t (30m file, consecutive bars only)
      rv24f  log sqrt(sum sq 30m spot returns in (t+1h, t+25h])   - FORWARD, the response
      rv24b, rv7d, rv30d  trailing log RV (per-day scale) ending t+1h - controls
      r24f   spot log return (t+1h, t+25h]
      dvol   DVOL close of hour t;  basis  mean of the two 30m-mark basis snapshots in hour t (bp)
    """
    lo_w = lo - pd.Timedelta(days=warm_days)
    m30 = load(PERP_30M, cell, use=["close"], lo=lo_w, hi=hi)["close"]
    grid30 = pd.date_range(m30.index.min(), m30.index.max(), freq="30min")
    c30 = m30.reindex(grid30)
    r30 = np.log(c30).diff()                                   # return of 30m bar ending at its stamp+30m, stamped at bar open
    # stamp returns at bar END time for clean windows
    r30_end = pd.Series(r30.values, index=grid30 + pd.Timedelta("30min"))  # value knowable at index time
    sq = r30_end ** 2
    # hour grid
    H = pd.date_range(lo_w.ceil("h"), hi.floor("h"), freq="h")
    t1 = H + pd.Timedelta("1h")                                 # knowable time
    cs = sq.fillna(0).cumsum(); cnt = sq.notna().astype(int).cumsum()
    def win(a, b):   # sum over (a, b]
        s = cs.reindex(b, method="ffill").values - cs.reindex(a, method="ffill").values
        n = cnt.reindex(b, method="ffill").values - cnt.reindex(a, method="ffill").values
        return s, n
    F = pd.DataFrame(index=H)
    s, n = win(t1, t1 + pd.Timedelta("24h")); F["rv24f"] = np.where(n >= 44, 0.5 * np.log(s * 48 / np.maximum(n, 1)), np.nan)
    s, n = win(t1 - pd.Timedelta("24h"), t1); F["rv24b"] = np.where(n >= 44, 0.5 * np.log(s * 48 / np.maximum(n, 1)), np.nan)
    s, n = win(t1 - pd.Timedelta("7D"), t1); F["rv7d"] = np.where(n >= 300, 0.5 * np.log(s * 48 / np.maximum(n, 1)), np.nan)
    s, n = win(t1 - pd.Timedelta("30D"), t1); F["rv30d"] = np.where(n >= 1200, 0.5 * np.log(s * 48 / np.maximum(n, 1)), np.nan)
    ch = c30.reindex(H + pd.Timedelta("30min"))                 # close of hour t = close of 2nd 30m bar
    F["close"] = ch.values
    F["r"] = np.log(F["close"]).diff()
    F["r24f"] = np.log(c30.reindex(t1 + pd.Timedelta("23h30min")).values / c30.reindex(t1 - pd.Timedelta("30min")).values)
    # perp metrics close of the 5m bar ending at each 30m mark X (create_time X-5min) vs spot 30m bar ending at X
    mt = load(METRICS, cell, use=["c"], lo=lo_w, hi=hi)["c"]
    marks = grid30 + pd.Timedelta("30min")
    perp_at = mt.reindex(marks - pd.Timedelta("5min")).values
    b30 = pd.Series(1e4 * np.log(perp_at / c30.values), index=marks)   # basis snapshot knowable at mark
    F["basis"] = pd.concat([b30.reindex(H + pd.Timedelta("30min")).rename("a").reset_index(drop=True),
                            b30.reindex(t1).rename("b").reset_index(drop=True)], axis=1).mean(axis=1, skipna=False).values
    try:
        dv = load(DVOL, cell, use=["close"], lo=lo_w, hi=hi)["close"]
        F["dvol"] = dv.reindex(H).values
    except G.HygieneError:
        F["dvol"] = np.nan
    return F, b30, c30

def resid_ranks(df, x, y, ctrl):
    import statsmodels.api as sm
    d = df[[x, y] + ctrl].replace([np.inf, -np.inf], np.nan).dropna()
    rk = d.rank()
    if ctrl:
        Xc = sm.add_constant(rk[ctrl])
        ex = sm.OLS(rk[x], Xc).fit().resid; ey = sm.OLS(rk[y], Xc).fit().resid
    else:
        ex, ey = rk[x] - rk[x].mean(), rk[y] - rk[y].mean()
    return (ex / ex.std()), (ey / ey.std())

def block_boot_corr(ex, ey, block=240, reps=2000, seed=0, n_out=None):
    """Moving-block bootstrap distribution of corr(ex, ey) (both standardized); returns array of resampled corrs."""
    rng = np.random.default_rng(seed)
    a, b = np.asarray(ex), np.asarray(ey); n = len(a); n_out = n_out or n
    nb = int(np.ceil(n_out / block)); out = np.empty(reps)
    for i in range(reps):
        st = rng.integers(0, n - block, nb)
        idx = (st[:, None] + np.arange(block)[None, :]).ravel()[:n_out]
        out[i] = np.corrcoef(a[idx], b[idx])[0, 1]
    return out
