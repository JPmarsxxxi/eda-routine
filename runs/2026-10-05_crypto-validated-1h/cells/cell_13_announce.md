### Cell 13 — EDA: H3 sub-claim C3-a on fold C1

**Sub-claim being tested:** C3-a on C1: top-tercile prior-session S&P 500 returns precede >= 89 bp higher next-day panel
returns than bottom-tercile ones.

**Why it matters to the hypothesis:** first clean fold for the risk-on spillover claim (EXPLORE t 2.18 in a 29-look screen).

**Test(s) used:** tercile sort + Welch t (code/cell_ts.py 13 H3 C1 test). Rule file: cells/cell_13_rule.md.

**Decision rule before running:** supported t >= 1.645 & spread >= 89.0; inconclusive t >= 1.645 & < 89.0; refuted t < 1.645.
Weights 4.54 / 1 / 0.814.

**Engine/library APIs used:** guarded loads of macro/yahoo_GSPC (lag one session) and primary (cut to C1).

**Decisions I need from you:** none.
