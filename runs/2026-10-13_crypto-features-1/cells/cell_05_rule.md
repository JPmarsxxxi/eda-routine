hypothesis: H3
slice: TRAIN
kind: search
controls: none
conditional: none

# cell 05 rule - H3: lookback x scaling sweep of the cross-sectional reversal (controls: none this cell; conditional: none)
Looked at: reversal feature -(log C_t - log C_{t-k}) on Binance closes (trailing, knowable at the end of bar t), k in 1,2,3,6,12,24,48,72,168 hours, four transforms: raw; vol-scaled (divided by the coin's trailing
168h std of 1h returns); market-residual (minus trailing-720h beta x equal-weight-market return over the same k hours); market-residual and vol-scaled. Horizons 1h, 6h, 24h. 9 x 4 x 3 = 108 variants (V = 108).
Hourly sampling (all hours), cross-sectional Spearman IC vs primary forward return, NW t (lags h+5). Slice TRAIN with per-slice report. Direction pre-stated: positive IC (past loser outperforms).
Pass rule: SUPPORTED if the best of the 108 variants has pooled-TRAIN IC >= +0.02 and NW t >= Sidak 3.50. Not supported otherwise. Lookback profile (the k at which IC peaks) is reported for each transform and horizon.
Power simulation (measured noise, work/noise.json; delta = min_useful 0.02; Sidak critical |t| = 3.50 for V = 108 variants; cap 3x):
  sampling h h=1: se 0.0026, power 1.00, alpha(one-sided) 0.0002, w_yes 4319.9 -> 3.00, w_no 0.00 -> 0.33
  sampling h h=6: se 0.0044, power 0.85, alpha(one-sided) 0.0002, w_yes 3680.5 -> 3.00, w_no 0.15 -> 0.33
  sampling h h=24: se 0.0058, power 0.49, alpha(one-sided) 0.0002, w_yes 2117.7 -> 3.00, w_no 0.51 -> 0.51
  sampling d h=1: se 0.0145, power 0.02, alpha(one-sided) 0.0002, w_yes 72.9 -> 3.00, w_no 0.98 -> 0.98
  sampling d h=6: se 0.0133, power 0.02, alpha(one-sided) 0.0002, w_yes 97.6 -> 3.00, w_no 0.98 -> 0.98
  sampling d h=24: se 0.0164, power 0.01, alpha(one-sided) 0.0002, w_yes 48.3 -> 3.00, w_no 0.99 -> 0.99
