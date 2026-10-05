"""Guarded loader for this run (TARGET.md NOTES: no eda_guard.py in this checkout, so the guard is an
assertion at every load that no row is later than VAL_END; every load is appended to ACCESS_LOG.md).
Also enforces the slice discipline declared in SPLITS.md: callers ask for a slice by name and get only
those rows; VAL may be requested only by a cell whose id is passed and is logged as a VAL opening."""
import os, datetime as _dt
import pandas as pd

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = "/home/user/eda-routine/data/crypto_panel_2026-09-30"
VAL_END = pd.Timestamp("2023-11-30 23:59:59", tz="UTC")
COINS = ["BTCUSD", "ETHUSD", "BNBUSD", "SOLUSD", "XRPUSD", "DOGEUSD", "ADAUSD", "LTCUSD", "BCHUSD", "DOTUSD"]

# Declared in SPLITS.md (filled after the coverage cell; None until then)
SPLITS = None
_split_file = os.path.join(RUN, "code", "splits.py")
if os.path.exists(_split_file):
    from importlib.machinery import SourceFileLoader
    SPLITS = SourceFileLoader("splits", _split_file).load_module().SPLITS


def _log(line):
    with open(os.path.join(RUN, "ACCESS_LOG.md"), "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def _manifest():
    return pd.read_csv(os.path.join(DATA, "MANIFEST.csv"))


def load(relpath, who, slice_name="ALL-TRAIN-COVERAGE", columns=None):
    """relpath like 'spot/binance_BTCUSD.parquet'. slice_name in SPLITS keys, or 'ALL-TRAIN-COVERAGE'
    (coverage counts / metadata only; still truncated at TRAIN_END), or 'FULL-TO-VALEND' (the guard
    check itself, used only by the coverage cell to verify CUT)."""
    full = os.path.realpath(os.path.join(DATA, relpath))
    assert full.startswith(os.path.realpath(DATA) + os.sep), f"refusing path outside DATA: {full}"
    man = _manifest().set_index("file")
    tcol = man.loc[relpath, "time_col"]
    df = pd.read_parquet(full, columns=None if columns is None else list(dict.fromkeys([tcol] + columns)))
    t = pd.to_datetime(df[tcol], utc=True)
    mx = t.max()
    ok = bool(mx <= VAL_END)
    stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _log(f"| {stamp} | {who} | {relpath} | rows={len(df)} | max={mx} | guard max<=VAL_END: {'PASS' if ok else 'FAIL'} | slice={slice_name} |")
    if not ok:
        raise AssertionError(f"GUARD FAIL: {relpath} has row {mx} > VAL_END {VAL_END} -> STOPPED.md")
    df = df.rename(columns={tcol: "t"})
    df["t"] = t
    df = df.sort_values("t").reset_index(drop=True)
    if slice_name == "FULL-TO-VALEND":
        return df
    if slice_name == "ALL-TRAIN-COVERAGE":
        return df[df.t < pd.Timestamp("2023-03-20", tz="UTC")].reset_index(drop=True)
    assert SPLITS is not None, "SPLITS.md not declared yet"
    lo, hi = SPLITS[slice_name]
    return df[(df.t >= lo) & (df.t < hi)].reset_index(drop=True)


def spot(coin, who, slice_name, columns=None):
    return load(f"spot/binance_{coin}.parquet", who, slice_name, columns)
