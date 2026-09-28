# Shared, claim-specific loaders for THIS hunt only (not a generic eda module).
import sys, numpy as np, pandas as pd
sys.path.insert(0, r"C:\Users\User\backtest_engine\backtest_engine2")
from cellplot import setup, PAL, GRAY  # palette/style only (DECISIONS.md item 3)
import matplotlib.pyplot as plt
import statsmodels.api as sm

TRAIN_END = pd.Timestamp("2023-03-19 23:59", tz="UTC")
VAL_START = pd.Timestamp("2023-03-25 00:00", tz="UTC")
VAL_END = pd.Timestamp("2023-11-30 23:59", tz="UTC")
ERAS = [("2017-08..2018-12", "2017-08-01", "2018-12-31"), ("2019", "2019-01-01", "2019-12-31"),
        ("2020", "2020-01-01", "2020-12-31"), ("2021", "2021-01-01", "2021-12-31"),
        ("2022-01..2023-03-19", "2022-01-01", "2023-03-19")]

def save(fig, name):
    fig.savefig(f"plots/{name}.png", bbox_inches="tight", dpi=130); plt.close(fig); print(f"[plot] plots/{name}.png")

def daily(split="TRAIN", shift_h=0.0):
    """Per-UTC-day legs from the half-hour table. shift_h moves the day boundary (placebo, C3)."""
    hh = pd.read_parquet(f"tables/halfhour_{split}.parquet")
    lp = np.log(hh["p"])
    if shift_h:
        lp = lp.copy(); lp.index = lp.index - pd.Timedelta(hours=shift_h)
    grid = pd.date_range(lp.index.min().floor("D"), lp.index.max().ceil("D"), freq="30min", tz="UTC", inclusive="left")
    lp = lp.reindex(grid)
    k = (grid.hour * 2 + grid.minute // 30)
    M = pd.DataFrame({"lp": lp.values, "d": grid.floor("D"), "k": k}).pivot(index="d", columns="k", values="lp")
    out = pd.DataFrame(index=M.index)
    out["r_first"] = M[0] - M[47].shift(1)
    out["r_mid"] = M[46] - M[0]
    out["r_last"] = M[47] - M[46]
    return out, M

def nw_ols(y, X, lags=5):
    X = sm.add_constant(X)
    return sm.OLS(y, X, missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags": lags})
