branch: supported
weight_applied: 3.311

# cell_08 result — H1 (A101) on C2

Deciding numbers: mean top-minus-bottom half spread = **+33.12 bp/day**, Newey-West(5) SE = 10.80 bp, t = +3.07,
n = 282 days (one-sided 95% upper bound +50.9 bp vs the 20 bp/day bar).
Rule (from cell_08_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **supported**.
Weight from the rule file: supported 3.311 / refuted 0.881 / inconclusive 1 -> applied 3.311
(no cap needed; within 10x).
Secondary (descriptive, not a decision input): mean daily Spearman IC +0.0492 (n 282 days,
t +2.33); realised spread SD 212.5 bp/day.
By calendar year inside the slice (mean bp/day, days):
| index | mean | count |
|---|---|---|
| 2021.0 | 37.9 | 230.0 |
| 2022.0 | 12.1 | 52.0 |

Plot: plots/cell_08_H1_A101_C2.png

## Notes added after the result (no number above changed)
- Realised SE 10.8 bp vs the 30.4 bp the D14 rule assumed for C2: C2's cross-section was far less noisy than C1's, so this
  cell's power was UNDER-stated and its weight 3.311 is conservative (honest power at SE 10.8 would be ~0.6 -> weight ~10).
- With cell_08, H1 reaches posterior 0.863 with two supported folds and none refuted -> state HIGH-CONFIRM, which is not
  pickable (RUNBOOK_v3 step 1): H1 goes to VAL in Phase 3 and does NOT open C3. Caveat carried to REPORT.md: the 0.863 rests
  on cell_01's overstated weight (D14); with cell_01 at its honest ~3.2 the posterior would be ~0.67 (OPEN) and C3 would
  have been H1's next test. C3 matters most for H1 because it is the first fold where the response (FTMO mid) is not the
  same print as the Binance signal inputs (Obs 3).
- 2022 days inside C2: +12.1 bp/day (52 days) vs 2021 +37.9 — a possible decay into 2022, noted, not tested here.
- Spawn: none.
