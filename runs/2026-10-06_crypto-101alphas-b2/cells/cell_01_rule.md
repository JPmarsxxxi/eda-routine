hypothesis: H2
slice: C1
kind: test
version: neutral

# cell_01 — RULE (test, written before any code for this cell runs)

**Sub-claim.** On C1 (signal days 2020-06-09 .. 2021-05-13, response window inside the slice), Alpha#35 computed from Binance daily
OHLCV (D2, D4) has a mean daily cross-sectional Spearman IC with the next-day primary return of at least MIN_USEFUL_IC = 0.02
in the stated direction (claim version `neutral`, DECISIONS D7). H2's first test: the largest expected shift in pick_01.

**14c menu row + tool.** "X predicts forward Y" -> IC at the stated horizon (1 day): daily cross-sectional Spearman IC across
the coins present (>= 5), mean over days, Newey-West(5) SE (`code/common.py::daily_rank_ic`, `summarize`).

**Decision rule (fixed now, D7).** x = mean daily IC, se = its NW(5) SE.
- supported if x >= 0.02 AND x / se >= 1.645;
- refuted if x + 1.645 se < 0.02 (a useful effect in the stated direction is excluded);
- inconclusive otherwise, or if fewer than 150 valid days.
Cost does not enter the branch (RUNBOOK v3.2).

**Evidence weights (fixed now, D10; `tables/power.csv`, row A35 / C1).** Simulation's own result: daily IC sd
0.368 (measured EXPLORE day-permutation null 0.487, lag-1 autocorr -0.002,
scaled to 8 coins/day), 329 days, 3,000 runs: P(supported | IC 0.02) = power = 0.268,
P(supported | IC 0) = alpha = 0.052; P(refuted | 0.02) = 0.058, P(refuted | 0) = 0.264.
- weight(supported) = power / alpha = 5.181 (not capped) -> **5.181**
- weight(refuted) = P(ref|0.02) / P(ref|0) = 0.221 (not capped) -> **0.221**
- weight(inconclusive) = 1
Guard (a): no earlier cell tested this sub-claim on C1 for H2 (slice rule 2, checked by gate.py). Guard (b): applied above.

**Pre-registered descriptives (do not decide the branch):** `raw` version (own-return prediction incl. market, trailing
scaling); IC net of 1-day reversal (alpha ranks residualised on b_rev1 ranks each day) and b_rev1's own IC on this slice
(OBSERVATIONS #1); top-half minus bottom-half spread bp/day, daily half-membership turnover and the cost per day it implies
(D11); the signal's correlation with the same-day panel and BTC return (market share); IC by half of the slice.

**Step-1 pick arithmetic.**
```
pick_01: E|shift| = sum over supported/refuted of P(branch) x |posterior(branch) - current|, P(branch) = p x P(b|IC=0.02) + (1-p) x P(b|IC=0); weights capped [0.1, 10] (D10, tables/power.csv)
  H2 A35 next=C1      p=0.170 w_sup=5.18 w_ref=0.221 -> E|shift| 5.95 pp
  H3 A38 next=C1      p=0.170 w_sup=5.18 w_ref=0.221 -> E|shift| 5.95 pp
  H5 A54 next=C1      p=0.170 w_sup=5.13 w_ref=0.223 -> E|shift| 5.88 pp
  H1 A30 next=C1      p=0.170 w_sup=5.10 w_ref=0.224 -> E|shift| 5.84 pp
  H4 A53 next=C1      p=0.150 w_sup=5.18 w_ref=0.221 -> E|shift| 5.38 pp
  H5 A54 next=EXPLORE p=0.170 w_sup=4.76 w_ref=0.198 -> E|shift| 5.33 pp
  H3 A38 next=EXPLORE p=0.170 w_sup=4.77 w_ref=0.222 -> E|shift| 4.93 pp
  H4 A53 next=EXPLORE p=0.150 w_sup=5.06 w_ref=0.196 -> E|shift| 4.90 pp
  H1 A30 next=EXPLORE p=0.170 w_sup=3.56 w_ref=0.253 -> E|shift| 4.41 pp
  H2 A35 next=EXPLORE p=0.170 w_sup=4.21 w_ref=0.266 -> E|shift| 4.27 pp
PICK: H2 on C1 (largest expected shift 5.95 pp)
```
