"""f006 - 3-day sign-streak fade at the UTC day boundary. s = sign(C[t]-C[t-24]) + sign(C[t-24]-C[t-48]) + sign(C[t-48]-C[t-72]); feature = 1 - cross-sectional pct rank of s, defined only at the 23:00 bar. Higher = longer down-streak. Carded: close."""
import numpy as np
import pandas as pd
from features._wide import wide, stack


def compute(df):
    c = wide(df, "close")
    s = sum(np.sign(c.shift(24 * i) - c.shift(24 * (i + 1))) for i in range(3))
    f = 1 - s.rank(axis=1, pct=True)
    g = np.where(f.index.hour == 23, 1.0, np.nan)
    f = pd.DataFrame(f.values * g[:, None], index=f.index, columns=f.columns)
    return stack(f, "f006")
