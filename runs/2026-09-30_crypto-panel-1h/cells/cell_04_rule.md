# cell_04 — RULE (written before any code for this cell exists)

**Hypothesis:** H4: high-volume relative winners keep winning the next day. Born on EXPLORE #12 -> this is H4's ONE CONFIRM
opening (first test of H4).

## Step-1 pick arithmetic (code/pick.py; OPEN and testable: H1 0.39, H2 0.35, H4 0.21. H3 OPEN 0.795 but its CONFIRM is spent
and no admissible slice remains -> expected shift 0; H5 HIGH-CONFIRM; H6 HIGH-EXPLORE)
- H4: prior 0.21, power 0.94, alpha 0.05 -> w_sup 10 (capped from 18.8), w_ref 0.1 (capped from 0.063) -> E|shift| **26.3 pp**
- H1 24.1 pp · H2 8.0 pp · H3 0 pp -> **H4 picked.**

## Sub-claim
C1(H4): on CONFIRM, in a daily cross-sectional regression of the next-day relative return (coin daily log return minus the
10-coin mean) on z(today's relative return), z(today's volume shock) and their product, the product coefficient b3 is positive.
Volume shock = log(today's daily vol / median daily vol of the 30 previous days) (known at the day's end, when the regression's
right-hand side is formed). Days need all 24 hours per coin and >= 8 coins.

## 14c menu row + tool
"X predicts forward Y" (cross-sectional) -> daily Fama-MacBeth with an interaction term, NW(2) SE over days.
`code/tests.py::fm_interaction(REL.shift(-1), REL, shock, min_n=8)`.

## Decision rule
- **supported** if z(b3) > +1.645 with >= 400 days.
- **refuted** if z(b3) <= +1.645 with >= 400 days (and no sign conflict).
- **inconclusive** if < 400 days, or sign conflict: z > 1.645 but the same regression on normal-scored (cross-sectional rank)
  regressors gives z < -1.645.

## Evidence weights
Power simulation (`code/power.py H4`, 300 sims): 620 days x 10 coins, relative returns t(3) with sd 349 bp (EXPLORE daily
relative sd), volume shock correlated with |rel| (0.4 loading, OBS #11), true b3 = 28 bp.
**Simulation's own result: "H4 size: 0.04", "H4 power (b3=28bp): 0.94".**
Smallest economically meaningful effect: a long/short pair at +1/-1 sd earns 2 x b3; it pays two round trips (2 x 19.8 bp)
plus two rollovers (2 x 8.2 bp) = 56 bp -> b3 >= 28 bp. alpha = max(0.05, 0.04) = 0.05, power 0.94.
- weight(supported) = 0.94/0.05 = 18.8 -> **capped 10** · weight(refuted) = 0.06/0.95 = 0.063 -> **capped 0.1** · inconclusive 1.
Guard (a): Phase 0 #12 was an EXPLORE tercile look (different slice) -> n/a.

## Descriptive (does not decide)
b3 in bp; b1 (relative-return slope, i.e. plain cross-sectional reversal/momentum) and b2; by CONFIRM half; the EXPLORE-style
tercile table (winners/losers x shock tercile) on CONFIRM.
