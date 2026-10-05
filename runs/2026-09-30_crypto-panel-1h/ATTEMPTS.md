# ATTEMPTS — every look at the data, in order. K counts every EXPLORE / CONFIRM / VAL look (for downstream DSR deflation).

| # | cell | slice | hypothesis | what was looked at | result (one line) | K running |
|---|---|---|---|---|---|---|
| 1 | p0_00 | ALL TRAIN (coverage counts only) | - | row counts per quarter, guard on 224 files | split declared (SPLITS.md); no returns computed | 0 (coverage, not a look at returns) |
| 2 | p0_01 | EXPLORE | - | return / activity distributions | fat tails 10/10; LTC zero-mass 1.1% | 1 |
| 3 | p0_02 | EXPLORE | - | missingness | consistent with known facts | 2 |
| 4 | p0_03 | EXPLORE | - | ACF r, |r|, vol, rel at 8 lags; VR; Roll | lag 1, 2, 24 negative 10/10; VR(6) 0.86 | 3 |
| 5 | p0_03b | EXPLORE | - | daily ACF raw/rel; cross-sectional quintile sort | raw ACF(1) -0.089 (6/10); quintiles flat (t 0.72) | 4 |
| 6 | p0_04 | EXPLORE | - | cross-coin corr; within-coin twins; venue twin; |r|~vol | no coin twins; vol=quote_vol twin; venue twin 0.95 | 5 |
| 7 | p0_04e | EXPLORE | - | volume shock x winners/losers, next-day rel return | +42 bp, t 1.5 (not significant) | 6 |
| 8 | p0_05 | EXPLORE | - | stats 1-4 by era; CUSUM | ACF(24) stable negative; 2020 kurtosis; vol break 2018-04 | 7 |
| 9 | p0_06 | EXPLORE | - | hour / weekday profiles of vol and |r| | volume clock 1.88x; |r| 1.47x; weekday < 1.3x | 8 |
| 10 | p0_07 | EXPLORE | - | row physics, venue alignment | open-stamped trade print; zero-gap 0.16-0.32 (below card band) | 9 |
| 11 | cell_01 | CONFIRM (1st opening for H5) | H5 | 6h-block IC lag 1 (+ pre-registered descriptive lags 2-4, halves, per coin) | supported: IC -0.032, z -1.89; half2 only; below cost | 10 |
| 12 | cell_02 | EXPLORE (H6 born on CONFIRM) | H6 | 6h IC, high trailing-vol days minus other (+ terciles, eras) | supported: -0.081, z -2.48 | 11 |
| 13 | cell_03 | CONFIRM (1st opening for H3) | H3 | 1h IC at lags 23/24/25 (+ desc lags 1,2,12,48, halves, per coin, by hour) | supported: -0.035, z -4.38; below economic size | 12 |
| 14 | cell_04 | CONFIRM (1st opening for H4) | H4 | daily FM interaction rel x volume shock (+ b1, b2, halves, tercile table) | refuted: b3 -14.5 bp, z -2.32 (opposite sign) | 13 |
| 15 | cell_05 | EXPLORE (redirect for H4, no weight) | (H4 closed) | FM interaction by era, raw + rank | absent everywhere: b3 +3.6 bp, z 0.40 | 14 |
| 16 | cell_06 | CONFIRM (1st opening for H1) | H1 | daily IC lag 1 (+ lags 2,3,7, halves, per coin, big-move split, weekday, deciles) | refuted: -0.047, z -1.38; extreme days -0.227 vs -0.027 | 15 |
| 17 | cell_07 | EXPLORE (redirect for H1, no weight) | (H1) | daily IC on top-10% |r| days vs others, by era | extreme-days only: -0.299 (z -2.5) vs -0.023; spawned H7 | 16 |
| 18 | cell_08 | CONFIRM (1st opening for H2) | H2 | daily IC, high panel-volume-shock days minus other (+ terciles, halves, excl. big moves) | supported: -0.202, z -2.14 | 17 |
| 19 | cell_09 | VAL (the session's one VAL opening) | H5 | 6h-block IC lag 1 (+ ex-BTC, per coin, halves, decay) | supported: -0.063, z -2.85; below costs | 18 |

**K = 18 looks**: 9 Phase 0 looks on EXPLORE (p0_01..p0_07, p0_03b, p0_04e) + 9 test cells = 5 CONFIRM openings (cell_01 H5,
cell_03 H3, cell_04 H4, cell_06 H1, cell_08 H2) + 3 EXPLORE cells (cell_02 H6, cell_05 and cell_07 redirects) + 1 VAL opening
(cell_09 H5). Each test cell also printed pre-registered descriptives (other lags / halves / per coin) that are not separate
decisions but ARE extra looks: counting every printed IC, the effective number of statistics seen is ~120; downstream DSR
deflation should use K >= 18 and treat ~120 as the upper bound. The cell_04 debug load re-read the same CONFIRM data to check an
intercept (no new statistic). Power simulations touched no data.
