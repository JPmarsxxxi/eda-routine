branch: inconclusive
weight_applied: 1.0

# cell_14 result — H4 (A6) on C2

Deciding numbers: mean top-minus-bottom half spread = **+6.83 bp/day**, Newey-West(5) SE = 12.59 bp, t = +0.54,
n = 282 days (one-sided 95% upper bound +27.5 bp vs the 20 bp/day bar).
Rule (from cell_14_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **inconclusive**.
Weight from the rule file: supported 10.0 / refuted 0.524 / inconclusive 1 -> applied 1.0
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC +0.0355 (n 282 days,
t +1.71); realised spread SD 212.3 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2021.0 | 4.9 | 230.0 |
| 2022.0 | 15.2 | 52.0 |

Plot: plots/cell_14_H4_A6_C2.png
