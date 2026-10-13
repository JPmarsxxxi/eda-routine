### Cell 08 — EDA: redirect for H2 on C1 ("where does the data point?")

**Sub-claim being tested:** none of H2's — five fixed looks (sign, 72h, extremes, change, BTC-only) on C1, already opened
by H2. Rule file: cells/cell_08_rule.md.

**Why it matters to the hypothesis:** RUNBOOK_v3 step 8; a qualifying look becomes a child born on C1.

**Test(s) used:** tercile / threshold sorts with Welch t.

**Decision rule before running:** spawn only for |t| >= 2.5 with a cost-clearing effect.

**Engine/library APIs used:** code/cell_ts_redirect.py 8 H2 C1 (guarded loads; primary cut to C1).

**Decisions I need from you:** none.
