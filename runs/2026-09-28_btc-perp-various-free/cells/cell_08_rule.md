# cell_08 RULE — H4 CONFIRM opening (written before any code for this cell exists)

**Hypothesis:** H4, high implied vol precedes positive next-24h spot return (born EXPLORE #8). This is H4's ONE CONFIRM opening.

**Pick arithmetic (Phase 2 step 1, `scripts/shift.py`):** H4 is the only OPEN hypothesis with an eligible slice (H6 spent, H5 spent, H1/H3 no
slice, H2 HIGH-CONFIRM waiting for VAL). H4: p 0.25, power 0.363, alpha 0.05: E|shift| 0.117 (> 3pp, so S2 does not apply). Picked.

**Sub-claim (14c floor Q5):** in CONFIRM, the Spearman correlation between the DVOL level at hour t and the next-24h spot log return
(t+1h, t+25h], hourly rows, is positive.

**14c menu row + tool:** "Level vs forward return (overlapping windows)" -> Spearman rho; block bootstrap (block 240 h, 2,000 reps) for the SE, which
handles the 24h overlap.

**Smallest economically meaningful effect:** rho = 0.05.

**Power (stated simulation, `scripts/power_all.py`, `tables/power_all.json` "H4"):** EXPLORE ranks, y circularly rolled, block-bootstrapped to
10,632, alt centred at rho0 = 0.05: null SE 0.04068, critical value 1.645 x SE = **+0.0669**, **power = 0.363**, empirical size 0.048. **alpha = 0.05 (one-sided).**
The power is low; the rule below says what a miss means.

**Decision rule (three branches) and evidence weights:**
- **SUPPORTED** if CONFIRM rho > +0.0669. weight = 0.363/0.05 = 7.26 (inside the cap, used as 7.26).
- **REFUTED** if rho < +0.025 (half the minimum effect). weight = 0.637/0.95 = 0.671.
- **INCONCLUSIVE** if 0.025 <= rho <= 0.0669. weight = 1 (no belief shift; the test cannot separate the two).

**Guard (a):** first CONFIRM look at this sub-claim (Phase 0 lead-lag screen was the birth, on EXPLORE).

**Reported, NOT weighted (14c floor Q4/Q6/Q7/Q8/Q9):**
- Rival "short-term reversal after crashes": Spearman partialled on the trailing 24h spot return.
- Rival "era trend": rho by CONFIRM quarter (decay-first); pooled rho with the best quarter removed.
- Q9 economics: N/A as a rule (it is a level relation, not a signal); the mean next-24h return in the top vs bottom DVOL tercile in bp is reported without a cost line.
