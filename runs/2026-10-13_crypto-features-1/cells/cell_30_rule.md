hypothesis: H12
slice: TRAIN
kind: search
controls: none
conditional: none

# cell 30 rule - H12: BTC / market lead-lag through beta (controls: none this cell; conditional: none)
Features (hourly, Binance closes; beta_i = trailing-720h beta of the coin's 1h return on BTC's (or on the EW-market's) 1h return, ending at t-1; the cross-sectional rank differs only through beta dispersion):
 lead_btc_k = beta_btc_i * (BTC log return over the last k hours), k = 1, 3, 6, 24; lead_mkt_k = beta_mkt_i * (EW-market log return over k hours), k = 1, 3, 6, 24. 8 features x h = 1, 6, 24 = 24 variants (V = 24).
Pre-stated direction (diffusion of market information to high-beta coins with a delay): POSITIVE IC (after a market rise high-beta coins keep rising). The reversal literature (cells 5-6: market-wide hourly reversal exists) argues the opposite; the sign is therefore a genuine test.
Pass rule: SUPPORTED if the best variant (pre-stated positive sign) has pooled-TRAIN IC >= +0.02 and NW t >= Sidak 3.08; wrong-signed significant results count as 'no'.
Power simulation (measured noise, work/noise.json; delta = min_useful 0.02; Sidak critical |t| = 3.08 for V = 24 variants; cap 3x):
  sampling h h=1: se 0.0026, power 1.00, alpha(one-sided) 0.0010, w_yes 960.0 -> 3.00, w_no 0.00 -> 0.33
  sampling h h=6: se 0.0044, power 0.93, alpha(one-sided) 0.0010, w_yes 891.8 -> 3.00, w_no 0.07 -> 0.33
  sampling h h=24: se 0.0058, power 0.65, alpha(one-sided) 0.0010, w_yes 628.7 -> 3.00, w_no 0.35 -> 0.35
  sampling d h=1: se 0.0145, power 0.04, alpha(one-sided) 0.0010, w_yes 42.8 -> 3.00, w_no 0.96 -> 0.96
  sampling d h=6: se 0.0133, power 0.06, alpha(one-sided) 0.0010, w_yes 54.8 -> 3.00, w_no 0.94 -> 0.94
  sampling d h=24: se 0.0164, power 0.03, alpha(one-sided) 0.0010, w_yes 30.1 -> 3.00, w_no 0.97 -> 0.97
