"""f005 - closing strength, rolling 24h: ((C - L24)/(H24 - L24)) * (O24/C)^5 with L24/H24 the min low / max high of bars t-23..t and O24 = open of bar t-23 (Alpha#54, sign as 'minus #54'). Higher = strong close. Carded: open, high, low, close."""
import numpy as np
from features._wide import wide, stack


def compute(df):
    o, h, l, c = (wide(df, k) for k in ("open", "high", "low", "close"))
    H = h.rolling(24, min_periods=22).max(); L = l.rolling(24, min_periods=22).min()
    rng = (H - L).where((H - L) > 0)
    return stack(((c - L) / rng) * (o.shift(23) / c) ** 5, "f005")
