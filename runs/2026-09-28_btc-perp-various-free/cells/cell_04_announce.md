### Cell 04 — EDA: redirect after H3's refutation (where does the EXPLORE basis-vs-vol link live?)

**Sub-claim being tested:** none weighted. Descriptive decomposition of the EXPLORE basis level by calendar quarter, plus two
alternative transforms of the basis (24h change; extremity vs 30d median) against the same response and controls.

**Why it matters to the hypothesis:** RUNBOOK_v3 Phase 2 step 8 makes this redirect mandatory after a refutation; its
finding becomes a child hypothesis or a recorded null redirect.

**Test(s) used:** partial Spearman by rank-residualisation per quarter and per transform; block bootstrap SE.

**Decision rule before running:** `cells/cell_04_rule.md` (B1, B2, B3). Weights: none (birth data).

**Engine/library APIs used:** `eda_guard.load` via `scripts/kit.hourly`, `statsmodels` OLS, numpy bootstrap.

**Slice:** EXPLORE only. CONFIRM and VAL not touched.

**Decisions I need from you:** none (unattended).
