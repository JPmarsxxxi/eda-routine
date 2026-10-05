# cell_09 RULE — mandatory REDIRECT cell after H4's refutation (written before any code for this cell exists)

**Trigger (Phase 2 step 8):** cell_08 REFUTED H4's core sub-claim on CONFIRM (pooled Spearman +0.0194 < the +0.025 bar). Redirect question:
"where does the data actually point?": opposite sign, one era only, a different horizon or transform, or absent everywhere.

**Slice: EXPLORE only** (H4's birth slice; birth data, not evidence). CONFIRM is not re-opened. **Disclosure:** cell_08 already printed
CONFIRM quarter numbers for the raw level (0.21, 0.09, 0.18, 0.06, -0.02, all positive while the pooled rho is 0.019). That pattern is what
motivates the "relative level" piece below. Any child spawned from it is therefore NOT a clean blind test on CONFIRM; the child rule
must say so and its only CONFIRM opening is weighted as usual but reported with this caveat. It is not spawned unless EXPLORE itself shows the effect.

**Pieces (Spearman with the forward spot log return over the stated horizon, EXPLORE rows only, moving-block bootstrap SE, block 240 h, 1,000 reps):**
- E: raw DVOL level vs next-24h return, by EXPLORE calendar quarter (2021Q2..2021Q4 complete; DVOL starts 2021-03), and pooled ex-best quarter.
- T: RELATIVE DVOL = dvol(t) - trailing 30-day (720 h) median of hourly dvol (min 500 h), vs next-24h return.
- Hz: raw DVOL level vs next-72h and next-168h spot return (windows (t+1h, t+73h], (t+1h, t+169h]).

**14c menu row + tool:** "Predictive relationship" -> Spearman with `kit.block_boot_corr` SE.

**Decision rule (every branch that holds fires; all reported):**
- **B1 one era only:** best-quarter raw rho >= 0.15 AND pooled raw rho of the other quarters < 0.0669. -> recorded as a lead (an era-conditional claim
  cannot get a fresh CONFIRM slice); nothing spawned.
- **B2 different transform or horizon:** T or Hz has rho >= 0.08 AND >= 2 bootstrap SE on EXPLORE. -> spawn child H7 with that variable (the larger if several),
  own rule file, own first CONFIRM opening later, with the disclosure above.
- **B3 opposite sign:** T or Hz has rho <= -0.08 AND >= 2 SE (negative). -> spawn child H7 with the negative sign, own rule, own first CONFIRM opening.
- **B4 absent / diffuse:** none of the above. -> nothing spawned; H4's redirect closes as "no localised effect".

**Evidence weights:** none applied (birth data, weight 1 for every branch).
