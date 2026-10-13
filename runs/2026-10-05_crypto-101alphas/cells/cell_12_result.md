branch: refuted
weight_applied: 0.524

# cell_12 result — H6 (A2RAWPOS) on C2

Deciding numbers: mean top-minus-bottom half spread = **-6.48 bp/day**, Newey-West(5) SE = 12.24 bp, t = -0.53,
n = 282 days (one-sided 95% upper bound +13.7 bp vs the 20 bp/day bar).
Rule (from cell_12_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **refuted**.
Weight from the rule file: supported 10.0 / refuted 0.524 / inconclusive 1 -> applied 0.524
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC -0.0509 (n 282 days,
t -2.42); realised spread SD 191.8 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2021.0 | 3.3 | 230.0 |
| 2022.0 | -49.9 | 52.0 |

Plot: plots/cell_12_H6_A2RAWPOS_C2.png
