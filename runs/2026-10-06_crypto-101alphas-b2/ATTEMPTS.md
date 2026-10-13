# ATTEMPTS — every look, recorded, never capped (K)

Splits: SPLITS.md (EXPLORE 2019-01-01..2020-06-02; C1 2020-06-09..2021-05-13; C2 2021-05-20..2022-03-22; C3 2022-03-29..
2023-03-20; VAL 2023-03-25..2023-12-01). Phase 0 looks (EXPLORE only, no alpha related to a forward return): p0_00 coverage
counts (no returns); p0_profile §1-7 (`tables/p0_profile_summary.json`); p0 power: day-permutation nulls on EXPLORE (effect
destroyed by construction, `tables/power.csv`). Every Phase-2 row below is one slice opening and counts in K.

| # | when (UTC) | cell | hypothesis | slice | result |
|---|---|---|---|---|---|
| 1 | 2026-10-06 10:32 | cell_01 test | H2 A35 | C1 | IC +0.0101 t +0.52 n 328 -> inconclusive (w 1; H2 0.170 -> 0.170 OPEN) |
| 2 | 2026-10-06 10:33 | cell_02 test | H2 A35 | C2 | IC -0.0086 t -0.46 n 286 -> inconclusive (w 1; H2 0.170 -> 0.170 OPEN) |
| 3 | 2026-10-06 10:33 | cell_03 test | H2 A35 | C3 | IC +0.0034 t +0.14 n 297 -> inconclusive (w 1; H2 0.170 -> 0.170 OPEN) |
| 4 | 2026-10-06 10:33 | cell_04 test | H3 A38 | C1 | IC +0.0191 t +0.88 n 329 -> inconclusive (w 1; H3 0.170 -> 0.170 OPEN) |
| 5 | 2026-10-06 10:33 | cell_05 test | H3 A38 | C2 | IC -0.0192 t -0.97 n 287 -> refuted (w 0.192; H3 0.170 -> 0.038 LOW) |
| 6 | 2026-10-06 10:33 | cell_06 redirect | H3 A38 x-1 | C2 | IC +0.0192 t +0.97 n 287 -> inconclusive (w 1; H3 0.038 -> 0.038 LOW) |
| 7 | 2026-10-06 10:33 | cell_07 test | H5 A54 | C1 | IC -0.0521 t -2.44 n 329 -> refuted (w 0.223; H5 0.170 -> 0.044 LOW) |
| 8 | 2026-10-06 10:34 | cell_08 redirect | H5 A54 x-1 | C1 | IC +0.0521 t +2.44 n 329 -> supported (w 1; H5 0.044 -> 0.044 LOW) |
| 9 | 2026-10-06 10:34 | cell_09 test | H6 A54 x-1 | C2 | IC +0.0567 t +2.35 n 287 -> supported (w 5.44; H6 0.150 -> 0.490 OPEN) |
| 10 | 2026-10-06 10:34 | cell_10 test | H6 A54 x-1 | C3 | IC +0.0229 t +1.01 n 298 -> inconclusive (w 1; H6 0.490 -> 0.490 OPEN) |
| 11 | 2026-10-06 10:34 | cell_11 test | H6 A54 x-1 | EXPLORE | IC +0.0091 t +0.39 n 504 -> inconclusive (w 1; H6 0.490 -> 0.490 OPEN) |
| 12 | 2026-10-06 10:34 | cell_12 test | H1 A30 | C1 | IC +0.0371 t +1.73 n 329 -> supported (w 5.1; H1 0.170 -> 0.511 OPEN) |
| 13 | 2026-10-06 10:34 | cell_13 test | H1 A30 | C2 | IC +0.0480 t +2.29 n 287 -> supported (w 5.41; H1 0.511 -> 0.850 OPEN) |
| 14 | 2026-10-06 10:34 | cell_14 test | H1 A30 | C3 | IC +0.0013 t +0.07 n 298 -> inconclusive (w 1; H1 0.850 -> 0.850 OPEN) |
| 15 | 2026-10-06 10:35 | cell_15 test | H4 A53 | C1 | IC +0.0096 t +0.50 n 329 -> inconclusive (w 1; H4 0.150 -> 0.150 OPEN) |
| 16 | 2026-10-06 10:35 | cell_16 test | H4 A53 | C2 | IC -0.0042 t -0.19 n 287 -> inconclusive (w 1; H4 0.150 -> 0.150 OPEN) |
| 17 | 2026-10-06 10:35 | cell_17 test | H4 A53 | C3 | IC -0.0291 t -1.39 n 298 -> refuted (w 0.189; H4 0.150 -> 0.032 LOW) |
| 18 | 2026-10-06 10:35 | cell_18 redirect | H4 A53 x-1 | C3 | IC +0.0291 t +1.39 n 298 -> inconclusive (w 1; H4 0.032 -> 0.032 LOW) |
| 19 | 2026-10-06 10:35 | cell_19 test | H2 A35 | EXPLORE | IC +0.0104 t +0.39 n 371 -> inconclusive (w 1; H2 0.170 -> 0.170 OPEN) |
| 20 | 2026-10-06 10:35 | cell_20 test | H1 A30 | EXPLORE | IC -0.0069 t -0.30 n 429 -> inconclusive (w 1; H1 0.850 -> 0.850 OPEN) |

Totals: 17 slice openings (H2 x4, H1 x4, H6 x3, H4 x3, H3 x2, H5 x1) + 3 redirect re-reads (cells 06, 08, 18) = **K 20**.
VAL openings: 0. Phase 0 looks: 7 profile sections + day-permutation nulls (EXPLORE only).
