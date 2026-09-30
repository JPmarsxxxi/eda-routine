# cell_03 — RESULT (H3 C1 on CONFIRM; rule: cells/cell_03_rule.md)

**Branch fired: SUPPORTED.** Deciding numbers: lag-24 normal-score IC = **-0.0348, NW se 0.0079, z = -4.38** (< -1.645), 619
day clusters; IC(24) -0.0348 < min(IC(23) -0.0105, IC(25) -0.0245) -> the lag-24-specific condition holds (narrowly vs lag 25).
Pearson -0.0367 (z -3.01): no conflict.
**Weight applied: 10 (capped from 12.5, guard b).** H3 posterior: odds 0.28/0.72 = 0.389 x 10 = 3.89 -> **0.795** -> stays
**OPEN** (5-85%). Its one CONFIRM opening is now spent, EXPLORE produced it, and VAL is only for HIGH-CONFIRM, so H3 has no
further admissible test this session (expected shift of any next pick on H3 = 0).

Stated beside it: size -0.035 is below the 0.05 economic threshold even for the cheapest coin (BTC -0.020); a 1-sd hour
predicts ~4-5 bp vs a 6.6-36.5 bp round trip -> a data-nature lead, not a trade. All 10 coins negative (BTC -0.020 .. DOGE
-0.052), both CONFIRM halves (-0.039 / -0.029). Neighbouring lags 25 (-0.025, z -3.4) and 1-2 (-0.033, -0.024) are also
negative: the effect is a smeared "about one day later" reversal, not a sharp lag-24 spike. By UTC hour of r(t) (descriptive,
no SE): most negative at 07, 14, 16, 19 UTC (-0.08 .. -0.11). Contamination (cell_01's 6h lag-24h descriptive) disclosed in the
rule file. Table `tables/cell_03_h3.csv`, `cell_03_h3_byhour.csv`; plot `plots/cell_03_h3_lag24.png`.

**Spawn (step 7).** No child. The smeared lag 23-25 reversal points to the same "reversal about a day later" family as H1,
which has its own pending CONFIRM test; entering a child here would duplicate H1's claim at another grain. Logged as a lead.
