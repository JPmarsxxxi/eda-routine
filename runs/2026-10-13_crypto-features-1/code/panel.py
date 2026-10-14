"""panel.py - run-local data access + IC machinery for runs/2026-10-13_crypto-features-1.
Every raw load goes through eda_guard (TRAIN bound by default, ACCESS_LOG row per load)."""
import os, sys, json, math, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, r"C:\Users\User\backtest_engine\backtest_engine2")
import eda_guard as G

ROOT = r"C:\Users\User\eda-routine"
RUN = os.path.join(ROOT, "runs", "2026-10-13_crypto-features-1")
D = os.path.join(ROOT, "data", "crypto_panel_validated_2026-10-05")
COINS = ["BTC", "ETH", "BNB", "SOL", "XRP", "DOGE", "ADA", "LTC", "BCH", "DOT"]
SLICES = {"EXPLORE": ("2019-01-01", "2021-07-01"), "C1": ("2021-07-08", "2022-01-01"),
          "C2": ("2022-01-08", "2022-07-01"), "C3": ("2022-07-08", "2023-03-20")}
GRID = pd.date_range("2018-01-01", "2023-03-19 23:00", freq="h")
HORIZONS = (1, 6, 24)


def _decl(inst, venue, cols):
    return dict(instrument=inst, venue=venue, time_col="t", columns=cols)


def _hourly(df):
    df = df.copy()
    df["t"] = pd.to_datetime(df["t"])
    return df.set_index("t").sort_index()


def prim(cell):
    """validated primary panel -> (P price, NS new_source bool, QV binance quote vol). Hourly grid, TRAIN only."""
    P, NS, QV, SRC = {}, {}, {}, {}
    for c in COINS:
        d = G.load(f"{D}/primary/validated_{c}USD.parquet", RUN, cell,
                   declare=_decl(f"{c}USD validated hourly price", "Binance spot trade close (validated years) + FTMO CFD hourly mid from 2022-01-01",
                                 {"price": "trade_print", "new_source": "other", "source": "other",
                                  "binance_quote_vol": "volume", "ftmo_spread_bp": "other"}),
                   use=["price", "new_source", "source", "binance_quote_vol"])
        d = _hourly(d)
        P[c] = d["price"].reindex(GRID)
        NS[c] = d["new_source"].reindex(GRID).fillna(False).astype(bool)
        QV[c] = d["binance_quote_vol"].reindex(GRID)
        SRC[c] = (d["source"] == "ftmo_mid").reindex(GRID)
    return pd.DataFrame(P), pd.DataFrame(NS), pd.DataFrame(QV), pd.DataFrame(SRC).astype(float)


def spot(cell, venue="binance"):
    """binance spot hourly OHLCV + trades + taker buy -> dict of wide frames (TRAIN only)."""
    fields = ["open", "high", "low", "close", "vol", "quote_vol", "n", "buy_vol", "buy_quote_vol"]
    out = {f: {} for f in fields}
    for c in COINS:
        d = G.load(f"{D}/spot/binance_{c}USD.parquet", RUN, cell,
                   declare=_decl(f"{c}USDT Binance spot hourly", "Binance spot",
                                 {"open": "trade_print", "high": "trade_print", "low": "trade_print", "close": "trade_print",
                                  "vol": "volume", "quote_vol": "volume", "n": "count", "buy_vol": "volume",
                                  "buy_quote_vol": "volume", "sell_vol": "volume", "ftmo_spread_rt_bp": "other"}),
                   use=fields)
        d = _hourly(d)
        for f in fields:
            out[f][c] = d[f].reindex(GRID)
    return {f: pd.DataFrame(v) for f, v in out.items()}


def fwd(P, NS, h):
    """forward log return from the END of bar t to the END of bar t+h; NaN if any new_source bar in (t, t+h]."""
    r = np.log(P.shift(-h) / P)
    bad = NS.astype(int).rolling(h).sum().shift(-h) > 0
    return r.mask(bad)


def back(P, NS, k):
    """trailing log return over k bars ending at bar t; NaN across a new_source bar."""
    r = np.log(P / P.shift(k))
    bad = NS.astype(int).rolling(k).sum() > 0
    return r.mask(bad)


def daily(S):
    """UTC-day OHLCV from the hourly binance dict. Decision stamp = the day's 23:00 bar. Needs >=20 of 24 bars."""
    o, h, l, c = S["open"], S["high"], S["low"], S["close"]
    day = o.index.floor("D")
    g = lambda df: df.groupby(day)
    nb = g(c.notna().astype(int)).sum()
    D_ = {
        "O": g(o).first(), "H": g(h).max(), "L": g(l).min(), "C": g(c).last(),
        "V": g(S["vol"]).sum(min_count=1), "QV": g(S["quote_vol"]).sum(min_count=1),
        "N": g(S["n"]).sum(min_count=1), "BV": g(S["buy_vol"]).sum(min_count=1),
    }
    # first/last skip NaN; mark days with too few bars invalid
    for k in D_:
        D_[k] = D_[k].where(nb >= 20)
    D_["nb"] = nb
    for k in D_:
        D_[k].index = D_[k].index + pd.Timedelta(hours=23)   # stamp at the day's last bar
    return D_


# ------------------------------------------------------------------ cross-sectional IC
def xs_ic(F, R, min_n=6):
    m = F.notna() & R.notna()
    n = m.sum(axis=1)
    rf = F.where(m).rank(axis=1)
    rr = R.where(m).rank(axis=1)
    rf = rf.sub(rf.mean(axis=1), axis=0)
    rr = rr.sub(rr.mean(axis=1), axis=0)
    num = (rf * rr).sum(axis=1)
    den = np.sqrt((rf ** 2).sum(axis=1) * (rr ** 2).sum(axis=1))
    ic = num / den
    ic[n < min_n] = np.nan
    return ic


def nw(x, L):
    """mean, Newey-West t, se, n for a series."""
    x = pd.Series(x).dropna().values
    n = len(x)
    if n < 30:
        return dict(mean=float(np.mean(x)) if n else np.nan, t=np.nan, se=np.nan, n=n)
    mu = x.mean(); e = x - mu
    s = (e * e).sum() / n
    for k in range(1, min(L, n - 1) + 1):
        w = 1 - k / (L + 1)
        s += 2 * w * (e[k:] * e[:-k]).sum() / n
    se = math.sqrt(max(s, 1e-18) / n)
    return dict(mean=float(mu), t=float(mu / se), se=float(se), n=n)


def in_slice(idx, name):
    a, b = SLICES[name]
    return (idx >= pd.Timestamp(a)) & (idx < pd.Timestamp(b))


def train_mask(idx):
    m = np.zeros(len(idx), dtype=bool)
    for nm in SLICES:
        m |= in_slice(idx, nm)
    return m


def slice_report(ic, L, names=("EXPLORE", "C1", "C2", "C3")):
    out = {}
    for nm in names:
        out[nm] = nw(ic[in_slice(ic.index, nm)], L)
    out["TRAIN"] = nw(ic[train_mask(ic.index)], L)
    return out


def fmt_rep(rep):
    return "  ".join(f"{k}: {v['mean']:+.4f} (t {v['t']:+.2f}, n {v['n']})" for k, v in rep.items())


def sample(df, mode):
    """mode 'h' = every hour, 'd' = decision at the day's 23:00 bar, '6h' = every 6th hour (00,06,12,18 stamps)"""
    if mode == "h":
        return df
    if mode == "d":
        return df[df.index.hour == 23]
    if mode == "6h":
        return df[df.index.hour % 6 == 5]
    raise ValueError(mode)


def to_hourly(Dd, idx):
    """daily-stamped frame (stamps at 23:00) -> hourly frame forward-filled for the next 24 hours is NOT done
    (point-in-time: only valid at the 23:00 bar). Returns reindex without fill."""
    return Dd.reindex(idx)


def rowz(df):
    return df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)


def pair_corr(F, G_, min_n=6):
    """mean over time of the cross-sectional Spearman correlation between two feature panels."""
    return xs_ic(F, G_, min_n).mean()


def residual_rank(F, Gs):
    """per-row: cross-sectional rank of F, residualised on the cross-sectional ranks of every panel in Gs."""
    idx = F.index
    m = F.notna()
    for g in Gs:
        m &= g.notna()
    rf = F.where(m).rank(axis=1)
    rg = [g.where(m).rank(axis=1) for g in Gs]
    out = pd.DataFrame(np.nan, index=idx, columns=F.columns)
    A = rf.values
    B = np.stack([r.values for r in rg], axis=2)  # T x N x k
    for i in range(A.shape[0]):
        a = A[i]; ok = ~np.isnan(a)
        if ok.sum() < 6:
            continue
        X = np.column_stack([np.ones(ok.sum()), B[i][ok]])
        beta, *_ = np.linalg.lstsq(X, a[ok], rcond=None)
        out.iloc[i, np.where(ok)[0]] = a[ok] - X @ beta
    return out


# ------------------------------------------------------------------ input families (perp, funding, metrics, venues)
def perp_hourly(cell, kind):
    """kind 'klines' | 'premium' -> dict of wide frames (open high low close volume quote_volume count taker_buy_volume taker_buy_quote_volume)"""
    fields = ["open", "high", "low", "close", "volume", "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume"]
    out = {f: {} for f in fields}
    for c in COINS:
        d = G.load(f"{D}/perp/perp_{kind}_{c}USD.parquet", RUN, cell,
                   declare=_decl(f"{c} USDT perpetual {kind}", "Binance USD-M futures",
                                 {"open": "trade_print" if kind == "klines" else "other", "high": "other", "low": "other",
                                  "close": "trade_print" if kind == "klines" else "other",
                                  "volume": "volume", "quote_volume": "volume", "count": "count",
                                  "taker_buy_volume": "volume", "taker_buy_quote_volume": "volume"}), use=fields)
        d = _hourly(d)
        for f in fields:
            out[f][c] = d[f].reindex(GRID)
    return {f: pd.DataFrame(v) for f, v in out.items()}


def funding(cell):
    """funding settlements -> wide frame at hourly grid: last settled rate with settlement stamp <= bar open (conservative)."""
    F, W = {}, {}
    for c in COINS:
        d = G.load(f"{D}/perp/funding_{c}USD.parquet", RUN, cell,
                   declare=_decl(f"{c} USDT perpetual funding", "Binance USD-M futures",
                                 {"last_funding_rate": "rate", "funding_interval_hours": "other"}),
                   use=["last_funding_rate", "funding_interval_hours"])
        d = _hourly(d)
        s = d["last_funding_rate"]
        F[c] = s.reindex(GRID, method="ffill", tolerance=pd.Timedelta(days=2))   # value at stamp <= bar open
        W[c] = d["funding_interval_hours"].reindex(GRID, method="ffill", tolerance=pd.Timedelta(days=2))
    return pd.DataFrame(F), pd.DataFrame(W)


def metrics_hourly(cell, cache=True):
    """5m perp metrics -> last snapshot inside each hour whose stamp <= open+55min (knowable by the bar end)."""
    cols = ["sum_open_interest", "sum_open_interest_value", "count_toptrader_long_short_ratio",
            "sum_toptrader_long_short_ratio", "count_long_short_ratio", "sum_taker_long_short_vol_ratio"]
    path = os.path.join(RUN, "work", "metrics_hourly_train.parquet")
    out = {k: {} for k in cols}
    for c in COINS:
        d = G.load(f"{D}/perp/metrics_{c}USD.parquet", RUN, cell,
                   declare=_decl(f"{c} USDT perpetual 5m metrics", "Binance USD-M futures",
                                 {"sum_open_interest": "open_interest", "sum_open_interest_value": "open_interest",
                                  "count_toptrader_long_short_ratio": "ratio", "sum_toptrader_long_short_ratio": "ratio",
                                  "count_long_short_ratio": "ratio", "sum_taker_long_short_vol_ratio": "ratio"}), use=cols)
        d = _hourly(d)
        d = d[d.index.minute <= 55]
        h = d.groupby(d.index.floor("h")).last()
        for k in cols:
            out[k][c] = h[k].reindex(GRID)
    res = {k: pd.DataFrame(v) for k, v in out.items()}
    return res


def venue(cell, name):
    """coinbase_<COIN>USD or upbit_<COIN>KRW close/volume panels"""
    out = {"close": {}, "volume": {}}
    for c in COINS:
        pth = f"{D}/spot/{name}_{c}USD.parquet" if name == "coinbase" else f"{D}/spot/{name}_{c}KRW.parquet"
        if not os.path.exists(pth):
            continue
        vcol = "volume" if name == "coinbase" else "vol"
        d = G.load(pth, RUN, cell, declare=_decl(f"{c} {name} spot hourly", name,
                                                 {"open": "trade_print", "high": "trade_print", "low": "trade_print",
                                                  "close": "trade_print", vcol: "volume"}), use=["close", vcol])
        d = _hourly(d)
        out["close"][c] = d["close"].reindex(GRID); out["volume"][c] = d[vcol].reindex(GRID)
    return {k: pd.DataFrame(v) for k, v in out.items()}
