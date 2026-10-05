# cell_10 RESULT — H2 VAL check (VAL opened once)

Script `scripts/cell_10_h2_val.py`; tables `tables/10_result.json`; plot `plots/10_h2_val.png`. VAL 2023-03-25 .. 2023-11-30, n = 5,977 hourly rows.

**Branch fired: PASS.** Partial Spearman(dvol_t, next-24h log RV | trailing 24h/7d/30d RV) = **+0.2985** (block-bootstrap SE 0.0422), above the +0.1213 critical value. Raw Spearman +0.442.

**VAL_NOTE, beside the number:** "Same VAL weaknesses as every other BTC target here: soft-clean (arc #047 crossed it twice, both pre-registered) and a different liquidity
regime from TRAIN post-2023-04." This is a pass on a soft-clean slice in a different regime; it is not proof of out-of-sample behaviour.

**Weight applied:** power/alpha = 0.414/0.05 = 8.28 (inside the cap). Odds 0.9375/0.0625 = 15 x 8.28 = 124 -> **posterior 0.992**. State: **HIGH-VAL**.

Unweighted (reported, not scored): + signed 24h return control 0.296; + EWMA control 0.322; 2023Q2 hours 0.324 (n 2,352), 2023H2 hours 0.284 (n 3,647) - no fade.
Decay-first shape across all slices: CONFIRM quarters 0.33, 0.38, 0.22, 0.31, 0.18, then VAL 0.32 / 0.28: a stable positive link, larger than the EXPLORE number (0.17); the
levels are higher partly because the split-level partials are rank-residualised on their own controls. The number carries no direction, so no cost line (N/A).
What it claims: DVOL, a model-free implied-vol index, contains information about next-day realised vol beyond trailing windows. A known property; no trade implied.
