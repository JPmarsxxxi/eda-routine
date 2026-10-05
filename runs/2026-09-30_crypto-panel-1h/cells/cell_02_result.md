# cell_02 — RESULT (H6 C1 on EXPLORE; rule: cells/cell_02_rule.md)

**Branch fired: SUPPORTED.** Deciding number: IC(high trailing-vol days) - IC(other days) = **-0.081, se 0.033, z = -2.48**
(< -1.645); 466 high days / 947 other days (both >= 300). Pearson version -0.087 (z -1.68): same sign, no conflict.
**Weight applied: 10 (capped from 19.7, guard b).** H6 posterior: odds 0.40/0.60 = 0.667 x 10 = 6.67 -> **0.870** (> 0.85)
-> state **HIGH-EXPLORE**. Per DECISIONS D10 it gets no CONFIRM opening (CONFIRM produced it) and is not eligible for VAL; it
awaits a fresh slice (user's call).

Descriptive (pre-registered): IC by trailing-vol tercile low +0.026 (z 1.3), mid -0.050 (z -2.6), high -0.063 (z -3.2) —
monotone. By era: 2017H2-18 -0.048, 2019 -0.053, 2020 -0.074, 2021H1 -0.009; all-EXPLORE -0.046 (z -3.9).
Size vs cost: even the high tercile (-0.063) sits at, not above, the 0.065 economic threshold of H5.
Table `tables/cell_02_h6.csv`; plot `plots/cell_02_h6_vol_conditional.png`.

**Spawn (step 7).** The low-vol tercile's positive IC (+0.026, z 1.3) hints at calm-market continuation. Not significant; logged
as a lead in REPORT.md, no child entered (a z of 1.3 on the slice that would have to produce it is curve-reading).
