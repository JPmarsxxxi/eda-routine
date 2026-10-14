"""f003 - 1-hour trade-count surprise, residualised on the same-hour return. nsurp = log(n[t] / mean(n[t-720..t-1])) (trailing-720h per-hour trade count, min 360); then, per timestamp, the cross-sectional rank of nsurp
residualised on the cross-sectional ranks of the 1h log return and |1h log return| of bar t. Higher = busier than usual beyond the move. Carded: n, close."""
import numpy as np
from features._wide import wide, stack, residual_rank


def compute(df):
    n = wide(df, "n").where(lambda x: x > 0)
    lr = np.log(wide(df, "close"))
    base = n.shift(1).rolling(720, min_periods=360).mean()
    nsurp = np.log(n / base)
    r1 = lr - lr.shift(1)
    return stack(residual_rank(nsurp, [r1, r1.abs()]), "f003")
