import pandas as pd
# Declared in SPLITS.md from coverage counts only (p0_00), before any forward return was measured. Never revised.
SPLITS = {
    "EXPLORE": (pd.Timestamp("2017-08-17", tz="UTC"), pd.Timestamp("2021-07-01", tz="UTC")),   # [lo, hi)
    "CONFIRM": (pd.Timestamp("2021-07-08", tz="UTC"), pd.Timestamp("2023-03-20", tz="UTC")),   # to TRAIN_END 2023-03-19 incl.
    "VAL":     (pd.Timestamp("2023-03-25", tz="UTC"), pd.Timestamp("2023-12-01", tz="UTC")),   # opened once, Phase 3 only
}
