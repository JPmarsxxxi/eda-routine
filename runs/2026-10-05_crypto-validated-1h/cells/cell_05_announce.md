### Cell 05 — EDA: H1 sub-claim C1-a on fold C3

**Sub-claim being tested:** C1-a on C3: top-third premium coins underperform bottom-third by >= 117.1 bp per 72h.

**Why it matters to the hypothesis:** H1's last admissible fold; completes its decay-first record (EXPLORE -> C1 -> C2 -> C3).

**Test(s) used:** as cell_01 / cell_03. Rule file: cells/cell_05_rule.md.

**Decision rule before running:** supported t <= -1.645 & spread <= -117.1 bp; inconclusive t <= -1.645 & spread >
-117.1 bp; refuted t > -1.645. Weights 4.78 / 1 / 0.801.

**Engine/library APIs used:** code/cell_h1.py (guarded loads; primary cut to the C3 window before returns).

**Decisions I need from you:** none.

Run: `.venv/bin/python code/cell_h1.py 5 C3 test`
