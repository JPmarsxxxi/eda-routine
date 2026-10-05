# cell_02 — RULE (written before any code for this cell exists)

**Hypothesis:** H6 (child of H5): 6h reversal is stronger when trailing volatility is high. Born on CONFIRM (cell_01) ->
tested on **EXPLORE** (2017-08-17 .. 2021-06-30), the slice it was not born on (DECISIONS D10). First and only test of H6 on
EXPLORE. Disclosure: Phase 0 on EXPLORE already showed 1h ACF(1) by era (OBS #14; -0.067 in 2017-18 vs -0.02 in 2019/2021H1),
which is related but is not this statistic (6h blocks, split by trailing vol, not by calendar era).

## Step-1 pick arithmetic (code/pick.py; OPEN: H1 0.39, H2 0.35, H3 0.28, H4 0.21, H6 0.40; H5 is HIGH-CONFIRM, queued for VAL)
- H6: prior 0.40, power 0.985, alpha 0.05 -> w_sup 10 (capped from 19.7), w_ref 0.1 (capped from 0.016) -> E|shift| **39.3 pp**
- H3 33.5 pp · H4 26.3 pp · H1 24.1 pp · H2 8.0 pp -> **H6 picked.**

## Sub-claim
C1(H6): the normal-score IC between consecutive 6h block returns is more negative on days whose trailing 7-day realized
volatility of the equal-weight panel (sum of squared EW 1h returns over the 168 h before 00:00 UTC of that day; known at the
day start) is in its top tercile (tercile cut over EXPLORE days) than on the other days.

## 14c menu row + tool
"Distribution differs between groups" x "X predicts forward Y": difference of day-clustered IC between high-vol and other days,
Welch t over day clusters. `code/tests.py::diff_ic_clustered(B, 1, high, day)`.

## Decision rule
- **supported** if difference z < -1.645 and both groups have >= 300 days.
- **refuted** if z >= -1.645 (both groups >= 300 days) and no sign conflict.
- **inconclusive** if a group has < 300 days, OR the Pearson version of the difference is positive with z > +1.645 while the
  normal-score version is negative with z < -1.645.

## Evidence weights
Power simulation (`code/power.py H6`, 200 sims): 1,400 days x 4 blocks, 6 coins (EXPLORE averages ~6 live coins), common
factor, t(3), persistent vol; an extra AR coefficient dphi = -0.065 on blocks following a top-tercile trailing-vol state.
**Simulation's own result: "H6 size (dphi=0): 0.05", "H6 power (dphi=-0.065): 0.985".**
Smallest economically meaningful effect: the extra reversal must itself be the economic threshold of H5, |dphi| = 19.8/306 =
0.065. alpha = 0.05, power = 0.985.
- weight(supported) = 0.985/0.05 = 19.7 -> **capped 10** · weight(refuted) = 0.015/0.95 = 0.0158 -> **capped 0.1** ·
  weight(inconclusive) = 1.
Guard (a): no earlier cell tested this sub-claim on EXPLORE -> n/a.

## Descriptive (does not decide)
IC in each trailing-vol tercile; IC by EXPLORE era (2017H2-18, 2019, 2020, 2021H1).
