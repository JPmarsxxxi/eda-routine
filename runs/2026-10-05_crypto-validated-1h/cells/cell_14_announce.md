### Cell 14 — EDA: redirect for H3 on C1 ("where does the data point?")

**Sub-claim being tested:** none of H3's — five fixed looks (sign, 72h, +-1% extremes, 5-session change, BTC-only) on C1, already opened
by H3. Rule file: cells/cell_14_rule.md.

**Why it matters to the hypothesis:** RUNBOOK_v3 step 8; a qualifying look becomes a child born on C1.

**Test(s) used:** tercile / threshold sorts with Welch t.

**Decision rule before running:** spawn only for |t| >= 2.5 with a cost-clearing effect.

**Engine/library APIs used:** code/cell_ts_redirect.py 14 H3 C1 (guarded loads; primary cut to C1).

**Decisions I need from you:** none.
