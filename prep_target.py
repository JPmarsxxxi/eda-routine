"""prep_target.py: build the copy of a dataset the EDA routine is allowed to see.

The routine is never given TEST or SEALED data. Rather than trust it to stay away, this script writes a copy that
STOPS at the end of the VAL window, so the rows do not exist anywhere the routine reads.

    python prep_target.py <source parquet file OR folder of dated parquets> <name> [--time-col t]

Output: C:\\Users\\User\\eda-routine\\data\\<name>\\   (data + CUT.json)

What it prints: ONLY the range and row count of the OUTPUT (which is <= the cutoff by construction). It never
prints, computes or plots anything about the source's full range: a coverage check on the sealed range has
already been recorded as a breach in _SEALED_HOLDOUT.md.

Cutoffs (calendar, UTC) come from _SEALED_HOLDOUT.md and the BTC split dates:
    TRAIN  <= 2023-03-19      VAL  2023-03-25 -> 2023-11-30      (TEST 2023-12-06 -> 2024-07-31 and everything
    from 2024-08-01 are NEVER copied). The SAME calendar cut is applied to every crypto asset, because a coin's
    behaviour in another coin's TEST window reveals that window (crypto is highly correlated).
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys

import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq

CUTOFF = dt.datetime(2023, 11, 30, 23, 59, 59, 999999, tzinfo=dt.timezone.utc)   # end of VAL, inclusive
CUT_DATE = dt.date(2023, 11, 30)
SPLITS = {"TRAIN_END": "2023-03-19", "VAL_START": "2023-03-25", "VAL_END": "2023-11-30"}
OUT_ROOT = r"C:\Users\User\eda-routine\data"
SRC_ROOT = r"C:\Users\User\backtest_engine\backtest_engine2\data"


def refuse(msg):
    print("REFUSED:", msg)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("name")
    ap.add_argument("--time-col", default=None, help="timestamp-typed column; default: a column called 't'")
    ap.add_argument("--accept-ftmo-leak", action="store_true",
                    help="allow an FTMO series (see refusal message before using this)")
    a = ap.parse_args()

    src = os.path.abspath(a.source)
    if not os.path.exists(src):
        refuse(f"{src} does not exist")
    if os.path.abspath(OUT_ROOT).lower() in src.lower():
        refuse("source is already inside the routine's data folder")
    if "ftmo" in src.lower() and not a.accept_ftmo_leak:
        refuse("FTMO BTCUSD's open window (2025-08 -> 2026-04) lies INSIDE the Binance sealed range (from "
               "2024-08-01). It is the same asset, so handing it over reveals how BTC behaved in the sealed period. "
               "It is also not aligned to the TRAIN/VAL calendar used here. Not prepared by default.")
    if not re.fullmatch(r"[A-Za-z0-9_\-]+", a.name):
        refuse("name must be letters, digits, _ or -")

    out = os.path.join(OUT_ROOT, a.name)
    if os.path.exists(out):
        refuse(f"{out} already exists; delete it deliberately if you want to rebuild")
    os.makedirs(out)
    n_rows = None
    lo = hi = None

    if os.path.isdir(src):
        # folder of dated files: cut by FILENAME, no file is opened
        kept = 0
        for f in sorted(os.listdir(src)):
            m = re.match(r"^(\d{4})-(\d{2})(?:-(\d{2}))?\.parquet$", f)
            if not m:
                continue
            y, mo, d = int(m[1]), int(m[2]), int(m[3]) if m[3] else None
            # a monthly file is kept only if the WHOLE month is <= the cut month; a daily file if its day is <= cut
            keep = (dt.date(y, mo, d) <= CUT_DATE) if d else ((y, mo) <= (CUT_DATE.year, CUT_DATE.month))
            if keep:
                shutil.copy2(os.path.join(src, f), os.path.join(out, f))
                kept += 1
        if kept == 0:
            shutil.rmtree(out)
            refuse("no dated *.parquet files matched (expected YYYY-MM-DD.parquet or YYYY-MM.parquet)")
        files = sorted(os.listdir(out))
        print(f"OUTPUT: {kept} files, {files[0]} .. {files[-1]}   (cut by filename; contents not opened)")
        out_desc = f"{kept} dated files"
    else:
        schema = pq.read_schema(src)                      # metadata only, no rows
        col = a.time_col or ("t" if "t" in schema.names else None)
        if col is None or col not in schema.names:
            shutil.rmtree(out)
            refuse(f"no time column found. Columns: {schema.names}. Re-run with --time-col <a timestamp-typed column>")
        typ = schema.field(col).type
        if not pa.types.is_timestamp(typ):
            shutil.rmtree(out)
            refuse(f"column {col!r} is {typ}, not a timestamp; this script will not guess an epoch unit")
        tz = typ.tz
        scalar = pa.scalar(CUTOFF if tz else CUTOFF.replace(tzinfo=None), type=typ)
        table = ds.dataset(src).to_table(filter=ds.field(col) <= scalar)   # predicate pushdown
        dest = os.path.join(out, os.path.basename(src))
        pq.write_table(table, dest)
        n_rows = table.num_rows
        chk = table.column(col).to_pandas()
        lo, hi = chk.min(), chk.max()
        assert hi.to_pydatetime() <= CUTOFF.replace(tzinfo=hi.to_pydatetime().tzinfo), "cut failed"
        print(f"OUTPUT: {n_rows:,} rows, {lo} .. {hi}   (time column {col!r})")
        out_desc = f"{n_rows} rows"

    with open(os.path.join(out, "CUT.json"), "w") as fh:
        json.dump({
            "prepared_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "source": src, "name": a.name, "cutoff_inclusive_utc": CUTOFF.isoformat(),
            "splits": SPLITS, "output": out_desc,
            "note": "TEST (2023-12-06 -> 2024-07-31) and everything from 2024-08-01 were NOT copied.",
        }, fh, indent=2)
    print("CUT.json written. Splits for TARGET.md:", SPLITS)


if __name__ == "__main__":
    main()
