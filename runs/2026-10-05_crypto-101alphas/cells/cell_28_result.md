branch: refuted
weight_applied: 0.914

# cell_28 result — VAL pass for H1 (Alpha#101)

> **VAL_NOTE (TARGET.md):** VAL is weak evidence. (1) BTC VAL was crossed twice by earlier work and overlaps a spent pooled row of an earlier BTC seasonality EDA. (2) VAL has since been opened ONCE more, on all 10 coins, for a pre-registered test of the crash-day rebound topic (see ALREADY TESTED): SOFT-clean for every coin for that topic. (3) VAL may be a DIFFERENT REGIME from TRAIN (2023 was calm; from 2023-04 BTC's 1-minute trade counts fell ~8x, cause not established).

Deciding numbers: mean top-minus-bottom half spread = **+4.70 bp/day**, NW(5) SE 8.79 bp, t = +0.53, n = 213 days
(one-sided 95% upper bound +19.2 bp vs the 20 bp/day bar). -> **refuted**, weight 0.914 (rule file: supported
2.653 / refuted 0.914 / inconclusive 1).
Descriptive: mean daily Spearman IC -0.0296 (t -1.13, n 213); realised SE 8.8 vs assumed 38.0.
This VAL number is weak evidence (VAL_NOTE) and is not out-of-sample proof.

Plot: plots/cell_28_H1_A101_VAL.png

## Note added after the result (no number above changed)
The rule assumed SE 38.0 bp (largest measured fold noise, conservative); VAL realised 8.8 bp. So the refuted weight 0.914 is
far too gentle: at the realised noise this rule's power is ~0.55 and the refuted weight ~0.47, which would put H1 at ~0.75
(OPEN) even before correcting cell_01 (D14); with both corrections H1 would sit near ~0.48. H1 stays HIGH-CONFIRM only by the
pre-registered arithmetic; REPORT.md states the VAL failure.
