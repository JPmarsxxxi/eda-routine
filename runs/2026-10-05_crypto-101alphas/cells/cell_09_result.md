branch: inconclusive
weight_applied: 1.0

# cell_09 result — H6 (A2RAWPOS) on C1

Deciding numbers: mean top-minus-bottom half spread = **-19.00 bp/day**, Newey-West(5) SE = 28.52 bp, t = -0.67,
n = 327 days (one-sided 95% upper bound +27.9 bp vs the 20 bp/day bar).
Rule (from cell_09_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **inconclusive**.
Weight from the rule file: supported 3.166 / refuted 0.886 / inconclusive 1 -> applied 1.0
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC -0.0038 (n 327 days,
t -0.20); realised spread SD 570.2 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2020.0 | -8.5 | 207.0 |
| 2021.0 | -37.1 | 120.0 |

Plot: plots/cell_09_H6_A2RAWPOS_C1.png
