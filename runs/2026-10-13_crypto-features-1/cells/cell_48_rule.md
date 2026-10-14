hypothesis: H13
slice: TRAIN
kind: search
controls: f001 / f002 and the market-residual own-return reversal (library orthogonality)
conditional: market-UP state

# cell 48 rule - H13: does the UP-state beta feature add to the reversal features? (controls: f001 and f002 and the market-residual own-return reversal; conditional: market-UP state)
Feature: bup_k = -beta_mkt_i (trailing-720h beta to the EW market, ending t-1), defined only when the EW-market return over the last k hours is > 0, with the response as in the delayed scoring of cell 47 (the feature is the lagged one: stamped t+1, so the response from the end of bar t+1 is the standard response). k = 1, 3, 6.
Orthogonality: mean XS correlation of bup_k with f001 (features/f001.py), f002 and the market-residual 3h reversal; incremental IC at h1 and h6 after partialling out f001 and the market-residual reversal (OLS on cross-sectional ranks), in the UP state.
Variants: 3 k x 2 forms (raw, residual on f001 + market-residual reversal) x 2 h = 12 (V = 12). Direction: score = IC of the feature -beta_i (i.e. positive when low-beta coins outperform).
Pre-stated primary (V_primary = 3: the residual form at h6 for k = 1, 3, 6; tcrit 2.64): SUPPORTED if the best residual variant has pooled UP-state score >= +0.015 with NW t >= 2.64 and the same sign in C2 and C3. REFUTED if every residual variant has score < 0.01 (it is the reversal's market component). Else INCONCLUSIVE.
Power: UP-state ~14,000 rows, se(h6) ~0.0062; delta 0.015: power at tcrit 2.64 0.41; w_yes capped 3.0; w_no 0.59.
