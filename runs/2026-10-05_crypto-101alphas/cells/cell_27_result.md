branch: inconclusive
weight_applied: 1.0

# cell_27 result — H5 (A4) on C2

Deciding numbers: mean top-minus-bottom half spread = **-2.33 bp/day**, Newey-West(5) SE = 60.89 bp, t = -0.04,
n = 84 days (one-sided 95% upper bound +97.8 bp vs the 20 bp/day bar).
Rule (from cell_27_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **inconclusive**.
Weight from the rule file: supported 4.85 / refuted 0.797 / inconclusive 1 -> applied 1.0
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC -0.0023 (n 84 days,
t -0.04); realised spread SD 551.0 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2021.0 | -24.9 | 76.0 |
| 2022.0 | 212.4 | 8.0 |

Plot: plots/cell_27_H5_A4_C2.png
