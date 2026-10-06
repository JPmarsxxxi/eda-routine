hypothesis: H1
slice: EXPLORE
kind: test
version: neutral

# cell_20 — RULE (test, written before any code for this cell runs)

**Sub-claim.** On EXPLORE (signal days 2019-01-01 .. 2020-06-02, response window inside the slice), Alpha#30 computed from Binance daily
OHLCV (D2, D4) has a mean daily cross-sectional Spearman IC with the next-day primary return of at least MIN_USEFUL_IC = 0.02
in the stated direction (claim version `neutral`, DECISIONS D7). Picked by pick_20 (largest expected shift).

**14c menu row + tool.** "X predicts forward Y" -> IC at the stated horizon (1 day): daily cross-sectional Spearman IC across
the coins present (>= 5), mean over days, Newey-West(5) SE (`code/common.py::daily_rank_ic`, `summarize`).

**Decision rule (fixed now, D7).** x = mean daily IC, se = its NW(5) SE.
- supported if x >= 0.02 AND x / se >= 1.645;
- refuted if x + 1.645 se < 0.02 (a useful effect in the stated direction is excluded);
- inconclusive otherwise, or if fewer than 150 valid days.
Cost does not enter the branch (RUNBOOK v3.2).

**Evidence weights (fixed now, D10; `tables/power.csv`, row A30 / EXPLORE).** Simulation's own result: daily IC sd
0.493 (measured EXPLORE day-permutation null 0.493, lag-1 autocorr -0.001,
scaled to 5 coins/day), 429 days, 3,000 runs: P(supported | IC 0.02) = power = 0.210,
P(supported | IC 0) = alpha = 0.059; P(refuted | 0.02) = 0.055, P(refuted | 0) = 0.216.
- weight(supported) = power / alpha = 3.559 (not capped) -> **3.559**
- weight(refuted) = P(ref|0.02) / P(ref|0) = 0.253 (not capped) -> **0.253**
- weight(inconclusive) = 1
Guard (a): no earlier cell tested this sub-claim on EXPLORE for H1 (slice rule 2, checked by gate.py). Guard (b): applied above.

**Pre-registered descriptives (do not decide the branch):** `raw` version (own-return prediction incl. market, trailing
scaling); IC net of 1-day reversal (alpha ranks residualised on b_rev1 ranks each day) and b_rev1's own IC on this slice
(OBSERVATIONS #1); top-half minus bottom-half spread bp/day, daily half-membership turnover and the cost per day it implies
(D11); the signal's correlation with the same-day panel and BTC return (market share); IC by half of the slice.

**Step-1 pick arithmetic.**
```
pick_20: E|shift| = sum over supported/refuted of P(branch) x |posterior(branch) - current|, P(branch) = p x P(b|IC=0.02) + (1-p) x P(b|IC=0); weights capped [0.1, 10] (D10, tables/power.csv)
  H1 A30 next=EXPLORE p=0.850 w_sup=3.56 w_ref=0.253 -> E|shift| 3.99 pp
PICK: H1 on EXPLORE (largest expected shift 3.99 pp)
```
