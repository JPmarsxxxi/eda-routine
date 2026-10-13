# SPLITS — EXPLORE / C1 / C2 / C3 (inside TRAIN) and VAL

Declared 2026-10-06 ~10:30 UTC by `code/p0_00_coverage.py` from **coverage counts only**: the number of primary coin-days with
all 24 hourly bars present, per quarter (`tables/p0_00_coin_days_by_quarter.csv`). No return of any kind had been computed when
this was written. **Never revised after this point.** Machine copy: `tables/p0_00_splits.json` (read by `code/common.py`).

slices:
- EXPLORE 2019-01-01 2020-06-02
- C1 2020-06-09 2021-05-13
- C2 2021-05-20 2022-03-22
- C3 2022-03-29 2023-03-20
- VAL 2023-03-25 2023-12-01

(from inclusive, to exclusive, UTC calendar days; a slice holds every SIGNAL day d whose response window, end of d to end
of d+1, lies inside it.)

**Cut.** n = 3 CONFIRM folds (the RUNBOOK_v3 default). The three cut dates are where cumulative TRAIN coin-days reach 25%, 50%
and 75% (2020-06-02, 2021-05-13, 2022-03-22), so each of the four slices holds about 2,880 coin-days. Each fold starts after a
7-day embargo (longest response horizon in this run is 1 day; 7 days is a margin, and keeps any EXPLORE-era statistic from
sharing a response window with a fold). Minimum fold length, declared now: 180 days; every fold is 300+ days, so n = 3 stands.

| slice | from | to (excl.) | approx coin-days | coins live (quarters inside) |
|---|---|---|---|---|
| EXPLORE | 2019-01-01 | 2020-06-02 | ~2,880 | 5 -> 7 |
| C1 | 2020-06-09 | 2021-05-13 | ~2,880 | 7 -> 10 |
| C2 | 2021-05-20 | 2022-03-22 | ~2,880 | 10 -> 9 (BCH ends 2021-12-31) |
| C3 | 2022-03-29 | 2023-03-20 | ~2,880 | 9 |
| VAL | 2023-03-25 | 2023-12-01 | not counted | 9 |

Signal INPUTS (Binance daily OHLCV) may use up to 40 days before a slice's start so that 32-day operators are defined from the
slice's first day (DECISIONS D6); RESPONSES never leave the slice. Regime content is noted, not chosen (calendar knowledge, not
measured): EXPLORE = 2019 recovery + the 2020-03 crash; C1 = the 2020-21 bull and alt-season; C2 = the late-2021 top and early
2022; C3 = the 2022 bear (LUNA, FTX) and early 2023; C3 is also the first fold where 7 coins' response is the FTMO mid, not
the Binance print the signal uses.

VAL_NOTE (TARGET.md), quoted wherever VAL is used: "VAL is weak evidence. (1) BTC VAL was crossed twice by earlier work and
overlaps a spent pooled row of an earlier BTC seasonality EDA. (2) VAL has since been opened ONCE more, on all 10 coins, for a
pre-registered test of the crash-day rebound topic (see ALREADY TESTED): SOFT-clean for every coin for that topic. (3) VAL may
be a DIFFERENT REGIME from TRAIN (2023 was calm; from 2023-04 BTC's 1-minute trade counts fell ~8x, cause not established)."

Rules (RUNBOOK_v3 v3.2 HOLDOUTS): every hypothesis here is SOURCE-born (the paper), so EXPLORE is an ordinary slice for it:
each may open EXPLORE once and C1, C2, C3 once each, in order; a child is never tested on its birth or `seen_on` slice; VAL
once per HIGH-CONFIRM hypothesis at Phase 3.
