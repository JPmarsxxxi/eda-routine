branch: refuted
weight_applied: 0.51

# cell_21 result — H2 (A42) on C3

Deciding numbers: mean top-minus-bottom half spread = **-28.77 bp/day**, Newey-West(5) SE = 12.76 bp, t = -2.25,
n = 292 days (one-sided 95% upper bound -7.8 bp vs the 20 bp/day bar).
Rule (from cell_21_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **refuted**.
Weight from the rule file: supported 10.0 / refuted 0.51 / inconclusive 1 -> applied 0.51
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC -0.1108 (n 292 days,
t -5.17); realised spread SD 201.2 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2022.0 | -24.0 | 227.0 |
| 2023.0 | -45.3 | 65.0 |

Plot: plots/cell_21_H2_A42_C3.png
