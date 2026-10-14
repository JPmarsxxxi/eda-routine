"""f002 - 24-hour reversal, lag-1, signal hours 21-06 UTC only. -(log C[t-1] - log C[t-25]), NaN unless the UTC hour of bar t is in {21,22,23,0,1,2,3,4,5,6}. Higher = past 24h loser. Carded: close."""
import numpy as np
import pandas as pd
from features._wide import wide, stack

HOURS = {21, 22, 23, 0, 1, 2, 3, 4, 5, 6}


def compute(df):
    lr = np.log(wide(df, "close"))
    f = -(lr.shift(1) - lr.shift(25))
    g = np.where(np.isin(f.index.hour, list(HOURS)), 1.0, np.nan)
    f = pd.DataFrame(f.values * g[:, None], index=f.index, columns=f.columns)
    return stack(f, "f002")
