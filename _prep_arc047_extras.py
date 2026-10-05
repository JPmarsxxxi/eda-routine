"""One-off prep for the two arc #047 sources prep_target.py's generic path can't handle directly:

  - binance_hourly.parquet   -- multi-symbol (a `symbol` column); prep_target.py has no symbol filter,
                                 so it would carry every coin through instead of just BTCUSDT.
  - btcusdt_metrics_5m.parquet -- `create_time` is stored as a STRING, and prep_target.py deliberately
                                 refuses any non-timestamp-typed column rather than guess a parse.

Same cutoff, same CUT.json shape, same safety property (hard-stop at VAL_END, TEST/SEALED never
written) as prep_target.py -- just the two column-shape exceptions it doesn't cover. Not merged into
prep_target.py itself: keeps that shared, audited tool's contract (timestamp-typed column in, no
per-source special-casing) intact rather than growing it for a two-file exception.
"""
import datetime as dt
import json
import os

import pandas as pd

CUTOFF = dt.datetime(2023, 11, 30, 23, 59, 59, 999999, tzinfo=dt.timezone.utc)
SPLITS = {"TRAIN_END": "2023-03-19", "VAL_START": "2023-03-25", "VAL_END": "2023-11-30"}
SRC_ROOT = r"C:\Users\User\backtest_engine\backtest_engine2\data"
OUT_ROOT = r"C:\Users\User\eda-routine\data"


def write(name, df, tcol, source_note):
    out = os.path.join(OUT_ROOT, name)
    os.makedirs(out, exist_ok=True)
    dest = os.path.join(out, f"{name}.parquet")
    df.to_parquet(dest)
    lo, hi = df[tcol].min(), df[tcol].max()
    assert hi <= CUTOFF.replace(tzinfo=getattr(hi, "tzinfo", None)), "cut failed"
    print(f"OUTPUT {name}: {len(df):,} rows, {lo} .. {hi}   (time column {tcol!r})")
    with open(os.path.join(out, "CUT.json"), "w") as fh:
        json.dump({
            "prepared_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "source": source_note, "name": name, "cutoff_inclusive_utc": CUTOFF.isoformat(),
            "splits": SPLITS, "output": f"{len(df)} rows",
            "note": "TEST (2023-12-06 -> 2024-07-31) and everything from 2024-08-01 were NOT copied. "
                    "Prepared by _prep_arc047_extras.py, not prep_target.py (see its docstring for why).",
        }, fh, indent=2)


def prep_hourly_btc_only():
    src = os.path.join(SRC_ROOT, "binance_hourly.parquet")
    df = pd.read_parquet(src)
    n_all = len(df)
    df = df[df["symbol"] == "BTCUSDT"].copy()
    n_btc = len(df)
    df = df[df["open_time"] <= CUTOFF]
    write("btcusdt_perp_hourly", df, "open_time",
          f"{src} (filtered symbol==BTCUSDT: {n_btc:,}/{n_all:,} rows carried other symbols; not copied)")


def prep_metrics_5m():
    src = os.path.join(SRC_ROOT, "btcusdt_metrics_5m.parquet")
    df = pd.read_parquet(src)
    df["create_time"] = pd.to_datetime(df["create_time"], utc=True)
    df = df[df["create_time"] <= CUTOFF]
    write("btcusdt_metrics_5m", df, "create_time", src)


if __name__ == "__main__":
    prep_hourly_btc_only()
    prep_metrics_5m()
