rule: S4
open_count: 3
low_count: 3
high_count: 0
detail: S4 - pick_21 found no pickable hypothesis: H1 (0.8497 OPEN) has opened EXPLORE, C1, C2, C3; H2 (0.17 OPEN) opened EXPLORE, C1, C2, C3; H6 (0.49 OPEN) was born on C1 and opened C2, C3, EXPLORE; H3, H4, H5 are LOW. 20 Phase-2 cells (17 tests, 3 redirects), well under S3's 30.

# STOP_REASON — notes (not parsed)

- `tables/pick_21.txt` is the step-1 pick that found nothing admissible (written by `code/pick.py`); gate.py recomputes the
  same admissibility from BELIEFS.md and the cell headers.
- Not S2: S2 needs admissible tests that are not worth running; here none exist. Not S1: H1, H2 and H6 are OPEN.
- VAL: no hypothesis reached HIGH-CONFIRM, so VAL was not opened (Phase 3 step 1 has nothing to do). H1 came closest:
  supported on C1 and C2 (posterior 0.8497, just under the 0.85 HIGH bar) and then flat on C3 and EXPLORE (inconclusive,
  weight 1, so neither moved it). Under v3.2, C3 had to be opened before any HIGH-CONFIRM in any case.
- The three OPEN hypotheses need a fresh slice to move (TEST is the user's to open, HOLDOUT_RULES rule 3).
