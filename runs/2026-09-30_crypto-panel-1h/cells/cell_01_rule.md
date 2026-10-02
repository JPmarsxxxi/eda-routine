# cell_01 — RULE (written before any code for this cell exists)

**Hypothesis:** H5 (Intraday 6-hour reversal). Born on EXPLORE #6 -> this is H5's ONE CONFIRM opening (first test of H5).
**Slice:** CONFIRM (2021-07-08 .. 2023-03-19), 10 coins, spot/binance_<COIN>, loaded through the guard.

## Step-1 pick arithmetic (code/pick.py; all five hypotheses OPEN, none tested yet)
E|shift| = P(sup) x |post_sup - prior| + P(ref) x |post_ref - prior|, with P(sup) = prior x power + (1 - prior) x alpha:
- H5: prior 0.39, power 0.990, alpha 0.063 -> w_sup 10 (capped from 15.6), w_ref 0.1 (capped from 0.0107) -> E|shift| **39.1 pp**
- H3: 33.5 pp · H4: 26.3 pp · H1: 24.1 pp · H2: 8.0 pp
-> **H5 has the largest expected shift; picked.** (Cost is the same order for all: one CONFIRM pass.)

## Sub-claim
C1(H5): on CONFIRM, a coin's 6h block return (blocks 00-06, 06-12, 12-18, 18-24 UTC; sum of six 1h log returns, block valid
only if all 6 hours exist) is negatively related to the same coin's next 6h block return.

## 14c menu row + tool
"X predicts forward Y" -> IC at a stated horizon: pooled normal-score IC between consecutive 6h blocks (per-coin normal scores
over CONFIRM, robust to OBS #1 tails), products averaged within each UTC day of the conditioning block (day clusters), mean
over days, Newey-West (2 lags) SE. `code/tests.py::lag_ic(X, 1, cluster=day)`.

## Decision rule (three branches, numbers fixed now)
- **supported** if z < -1.645 (one-sided 5%) with >= 400 day clusters.
- **refuted** if z >= -1.645 with >= 400 day clusters and no sign conflict.
- **inconclusive** if < 400 day clusters, OR sign conflict: normal-score IC significantly negative (z < -1.645) while the raw
  Pearson version (same clustering) is positive with z > +1.645.

## Evidence weights (fixed now)
Power simulation (`code/power.py H5`, 300 sims): 10-coin panel, common factor (pairwise corr ~0.62), t(3) shocks, persistent
common volatility, 2,480 blocks (620 days x 4), AR coefficient phi = -0.065 between consecutive blocks.
**Simulation's own result: "H5 size: 0.0633", "H5 power (phi=-0.065): 0.99".**
Smallest economically meaningful effect: EXPLORE median 6h sd = 306 bp; a 1-sd block must predict a move >= the panel median
round trip 19.8 bp -> |phi| >= 19.8/306 = 0.065 (intraday; a block that crosses the daily rollover would also pay ~8.2 bp,
ignored here, which makes the threshold if anything too lenient).
alpha = max(nominal 0.05, simulated size 0.0633) = 0.0633; power = 0.99.
- weight(supported) = 0.99 / 0.0633 = 15.6 -> **capped to 10** (guard b)
- weight(refuted) = 0.01 / 0.9367 = 0.0107 -> **capped to 0.1** (guard b)
- weight(inconclusive) = 1
Guard (a): no earlier cell tested this sub-claim on CONFIRM (Phase 0 VR(6) was EXPLORE) -> not applicable.

## Descriptive only (pre-registered, do NOT decide the branch)
Decay shape: the same IC at block lags 1, 2, 3, 4 (6-24 h); per-coin IC; IC by CONFIRM half (2021-07..2022-05 / 2022-05..2023-03);
gross next-block move in bp for the bottom vs top decile of the current block (pooled), set against the panel median round trip
19.8 bp (cost line).
