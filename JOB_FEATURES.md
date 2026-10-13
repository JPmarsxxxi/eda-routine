# JOB: features — engineer as many predictive, non-redundant features as possible (v3.4)

Read RUNBOOK_v3.md first: every core rule there applies (TRAIN-only search, VAL only for frozen specs, never TEST, priors
updated after every cell, K counted, effort floors, gate.py). This file says only what is different for this job.

**The job.** From data we already have (TARGET.md `DATA`), build as many features with predictive power as possible, and
keep only those that add something: each new feature is checked against the others and against the library. The product
is the shared feature library `features\`, which every later run (any job) starts from.

**The target** is the forward return of the bundle's main instrument(s), at the horizons this run declares (each horizon
tried counts in K). TARGET.md may name a different one.

## Start from the library

Read `features\REGISTRY.md` first. Existing features are the baseline: a new one must beat them on incremental power, and
library features may be recombined, transformed or ported to this dataset (say which, and the parent id).

## What a hypothesis is here

A **feature family** — one mechanism, many parameterisations: e.g. "short-horizon reversal scaled by volume", "funding
pressure", "range position". `hypothesis:` "[family] predicts [target, horizon] because [reason]". Search cells sweep the
family's transforms and parameters: lookbacks, normalisations (trailing z-score, rank, ratio to trailing volatility),
differences vs levels, interactions, regime conditioning. Count every variant in `variants:`.

## Two numbers every search cell reports

1. **Predictive power** — rank IC (or the family's natural statistic) per fold, and its stability across folds.
2. **Orthogonality** — max |correlation| with every library feature and every other feature this run has kept, and the
   **incremental** IC after partialling out the most correlated ones. A feature with max |corr| above 0.7 is a duplicate
   unless its incremental IC clears `min_useful`; it is merged into the existing feature (a variant), not added.

## Freeze, confirm, VAL

Freeze one candidate per kept feature with `feature: <id>` in `candidates\F<n>.md` and the construction floor from the core
(point-in-time, trailing-only scaling, tails stated, raw and market-neutral versions, market correlation reported). Confirm
and VAL as in the core.

## Product — `features\`

- `features\<id>.py` — a pure function `compute(df) -> pd.Series` from carded columns, point-in-time, no look-ahead. Ids
  are `f` + a zero-padded number, never reused.
- `features\REGISTRY.md` — one row per feature (gate.py parses it):
  ```
  | id | family | definition | inputs | dataset | code | folds | val | max_corr | incremental | status | run |
  |---|---|---|---|---|---|---|---|---|---|---|---|
  | f001 | reversal | -(6h log return) / trailing 30d vol | close | crypto_panel_validated_2026-10-05 | features/f001.py | C1+ C2+ C3= | +0.041 | 0.31 (f000) | +0.012 | VAL-PASS | <run> |
  ```
  `status`: CONFIRM-SHOWN, CONFIRM-FAIL, VAL-PASS or VAL-FAIL (must match the candidate). A feature tried on another dataset
  later gets a new row with the same family and a pointer to the original id in `definition`.
- Every candidate this run froze has a row; dropped families get one line each in REPORT.md, not a row.
