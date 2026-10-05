# STOP_REASON

rule: S4
open_count: 2
low_count: 1
high_count: 0
detail: S4 slices exhausted after 14 cells (7 tests + 7 redirects, ~25 min of wall clock by the sandbox clock) - H1 (OPEN 0.321) born EXPLORE, opened C1 C2 C3 (all refuted): no admissible slice; H2 (OPEN 0.059) born EXPLORE, opened C1 C2 C3 (all refuted): no admissible slice; H3 is LOW (0.049) after C1. No redirect qualified to spawn a child, so no hypothesis is pickable. S2 not claimed (only one pick, cell_13, was <= 3 pp). Not S3 (14 of 30 cells).

H1 and H2 are left OPEN only because each fold's refuted weight is weak (low power, 0.20-0.31); opening a fresh slice
(TEST) for them is the user's call, and nothing in this run argues for it. No VAL cell was run: nothing reached
HIGH-CONFIRM (VAL stays unopened by this session).
