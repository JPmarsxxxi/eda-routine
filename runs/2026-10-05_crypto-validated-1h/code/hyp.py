"""Hypothesis-specific statistics for this run (H1 XS premium 72h; H2/H3 TS market-timing 24h). Each cell script calls
exactly one of these on exactly one slice. Forward returns are only formed inside the requested slice."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from scipy import stats
from panel import *
from guard import load

ALPHA = 0.05
Z = 1.6448536


def primary_daily(cell, slice_name=None):
    """Daily primary panel; if slice_name is given, hourly rows are cut to [slice start - 1 day, slice end) BEFORE any
    return is computed, so no return outside the slice ever exists in memory."""
    if slice_name:
        a, b = ts(SLICES[slice_name][0]) - pd.Timedelta(days=1), ts(SLICES[slice_name][1])
        return daily(hourly(cell, window=(a - pd.Timedelta(hours=1), b)))
    return daily(hourly(cell))


def h1_blocks(cell, slice_name, D=None, need=5):
    """Every-3rd-day decision grid inside the slice; per block: premium rank top third minus bottom third fwd 72h."""
    D = D if D is not None else primary_daily(cell, slice_name)
    R3 = fwd(D["r24"], 3)
    m = in_slice(R3.index, slice_name, 3)
    R3 = R3[m]
    P = feat_premium(cell)
    rows = []
    for d in R3.index[::3]:
        a = pd.DataFrame({"prem": P.reindex(index=[d], columns=R3.columns).iloc[0], "fwd": R3.loc[d]}).dropna()
        if len(a) < need:
            rows.append(dict(d=d, n_coins=len(a))); continue
        q = a.prem.rank(pct=True)
        top, bot = a.fwd[q > 2 / 3], a.fwd[q <= 1 / 3]
        rows.append(dict(d=d, n_coins=len(a), spread=top.mean() - bot.mean(), ic=stats.spearmanr(a.prem, a.fwd)[0],
                         top=",".join(top.index.str[:-3]), bottom=",".join(bot.index.str[:-3])))
    return pd.DataFrame(rows).set_index("d"), R3


def h1_threshold(coins):
    return 2 * np.mean([rt_cost(c, 72) for c in coins])


def ts_daily(cell, feature, slice_name, D=None, need=5):
    """Panel equal-weight next-24h return vs a market-wide feature known at d+1 00:00."""
    D = D if D is not None else primary_daily(cell, slice_name)
    R1 = fwd(D["r24"], 1)
    m = in_slice(R1.index, slice_name, 1)
    R1 = R1[m]
    cnt = R1.notna().sum(1)
    panel = R1.mean(1).where(cnt >= need)
    z = pd.DataFrame({"f": feature.reindex(R1.index), "r": panel, "n_coins": cnt}).dropna()
    return z


def ts_stat(z):
    q = z.f.rank(pct=True)
    top, bot = z.r[q > 2 / 3], z.r[q <= 1 / 3]
    spread = top.mean() - bot.mean()
    se = np.sqrt(top.var() / len(top) + bot.var() / len(bot))
    ic = stats.spearmanr(z.f, z.r)[0]
    return dict(n=len(z), ic=ic, ic_t=ic * np.sqrt(len(z) - 2), spread_bp=spread * 1e4, t=spread / se, n_top=len(top), n_bot=len(bot))


def ts_threshold(coins):
    return 2 * np.mean([rt_cost(c, 24) for c in coins])


def branch(t, eff_bp, T_bp, sign):
    """sign=-1: hypothesis predicts a negative effect. supported: significant AND |effect| >= T; refuted: not significant
    in the predicted direction; inconclusive: significant but smaller than T."""
    sig = (sign * t) >= Z
    if not sig:
        return "refuted"
    return "supported" if sign * eff_bp >= T_bp else "inconclusive"


def weights(power):
    return {"supported": power / ALPHA, "refuted": (1 - power) / (1 - ALPHA), "inconclusive": 1.0}


def cap(w):
    return min(10.0, max(0.1, w)), (w > 10.0 or w < 0.1)


def post(p, w):
    o = p / (1 - p) * w
    return o / (1 + o)
