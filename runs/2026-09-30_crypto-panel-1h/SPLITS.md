# SPLITS — EXPLORE / CONFIRM (inside TRAIN) and VAL

Declared 2026-09-30 ~12:40 UTC by cell p0_00 from **coverage counts only** (table `tables/p0_00_primary_coinhours_by_quarter.csv`,
all 224 files guard-checked `tables/p0_00_all_files_coverage.csv`). No return, forward or otherwise, had been computed when
this was written. **Never revised after this point.** Machine copy: `code/splits.py` (the loader slices before any return is
computed, so a forward return can never cross a slice boundary).

| slice | from (UTC, incl.) | to (UTC, excl.) | primary-panel coin-hours | share of TRAIN coin-hours | coins live |
|---|---|---|---|---|---|
| EXPLORE | 2017-08-17 | 2021-07-01 | 232,745 (2017Q3-2021Q2) | ~61% | 2 -> 10 (all 10 from 2020-08) |
| embargo | 2021-07-01 | 2021-07-08 | 7 days dropped | - | - |
| CONFIRM | 2021-07-08 | 2023-03-20 (TRAIN_END 2023-03-19 incl.) | ~148,700 (150,420 minus the 7-day embargo) | ~39% | 10 |
| (gap, per HOLDOUT_RULES) | 2023-03-20 | 2023-03-25 | - | - | - |
| VAL | 2023-03-25 | 2023-12-01 (VAL_END 2023-11-30 23:59:59) | opened once, Phase 3, only for HIGH-CONFIRM | - | 10 |

Why this cut (coverage reasoning only):
- ~60/40 by coin-hours gives EXPLORE enough to look and CONFIRM enough power: CONFIRM is ~20 months x 10 coins, ~14,500
  hours per coin (~600 days).
- Cut at a quarter boundary where all 10 coins had been live for 3+ quarters, so CONFIRM is a full, balanced 10-coin panel.
- 7-day embargo >= the longest horizon this run intends to use (168h), so no EXPLORE-born statistic shares a forward window
  with CONFIRM.
- Regime content is not chosen, it is only noted (from calendar knowledge, not measured): EXPLORE holds the 2018 bear, 2019,
  the 2020-03 crash and the 2020-21 bull; CONFIRM holds the late-2021 top, the 2022 bear (LUNA 2022-05, FTX 2022-11) and early
  2023. The two slices are different regimes by construction; a CONFIRM pass therefore also means "survived a regime change".
- VAL_NOTE (TARGET.md), quoted wherever VAL is used: "Two reasons VAL is weak evidence. (1) BTC VAL was crossed twice by
  earlier work (both pre-registered) and overlaps a spent pooled row of an earlier BTC seasonality EDA: SOFT-clean for BTC; clean
  for the other nine coins as far as this file knows. (2) VAL may be a DIFFERENT REGIME from TRAIN: from 2023-04 BTC's 1-minute
  trade counts fell ~8x (cause not established)."

Rules: Phase 0 and all hypothesis generation on EXPLORE only. A data-born hypothesis opens CONFIRM as its first and only
CONFIRM look (one opening per hypothesis id, logged in ATTEMPTS.md). VAL once per session at Phase 3.
