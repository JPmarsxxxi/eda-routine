# SPLITS — declared from coverage counts only, BEFORE any forward return was measured

Written 2026-10-05 ~14:40 UTC by `code/p0_splits.py`, which reads only `t` and `new_source` of primary/validated_<COIN>
(row existence and flags; no price enters any statistic). Never revised after a forward return is measured.

**Coverage unit.** A *valid response day* for a coin = all 24 hourly bars present and no `new_source=True` row (TARGET.md:
never take a return across one). A *usable day* = >= 5 coins with a valid response day (cross-sectional minimum, DECISIONS D5).
TRAIN (<= 2023-03-19) has 1,445 usable days and 11,363 usable coin-days.

**Cut.** n = 3 CONFIRM folds (the default). The cut points split TRAIN's usable coin-days into four equal quarters (cross-
sectional information grows with the number of coins, so equal coin-days rather than equal calendar time). Embargo between
slices: 7 days (>= the longest horizon this run intends to use, 1 day response; also >= the 6-day correlation window of #2).
**Minimum fold length: 250 usable days** (below that a fold's simulated power at the 20 bp/day economic effect drops under
~0.25 and the fold is not worth its K). Every fold clears it (smallest: C2, 283), so n = 3 stands.

| slice | from | to (excl.) | usable days | usable coin-days | mean coins/day | coins present |
|---|---|---|---:|---:|---:|---|
| EXPLORE | 2019-01-01 | 2020-05-28 | 503 | 2,835 | 5.64 | ADA BCH BNB BTC ETH LTC XRP |
| C1 | 2020-06-04 | 2021-05-06 | 328 | 2,789 | 8.50 | + DOGE DOT SOL |
| C2 | 2021-05-13 | 2022-03-08 | 283 | 2,778 | 9.82 | all 10 |
| C3 | 2022-03-15 | 2023-03-20 | 311 | 2,788 | 8.96 | all but BCH |
| VAL | 2023-03-25 | 2023-12-01 | (not counted; opened only at Phase 3 for HIGH-CONFIRM) | | | |

Note C3 (2022+) loses most Saturdays-as-response-days: FTMO rows carry `new_source=True` after the fixed Saturday gaps, so a
response day containing them is invalid for the 7 FTMO coins (DECISIONS D3).

A test cell uses a slice's responses only for signal days d with d >= from and d + 2 days <= to (the response ends inside the
slice). Signal INPUTS (Binance OHLCV) may use a 40-day lookback buffer before `from` so that the 6/9/10-day operators are
defined on the slice's first days; no response from outside the slice is ever used (DECISIONS D6).

```
slices:
- EXPLORE 2019-01-01 2020-05-28
- C1 2020-06-04 2021-05-06
- C2 2021-05-13 2022-03-08
- C3 2022-03-15 2023-03-20
- VAL 2023-03-25 2023-12-01
```
