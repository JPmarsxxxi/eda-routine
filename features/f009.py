"""f009 - funding crowding beyond the premium. funding_dtr = last settled funding rate (stamp <= bar open t) minus the coin's trailing-720h mean of the same series (min 360); cross-sectional rank residualised on the ranks of r3s = -(log C[t-1]-log C[t-4]),
r24 = -(log C[t]-log C[t-24]) and f004 (features/f004.py); the residual is NEGATED (higher = less crowded long beyond what premium and trailing returns explain). Carded: funding, prem_close, close."""
import numpy as np
from features._wide import wide, stack, residual_rank
import features.f004 as f004mod


def compute(df):
    fund = wide(df, "funding")
    lr = np.log(wide(df, "close"))
    dtr = fund - fund.shift(1).rolling(720, min_periods=360).mean()
    r3s = -(lr.shift(1) - lr.shift(4)); r24 = -(lr - lr.shift(24))
    s4 = f004mod.compute(df)
    f4 = s4.unstack("coin").reindex(index=dtr.index, columns=dtr.columns)
    return stack(-residual_rank(dtr, [r3s, r24, f4]), "f009")
