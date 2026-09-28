### Cell 04 — EDA: does r_first predict r_last? (C5, the effect)

**Sub-claim being tested:** C5: "The effect: r_first predicts r_last with positive sign, at the last half-hour"

**Why it matters to the hypothesis:** this IS the claim. Refuted -> the hunt stops here.

**Test(s) used:** pooled TRAIN OLS slope of r_last on r_first with Newey-West (5 lags) t; Pearson and Spearman IC of r_first with the return over the last tau half-hours ending 24:00, tau in {1, 5, 20} (tau = 1 is the claim); lead-lag cross-correlation profile of r_first with every later half-hour of the same day (half-hours 2..48); sign hit rate with a two-sided binomial test vs 50%.

**Decision rule before running:** "I will consider C5 **supported** if slope > 0 AND NW t >= 2.0 AND Spearman p < 0.05 (tau = 1); **refuted** if slope <= 0 OR NW t < 1.0; **inconclusive** if slope > 0 with 1.0 <= NW t < 2.0 (or t >= 2 but Spearman p >= 0.05)." The tau = 5 / 20 ICs and the lead-lag profile are reported, not scored (the claim's horizon is tau = 1).

**Engine/library APIs used:** `statsmodels.OLS` HAC; `scipy.stats.pearsonr`, `spearmanr`, `binomtest`.

**Data:** TRAIN usable days.

**Decisions I need from you:** none.

Proceeding (unattended).
