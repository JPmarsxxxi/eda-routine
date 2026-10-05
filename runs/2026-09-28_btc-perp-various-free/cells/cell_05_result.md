# cell_05 RESULT — H2 CONFIRM opening

Script `scripts/cell_05_h2_confirm.py`; tables `tables/05_result.json`, `tables/05_by_quarter.csv`; plot `plots/05_h2_confirm.png`.
Slice: CONFIRM, n = 10,585 hourly rows.

**Branch fired: SUPPORTED.** Deciding number: partial Spearman (dvol vs next-24h log RV | trailing 24h/7d/30d RV) =
**+0.174** (block-bootstrap SE 0.040), above the 0.0869 critical value. Raw Spearman 0.529. EXPLORE partial was 0.17.

**Weight applied:** power/alpha = 0.609/0.05 = 12.2 -> **capped to 10** (guard b). H2 odds 0.60/0.40 = 1.5 x 10 = 15 ->
**posterior 0.9375 (recorded 0.938)**. State: HIGH-CONFIRM, queued for the Phase 3 VAL check.

Unweighted rivals / stability (reported, not scored):
- + trailing 24h signed log return (leverage effect): 0.176 (unchanged).
- + EWMA of hourly squared returns, half-life 72 h (HAR impostor): 0.180 (unchanged).
- By quarter (decay-first): 0.332, 0.384, 0.220, 0.313, 0.175 (2022Q1..2023Q1). Positive in all five; the last quarter is the
  lowest, so a fade is possible but not established from one quarter. (Quarterly values exceed the pooled value because each
  quarter is rank-residualised on its own controls.)

What this claims and does not: DVOL carries information about next-24h realized vol beyond three trailing RV windows. It is
a volatility forecast, not a return predictor and not a trade; it is a known property of implied volatility, so its value here
is confirming the data behaves as expected on this bundle, not novelty. Cost: N/A (no direction).
