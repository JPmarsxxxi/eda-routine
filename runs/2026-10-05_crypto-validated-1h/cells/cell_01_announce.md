### Cell 01 — EDA: H1 sub-claim C1-a on fold C1

**Sub-claim being tested:** C1-a: "On C1, top-third perp-premium coins earn a lower 72h primary return than bottom-third
coins, by at least the cost of trading it (121.8 bp per 72h)."

**Why it matters to the hypothesis:** H1 says crowded perp longs underperform; if the sort does not separate on a fold
that never fed its birth, the EXPLORE spread was a sample artefact.

**Test(s) used:** tercile sort of 72h forward primary log returns by daily-mean perp premium, non-overlapping 3-day grid,
t-test on block spreads; Spearman IC as a descriptive. Rule file: cells/cell_01_rule.md.

**Decision rule before running:** supported if t <= -1.645 and spread <= -121.8 bp; inconclusive if t <= -1.645 and
spread > -121.8 bp; refuted if t > -1.645. Weights 6.14 / 1 / 0.729.

**Engine/library APIs used:** pandas, numpy, scipy.stats.spearmanr; code/cell_h1.py -> code/hyp.py:h1_blocks (loads
via code/guard.py: primary/validated_* cut to the C1 window before any return is computed; perp/perp_premium_*).

**Decisions I need from you:** none open (unattended; defaults in DECISIONS.md D5-D7).

Run: `.venv/bin/python code/cell_h1.py 1 C1 test`
