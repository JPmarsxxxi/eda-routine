# cell_01 — RESULT (H5 C1 on CONFIRM; rule: cells/cell_01_rule.md)

**Branch fired: SUPPORTED.** Deciding number: pooled normal-score IC between consecutive 6h blocks = **-0.0316, NW se 0.0167,
z = -1.89** (< -1.645), 620 day clusters (>= 400). Pearson IC -0.0136 (z -0.74): same sign, no conflict.
**Weight applied: 10 (capped from 15.6, guard b).** H5 posterior: odds 0.39/0.61 = 0.639 x 10 = 6.39 -> **0.865** (> 0.85)
-> state **HIGH-CONFIRM** -> queued for the Phase 3 VAL check.

Not softened, but stated beside it because the rule is about sign and significance, not size:
- The measured IC (-0.032) is **half the smallest economically meaningful effect (-0.065)** the power simulation used. Implied
  gross move for a 1-sd block on CONFIRM: 0.032 x 232 bp = **7.3 bp vs the 19.8 bp median round trip** (cost line: does not
  clear costs). Pooled decile check: next block after the bottom decile -1.1 bp, after the top decile -11.5 bp (only the
  up-move side reverses at all).
- It is concentrated in the second half of CONFIRM: 2021-07..2022-05 IC +0.004 (z 0.19); 2022-05..2023-03 IC -0.074 (z -3.17).
- Per coin all 10 are negative (-0.019 BTC .. -0.061 DOGE), individually significant only for DOGE and BCH.
- Decay shape (descriptive): lag 6h -0.032 (z -1.9), 12h -0.024 (z -1.5), 18h +0.024 (z +1.4), **24h -0.054 (z -3.0)** — the
  same-block-yesterday lag is the strongest, echoing OBS #5 (lag-24 in 1h returns). This descriptive lag-24 number was seen
  on CONFIRM before H3's own CONFIRM opening; that contamination is disclosed in H3's rule file.

Table `tables/cell_01_h5.csv`, `tables/cell_01_h5_primary.csv`; plot `plots/cell_01_h5_6h_reversal.png`.

**Spawn (step 7).** The result suggests the reversal is a stressed-market phenomenon (only the post-LUNA half carries it) ->
child **H6** (parent H5): 6h reversal is stronger when trailing volatility is high (Nagel 2012 "evaporating liquidity"
mechanism). Born on CONFIRM (this cell), so its test must be on a slice it was not born on: EXPLORE.
