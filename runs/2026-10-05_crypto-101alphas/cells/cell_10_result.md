branch: refuted
weight_applied: 0.886

# cell_10 result — H4 (A6) on C1

Deciding numbers: mean top-minus-bottom half spread = **-32.71 bp/day**, Newey-West(5) SE = 26.95 bp, t = -1.21,
n = 327 days (one-sided 95% upper bound +11.6 bp vs the 20 bp/day bar).
Rule (from cell_10_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **refuted**.
Weight from the rule file: supported 3.166 / refuted 0.886 / inconclusive 1 -> applied 0.886
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC -0.0079 (n 327 days,
t -0.42); realised spread SD 569.0 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2020.0 | -13.6 | 207.0 |
| 2021.0 | -65.7 | 120.0 |

Plot: plots/cell_10_H4_A6_C1.png
