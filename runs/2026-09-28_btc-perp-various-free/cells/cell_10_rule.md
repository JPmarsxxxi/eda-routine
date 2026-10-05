# cell_10 RULE — Phase 3 VAL check, hypothesis H2 (written before VAL is opened)

**Hypothesis:** H2, DVOL adds next-day realized-vol information beyond trailing RV. State HIGH-CONFIRM (cell_05 SUPPORTED, posterior 0.938).
This is the one VAL opening of the session (only H2 is HIGH-CONFIRM). It is not proof of out-of-sample behaviour.

**VAL slice:** 2023-03-25 .. 2023-11-30 (embargo 03-20..24 untouched). Rows whose 24h forward window would cross 2023-11-30 23:59 are dropped.
Trailing controls (24h / 7d / 30d RV) need pre-VAL hours; they are read from the 31 days before 2023-03-25 as trailing inputs only, exactly as the CONFIRM cell did.
No VAL outcome is used except the rows from 2023-03-25 on.

**VAL_NOTE (TARGET.md), quoted beside the number:** "Same VAL weaknesses as every other BTC target here: soft-clean (arc #047 crossed it twice, both
pre-registered) and a different liquidity regime from TRAIN post-2023-04."

**Sub-claim:** partial Spearman(dvol_t, next-24h log RV | trailing 24h/7d/30d log RV) is positive in VAL.

**Power (stated simulation, `scripts/power_val_h2.py`, `tables/power_val_h2.json`):** EXPLORE residual ranks, y circularly rolled, block-bootstrapped to VAL length
5,990, alt centred at rho0 = 0.10: null SE 0.0737, critical value **+0.1213**, **power = 0.414**, empirical size 0.036. alpha = 0.05 (one-sided).
The VAL test is much weaker than the CONFIRM test (fewer hours), so a miss is weak evidence.

**Decision rule and weights (applied once):**
- **PASS** if VAL partial rho > +0.1213. weight = 0.414/0.05 = 8.28. Odds 0.938/0.062 = 15.1 x 8.28 (cap not hit) -> state **HIGH-VAL**.
- **FAIL** if partial rho < +0.05 (half the minimum effect). weight = 0.586/0.95 = 0.617. Odds 15.1 x 0.617 = 9.3 -> posterior 0.903; state stays HIGH-CONFIRM (reported as a VAL failure, not hidden).
- **INCONCLUSIVE** if between: weight 1, state stays HIGH-CONFIRM.

**Guard (a):** first and only VAL look. Guard (b): weights inside [0.1, 10].

**Reported, NOT weighted:** by-quarter-style split of VAL (Q2 2023 hours vs Q3/Q4 2023 hours) and the signed-return / EWMA controls, as in cell_05.
Cost: N/A (no direction).
