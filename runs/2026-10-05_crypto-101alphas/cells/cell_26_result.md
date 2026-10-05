branch: inconclusive
weight_applied: 1.0

# cell_26 result — H5 (A4) on C1

Deciding numbers: mean top-minus-bottom half spread = **-4.71 bp/day**, Newey-West(5) SE = 97.21 bp, t = -0.05,
n = 92 days (one-sided 95% upper bound +155.2 bp vs the 20 bp/day bar).
Rule (from cell_26_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **inconclusive**.
Weight from the rule file: supported 1.923 / refuted 0.951 / inconclusive 1 -> applied 1.0
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC -0.0142 (n 92 days,
t -0.40); realised spread SD 923.2 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2020.0 | -21.6 | 38.0 |
| 2021.0 | 7.2 | 54.0 |

Plot: plots/cell_26_H5_A4_C1.png
