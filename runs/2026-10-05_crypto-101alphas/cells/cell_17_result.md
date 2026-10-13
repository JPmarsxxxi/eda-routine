branch: refuted
weight_applied: 0.51

# cell_17 result — H6 (A2RAWPOS) on C3

Deciding numbers: mean top-minus-bottom half spread = **+3.69 bp/day**, Newey-West(5) SE = 9.69 bp, t = +0.38,
n = 310 days (one-sided 95% upper bound +19.6 bp vs the 20 bp/day bar).
Rule (from cell_17_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **refuted**.
Weight from the rule file: supported 10.0 / refuted 0.51 / inconclusive 1 -> applied 0.51
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC +0.0240 (n 310 days,
t +1.12); realised spread SD 177.4 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2022.0 | 0.2 | 244.0 |
| 2023.0 | 16.6 | 66.0 |

Plot: plots/cell_17_H6_A2RAWPOS_C3.png
