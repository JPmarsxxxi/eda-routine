"""Holdout guard for this run (TARGET.md NOTES: no eda_guard.py in this checkout -> an assertion at every
load that no row is later than VAL_END, logged). Every parquet this run reads goes through load()."""
import datetime as _dt
import os

import pandas as pd

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = "/home/user/eda-routine/data/crypto_panel_validated_2026-10-05"
VAL_END = pd.Timestamp("2023-11-30 23:59:59", tz="UTC")
LOG = os.path.join(RUN, "ACCESS_LOG.md")
_MAN = None


def manifest():
    global _MAN
    if _MAN is None:
        _MAN = pd.read_csv(os.path.join(DATA, "MANIFEST.csv"))
    return _MAN


def load(rel, cell="?"):
    """Read DATA/rel, find its time column from MANIFEST.csv, assert max(time) <= VAL_END, log the load."""
    path = os.path.realpath(os.path.join(DATA, rel))
    assert path.startswith(DATA + os.sep), f"guard: {rel} is outside the run's data folder"
    m = manifest()
    row = m[m.file == rel]
    assert len(row) == 1, f"guard: {rel} not in MANIFEST.csv"
    tcol = row.time_col.iloc[0]
    df = pd.read_parquet(path)
    t = pd.to_datetime(df[tcol], utc=True)
    tmax = t.max()
    ok = bool(tmax <= VAL_END)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(f"| {_dt.datetime.utcnow():%Y-%m-%d %H:%M:%S} | {cell} | data/{os.path.basename(DATA)}/{rel} | "
                 f"{len(df):,} | {t.min()} | {tmax} | {'PASS' if ok else 'FAIL'} |\n")
    if not ok:
        raise AssertionError(f"guard: {rel} has a row at {tmax} > VAL_END {VAL_END} -> STOPPED.md")
    df = df.copy()
    df["_t"] = t
    return df
