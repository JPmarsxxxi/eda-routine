# STOP_REASON

rule: S2
open_count: 3
low_count: 3
high_count: 1
detail: S2 — three consecutive picks with best expected shift <= 3 pp on every pickable hypothesis (code/pick.py tables in cells/cell_26_rule.md, cells/cell_27_rule.md and code/pick.py after cell_27): before cell_26 best = H5 on C1 0.42 pp; before cell_27 best = H5 on C2 1.96 pp; after cell_27 best = H5 on C3 1.69 pp (H5 on EXPLORE 0.32 pp) — the third pick was not run. Admissible tests still exist (H5: C3, EXPLORE), they are just not worth running: #4 is all-ties on most days (power ~0.1-0.2). Earlier S2 counts were reset whenever a pick exceeded 3 pp (code/s2_log.md). Counts are final, after the Phase-3 VAL cell (cell_28: H1 refuted on VAL, stays HIGH-CONFIRM at 0.852). Cells used: 27 Phase-2 cells (19 test + 8 redirect, ATTEMPTS.md) + 1 VAL; the S3 cap is 30; wall clock ~0.5 h of 3 h. Other non-resolved: H4 OPEN 0.079 (all four slices used), H7 OPEN 0.09 (born C3, seen_on EXPLORE/C1/C2: no TRAIN slice left), H1 HIGH-CONFIRM (VAL refuted).
