branch: refuted
weight_applied: 0.569

# cell_03 result — H2 (A42) on EXPLORE

Deciding numbers: mean top-minus-bottom half spread = **-6.15 bp/day**, Newey-West(5) SE = 13.20 bp, t = -0.47,
n = 419 days (one-sided 95% upper bound +15.6 bp vs the 20 bp/day bar).
Rule (from cell_03_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **refuted**.
Weight from the rule file: supported 9.117 / refuted 0.569 / inconclusive 1 -> applied 0.569
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC -0.0556 (n 419 days,
t -2.33); realised spread SD 260.5 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2019.0 | -11.1 | 300.0 |
| 2020.0 | 6.3 | 119.0 |

Plot: plots/cell_03_H2_A42_EXPLORE.png
