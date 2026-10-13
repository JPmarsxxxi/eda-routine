### Cell 04 — EDA: redirect for H1 on C2 ("where does the data point?")

**Sub-claim being tested:** none of H1's — the same five pre-listed looks as cell_02 (sign, 24h horizon, premium
dispersion, extremes, era) on C2, the fold H1 just opened. Rule file: cells/cell_04_rule.md.

**Why it matters to the hypothesis:** RUNBOOK_v3 step 8; a qualifying look becomes a new child born on C2.

**Test(s) used:** tercile / extreme sorts, t-tests on block spreads.

**Decision rule before running:** spawn only for |t| >= 2.5 with a cost-clearing effect; else "absent everywhere".

**Engine/library APIs used:** code/cell_h1_redirect.py 4 C2 (guarded loads, C2 window only).

**Decisions I need from you:** none.
