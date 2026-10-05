### Cell 12 — EDA: redirect for H2 on C3 ("where does the data point?")

**Sub-claim being tested:** none of H2's — five fixed looks (sign, 72h, extremes, change, BTC-only) on C3, already opened
by H2. Rule file: cells/cell_12_rule.md.

**Why it matters to the hypothesis:** RUNBOOK_v3 step 8; a qualifying look becomes a child born on C3.

**Test(s) used:** tercile / threshold sorts with Welch t.

**Decision rule before running:** spawn only for |t| >= 2.5 with a cost-clearing effect.

**Engine/library APIs used:** code/cell_ts_redirect.py 12 H2 C3 (guarded loads; primary cut to C3).

**Decisions I need from you:** none.
