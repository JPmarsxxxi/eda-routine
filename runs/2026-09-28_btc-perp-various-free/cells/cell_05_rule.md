# cell_05 RULE — H2 CONFIRM opening (written before any code for this cell exists)

**Hypothesis:** H2, DVOL adds next-day realized-vol information beyond trailing RV (born EXPLORE #2). This is H2's ONE CONFIRM opening.

**Pick arithmetic (Phase 2 step 1, `scripts/shift.py`):** E|shift| H2 0.264 > H5 0.253 > H4 0.117 (H1 and H3 have no eligible
test: birth slice and CONFIRM both spent). H2 has the largest expected shift -> picked.

**Sub-claim (14c floor Q5):** in CONFIRM, the partial Spearman correlation between `dvol` (Deribit DVOL close of hour t) and
next-24h log realized vol of 30m spot returns over (t+1h, t+25h], controlling for trailing 24h, 7d and 30d log RV, is positive.

**14c menu row + tool:** "Predictive relationship, controlled" -> `kit.resid_ranks` partial Spearman; block bootstrap
(`kit.block_boot_corr`, block 240 h, 2,000 reps) for the SE.

**Smallest economically meaningful effect:** partial rho = 0.10 (same argument as cell_03: below it a vol forecast gains
nothing after estimation noise).

**Power (stated simulation, `scripts/power_all.py`, `tables/power_all.json` "H2"):** EXPLORE (2021-04..12, n = 6,369) residual
ranks, y circularly rolled to break the link, block-bootstrapped to CONFIRM length 10,632, alt centred at rho0 = 0.10: null SE
0.0528, critical value 1.645 x SE = **0.0869**, **power = 0.609**, empirical size 0.046. **alpha = 0.05 (one-sided).**
(Power is modest because the only EXPLORE sample is 9 months; stated, not hidden.)

**Decision rule (three branches) and evidence weights:**
- **SUPPORTED** if CONFIRM partial rho > 0.0869. weight = power/alpha = 0.609/0.05 = 12.2 -> **capped to 10** (guard b).
- **REFUTED** if partial rho < 0.0869 AND partial rho < 0.05. weight = (1-power)/(1-alpha) = 0.391/0.95 = **0.412** (not capped).
- **INCONCLUSIVE** otherwise (0.05 <= rho < 0.0869). weight = 1.

**Guard (a):** first CONFIRM look at this sub-claim. cell_03 used the basis, a different predictor; the `+dvol` control in
cell_03 was a rival check on H3, not a test of this sub-claim, and is not counted here.

**Reported, NOT weighted:**
- Rival "leverage effect": partial rho additionally controlling the trailing 24h signed log return.
- Rival "HAR impostor: DVOL is a smoothed past RV": partial rho with an EWMA of hourly squared returns (half-life 72 h) added
  to the three RV controls.
- Rival "era/level": partial rho by CONFIRM quarter (decay-first).
- Q9: not a return predictor; no cost, stated N/A.
