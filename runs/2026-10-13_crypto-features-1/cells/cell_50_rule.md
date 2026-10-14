hypothesis: H17
slice: TRAIN
kind: search
controls: same-window signed return and |return|; coin fixed effect (detrending)
conditional: none

# cell 50 rule - H17: perp aggressive flow and derivatives intensity (controls: same-window return and |return|; coin fixed effect via within-coin detrending; conditional: none)
Features (hourly, Binance USD-M perp klines + spot; w = window hours): ptaker_w = sum(perp taker_buy_volume, w)/sum(perp volume, w) - 0.5, w = 1, 6, 24; pgap_w = ptaker_w - staker_w (spot buy_vol/vol - 0.5 over w), w = 6, 24; pshare = log(perp quote_volume_24h / spot quote_volume_24h) minus its coin's trailing-2160h mean;
 pnsurp_w = log(perp trade count over w / (w x trailing-720h mean per hour)), w = 1, 6. 8 features. Forms: (a) rank of the feature detrended within coin (minus its trailing 2160h mean ending t-1, except pshare/pnsurp already scaled); (b) (a) residualised on the cross-sectional ranks of the same-window signed return and |return|.
Horizons 1, 6, 24. 8 features x 2 forms x 3 h = 48 (V = 48). Direction two-sided (exploratory family; the sign found is a finding, not a pre-stated claim): score = |IC| with its sign reported.
Pre-stated primary: SUPPORTED if the best form-(b) variant has |pooled-TRAIN IC| >= 0.02 and NW |t| >= Sidak 3.28, with the same sign in C2 and C3. Not supported otherwise.
Power simulation (measured noise, work/noise.json; delta = min_useful 0.02; Sidak critical |t| = 3.28 for V = 48 variants; cap 3x):
  sampling h h=1: se 0.0026, power 1.00, alpha(one-sided) 0.0005, w_yes 1920.0 -> 3.00, w_no 0.00 -> 0.33
  sampling h h=6: se 0.0044, power 0.90, alpha(one-sided) 0.0005, w_yes 1723.1 -> 3.00, w_no 0.10 -> 0.33
  sampling h h=24: se 0.0058, power 0.58, alpha(one-sided) 0.0005, w_yes 1110.5 -> 3.00, w_no 0.42 -> 0.42
  sampling d h=1: se 0.0145, power 0.03, alpha(one-sided) 0.0005, w_yes 55.1 -> 3.00, w_no 0.97 -> 0.97
  sampling d h=6: se 0.0133, power 0.04, alpha(one-sided) 0.0005, w_yes 72.0 -> 3.00, w_no 0.96 -> 0.96
  sampling d h=24: se 0.0164, power 0.02, alpha(one-sided) 0.0005, w_yes 37.7 -> 3.00, w_no 0.98 -> 0.98
