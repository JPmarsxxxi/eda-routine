# cell_03 RULE — H3 CONFIRM opening (written before any code for this cell exists)

**Hypothesis:** H3, perp basis level forecasts next-day realized vol beyond trailing RV (born EXPLORE #4). This is H3's ONE
CONFIRM opening.

**Pick arithmetic (Phase 2 step 1, `scripts/shift.py`, H1 removed as it has no eligible test):**
E|shift| H3 0.314 > H2 0.264 > H5 0.253 > H4 0.117 > H1 0.102 (H1's number assumes a test that does not exist here).
H3 has the largest expected shift -> picked.

**Sub-claim (14c floor Q5):** in CONFIRM, the partial Spearman correlation between the hourly basis (bp; mean of the two
30m-mark snapshots in hour t) and next-24h log realized vol of 30m spot returns over (t+1h, t+25h], controlling for
trailing 24h, 7d and 30d log RV, is positive.

**14c menu row + tool:** "Predictive relationship, controlled" -> rank-residual (partial) Spearman via `kit.resid_ranks`;
uncertainty from a moving-block bootstrap (`kit.block_boot_corr`, block = 240 h, 2,000 reps, n = observed rows).

**Smallest economically meaningful effect:** partial rho = 0.10 (a basis that explains 1% of residual rank variance in next-day
vol is the least that could change a vol forecast; below it, a forecast model gains nothing after estimation noise).

**Power (stated simulation, `scripts/power_all.py`, `tables/power_all.json` "H3"):** EXPLORE residual ranks, y circularly
rolled to break the real link, block-bootstrapped to CONFIRM length 10,632 h, alt centred at rho0 = 0.10: null SE = 0.0419,
critical value 1.645 x SE = **0.0689**, **power = 0.772**, empirical size 0.057. **alpha = 0.05 (one-sided).**

**Decision rule (three branches) and evidence weights:**
- **SUPPORTED** if CONFIRM partial rho > 0.0689. weight = power/alpha = 0.772/0.05 = 15.4 -> **capped to 10** (guard b).
- **REFUTED** if partial rho < 0.0689 AND partial rho < 0.05 (half the minimum effect). weight = (1-power)/(1-alpha) =
  0.228/0.95 = 0.240 (inside the cap; not capped).
- **INCONCLUSIVE** otherwise (0.05 <= rho < 0.0689). weight = 1.

**Guard (a):** first CONFIRM look at this sub-claim. EXPLORE partial (0.15, #4) is its birth and is not counted. H2 (dvol) uses a
different predictor, so it is not the same piece of evidence; the two rivals' overlap is dealt with in the reported rival check.

**Reported, NOT weighted (14c floor Q4/Q6/Q7/Q8/Q9):**
- Rival "basis is a proxy for implied vol": partial rho additionally controlling log dvol (CONFIRM has dvol throughout).
- Rival "volume/activity": partial rho additionally controlling log trailing-24h perp volume (metrics `v`).
- Rival "regime": the partial rho by calendar quarter of CONFIRM (decay-first shape) and the raw rho.
- Q9: no directional trade is implied (response is vol magnitude), so no round-trip cost is priced; stated N/A.
