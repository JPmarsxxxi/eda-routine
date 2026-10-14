hypothesis: H15
slice: TRAIN
kind: search
controls: own 1-hour reversal rev1
conditional: none

# cell 39 rule - H15: what is left of the bar-shape features after the last hour's own reversal? (controls: the 1h reversal rev1 and the lag-1 bounce-free reversal; conditional: none)
Features (cell 38): clv1, body_n, upper_wick, lower_wick, vwap_dev; each residualised, per timestamp, on the cross-sectional ranks of rev1 = -(log C_t - log C_(t-1)) (OLS on ranks, residual rank) - the pure shape information net of the hour's return.
Scored delayed-entry (response starts at the end of bar t+1) at h = 1, 6 (5 features x 2 h = 10 variants, V = 10) and undelayed (reported only).
Pre-stated primary: SUPPORTED if any residual delayed variant has |IC| >= 0.02 and NW |t| >= 2.81; REFUTED if every residual delayed variant has |IC| < 0.01; else INCONCLUSIVE.
Power: hourly h1 se 0.0026, h6 0.0044; delta 0.02 -> power ~1.0 at tcrit 2.81; w_yes capped 3.0; w_no capped 0.33.
