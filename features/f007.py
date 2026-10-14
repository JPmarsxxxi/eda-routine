"""f007 - Alpha#30 as written, at the UTC day boundary: (1 - pct rank of the 3-day sign-streak) * sum(vol,5d)/sum(vol,20d), 24h blocks ending at the 23:00 bar, volumes summed over 120 / 480 hours (min 90%). Carded: close, vol."""
import numpy as np
import pandas as pd
from features._wide import wide, stack


def compute(df):
    c = wide(df, "close"); v = wide(df, "vol")
    s = sum(np.sign(c.shift(24 * i) - c.shift(24 * (i + 1))) for i in range(3))
    f = 1 - s.rank(axis=1, pct=True)
    sc = v.rolling(120, min_periods=108).sum() / v.rolling(480, min_periods=432).sum()
    g = np.where(f.index.hour == 23, 1.0, np.nan)
    f = pd.DataFrame((f * sc).values * g[:, None], index=f.index, columns=f.columns)
    return stack(f, "f007")
