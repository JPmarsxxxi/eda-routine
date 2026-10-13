# FEATURE LIBRARY — every feature a features run kept (JOB_FEATURES.md). Shared by all jobs; gate.py parses the table.

One row per feature (per dataset it was tried on). Code in `features/<id>.py`: `compute(df) -> pd.Series`, point-in-time,
no look-ahead. `status` follows the feature's candidate: CONFIRM-SHOWN, CONFIRM-FAIL, VAL-PASS or VAL-FAIL. `max_corr` is the
largest |correlation| with any other library feature (and which); `incremental` is its effect after partialling those out.

| id | family | definition | inputs | dataset | code | folds | val | max_corr | incremental | status | run |
|---|---|---|---|---|---|---|---|---|---|---|---|
