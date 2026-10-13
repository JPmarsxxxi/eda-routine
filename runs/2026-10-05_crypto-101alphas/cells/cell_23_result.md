branch: inconclusive
weight_applied: 1.0

# cell_23 result — H3 (A2) on C1

Deciding numbers: mean top-minus-bottom half spread = **-5.03 bp/day**, Newey-West(5) SE = 28.17 bp, t = -0.18,
n = 327 days (one-sided 95% upper bound +41.3 bp vs the 20 bp/day bar).
Rule (from cell_23_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **inconclusive**.
Weight from the rule file: supported 3.166 / refuted 0.886 / inconclusive 1 -> applied 1.0
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC +0.0686 (n 327 days,
t +3.64); realised spread SD 580.4 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2020.0 | 17.3 | 207.0 |
| 2021.0 | -43.5 | 120.0 |

Plot: plots/cell_23_H3_A2_C1.png
