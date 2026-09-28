# ATTEMPTS (every look, recorded, never capped)

Splits from TARGET.md: TRAIN_END = 2023-03-19 (inclusive, through 23:59 UTC); VAL_START = 2023-03-25; VAL_END = 2023-11-30.
Embargo 2023-03-20..24 is used by nothing. TRAIN is used by every cell; VAL is opened once, at step 7.

| # | when (UTC) | cell | data | what was looked at |
|---|---|---|---|---|
| 1 | 2026-09-25 | 00 data card | ALL rows, structure only | row counts, min/max stamp, month/day first-last minute, open vs prev close on TRAIN; no VAL distribution stats |
| 2 | 2026-09-25 | step 1 search | none (browser) | 5 SSRN pages, see DECISIONS.md page log |
| 3 | 2026-09-25 | 01 C1 existence | TRAIN | half-hour table, daily legs, coverage/zero shares by year, std by era -> SUPPORTED (2,038/2,040 days) |
| 4 | 2026-09-25 | 02 C2 assumption | TRAIN | half-hour volume shares; boundary vs median half-hour -> SUPPORTED narrowly (first 1.204x; last 0.918x) |
| 5 | 2026-09-25 | 03 C8 decay-first | TRAIN | 5 era slopes, rolling slope, Chow x4, CUSUM -> MIXED/INCONCLUSIVE (4 of 5 eras negative, all |t|<1) |
| 6 | 2026-09-25 | 04 C5 effect | TRAIN | pooled OLS/NW, Pearson/Spearman at tau 1/5/20, lead-lag x47, binomial -> REFUTED (slope -0.038, t -1.23). Hunt stopped. VAL not opened. |
Total looks at TRAIN: 4 cells (01-04). Looks at VAL: 0. Tests on the claim horizon scored: C1, C2, C8, C5. Unscored reported numbers: 3 tau ICs, 47 lead-lag ICs, 4 Chow, 1 CUSUM.
