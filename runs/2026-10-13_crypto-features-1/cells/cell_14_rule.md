hypothesis: H6
slice: TRAIN
kind: search
controls: Binance bid-ask bounce / own-coin 1-3h reversal
conditional: none

# cell 14 rule - H6: do the venue features survive the Binance-bounce rival? (controls: Binance bid-ask bounce / own-coin reversal; conditional: none)
Features: cb_gap_lvl, ub_gap_lvl, cb_retdiff_3, ub_retdiff_3, ub_retdiff_6 (cell 13). Three forms at h = 1 and 6:
 (a) base (as cell 13, reference);
 (b) entry delay 1: the response starts at the END of bar t+1 (so the Binance print at t cannot be the start of the response);
 (c) entry delay 1 AND residualised, per timestamp, on the cross-sectional ranks of the Binance 1-hour reversal rev1 = -(log C_t - log C_(t-1)) and the 3-hour reversal rev3 = -(log C_t - log C_(t-3)) (OLS on ranks, residual rank).
Variants evaluated: 5 features x 3 forms x 2 horizons = 30 (V = 30; the pre-stated primary family is the form-(c) cells: 10 variants, tcrit 2.81).
Pass rule: SUPPORTED if the best form-(c) variant has pooled-TRAIN IC >= +0.02 and NW t >= 2.81, and the IC is positive in C2 and C3. REFUTED if every form-(c) variant has IC <= 0.01. Else INCONCLUSIVE.
The share of the base IC kept by (b) and (c) is reported per feature.
Power: hourly h1/h6, coverage 17-26k rows, se 0.0033-0.0053 (venue sample, min_n 5): delta 0.02, tcrit 2.81: power 0.95; w_yes -> 3.0; w_no 0.05.
