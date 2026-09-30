# Assemble the 10-coin 1h panel for ONE slice (loader slices first, so nothing crosses a slice edge).
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from guarded_load import spot, COINS

COLS = ["open", "high", "low", "close", "vol", "quote_vol", "n", "buy_vol"]

def build(slice_name, who, coins=COINS):
    frames = {}
    for c in coins:
        d = spot(c, who, slice_name, columns=COLS).set_index("t")
        assert d.index.is_unique, c
        frames[c] = d
    lo = min(f.index.min() for f in frames.values()); hi = max(f.index.max() for f in frames.values())
    idx = pd.date_range(lo, hi, freq="1h", tz="UTC")
    P = {k: pd.DataFrame({c: frames[c][k].reindex(idx) for c in coins}) for k in COLS}
    lc = np.log(P["close"])
    P["r"] = lc.diff()                          # NaN across any missing hour (reindexed -> NaN)
    return P

def fwd(P, h):
    """log(close_{t+h}/close_t); NaN if any bar in (t, t+h] missing (sum of 1h returns, min_count=h)."""
    r = P["r"]
    return r[::-1].rolling(h, min_periods=h).sum()[::-1].shift(-1)
