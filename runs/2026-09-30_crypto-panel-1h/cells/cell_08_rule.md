# cell_08 — RULE (written before any code for this cell exists)

**Hypothesis:** H2: daily reversal is stronger after panel-wide volume-shock days. Born on EXPLORE #13 -> this is H2's ONE
CONFIRM opening. Contamination disclosure: cell_06 (H1) printed, on CONFIRM, the day->next-day IC for the 10% largest |r| days
(-0.227) vs the rest; big-move days overlap with volume-shock days (OBS #11: volume ~ |r| at 0.4-0.5). This statistic (split by
PANEL VOLUME SHOCK tercile, not by |r|) has not been computed on CONFIRM, but it is not a blind look.

## Step-1 pick arithmetic (code/pick.py)
- H2: prior 0.35, power 0.225, alpha 0.05 -> w_sup 4.5, w_ref 0.816 -> E|shift| **8.0 pp**
- H1 (0.227), H3 (0.795), H7 (0.42): no admissible test (H1/H3: CONFIRM spent and EXPLORE produced them; H7: DECISIONS D11)
  -> 0 pp. -> **H2 picked** (the only OPEN hypothesis with an admissible test).

## Sub-claim
C1(H2): on CONFIRM, the normal-score day->next-day IC (per coin, daily returns) is more negative on days whose panel volume shock
(mean over live coins of log(daily vol / median daily vol of the prior 30 days); known at the day's end) is in the top tercile
(cut over CONFIRM days) than on the other days.

## 14c menu row + tool
"Distribution differs between groups": difference of per-day IC means (high-shock days minus others), Welch t.
`code/tests.py::diff_ic(R, 1, high)`.

## Decision rule
- **supported** if z < -1.645 and both groups >= 150 days.
- **refuted** if z >= -1.645 (both groups >= 150 days), no sign conflict.
- **inconclusive** if a group < 150 days, or sign conflict (normal-score z < -1.645 but Pearson-version z > +1.645).

## Evidence weights
Power simulation (`code/power.py H2`, 400 sims): 620 days x 10 coins, common factor, t(3), persistent vol, base AR -0.03 and an
extra -0.045 on "high" days (top tercile of a latent correlated with |f|).
**Simulation's own result: "H2 size: 0.0375", "H2 power (dphi=-0.045): 0.225".**
Smallest economically meaningful effect: the extra reversal must itself reach H1's economic threshold (|phi| 0.045, 28 bp per
1-sd day). alpha = max(0.05, 0.0375) = 0.05; power 0.225.
- weight(supported) = 0.225/0.05 = **4.5** (not capped) · weight(refuted) = 0.775/0.95 = **0.816** · inconclusive 1.
Guard (a): cell_06 tested H1's unconditional IC, a different sub-claim; its |r| split was descriptive -> not merged.

## Descriptive (does not decide)
IC per volume-shock tercile; by CONFIRM half; the same split with |r|-matched days (IC on high-shock days excluding the top-10%
|r| coin-days) to separate volume from move size.
