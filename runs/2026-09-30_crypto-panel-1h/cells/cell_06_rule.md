# cell_06 — RULE (written before any code for this cell exists)

**Hypothesis:** H1: daily time-series reversal of coin returns. Born on EXPLORE #9 -> this is H1's ONE CONFIRM opening.
Disclosure: cell_01 (H5) and cell_03 (H3) have looked at CONFIRM intraday returns (6h blocks; 1h lags incl. 23-25 h), which
overlap in data but not in statistic (neither computed a UTC-day to next-UTC-day relation).

## Step-1 pick arithmetic (code/pick.py; OPEN and testable: H1 0.39, H2 0.35; H3 OPEN 0.795 with no admissible slice -> 0)
- H1: prior 0.39, power 0.5625, alpha 0.05 -> w_sup 10 (capped from 11.25), w_ref 0.4605 -> E|shift| **24.1 pp**
- H2: 8.0 pp · H3: 0 pp -> **H1 picked.**

## Sub-claim
C1(H1): on CONFIRM, a coin's UTC-day log return (all 24 hours present) is negatively related to its next UTC-day log return.

## 14c menu row + tool
"X predicts forward Y" at horizon 1 day: pooled normal-score IC (per-coin normal scores over CONFIRM), products averaged across
coins within each day, NW(2) SE over days. `code/tests.py::lag_ic(Rdaily, 1)`.

## Decision rule
- **supported** if z < -1.645 with >= 400 days.
- **refuted** if z >= -1.645 with >= 400 days, no sign conflict.
- **inconclusive** if < 400 days, or sign conflict (normal-score z < -1.645 while Pearson z > +1.645).

## Evidence weights
Power simulation (`code/power.py H1`, 400 sims): 620 days x 10 coins, common factor (corr ~0.62), t(3), persistent vol,
AR(1) phi = -0.045 on daily returns. **Simulation's own result: "H1 size (phi=0): 0.05", "H1 power (phi=-0.045): 0.5625".**
Smallest economically meaningful effect: EXPLORE median daily sd 649 bp; a 1-sd day must predict >= the 19.8 bp median round
trip + one rollover 8.2 bp = 28 bp -> |phi| >= 28/649 = 0.043 -> -0.045. alpha 0.05, power 0.5625.
- weight(supported) = 0.5625/0.05 = 11.25 -> **capped 10** · weight(refuted) = 0.4375/0.95 = **0.4605** (not capped) ·
  inconclusive 1.
Guard (a): no earlier cell tested this sub-claim on CONFIRM -> n/a.

## Descriptive (does not decide)
IC at day lags 1, 2, 3, 7; per coin; by CONFIRM half; IC on the 10% largest |day| moves vs the rest (rival: outlier impostor);
IC by weekday of day d (rival: weekday composition); gross next-day move after bottom / top decile days vs the 28 bp cost line.
