### Cell 07 — EDA: H2 sub-claim C2-a on fold C1

**Sub-claim being tested:** C2-a on C1: top-tercile Fear & Greed days precede a panel return >= 89 bp above bottom-tercile days.

**Why it matters to the hypothesis:** first clean fold for the sentiment-momentum claim; EXPLORE was bull-heavy.

**Test(s) used:** tercile sort + Welch t; Spearman IC descriptive. Rule file: cells/cell_07_rule.md.

**Decision rule before running:** supported t >= 1.645 & spread >= 89.0 bp; inconclusive t >= 1.645 & spread < 89.0;
refuted t < 1.645. Weights 5.57 / 1 / 0.759.

**Engine/library APIs used:** code/cell_ts.py 7 H2 C1 test (guarded loads: attention/fear_greed, primary cut to C1).

**Decisions I need from you:** none.
