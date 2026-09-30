# Phase 0 cell p0_00 - coverage counts ONLY (no returns), to declare SPLITS.md. Also runs the guard on
# all 224 files (time column only) so every file's cut is verified in this run, not just trusted.
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd, numpy as np
from guarded_load import load, _manifest, COINS, RUN
man = _manifest()
rows = []
for _, r in man.iterrows():
    d = load(r.file, "p0_00", "FULL-TO-VALEND", columns=[])
    rows.append((r.family, r.file, len(d), d.t.min(), d.t.max(), (d.t < pd.Timestamp("2023-03-20", tz="UTC")).sum()))
cov = pd.DataFrame(rows, columns=["family", "file", "rows", "first", "last", "rows_train"])
cov.to_csv(os.path.join(RUN, "tables", "p0_00_all_files_coverage.csv"), index=False)
print("files", len(cov), "rows", cov.rows.sum(), "max last", cov["last"].max())
print(cov.groupby("family").agg(files=("file", "count"), rows=("rows", "sum"), first=("first", "min"), last=("last", "max")))
# primary panel coin-hours per quarter in TRAIN
ph = {}
for c in COINS:
    d = load(f"spot/binance_{c}.parquet", "p0_00", "ALL-TRAIN-COVERAGE", columns=[])
    ph[c] = d.t.dt.to_period("Q").value_counts().sort_index()
q = pd.DataFrame(ph).fillna(0).astype(int)
q["total"] = q.sum(1); q["coins_live"] = (q[COINS] > 0).sum(1)
q["cum_share"] = q.total.cumsum() / q.total.sum()
q.to_csv(os.path.join(RUN, "tables", "p0_00_primary_coinhours_by_quarter.csv"))
print(q.to_string())
