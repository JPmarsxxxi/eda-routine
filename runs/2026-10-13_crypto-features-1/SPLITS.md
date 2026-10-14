# SPLITS (declared 2026-10-13 from coverage counts only, BEFORE any forward return was measured)

Coverage counts (hourly primary rows, TRAIN only, from code/p0_01_coverage.py; ACCESS_LOG phase0_01):
EXPLORE 2019-01..2021-06: BTC ETH BNB XRP LTC 21,835 h each; ADA 13,103; BCH 13,909; DOT 7,572; SOL and DOGE 4,337 (from 2021-01).
C1 2021-H2: all 10 coins, 4,242 h each. C2 2022-H1: 9 coins (BCH ends 2021-12-31), ~4,045 h. C3 2022-07..2023-03-19: 9 coins, ~6,020 h.
Median coins per hour: EXPLORE 7, C1 10, C2 9, C3 9. Hours with >= 6 coins: EXPLORE 13,909, C1 4,242, C2 4,046, C3 6,023.
n = 3 CONFIRM folds: each has >= 4,000 hours (~170 days) with >= 6 coins, so three folds are not under the minimum length
(minimum: 4,000 hourly rows with >= 6 coins ~ 165 days). Embargo between neighbours = 7 days >= the longest horizon (24 h) and the
longest lookback-to-label overlap of any 1h/6h/24h target. Horizons declared for this run: next 1h, next 6h, next 24h
(every horizon tried counts in K). Folds match the C1/C2/C3 labels used by earlier runs on this panel, so MEMORY lines compare.

slices:
- EXPLORE 2019-01-01 2021-07-01
- C1 2021-07-08 2022-01-01
- C2 2022-01-08 2022-07-01
- C3 2022-07-08 2023-03-20
- VAL 2023-03-25 2023-12-01

TRAIN = EXPLORE + C1 + C2 + C3 (the guard's default bound 2023-03-19 23:59:59). VAL is opened only by `kind: val` cells,
with the guard's train_hi widened to VAL_END for that load, never in a search cell.
