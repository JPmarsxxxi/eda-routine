"""f001 - bounce-free 3-hour reversal. -(log C[t-1] - log C[t-4]) on Binance spot closes: the last print (bar t) is skipped so the Binance bid-ask bounce cannot be in the feature. Higher = past loser. Carded: close."""
import numpy as np
from features._wide import wide, stack


def compute(df):
    lr = np.log(wide(df, "close"))
    return stack(-(lr.shift(1) - lr.shift(4)), "f001")
