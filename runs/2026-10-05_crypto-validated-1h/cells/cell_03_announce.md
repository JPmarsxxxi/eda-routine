### Cell 03 — EDA: H1 sub-claim C1-a on fold C2

**Sub-claim being tested:** C1-a on C2: top-third premium coins underperform bottom-third by >= 117.1 bp per 72h.

**Why it matters to the hypothesis:** second independent fold; if refuted again H1 drifts toward LOW.

**Test(s) used:** as cell_01 (tercile sort, block t-test, IC descriptive). Rule file: cells/cell_03_rule.md.

**Decision rule before running:** supported t <= -1.645 & spread <= -117.1 bp; inconclusive t <= -1.645 & spread >
-117.1 bp; refuted t > -1.645. Weights 3.98 / 1 / 0.843.

**Engine/library APIs used:** code/cell_h1.py (guarded loads; primary cut to the C2 window before returns).

**Decisions I need from you:** none (FTMO Saturday windows dropped per DECISIONS D5).

Run: `.venv/bin/python code/cell_h1.py 3 C2 test`
