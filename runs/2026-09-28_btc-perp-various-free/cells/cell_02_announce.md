### Cell 02 — EDA: redirect after H1's refutation (where does the EXPLORE jump live?)

**Sub-claim being tested:** none is being weighted. Descriptive decomposition of EXPLORE D by funding state, sign of funding
vs default, and calendar quarter, to name where the data points after H1's CONFIRM refutation.

**Why it matters to the hypothesis:** RUNBOOK_v3 Phase 2 step 8 makes this redirect cell mandatory after a refutation; its
finding becomes a new child hypothesis (H6) or a recorded null redirect.

**Test(s) used:** per-settlement D (same definition as cell_01), NW(3) t on `D ~ 1 + 1[HI]`, group means, quarter shares.

**Decision rule before running:** see `cells/cell_02_rule.md` (B1..B4). Weights: none (birth data).

**Engine/library APIs used:** `eda_guard.load` via `scripts/kit.hourly`, `statsmodels` OLS HAC.

**Slice:** EXPLORE (2020-09-01 .. 2021-12-31). CONFIRM and VAL not touched.

**Decisions I need from you:** none (unattended).
