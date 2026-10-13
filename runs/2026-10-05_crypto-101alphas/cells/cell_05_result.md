branch: refuted
weight_applied: 0.569

# cell_05 result — H3 (A2) on EXPLORE

Deciding numbers: mean top-minus-bottom half spread = **-1.01 bp/day**, Newey-West(5) SE = 10.40 bp, t = -0.10,
n = 470 days (one-sided 95% upper bound +16.1 bp vs the 20 bp/day bar).
Rule (from cell_05_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **refuted**.
Weight from the rule file: supported 9.117 / refuted 0.569 / inconclusive 1 -> applied 0.569
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC -0.0080 (n 470 days,
t -0.38); realised spread SD 227.0 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2019.0 | -6.7 | 335.0 |
| 2020.0 | 13.0 | 135.0 |

Plot: plots/cell_05_H3_A2_EXPLORE.png
