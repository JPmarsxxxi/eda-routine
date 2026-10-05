# cell_03 — RULE (written before any code for this cell exists)

**Hypothesis:** H3 (NO-STORY lead): same-hour-yesterday reversal of 1h returns. Born on EXPLORE #5 -> this is H3's ONE
CONFIRM opening. H3 carries a real `forbids` line (not `none - NO-STORY`), so a CONFIRM test is allowed (RUNBOOK Phase 1).
**Contamination disclosure:** cell_01 (H5) reported, as a pre-registered descriptive, the 6h-block lag-24h IC on CONFIRM
(-0.054, z -3.0). That is a different statistic (6h sums, not 1h returns) but it overlaps this sub-claim; this opening is
therefore not a fully blind look. The weight below is NOT reduced for it by formula; the REPORT flags it.

## Step-1 pick arithmetic (code/pick.py; OPEN: H1 0.39, H2 0.35, H3 0.28, H4 0.21; H5 HIGH-CONFIRM, H6 HIGH-EXPLORE)
- H3: prior 0.28, power 1.000, alpha 0.08 -> w_sup 10 (capped from 12.5), w_ref 0.1 (capped from 0.0) -> E|shift| **33.5 pp**
- H4 26.3 pp · H1 24.1 pp · H2 8.0 pp -> **H3 picked.**

## Sub-claim
C1(H3): on CONFIRM, a coin's 1h return r(t) is negatively related to its 1h return 24 hours later r(t+24h), AND this lag is
more negative than the neighbouring lags 23 h and 25 h (the lead claims something lag-24-specific).

## 14c menu row + tool
"X predicts forward Y" / ACF at a stated lag: pooled normal-score IC at lag 24 (per-coin normal scores over CONFIRM), products
averaged within the UTC day of r(t), NW(2) SE over days. Same statistic at lags 23 and 25 for the second condition.
`code/tests.py::lag_ic(r1h, 24, cluster=day)`.

## Decision rule
- **supported** if z(lag 24) < -1.645 AND IC(24) < min(IC(23), IC(25)), with >= 400 day clusters.
- **refuted** if either condition fails (>= 400 day clusters, no sign conflict).
- **inconclusive** if < 400 day clusters, or sign conflict (normal-score z < -1.645 but Pearson z > +1.645).

## Evidence weights
Power simulation (`code/power.py H3`, 150 sims): 620 days x 24 h, 10 coins, common factor, t(3), persistent vol, r(t) +=
rho x r(t-24) with rho = -0.05. **Simulation's own result: "H3 size: 0.08", "H3 power (rho=-0.05): 1.0".**
Smallest economically meaningful effect: EXPLORE median 1h sd 131 bp; the cheapest coin's round trip is 6.6 bp (BTC/BNB) ->
|rho| >= 6.6/131 = 0.05 (for every other coin it is uneconomic at any size seen). alpha = max(0.05, simulated size 0.08) = 0.08.
The lag-23/25 condition is not in the simulation; under H it holds almost surely (neighbours ~0), under the null it only makes
false support rarer, so using alpha 0.08 is conservative.
- weight(supported) = 1.0/0.08 = 12.5 -> **capped 10** · weight(refuted) = 0/0.92 = 0 -> **capped 0.1** · inconclusive 1.
Guard (a): no earlier cell tested THIS sub-claim (1h lag-24) on CONFIRM; cell_01's 6h lag-4 figure was descriptive and is a
different statistic -> not merged, disclosed above.

## Descriptive (does not decide)
IC at lags 1, 2, 12, 23, 24, 25, 48 on CONFIRM; per-coin lag-24 IC; by CONFIRM half; lag-24 IC by UTC hour of r(t).
