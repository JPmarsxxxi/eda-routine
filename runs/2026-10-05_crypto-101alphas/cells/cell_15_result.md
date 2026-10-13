branch: refuted
weight_applied: 0.888

# cell_15 result — H4 (A6) on C3

Deciding numbers: mean top-minus-bottom half spread = **-10.49 bp/day**, Newey-West(5) SE = 9.65 bp, t = -1.09,
n = 310 days (one-sided 95% upper bound +5.4 bp vs the 20 bp/day bar).
Rule (from cell_15_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **refuted**.
Weight from the rule file: supported 3.153 / refuted 0.888 / inconclusive 1 -> applied 0.888
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC +0.0003 (n 310 days,
t +0.01); realised spread SD 171.2 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2022.0 | -19.8 | 244.0 |
| 2023.0 | 24.1 | 66.0 |

Plot: plots/cell_15_H4_A6_C3.png
