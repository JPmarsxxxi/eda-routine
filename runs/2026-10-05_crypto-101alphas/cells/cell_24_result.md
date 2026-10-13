branch: refuted
weight_applied: 0.524

# cell_24 result — H3 (A2) on C2

Deciding numbers: mean top-minus-bottom half spread = **-1.82 bp/day**, Newey-West(5) SE = 9.94 bp, t = -0.18,
n = 282 days (one-sided 95% upper bound +14.5 bp vs the 20 bp/day bar).
Rule (from cell_24_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **refuted**.
Weight from the rule file: supported 10.0 / refuted 0.524 / inconclusive 1 -> applied 0.524
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC +0.0064 (n 282 days,
t +0.37); realised spread SD 197.2 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2021.0 | 4.2 | 230.0 |
| 2022.0 | -28.3 | 52.0 |

Plot: plots/cell_24_H3_A2_C2.png
