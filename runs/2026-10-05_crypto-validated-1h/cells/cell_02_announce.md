### Cell 02 — EDA: redirect for H1 on C1 ("where does the data point?")

**Sub-claim being tested:** none of H1's — five pre-listed looks (sign, 24h horizon, premium dispersion, extremes, era)
on C1, the fold H1 already opened. Rule file: cells/cell_02_rule.md.

**Why it matters to the hypothesis:** RUNBOOK_v3 step 8 makes a redirect mandatory after a refutation; a qualifying look
becomes a new child hypothesis (never a rewrite of H1).

**Test(s) used:** tercile / extreme sorts, t-tests on block spreads.

**Decision rule before running:** spawn only for |t| >= 2.5 with a cost-clearing effect; else "absent everywhere".

**Engine/library APIs used:** pandas, numpy, scipy; code/cell_02_redirect.py (guarded loads, C1 window only).

**Decisions I need from you:** none.

Run: `.venv/bin/python code/cell_02_redirect.py`
