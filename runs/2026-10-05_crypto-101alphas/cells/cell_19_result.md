branch: inconclusive
weight_applied: 1.0

# cell_19 result — H2 (A42) on C1

Deciding numbers: mean top-minus-bottom half spread = **+32.76 bp/day**, Newey-West(5) SE = 28.96 bp, t = +1.13,
n = 311 days (one-sided 95% upper bound +80.4 bp vs the 20 bp/day bar).
Rule (from cell_19_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **inconclusive**.
Weight from the rule file: supported 3.166 / refuted 0.886 / inconclusive 1 -> applied 1.0
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC -0.0519 (n 311 days,
t -2.28); realised spread SD 455.8 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2020.0 | -17.6 | 195.0 |
| 2021.0 | 117.4 | 116.0 |

Plot: plots/cell_19_H2_A42_C1.png
