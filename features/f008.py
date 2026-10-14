"""f008 - hour-of-day seasonality persistence, demeaned. For the signal stamped at the END of bar t, the next bar has hour-of-day u. season = mean of the coin's 1h log returns at bars t+1-24j, j=1..60 (the previous 60 days' bars at the same hour u; at least 80% present);
f008 = season - the coin's mean 1h log return over the trailing 1440 hours ending at t (min 864). Higher = the coin has tended to rise at the upcoming hour. Carded: close."""
import numpy as np
from features._wide import wide, stack


def compute(df):
    lr = np.log(wide(df, "close"))
    r = lr.diff()
    N = 60
    acc = sum(r.shift(24 * j - 1) for j in range(1, N + 1))
    cnt = sum(r.shift(24 * j - 1).notna().astype(int) for j in range(1, N + 1))
    season = (acc / cnt).where(cnt >= int(0.8 * N))
    drift = r.rolling(24 * N, min_periods=864).mean()
    return stack(season - drift, "f008")
