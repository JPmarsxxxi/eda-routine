branch: supported
weight_applied: 10.0

# cell_01 result — H1 (A101) on C1

Deciding numbers: mean top-minus-bottom half spread = **+56.83 bp/day**, Newey-West(5) SE = 32.71 bp, t = +1.74,
n = 327 days (one-sided 95% upper bound +110.6 bp vs the 20 bp/day bar).
Rule (from cell_01_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **supported**.
Weight from the rule file: supported 10.0 / refuted 0.541 / inconclusive 1 -> applied 10.0
(supported weight capped at 10x, guard b).
Secondary (descriptive, not a decision input): mean daily Spearman IC -0.0059 (n 327 days,
t -0.26); realised spread SD 581.0 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2020.0 | 20.5 | 207.0 |
| 2021.0 | 119.6 | 120.0 |

Plot: plots/cell_01_H1_A101_C1.png

## Notes added after the result (no number above changed)
- **The pre-registered weight is overstated (DECISIONS D14).** The rule's power simulation assumed an SE of ~12 bp (EXPLORE
  noise x1.5); the realised SE was 32.7 bp and a null random-split calibration on C1 gives 31.0 bp. At that noise the same
  rule has power ~0.16 and alpha ~0.05 (weight ~3.2, not 10). The 10.0 stands because it was pre-registered; REPORT.md
  flags H1's posterior as inflated by roughly 3x in odds.
- **Rank IC ~0 while the mean spread is +57 bp/day.** The positive mean is carried by a few extreme days (2021: +120 bp/day
  over 120 days vs 2020: +20 bp/day over 207 days), not by a consistent ordering. Rival "high-vol/alt-season tail" is alive.
- Spawn (step 7): no child; the tail-day reading is a rival for H1 itself, tested by its remaining slices.
