# cell_06 RULE — H5 CONFIRM opening (written before any code for this cell exists)

**Hypothesis:** H5, hourly spot return reversal (born EXPLORE #6). This is H5's ONE CONFIRM opening.

**Pick arithmetic (Phase 2 step 1, `scripts/shift.py`):** with H2 now HIGH-CONFIRM (waits for VAL) and H1/H3 without an
eligible test, OPEN candidates are H5 (p 0.20, power 0.946, alpha 0.05: E|shift| 0.253) and H4 (p 0.25, power 0.363: 0.117).
H5 has the larger expected shift -> picked.

**Sub-claim (14c floor Q5):** in CONFIRM, the Spearman correlation between the hourly spot log return r_t (close of hour t
over close of hour t-1, from the 30m spot file) and r_{t+1} is negative.

**14c menu row + tool:** "Serial dependence" -> Spearman rho of (r_t, r_{t+1}), consecutive-hour pairs only; block bootstrap
(block 240 h, 2,000 reps) for the SE.

**Smallest economically meaningful effect:** rho = -0.03 (a reversal that moves next-hour return by 3% of its rank spread
per unit rank; smaller is not usable after the 0.3 bp typical round-trip cost in the half-spread file).

**Power (stated simulation, `scripts/power_all.py`, `tables/power_all.json` "H5"):** EXPLORE residual ranks, y circularly
rolled to break the link, block-bootstrapped to CONFIRM length 10,632, alt centred at rho0 = -0.03: null SE 0.00927, critical
value -1.645 x SE = **-0.01526**, **power = 0.946**, empirical size 0.042. **alpha = 0.05 (one-sided).**

**Decision rule (three branches) and evidence weights:**
- **SUPPORTED** if CONFIRM rho < -0.01526. weight = power/alpha = 0.946/0.05 = 18.9 -> **capped to 10** (guard b).
- **REFUTED** if rho > -0.015 (half the minimum effect; it is above -0.01526 too). weight = (1-power)/(1-alpha) =
  0.054/0.95 = 0.0568 -> **capped to 0.1** (guard b).
- **INCONCLUSIVE** if -0.01526 <= rho <= -0.015 (a 0.00026-wide band; stated for completeness). weight = 1.

**Guard (a):** first CONFIRM look at this sub-claim (Phase 0 ACF and era table were the birth).

**Reported, NOT weighted (14c floor Q4/Q6/Q7/Q8/Q9):**
- Rival "a handful of crash hours": rho with the 1% largest |r_t| hours removed; and Pearson rho.
- Rival "bid-ask bounce": Roll-type bounce is sized at about -0.001 in Phase 0 (DATA_PROFILE); the CONFIRM rho is compared
  with it, not rescored.
- Q8 stability: rho by CONFIRM quarter (decay-first).
- Q9 economics: mean gross of -sign(r_t) x r_{t+1} in bp, and cost per event from the half-spread of the trade hour (hour t+1)
  where present (round trip = 2 x half_bp; coverage stated; missing never filled).
- Mechanism side bet (Q6): reversal is stronger after high-|r| hours. rho within the top |r_t| tercile vs the bottom tercile.
