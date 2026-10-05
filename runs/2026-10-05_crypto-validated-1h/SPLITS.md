# SPLITS — declared 2026-10-05 ~12:35 UTC from COVERAGE COUNTS ONLY, before any forward return was measured

Never revised after a forward return is measured (RUNBOOK_v3 HOLDOUTS; x101 `G.declare_split` mechanics).
Evidence used: `tables/00_coverage_primary_by_quarter.csv` (primary/ row counts per coin per quarter, TRAIN only) and
row counts per year of 12 representative explanatory files (printed by `code/p0_coverage.py`). No price or return was read.

## Choices and why
- TRAIN usable span for the PRIMARY TARGET: 2019-01-01 (earliest primary row) -> TRAIN_END 2023-03-19 (inclusive).
- Longest horizon this run intends to use: 72h (3 days). Embargo between slices: 7 days (>= 72h, matches the
  runbook's example and the 2023-03-19 -> 2023-03-25 TRAIN/VAL gap).
- Minimum CONFIRM fold length: **150 days** (so a daily-return test has >= ~150 days x >= 8 coins; below that a fold
  cannot carry a cost-sized effect with any power). A three-way cut of 2021-07-08 -> 2023-03-20 gives 177 / 174 / 255
  days: all >= 150, so **n = 3** (the default).
- EXPLORE 2019-01-01 -> 2021-07-01 (912 days): holds 2019-2021H1 for the 6 long-history coins, ADA from 2020, DOT from
  2020-08, SOL/DOGE from 2021-01, BCH from 2019-11; holds the first 18 months of funding / perp premium (from 2020-01),
  BTC perp metrics from 2020-09, Deribit funding from 2019-05, and 3 months of DVOL. All EXPLORE primary rows are
  `binance_trade` (FTMO starts 2022-01-01, inside C1's embargo boundary -> C2).
- C1 2021-07-08 -> 2022-01-01: 177 days, 10 coins (BCH ends 2021-12-31), all `binance_trade`.
- C2 2022-01-08 -> 2022-07-01: 174 days, 9 coins, 7 coins on `ftmo_mid` (source switch 2022-01-01 falls in the
  C1->C2 embargo, so no fold straddles it).
- C3 2022-07-08 -> 2023-03-20: 255 days, 9 coins, 7 on `ftmo_mid`.
- VAL as TARGET.md: 2023-03-25 -> 2023-12-01 (exclusive; = through VAL_END 2023-11-30).

Known consequence, stated now: EXPLORE and C1 are Binance last-trade prints; C2/C3 are FTMO mids for 7 coins. A
short-horizon effect that lives in bid/ask bounce would show on EXPLORE/C1 and vanish on C2/C3 (data-hygiene.md, Roll).

## Machine-readable block (gate.py)
slices:
- EXPLORE 2019-01-01 2021-07-01
- C1 2021-07-08 2022-01-01
- C2 2022-01-08 2022-07-01
- C3 2022-07-08 2023-03-20
- VAL 2023-03-25 2023-12-01

(from inclusive, to exclusive, UTC dates.) A forward return belongs to a slice only if its START and its END both lie
inside the slice.
