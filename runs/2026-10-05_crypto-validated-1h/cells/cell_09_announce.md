### Cell 09 — EDA: H2 sub-claim C2-a on fold C2

**Sub-claim being tested:** C2-a on C2 (2022H1 bear market): greed-tercile days precede >= 84.3 bp higher panel returns
than fear-tercile days.

**Why it matters to the hypothesis:** second fold; a sentiment-momentum effect should survive a bear regime.

**Test(s) used:** tercile sort + Welch t (code/cell_ts.py 9 H2 C2 test). Rule file: cells/cell_09_rule.md.

**Decision rule before running:** supported t >= 1.645 & spread >= 84.3; inconclusive t >= 1.645 & < 84.3; refuted t < 1.645.
Weights 4.72 / 1 / 0.804.

**Engine/library APIs used:** guarded loads of attention/fear_greed and primary (cut to C2).

**Decisions I need from you:** none.
