# cell_07 RULE — H6 CONFIRM opening (written before any code for this cell exists)

**Hypothesis:** H6, hourly basis change vs next-hour spot return beyond r_t (child of H5, born EXPLORE #10). This is H6's ONE CONFIRM opening.

**Pick arithmetic (Phase 2 step 1, `scripts/shift.py`):** OPEN candidates: H6 (p 0.15, power 0.903, alpha 0.05: E|shift| 0.196) and
H4 (p 0.25, power 0.363: 0.117). H1/H3 have no eligible slice; H2 is HIGH-CONFIRM (waits for VAL); H5 is spent. H6 is picked.

**Sub-claim (14c floor Q5):** in CONFIRM, the partial Spearman correlation between d_basis_t (hourly basis level minus the previous
hour's, in bp; knowable at the close of hour t) and the next-hour spot log return r_{t+1}, controlling for r_t, is negative.

**14c menu row + tool:** "Lead-lag / partial association" -> rank-residualise x and y on the control (`kit.resid_ranks`), Spearman of the residuals,
moving-block bootstrap (block 240 h) for the SE.

**Smallest economically meaningful effect:** partial rho = -0.03 (same scale as H5).

**Power (stated simulation, `scripts/power_h6.py`, `tables/power_h6.json`):** EXPLORE residual ranks, y circularly rolled to break the link,
block-bootstrapped to CONFIRM length 10,632, alt centred at rho0 = -0.03: null SE 0.01022, critical value -1.645 x SE =
**-0.01680**, **power = 0.903**, empirical size 0.047. **alpha = 0.05 (one-sided).**

**Decision rule (three branches) and evidence weights:**
- **SUPPORTED** if CONFIRM partial rho < -0.0168. weight = 0.903/0.05 = 18.1 -> **capped to 10** (guard b).
- **REFUTED** if partial rho > -0.015 (half the minimum effect). weight = 0.097/0.95 = 0.102 (inside the [0.1,10] cap; used as 0.102).
- **INCONCLUSIVE** if -0.0168 <= rho <= -0.015 (a 0.0018-wide band, stated for completeness). weight = 1.

**Guard (a):** first CONFIRM look at this sub-claim. Its birth (Phase 0 lead-lag screen #10) was on EXPLORE. This is not double-counting H5's CONFIRM
evidence: the control r_t removes H5's own signal from x and y, so the partial is a different statistic; it uses the same CONFIRM hours as H5
but a different question. Noted for the judge.

**Reported, NOT weighted (14c floor Q4/Q6/Q7/Q8/Q9):**
- Rival "H5 impostor" (basis contains -r_t mechanically): also control r_{t-1}; and the unpartialled Spearman.
- Rival "a handful of large moves": 1% largest |d_basis| hours removed.
- Q8 stability: partial rho by CONFIRM quarter (decay-first).
- Q9 economics: mean gross of -sign(d_basis) x r_{t+1} in bp and cost per event from the trade-hour half-spread where present
  (round trip = 2 x half_bp, coverage stated, missing never filled).
