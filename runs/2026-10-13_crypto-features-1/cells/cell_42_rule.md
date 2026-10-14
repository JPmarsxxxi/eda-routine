hypothesis: H16
slice: TRAIN
kind: search
controls: coin fixed effect (persistent range position of trending coins)
conditional: none

# cell 42 rule - H16: multi-day range position, drawdown, rally and moving-average distance (controls: coin fixed effect via within-coin detrending; conditional: none)
Features (hourly, Binance, trailing-only), windows w in 72, 168, 336, 720 hours: pos_w = (C - min low_w)/(max high_w - min low_w); dd_w = log(C / max close_w) (<= 0); ru_w = log(C / min close_w) (>= 0); madev_w = log(C / mean close_w).
Forms: (a) level; (b) within-coin detrended: minus the coin's own trailing-2160h mean ending at t-1. 4 features x 4 w x 2 forms x 3 h = 96 variants (V = 96); the pre-stated one-sided primary family is the detrended forms at h6 and h24 (4 x 4 x 2 = 32, tcrit 3.16).
Direction (range mean reversion): NEGATIVE IC for pos_w, ru_w, madev_w (high = near top / far above mean); POSITIVE for dd_w (deep drawdown = lower = more negative value; a higher dd, i.e. near the high, predicts lower, so dd_w is also NEGATIVE; all four scored as -IC).
Pass rule: SUPPORTED if the best detrended (b) primary variant has pooled-TRAIN score (-IC) >= +0.02 and NW t >= 3.16. Not supported otherwise; wrong-signed significant results count as 'no'. Level (a) is reported for the fixed-effect share.
Power simulation (measured noise, work/noise.json; delta = min_useful 0.02; Sidak critical |t| = 3.47 for V = 96 variants; cap 3x):
  sampling h h=1: se 0.0026, power 1.00, alpha(one-sided) 0.0003, w_yes 3840.0 -> 3.00, w_no 0.00 -> 0.33
  sampling h h=6: se 0.0044, power 0.86, alpha(one-sided) 0.0003, w_yes 3299.1 -> 3.00, w_no 0.14 -> 0.33
  sampling h h=24: se 0.0058, power 0.50, alpha(one-sided) 0.0003, w_yes 1930.7 -> 3.00, w_no 0.50 -> 0.50
  sampling d h=1: se 0.0145, power 0.02, alpha(one-sided) 0.0003, w_yes 70.1 -> 3.00, w_no 0.98 -> 0.98
  sampling d h=6: se 0.0133, power 0.02, alpha(one-sided) 0.0003, w_yes 93.4 -> 3.00, w_no 0.98 -> 0.98
  sampling d h=24: se 0.0164, power 0.01, alpha(one-sided) 0.0003, w_yes 46.7 -> 3.00, w_no 0.99 -> 0.99
