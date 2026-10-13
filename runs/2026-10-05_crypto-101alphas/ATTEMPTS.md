# ATTEMPTS — every slice opening (EXPLORE test, CONFIRM fold, VAL) and every redirect look; each counts toward K

| cell | hypothesis | slice | kind | statistic | result | branch | K (cumulative slice openings) |
|---|---|---|---|---|---|---|---:|
| 01 | H1 | C1 | test | A101 top-minus-bottom half spread | +56.8 bp/day, t +1.74, n 327 | supported | 1 |
| 02 | H1 | EXPLORE | test | A101 top-minus-bottom half spread | +8.2 bp/day, t +0.75, n 499 | inconclusive | 2 |
| 03 | H2 | EXPLORE | test | A42 top-minus-bottom half spread | -6.1 bp/day, t -0.47, n 419 | refuted | 3 |
| 04 | H2 | EXPLORE | redirect | 16 pointer sorts (see result) | none clears the bar | (redirect, weight 1) | 4 |
| 05 | H3 | EXPLORE | test | A2 top-minus-bottom half spread | -1.0 bp/day, t -0.10, n 470 | refuted | 5 |
| 06 | H3 | EXPLORE | redirect | 16 pointer sorts (see result) | best: P4 variant, flipped 29.5 bp/day t 3.06 | (redirect, weight 1) | 6 |
| 07 | H4 | EXPLORE | test | A6 top-minus-bottom half spread | +7.6 bp/day, t +0.74, n 463 | inconclusive | 7 |
| 08 | H1 | C2 | test | A101 top-minus-bottom half spread | +33.1 bp/day, t +3.07, n 282 | supported | 8 |
| 09 | H6 | C1 | test | A2RAWPOS top-minus-bottom half spread | -19.0 bp/day, t -0.67, n 327 | inconclusive | 9 |
| 10 | H4 | C1 | test | A6 top-minus-bottom half spread | -32.7 bp/day, t -1.21, n 327 | refuted | 10 |
| 11 | H4 | C1 | redirect | 16 pointer sorts (see result) | none clears the bar | (redirect, weight 1) | 11 |
| 12 | H6 | C2 | test | A2RAWPOS top-minus-bottom half spread | -6.5 bp/day, t -0.53, n 282 | refuted | 12 |
| 13 | H6 | C2 | redirect | 16 pointer sorts (see result) | none clears the bar | (redirect, weight 1) | 13 |
| 14 | H4 | C2 | test | A6 top-minus-bottom half spread | +6.8 bp/day, t +0.54, n 282 | inconclusive | 14 |
| 15 | H4 | C3 | test | A6 top-minus-bottom half spread | -10.5 bp/day, t -1.09, n 310 | refuted | 15 |
| 16 | H4 | C3 | redirect | 16 pointer sorts (see result) | none clears the bar | (redirect, weight 1) | 16 |
| 17 | H6 | C3 | test | A2RAWPOS top-minus-bottom half spread | +3.7 bp/day, t +0.38, n 310 | refuted | 17 |
| 18 | H6 | C3 | redirect | 16 pointer sorts (see result) | none clears the bar | (redirect, weight 1) | 18 |
| 19 | H2 | C1 | test | A42 top-minus-bottom half spread | +32.8 bp/day, t +1.13, n 311 | inconclusive | 19 |
| 20 | H2 | C2 | test | A42 top-minus-bottom half spread | -0.4 bp/day, t -0.03, n 259 | inconclusive | 20 |
| 21 | H2 | C3 | test | A42 top-minus-bottom half spread | -28.8 bp/day, t -2.25, n 292 | refuted | 21 |
| 22 | H2 | C3 | redirect | 16 pointer sorts (see result) | best: P2 flipped, h=2 35.6 bp/day t 2.99 | (redirect, weight 1) | 22 |
| 23 | H3 | C1 | test | A2 top-minus-bottom half spread | -5.0 bp/day, t -0.18, n 327 | inconclusive | 23 |
| 24 | H3 | C2 | test | A2 top-minus-bottom half spread | -1.8 bp/day, t -0.18, n 282 | refuted | 24 |
| 25 | H3 | C2 | redirect | 16 pointer sorts (see result) | none clears the bar | (redirect, weight 1) | 25 |
| 26 | H5 | C1 | test | A4 top-minus-bottom half spread | -4.7 bp/day, t -0.05, n 92 | inconclusive | 26 |
| 27 | H5 | C2 | test | A4 top-minus-bottom half spread | -2.3 bp/day, t -0.04, n 84 | inconclusive | 27 |
| 28 | H1 | VAL | val | A101 top-minus-bottom half spread | +4.7 bp/day, t +0.53, n 213 | refuted | 28 |

**K (for downstream DSR deflation).** Hypothesis slice openings: 19 test cells + 1 VAL = **20**; including the 8 redirect
cells (each ~15 pointer sorts on an already-opened or EXPLORE slice) as looks: **28 cells, ~140 sorts**. Not hypothesis tests,
but looks at returns that should be known to a deflation step: three NULL noise calibrations (random half splits, no alpha) on
C1 (after cell_01, D14), C2 (after cell_08, D15) and C3 (after cell_15, D17), and the Phase-0 EXPLORE profile.
Process deviation: cell_10 was not the top pick (DECISIONS D16).
