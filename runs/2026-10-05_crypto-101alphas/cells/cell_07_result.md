branch: inconclusive
weight_applied: 1.0

# cell_07 result — H4 (A6) on EXPLORE

Deciding numbers: mean top-minus-bottom half spread = **+7.64 bp/day**, Newey-West(5) SE = 10.39 bp, t = +0.74,
n = 463 days (one-sided 95% upper bound +24.7 bp vs the 20 bp/day bar).
Rule (from cell_07_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **inconclusive**.
Weight from the rule file: supported 9.117 / refuted 0.569 / inconclusive 1 -> applied 1.0
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC +0.0185 (n 463 days,
t +0.81); realised spread SD 223.8 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2019.0 | 2.3 | 330.0 |
| 2020.0 | 21.0 | 133.0 |

Plot: plots/cell_07_H4_A6_EXPLORE.png
