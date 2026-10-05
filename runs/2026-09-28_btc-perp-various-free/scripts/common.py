# Shared loaders for THIS session only (not a generic eda module). Every load goes through eda_guard.load,
# which writes ACCESS_LOG.md + HYGIENE.jsonl rows itself and refuses rows past the slice bound.
import os, sys, glob, json
import numpy as np, pandas as pd
sys.path.insert(0, r"C:\Users\User\backtest_engine\backtest_engine2")
import eda_guard as G
from cellplot import setup, PAL, GRAY
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUN = r"C:\Users\User\eda-routine\runs\2026-09-28_btc-perp-various-free"
D = r"C:\Users\User\eda-routine\data"
os.chdir(RUN)
setup()

TRAIN_LO = pd.Timestamp("2017-08-17 00:00")
TRAIN_HI = pd.Timestamp("2023-03-19 23:59:59")
VAL_LO = pd.Timestamp("2023-03-25 00:00")
VAL_HI = pd.Timestamp("2023-11-30 23:59:59")
# SPLITS.md (declared from coverage only, before any forward return): EXPLORE <= 2021-12-31, CONFIRM 2022-01-01..TRAIN_END
EXPLORE_HI = pd.Timestamp("2021-12-31 23:59:59")
CONFIRM_LO = pd.Timestamp("2022-01-01 00:00")

# eda_guard._read concatenates directories with ignore_index and does not reset a time index; these files keep
# their stamp in the index, so reset it on read (wrapper only, no data changed).
_orig_read = G._read
def _read_reset(path, columns=None):
    if os.path.isdir(path):
        files = sorted(glob.glob(os.path.join(path, "*.parquet")))
        return pd.concat([pd.read_parquet(f).reset_index() for f in files], ignore_index=True)
    df = _orig_read(path, columns)
    if not isinstance(df.index, pd.RangeIndex):
        df = df.reset_index()
    return df
G._read = _read_reset

PERP_HOURLY = dict(path=rf"{D}\btcusdt_perp_hourly\btcusdt_perp_hourly.parquet",
    declare=dict(instrument="BTCUSDT (labelled perp; see DATA_CARD identity check)", venue="Binance",
                 time_col="open_time", columns={"close": "trade_print", "quote_volume": "volume"}))
PERP_30M = dict(path=rf"{D}\btc_perp_30m\btc_30m.parquet",
    declare=dict(instrument="BTCUSDT (labelled perp; see DATA_CARD identity check)", venue="Binance",
                 time_col="open_time", columns={"close": "trade_print", "quote_volume": "volume"}))
PERP_1M = dict(path=rf"{D}\btcusdt_perp_1m",
    declare=dict(instrument="BTCUSDT (labelled perp; see DATA_CARD identity check)", venue="Binance",
                 time_col="ts", columns={"open": "trade_print", "high": "trade_print", "low": "trade_print",
                 "close": "trade_print", "vol": "volume", "quote": "volume", "n": "count",
                 "buy_vol": "volume", "sell_vol": "volume", "n_buy": "count", "n_sell": "count"}))
DVOL = dict(path=rf"{D}\btc_dvol_hourly\btc_dvol_hourly.parquet",
    declare=dict(instrument="Deribit BTC DVOL implied-vol index", venue="Deribit", time_col="ts_ms",
                 columns={"open": "indicative", "high": "indicative", "low": "indicative", "close": "indicative"}))
HSPREAD = dict(path=rf"{D}\btc_hist_halfspread_hourly\btc_hist_halfspread_hourly.parquet",
    declare=dict(instrument="BTCUSDT measured half-spread (bp)", venue="Binance (per source cache)",
                 time_col="index", columns={"half_bp": "other"}))
FUNDING = dict(path=rf"{D}\btcusdt_funding_8h\btcusdt_funding_8h.parquet",
    declare=dict(instrument="BTCUSDT perpetual funding rate", venue="Binance USD-M futures", time_col="t",
                 columns={"funding": "rate"}))
METRICS = dict(path=rf"{D}\btcusdt_metrics_5m\btcusdt_metrics_5m.parquet",
    declare=dict(instrument="BTCUSDT perpetual", venue="Binance USD-M futures", time_col="create_time",
                 columns={"sum_open_interest": "open_interest", "sum_open_interest_value": "open_interest",
                          "count_toptrader_long_short_ratio": "ratio", "sum_toptrader_long_short_ratio": "ratio",
                          "count_long_short_ratio": "ratio", "sum_taker_long_short_vol_ratio": "ratio",
                          "o": "trade_print", "h": "trade_print", "l": "trade_print", "c": "trade_print",
                          "v": "volume", "n": "count", "tbv": "volume"}))


def load(spec, cell, use=None, lo=TRAIN_LO, hi=TRAIN_HI):
    df = G.load(spec["path"], run_dir=RUN, cell=cell, declare=spec["declare"], use=use,
                train_lo=lo, train_hi=hi)
    t = spec["declare"]["time_col"]
    return df.set_index(t).sort_index()


def save(fig, name):
    fig.savefig(f"plots/{name}.png", bbox_inches="tight", dpi=120); plt.close(fig); print(f"[plot] plots/{name}.png")


def explore(df):
    return df.loc[:EXPLORE_HI]


def confirm(df):
    return df.loc[CONFIRM_LO:TRAIN_HI]
