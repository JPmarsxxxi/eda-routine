branch: inconclusive
weight_applied: 1.0

# cell_02 result — H1 (A101) on EXPLORE

Deciding numbers: mean top-minus-bottom half spread = **+8.19 bp/day**, Newey-West(5) SE = 10.90 bp, t = +0.75,
n = 499 days (one-sided 95% upper bound +26.1 bp vs the 20 bp/day bar).
Rule (from cell_02_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **inconclusive**.
Weight from the rule file: supported 9.117 / refuted 0.569 / inconclusive 1 -> applied 1.0
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC -0.0129 (n 499 days,
t -0.52); realised spread SD 227.0 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2019.0 | 7.1 | 357.0 |
| 2020.0 | 10.9 | 142.0 |

Plot: plots/cell_02_H1_A101_EXPLORE.png
