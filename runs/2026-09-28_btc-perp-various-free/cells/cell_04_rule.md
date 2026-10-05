# cell_04 RULE — mandatory REDIRECT cell after H3's refutation (written before any code for this cell exists)

**Trigger (Phase 2 step 8):** cell_03 refuted H3's core sub-claim on CONFIRM (partial rho 0.0099 vs the 0.0689 bar). Redirect
question: "where does the data actually point?": one era only, a different transform of the basis, or absent everywhere.

**Slice: EXPLORE only** (2020-09-01 .. 2021-12-31 minus the last 25 h). H3's birth slice; birth data, not evidence. CONFIRM is
not re-opened here. A child hypothesis spawned by this cell gets its OWN first CONFIRM opening later (CONFIRM has been looked
at for the basis LEVEL only, in cell_03; a transform of the basis is a different sub-claim, guard a does not merge them).

**Pieces (all partial Spearman with next-24h log RV, controls trailing 24h/7d/30d log RV, exactly as in cell_03/H3):**
- L: basis LEVEL, split by calendar quarter (2020Q4..2021Q4, 5 quarters; 2020Q3 has < 31 days of controls) and the pooled
  partial over EXPLORE excluding the single best quarter.
- C: basis 24-hour CHANGE, basis(t) - basis(t-24h) (both known at t+1h).
- X: basis EXTREMITY, |basis(t) - trailing-30-day median of hourly basis| (trailing, min 500 h).
Uncertainty: moving-block bootstrap SE (block 240 h, 1,000 reps) for C and X.

**14c menu row + tool:** "Predictive relationship, controlled" -> same `kit.resid_ranks` / `kit.block_boot_corr`.

**Decision rule (every branch that holds fires; all reported):**
- **B1 one era only:** best-quarter level partial >= 0.25 AND pooled level partial of the other four quarters < 0.0689.
  -> spawn an era-specific child (H6): "the basis level forecasts RV only in bull-trend regimes". Untestable on CONFIRM (it is the
  quarter structure of 2022 that refuted it); recorded as a lead unless a fresh slice exists.
- **B2 different transform:** partial rho of C or X >= 0.10 AND >= 2 block-bootstrap SE, on EXPLORE. -> spawn child H7 with
  that transform (the larger if both), own rule file, own first CONFIRM opening later. NO-STORY unless a mechanism holds.
- **B3 absent / diffuse:** neither. -> nothing spawned; H3's redirect closes as "no localised effect".

**Evidence weights:** none applied (birth data, weight 1 for every branch).
