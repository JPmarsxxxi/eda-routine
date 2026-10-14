"""f004 - perp premium crowding (sign flipped so that higher = less crowded long). prem_dtr = premium_index_close[t] - mean(premium_index_close[t-720..t-1]) (per coin, min 360);
cross-sectional rank residualised on the ranks of r3s = -(log C[t-1]-log C[t-4]) and r24 = -(log C[t]-log C[t-24]); the residual is NEGATED. Carded: prem_close, close."""
import numpy as np
from features._wide import wide, stack, residual_rank


def compute(df):
    prem = wide(df, "prem_close")
    lr = np.log(wide(df, "close"))
    dtr = prem - prem.shift(1).rolling(720, min_periods=360).mean()
    r3s = -(lr.shift(1) - lr.shift(4)); r24 = -(lr - lr.shift(24))
    return stack(-residual_rank(dtr, [r3s, r24]), "f004")
