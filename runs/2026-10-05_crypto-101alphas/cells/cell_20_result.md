branch: inconclusive
weight_applied: 1.0

# cell_20 result — H2 (A42) on C2

Deciding numbers: mean top-minus-bottom half spread = **-0.43 bp/day**, Newey-West(5) SE = 15.68 bp, t = -0.03,
n = 259 days (one-sided 95% upper bound +25.4 bp vs the 20 bp/day bar).
Rule (from cell_20_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **inconclusive**.
Weight from the rule file: supported 10.0 / refuted 0.524 / inconclusive 1 -> applied 1.0
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC -0.0729 (n 259 days,
t -3.43); realised spread SD 260.6 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2021.0 | -2.6 | 208.0 |
| 2022.0 | 8.5 | 51.0 |

Plot: plots/cell_20_H2_A42_C2.png

## Note added after the result (no number above changed)
- Spawn (step 7) considered: the descriptive rank IC is strongly NEGATIVE on C2 (-0.073, t -3.43) while the half spread is ~0.
  A child "-#42 (flipped)" would have its statistic already displayed on EXPLORE (cell_03), C1 (cell_19) and C2 (here), leaving
  only C3 — one fold can never make HIGH-CONFIRM, and the IC/spread disagreement points at the price-level rank inside #42
  (D2) rather than a mechanism. Not spawned; logged as a lead in REPORT.md.
