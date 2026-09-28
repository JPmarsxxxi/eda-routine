"""Shared helpers for this EDA run. TRAIN-only loader; VAL is loaded only by s6_val.py."""
import os, sys, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, r"C:\Users\User\backtest_engine\backtest_engine2")
from cellplot import PAL, GRAY, DIV, setup  # palette + style only (plots saved with our own naming)
setup()

RUN = r"C:\Users\User\eda-routine\runs\2026-09-25_btc-spot-1m-clean"
DATA = r"C:\Users\User\eda-routine\data\btcusdt_spot_1m_clean\btcusdt_spot_1m_clean.parquet"
TRAIN_END = pd.Timestamp("2023-03-19 23:59:59", tz="UTC")
VAL_START = pd.Timestamp("2023-03-25 00:00:00", tz="UTC")
VAL_END = pd.Timestamp("2023-11-30 23:59:59", tz="UTC")
PVALS = os.path.join(RUN, "tables", "pvals_registry.csv")


def load_train(cols=None):
    df = pd.read_parquet(DATA, columns=cols, filters=[("t", "<=", TRAIN_END)])
    assert df.index.max() <= TRAIN_END
    return df


def add_returns(df):
    """1-minute log close-to-close return, only where the previous minute exists (gap_min == 1)."""
    lc = np.log(df["close"])
    r = lc.diff()
    r[df["gap_min"] != 1] = np.nan
    df["r"] = r
    return df


def grid(df):
    """Reindex onto the full minute grid (missing minutes stay NaN, nothing filled) and derive columns."""
    df = add_returns(df)
    full = pd.date_range(df.index.min(), df.index.max(), freq="1min", tz="UTC")
    g = df.reindex(full)
    g.index.name = "t"
    g["imb"] = g["buy_vol"] / g["vol"] - 0.5          # taker imbalance in [-0.5, 0.5]
    g["logn"] = np.log(g["n"])
    return g


def fwd(r, tau, skip=1):
    """Forward sum of 1-min returns over bars T+1+skip .. T+skip+tau, i.e. from close(T+skip) to close(T+skip+tau).
    NaN if any minute in the window is missing. skip=1: from the close of bar T+1."""
    s = r.rolling(tau, min_periods=tau).sum()
    return s.shift(-(tau + skip))


def trail(r, k):
    """Trailing sum over bars T-k+1..T (knowable at T+60s)."""
    return r.rolling(k, min_periods=k).sum()


ERAS = ["2017", "2018", "2019", "2020", "2021", "2022", "2023Q1"]


def era(idx):
    y = idx.year.astype(str)
    return pd.Index(np.where(idx.year == 2023, "2023Q1", y), name="era")


def save(fig, nn, slug):
    p = os.path.join(RUN, "plots", f"{nn:02d}_{slug}.png")
    fig.savefig(p, bbox_inches="tight", dpi=110)
    plt.close(fig)
    print("[plot]", p)
    return p


def table(df, nn, slug):
    p = os.path.join(RUN, "tables", f"{nn:02d}_{slug}.csv")
    df.to_csv(p)
    print("[table]", p)
    return p


def reg_p(test_id, tool, series, stat, p, note=""):
    """Register every p-value for the Step-4 Benjamini-Hochberg adjustment (K = rows in registry)."""
    row = pd.DataFrame([dict(test_id=test_id, tool=tool, series=series, stat=stat, p=p, note=note)])
    if os.path.exists(PVALS):
        old = pd.read_csv(PVALS)
        old = old[old.test_id != test_id]
        row = pd.concat([old, row], ignore_index=True)
    row.to_csv(PVALS, index=False)


def nw_mean(x, lags):
    """Mean with Newey-West (HAC) standard error. Returns mean, se, t, p."""
    import statsmodels.api as sm
    x = pd.Series(x).dropna().values
    m = sm.OLS(x, np.ones_like(x)).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return m.params[0], m.bse[0], m.tvalues[0], m.pvalues[0]


def nw_slope(y, x, lags):
    import statsmodels.api as sm
    d = pd.concat([pd.Series(y), pd.Series(x)], axis=1).dropna()
    m = sm.OLS(d.iloc[:, 0].values, sm.add_constant(d.iloc[:, 1].values)).fit(
        cov_type="HAC", cov_kwds={"maxlags": lags})
    return m.params[1], m.bse[1], m.tvalues[1], m.pvalues[1], len(d)
