"""Shared helpers for this run only (not a generic eda.py): guarded loads, daily bars, responses, the five
alphas, and the test statistics. Every number in a cell comes from a function here plus that cell's own script.
"""
import json
import os
import sys
from datetime import datetime, timezone

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = "/home/user/eda-routine/data/crypto_panel_validated_2026-10-05"
VAL_END = pd.Timestamp("2023-11-30 23:59:59", tz="UTC")
COINS = ["BTCUSD", "ETHUSD", "BNBUSD", "SOLUSD", "XRPUSD", "DOGEUSD", "ADAUSD", "LTCUSD", "BCHUSD", "DOTUSD"]
MIN_COINS = 5
MIN_USEFUL_IC = 0.02

# Slices: SPLITS.md is the source of truth; this mirrors it (written by p0_00 from coverage counts only).
SLICES = {}
_splits_json = os.path.join(RUN, "tables", "p0_00_splits.json")
if os.path.exists(_splits_json):
    with open(_splits_json) as fh:
        SLICES = {k: (pd.Timestamp(v[0]).date(), pd.Timestamp(v[1]).date()) for k, v in json.load(fh).items()}

# cellplot.py palette (backtest_engine2/cellplot.py PAL/GRAY); cellplot itself imports seaborn, not pre-approved (D8).
PAL = ["#2a78d6", "#008300", "#e87ba4", "#eda100", "#1baf7a", "#eb6834", "#4a3aa7", "#e34948"]
GRAY = "#9b9a94"


def setup_plot():
    matplotlib.rcParams.update({
        "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb",
        "text.color": "#0b0b0b", "axes.labelcolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#52514e",
        "axes.edgecolor": "#e5e4e0", "grid.color": "#e5e4e0", "grid.linewidth": 0.6, "axes.grid": True,
        "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 11, "axes.titleweight": "bold",
        "figure.dpi": 110, "lines.linewidth": 1.6, "font.size": 9, "axes.prop_cycle": matplotlib.cycler(color=PAL),
    })


def savefig(fig, name):
    path = os.path.join(RUN, "plots", name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ------------------------------------------------------------------ guarded loading

def _log_access(path, df, tcol, cell):
    line = (f"| {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S} | {cell} | {os.path.relpath(path, DATA)} | {len(df):,} | "
            f"{df[tcol].min()} | {df[tcol].max()} | PASS |\n")
    with open(os.path.join(RUN, "ACCESS_LOG.md"), "a") as fh:
        fh.write(line)


def load(rel, cell, tcol="t"):
    """The guard (no eda_guard.py in this checkout, TARGET NOTES): every load asserts no row after VAL_END."""
    path = os.path.join(DATA, rel)
    df = pd.read_parquet(path)
    df[tcol] = pd.to_datetime(df[tcol], utc=True)
    assert df[tcol].max() <= VAL_END, f"GUARD: {rel} has a row after VAL_END ({df[tcol].max()}) -> STOPPED.md"
    _log_access(path, df, tcol, cell)
    return df


# ------------------------------------------------------------------ daily bars (signal inputs) and responses

def daily_ohlcv(coin, cell):
    """Binance spot 1h -> UTC daily bar (TARGET.md translation; DECISIONS D4): valid only with >= 20 of 24 hours AND
    hours 00 and 23 present, so open/close really are 00:00/24:00."""
    h = load(f"spot/binance_{coin}.parquet", cell)
    h["day"] = h["t"].dt.floor("D")
    h["hour"] = h["t"].dt.hour
    g = h.sort_values("t").groupby("day")
    d = pd.DataFrame({
        "open": g["open"].first(), "high": g["high"].max(), "low": g["low"].min(), "close": g["close"].last(),
        "volume": g["vol"].sum(), "nh": g["t"].count(),
        "h0": g["hour"].min().eq(0), "h23": g["hour"].max().eq(23),
    })
    ok = (d["nh"] >= 20) & d["h0"] & d["h23"]
    d.loc[~ok, ["open", "high", "low", "close", "volume"]] = np.nan
    d.index = d.index.tz_convert("UTC").date
    return d[["open", "high", "low", "close", "volume", "nh"]]


def daily_response(coin, cell):
    """Primary validated price -> r(d) = ln(P[end of d+1] / P[end of d]) indexed by SIGNAL day d (DECISIONS D3/D5):
    valid only if all 24 bars of d+1 exist, the bar ending d exists, and no new_source=True among d+1's bars."""
    p = load(f"primary/validated_{coin}.parquet", cell)
    p["day"] = p["t"].dt.floor("D").dt.tz_convert("UTC").dt.date
    p = p.sort_values("t")
    g = p.groupby("day")
    end = g["price"].last().where(g["t"].max().dt.hour.eq(23))
    n = g["t"].count()
    flag = g["new_source"].any()
    full = (n == 24) & ~flag
    end_next = end.shift(-1)
    days = pd.Index(end.index)
    nxt_is_next = pd.Series([d + pd.Timedelta(days=1) for d in days], index=days)
    idx_next = pd.Series(list(days[1:]) + [None], index=days)
    ok_next = (idx_next == nxt_is_next) & full.shift(-1, fill_value=False)
    r = np.log(end_next / end).where(ok_next)
    return r.rename(coin)


def panel(fn, cell):
    return pd.DataFrame({c: fn(c, cell) for c in COINS})


def in_slice(index, name):
    a, b = SLICES[name]
    idx = pd.Index(index)
    return (idx >= a) & (idx < b)


def response_in_slice(R, name):
    """Responses whose window (end of d -> end of d+1) lies fully inside the slice: d >= start, d+1 < end."""
    a, b = SLICES[name]
    keep = [(d >= a) and (d + pd.Timedelta(days=1) < b) for d in R.index]
    return R.loc[keep]


# ------------------------------------------------------------------ the five alphas (paper Appendix A.1, verbatim ops)

def xrank(df):
    """rank(x): cross-sectional percentile rank over the coins present that day (paper A.2)."""
    return df.rank(axis=1, pct=True)


def ts_rank(df, d):
    """Ts_Rank(x, d): rank of today's value within the past d days (inclusive), as a fraction in (0, 1]."""
    return df.rolling(d, min_periods=d).apply(lambda a: (a <= a[-1]).sum() / len(a), raw=True)


def delay(df, d):
    return df.shift(d)


def alpha30(D):
    c = D["close"]
    s = np.sign(c - delay(c, 1)) + np.sign(delay(c, 1) - delay(c, 2)) + np.sign(delay(c, 2) - delay(c, 3))
    v = D["volume"]
    return ((1.0 - xrank(s)) * v.rolling(5, min_periods=5).sum()) / v.rolling(20, min_periods=20).sum()


def alpha35(D):
    c, h, l, v = D["close"], D["high"], D["low"], D["volume"]
    ret = c / delay(c, 1) - 1
    return ts_rank(v, 32) * (1 - ts_rank((c + h) - l, 16)) * (1 - ts_rank(ret, 32))


def alpha38(D):
    c, o = D["close"], D["open"]
    return (-1 * xrank(ts_rank(c, 10))) * xrank(c / o)


def alpha53(D):
    c, h, l = D["close"], D["high"], D["low"]
    den = (c - l)
    x = ((c - l) - (h - c)) / den.where(den > 0)       # DECISIONS D9: close == low -> NaN, not inf
    return -1 * (x - delay(x, 9))


def alpha54(D):
    c, h, l, o = D["close"], D["high"], D["low"], D["open"]
    den = (l - h) * (c ** 5)
    return (-1 * ((l - c) * (o ** 5))) / den.where((h - l) > 0)   # D9: high == low -> NaN


ALPHAS = {"A30": alpha30, "A35": alpha35, "A38": alpha38, "A53": alpha53, "A54": alpha54}


def daily_fields(cell):
    """Dict field -> date x coin frame, from Binance daily bars."""
    bars = {c: daily_ohlcv(c, cell) for c in COINS}
    days = sorted(set().union(*[set(b.index) for b in bars.values()]))
    return {f: pd.DataFrame({c: bars[c][f] for c in COINS}).reindex(days)
            for f in ["open", "high", "low", "close", "volume"]}


# ------------------------------------------------------------------ statistics

def nw_se(x, lags=5):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 10:
        return np.nan, n
    e = x - x.mean()
    s = e @ e / n
    for k in range(1, lags + 1):
        w = 1 - k / (lags + 1)
        s += 2 * w * (e[k:] @ e[:-k]) / n
    return np.sqrt(s / n), n


def daily_rank_ic(S, R):
    """NEUTRAL version: per day, Spearman between signal and next-day return across coins (>= MIN_COINS both present).
    Cross-sectional ranks remove the common market move by construction."""
    S, R = S.align(R, join="inner")
    out = {}
    for d in S.index:
        s, r = S.loc[d], R.loc[d]
        m = s.notna() & r.notna()
        if m.sum() >= MIN_COINS and s[m].nunique() > 1 and r[m].nunique() > 1:
            out[d] = s[m].rank().corr(r[m].rank())
    return pd.Series(out, dtype=float)


def trailing_z(df, w=120, minp=60):
    """Per-coin trailing z-score ending at t (SIGNAL CONSTRUCTION STANDARD 2): no whole-slice statistics."""
    m = df.rolling(w, min_periods=minp).mean()
    s = df.rolling(w, min_periods=minp).std()
    return (df - m) / s


def daily_ts_ic(S, R, Rhist):
    """RAW version (descriptive): per day, mean over coins of z(signal) * z(return), both scaled by trailing
    per-coin statistics (return sd from Rhist shifted so it ends before d). Measures own-return prediction incl. market."""
    zS = trailing_z(S)
    sd = Rhist.rolling(120, min_periods=60).std().shift(1)
    zR = R / sd.reindex(R.index)
    zS, zR = zS.align(zR, join="inner")
    prod = (zS * zR)
    cnt = prod.notna().sum(axis=1)
    return prod.mean(axis=1).where(cnt >= MIN_COINS).dropna()


def ls_spread_bp(S, R):
    """Top half minus bottom half of coins by signal, next-day return, bp; plus daily half-membership turnover."""
    S, R = S.align(R, join="inner")
    spr, mem = {}, {}
    for d in S.index:
        s, r = S.loc[d], R.loc[d]
        m = s.notna() & r.notna()
        if m.sum() < MIN_COINS:
            continue
        rk = s[m].rank(method="average")
        n = m.sum()
        top = rk > (n + 1) / 2
        bot = rk < (n + 1) / 2
        spr[d] = (r[m][top].mean() - r[m][bot].mean()) * 1e4
        mem[d] = set(rk.index[top])
    spr = pd.Series(spr, dtype=float)
    days = sorted(mem)
    turn = []
    for a, b in zip(days[:-1], days[1:]):
        if (pd.Timestamp(b) - pd.Timestamp(a)).days == 1:
            u = mem[a] | mem[b]
            turn.append(len(mem[a] ^ mem[b]) / 2 / max(len(mem[b]), 1))
    return spr, (float(np.mean(turn)) if turn else np.nan)


def summarize(ic):
    se, n = nw_se(ic.values)
    m = float(ic.mean()) if len(ic) else np.nan
    return {"mean": m, "se": se, "t": m / se if se and se > 0 else np.nan, "n": n}


def branch(stat, sign):
    """The pre-registered rule (DECISIONS D7), on the signed statistic x = sign * mean IC:
    supported if x >= MIN_USEFUL_IC and x / se >= 1.645; refuted if x + 1.645 se < MIN_USEFUL_IC and x / se < 1.645
    (the data exclude a useful effect); inconclusive otherwise, or n < the slice's stated minimum."""
    x = sign * stat["mean"]
    se = stat["se"]
    if not np.isfinite(x) or not np.isfinite(se):
        return "inconclusive"
    if x >= MIN_USEFUL_IC and x / se >= 1.645:
        return "supported"
    if x + 1.645 * se < MIN_USEFUL_IC:
        return "refuted"
    return "inconclusive"


def simulate_branch_probs(sd_ic, n_days, ar1=0.0, effect=MIN_USEFUL_IC, sims=4000, seed=7):
    """Power simulation: daily IC ~ AR(1) Gaussian with the measured sd and autocorrelation, n_days, mean 0 or effect.
    Returns P(branch | effect) and P(branch | 0) and the implied weights (DECISIONS D10)."""
    rng = np.random.default_rng(seed)
    out = {}
    for mu in (effect, 0.0):
        cnt = {"supported": 0, "refuted": 0, "inconclusive": 0}
        for _ in range(sims):
            e = rng.normal(0, sd_ic * np.sqrt(1 - ar1 ** 2), n_days)
            x = np.empty(n_days)
            x[0] = rng.normal(0, sd_ic)
            for i in range(1, n_days):
                x[i] = ar1 * x[i - 1] + e[i]
            x += mu
            st = summarize(pd.Series(x))
            cnt[branch(st, 1)] += 1
        out[mu] = {k: v / sims for k, v in cnt.items()}
    p1, p0 = out[effect], out[0.0]
    w_sup = p1["supported"] / max(p0["supported"], 1e-9)
    w_ref = p1["refuted"] / max(p0["refuted"], 1e-9)
    return {"P_H1": p1, "P_H0": p0, "w_sup_raw": w_sup, "w_ref_raw": w_ref,
            "w_sup": min(w_sup, 10.0), "w_ref": max(w_ref, 0.1)}


def expected_shift(prior, sim):
    """E|posterior - prior| over the three branches (inconclusive weight 1 -> no shift)."""
    o = prior / (1 - prior)
    out = 0.0
    for b, w in (("supported", sim["w_sup"]), ("refuted", sim["w_ref"])):
        pb = prior * sim["P_H1"][b] + (1 - prior) * sim["P_H0"][b]
        post = o * w / (1 + o * w)
        out += pb * abs(post - prior)
    return out


def cached():
    """Daily fields and responses, built once by p0_build.py (loads logged there)."""
    F = {k: pd.read_parquet(os.path.join(RUN, "tables", f"_daily_{k}.parquet")) for k in
         ["open", "high", "low", "close", "volume"]}
    for v in F.values():
        v.index = pd.Index([x.date() for x in v.index])
    R = pd.read_parquet(os.path.join(RUN, "tables", "_response.parquet"))
    R.index = pd.Index([x.date() for x in R.index])
    return F, R
