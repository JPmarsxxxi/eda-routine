# cell_04 — RESULT (H4 C1 on CONFIRM; rule: cells/cell_04_rule.md)

**Branch fired: REFUTED.** Deciding number: Fama-MacBeth interaction b3 = **-14.5 bp per 1sd x 1sd, NW se 6.2 bp, z = -2.32**
(<= +1.645; the sign is the OPPOSITE of the hypothesis), 594 days (>= 400). Rank-regressor version z -0.83 (no sign conflict:
the conflict branch needs the rank version significantly negative while the primary is significantly positive).
**Weight applied: 0.1 (capped from 0.063, guard b).** H4 posterior: odds 0.21/0.79 = 0.266 x 0.1 = 0.0266 -> **0.026** (< 0.05)
-> state **LOW**, closed for this session. H4 is a sub-claim H4 cannot survive without -> mandatory redirect cell next (cell_05).

Descriptive (pre-registered): b1 (plain relative-return slope) +12.5 bp (t 1.6: mild cross-sectional continuation, not
reversal), b2 (shock) +1.2 bp (t 0.2); b3 -16.5 / -12.6 bp in the two CONFIRM halves. The tercile table on CONFIRM, the EXPLORE
style of OBS #12, reads the other way: high-shock winners +12.1 / losers -5.7 bp, low-shock +0.2 / -3.6 bp -> high-minus-low
W-L +14 bp. So the tercile sort and the regression interaction disagree in sign on the same data — the "interaction" is
fragile to how it is measured (and the rank version is ~0). Note: the intercept b0 = +7.8 bp is not a bug: with an interaction
regressor of non-zero mean, b0 = mean(y) - b3 x mean(z_a z_b), and mean(y) is exactly 0 (checked in a debug load logged as
`cell_04_debug` in ACCESS_LOG.md; same CONFIRM data, same cell, no new statistic).
Table `tables/cell_04_h4.csv`, `cell_04_h4_primary.csv`; plot `plots/cell_04_h4_fm.png`.

**Spawn (step 7):** deferred to the mandatory redirect cell (cell_05), which decides where the data points.
