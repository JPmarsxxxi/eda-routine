"""Run-specific data assembly for 2026-10-05_crypto-validated-1h (NOT a generic eda module: it knows this bundle's
files, this run's slices and this run's lag rules, nothing else). All reads go through guard.load()."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from guard import load, RUN

COINS = ["BTCUSD", "ETHUSD", "BNBUSD", "SOLUSD", "XRPUSD", "DOGEUSD", "ADAUSD", "LTCUSD", "BCHUSD", "DOTUSD"]
RT24 = {"BTCUSD": 18.9, "ETHUSD": 25.4, "LTCUSD": 36.5, "ADAUSD": 46, "DOGEUSD": 46, "DOTUSD": 46, "BNBUSD": 46,
        "SOLUSD": 46, "BCHUSD": 65.5, "XRPUSD": 68.6}
NIGHT = 8.2
SLICES = {"EXPLORE": ("2019-01-01", "2021-07-01"), "C1": ("2021-07-08", "2022-01-01"),
          "C2": ("2022-01-08", "2022-07-01"), "C3": ("2022-07-08", "2023-03-20"), "VAL": ("2023-03-25", "2023-12-01")}

# cellplot.py palette, copied verbatim (DECISIONS D4)
PAL = ["#2a78d6", "#008300", "#e87ba4", "#eda100", "#1baf7a", "#eb6834", "#4a3aa7", "#e34948"]
SURFACE, TEXT, TEXT2, GRID, GRAY = "#fcfcfb", "#0b0b0b", "#52514e", "#e5e4e0", "#9b9a94"
DIV = ["#2a78d6", "#f0efec", "#e34948"]


def setup():
    matplotlib.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "text.color": TEXT, "axes.labelcolor": TEXT2, "xtick.color": TEXT2, "ytick.color": TEXT2,
        "axes.edgecolor": GRID, "grid.color": GRID, "grid.linewidth": 0.6, "axes.grid": True,
        "axes.spines.top": False, "axes.spines.right": False, "axes.prop_cycle": matplotlib.cycler(color=PAL),
        "axes.titlesize": 11, "axes.titleweight": "bold", "figure.dpi": 110, "lines.linewidth": 1.6, "font.size": 9})


def save(fig, name):
    p = os.path.join(RUN, "plots", name)
    fig.savefig(p, bbox_inches="tight"); plt.close(fig)
    print(f"[plot] plots/{name}")
    return p


def rt_cost(coin, hours):
    """Round-trip bp for a hold of `hours` (24h figure includes one night; intraday subtracts it)."""
    nights = max(0, int(np.ceil(hours / 24)))
    return RT24[coin] - NIGHT + NIGHT * nights


def ts(s):
    return pd.Timestamp(s, tz="UTC")


# ------------------------------------------------------------------ primary target

def hourly(cell, coins=COINS, window=None):
    """Long frame t, coin, price, qvol, src, ok (valid 1h log return r1 at t), r1. window=(a, b): rows cut to [a, b)
    right after the guarded load, before any return is computed."""
    out = []
    for c in coins:
        d = load(f"primary/validated_{c}.parquet", cell)
        if window is not None:
            d = d[(d._t >= window[0]) & (d._t < window[1])]
            if len(d) == 0:
                continue
        d = d.sort_values("_t")
        full = pd.DataFrame(index=pd.date_range(d._t.min(), d._t.max(), freq="h"))
        d = d.set_index("_t").reindex(full.index)
        d.index.name = "t"
        prev = d.price.shift(1)
        ok = d.price.notna() & prev.notna() & (d.new_source == False)
        r1 = np.log(d.price / prev).where(ok)
        out.append(pd.DataFrame({"coin": c, "price": d.price, "qvol": d.binance_quote_vol, "src": d.source,
                                 "ns": d.new_source.fillna(True).astype(bool), "r1": r1}, index=d.index))
    return pd.concat(out).reset_index()


def daily(h):
    """Day d close = price at bar stamped d 23:00. r24 = log return over day d (valid iff no new_source / hole in
    (d-1 23:00, d 23:00]). Returns wide frames indexed by day d (date of the close, decision at d+1 00:00)."""
    h = h.copy()
    h["day"] = h.t.dt.floor("D")
    g = h.groupby(["coin", "day"])
    nvalid = g.r1.count()
    close = h[h.t.dt.hour == 23].set_index(["coin", "day"]).price
    r24 = g.r1.sum().where(nvalid == 24)  # sum of 24 valid hourly log returns == log(close_d / close_{d-1})
    qv = g.qvol.sum()
    W = lambda s: s.unstack("coin").sort_index()
    return {"close": W(close), "r24": W(r24), "qvol": W(qv)}


def fwd(r24, h_days):
    """Forward h-day log return from close of day d to close of day d+h (valid iff all h daily returns valid)."""
    acc = sum(r24.shift(-k) for k in range(1, h_days + 1))
    return acc


def in_slice(days, name, h_days=0):
    """Decision day d (close at d+1 00:00) belongs to slice if the forward window [d+1 00:00, d+1+h 00:00] lies inside."""
    a, b = ts(SLICES[name][0]), ts(SLICES[name][1])
    start = days + pd.Timedelta(days=1)
    end = start + pd.Timedelta(days=h_days)
    return (start >= a) & (end <= b)


# ------------------------------------------------------------------ explanatory features (knowable at d+1 00:00)

def feat_funding(cell, coins=COINS):
    """Mean of perp last_funding_rate over settlements strictly before d+1 00:00 and after d 00:00 (lag: settlement)."""
    out = {}
    for c in coins:
        try:
            d = load(f"perp/funding_{c}.parquet", cell)
        except AssertionError:
            raise
        s = d.set_index("_t").last_funding_rate.sort_index()
        # settlement at exactly 00:00:00.00x belongs to the NEXT decision: shift stamps by -1s then floor to day
        day = (s.index - pd.Timedelta(seconds=1)).floor("D")
        # stamps in (d 00:00:01, d+1 00:00:00.999] -> day d; strictly-before-tau rule: drop the ones at/after tau
        keep = s.index < (day + pd.Timedelta(days=1))
        out[c] = s[keep].groupby(day[keep]).mean()
    return pd.DataFrame(out).sort_index()


def feat_premium(cell, coins=COINS):
    """Mean perp premium-index close over bars stamped d 00:00..23:00 (knowable open+1h -> all by d+1 00:00)."""
    out = {}
    for c in coins:
        d = load(f"perp/perp_premium_{c}.parquet", cell)
        s = d.set_index("_t").close.sort_index()
        out[c] = s.groupby(s.index.floor("D")).mean()
    return pd.DataFrame(out).sort_index()


def feat_coinbase_premium(cell, binance_close, coins=COINS):
    """log(coinbase close / Binance-spot close) at the bar stamped d 23:00 (both knowable d+1 00:00), daily mean of
    hourly values. binance_close: hourly wide frame from spot/binance_* close."""
    out = {}
    for c in coins:
        f = f"spot/coinbase_{c}.parquet"
        try:
            d = load(f, cell)
        except Exception:
            continue
        s = d.set_index("_t").close.sort_index()
        b = binance_close[c].reindex(s.index)
        x = np.log(s / b)
        out[c] = x.groupby(x.index.floor("D")).mean()
    return pd.DataFrame(out).sort_index()


def binance_spot_hourly(cell, coins=COINS, cols=("close",)):
    out = {}
    for c in coins:
        d = load(f"spot/binance_{c}.parquet", cell).set_index("_t").sort_index()
        for col in cols:
            out[(col, c)] = d[col]
    return pd.DataFrame(out)
