# ATTEMPTS: every look at the data, in order

Splits (from TARGET.md, Step 1):
- TRAIN: 2017-08-17 04:00 -> **2023-03-19** 23:59 UTC (explore here only)
- EMBARGO: 2023-03-20 -> 2023-03-24 (ignored)
- VAL: **2023-03-25 -> 2023-11-30** (opened ONCE, Step 6, top-3 leads, rules written first)
- TEST: not given, not looked for.

TRAIN loader: `scripts/lib.py::load_train` reads the parquet with a pyarrow filter `t <= 2023-03-19 23:59:59 UTC` and asserts it.

| # | when (UTC run order) | script | rows read | what was looked at |
|---|---|---|---|---|
| A0 | 1 | inline python (schema) | index only, all rows | schema + min/max stamp: max == 2023-11-30 23:59 == VAL_END -> no row past VAL_END. No values of VAL looked at. |
| A1 | 2 | s0_datacard.py | TRAIN | day boundaries, activity by minute-of-hour (2018+), zero-gap rate, Roll, Corwin-Schultz by year |
| A2 | 3 | s2a_memory.py (run twice: 2nd run only changed plot 02's title to computed numbers) | TRAIN | sweep 01-05 |
| A3 | 4 | s2b_dist.py (run twice: 2nd run only changed plot 07's title) | TRAIN | sweep 06-08 + HAC p for ACF lags 2, 7 |
| A4 | 5 | s2c_predict.py (run twice: 2nd run only changed plots 12, 13 titles) | TRAIN | sweep 09-14 |
| A5 | 6 | s4_checks.py (1st run crashed at the OBS1 session split before writing any table; fixed the loop, re-ran whole script) | TRAIN | Step 4 checks OBS1-OBS7, BH table |
| A6 | 7 | s5_rank.py | tables only | BH plot, Bayes ranking |
| A7 | 8 | **s6_val.py: THE ONE VAL OPENING** (rules in VAL_RULES.md written first) | VAL 2023-03-25 -> 2023-11-30 only (361,440 rows) | L1 (OBS5), L2 (OBS6), L3 (OBS1) |
| A8 | 9 | s6b_val_replot.py | tables/24_val_results.json only (VAL not re-read) | redraw of plot 24 (title overlap) |

Embargo rows (2023-03-20 -> 2023-03-24) were never read: the TRAIN loader stops at 2023-03-19 23:59 and the VAL loader starts at 2023-03-25 00:00.
