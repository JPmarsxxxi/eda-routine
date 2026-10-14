hypothesis: H2
slice: TRAIN
kind: search
controls: close-location alone, (open/close)^5 alone, same-window 24h return
conditional: none

# cell 15 rule - H2: Alpha#54 family, closing strength (controls: close-location alone, (open/close)^5 alone, same-window return; conditional: none)
Seed (sign as in TARGET.md, 'minus #54'): f54 = ((close - low)/(high - low)) * (open/close)^5 on (a) UTC-day OHLC at the 23:00 bar (sampling d) and (b) rolling 24h blocks ending at every hour (open = bar t-23 open, high/low = rolling 24h max/min; sampling h).
Rivals: clv = (close - low)/(high - low) alone; oc5 = (open/close)^5 alone; the 24h return r24' = +(log C_t - log C_(t-24)) (continuation sign, the same-window return) - each a variant. Residual form: f54 (rolling) residualised on the rank of r24' (3 variants).
Horizons 1h, 6h, 24h. Variants: f54 (2) + clv (2) + oc5 (2) + r24' (1) = 7 features x 3 h = 21, + 3 residual variants = 24. V = 24.
Direction (pre-stated, TARGET.md: closing strength continues): POSITIVE IC.
Pre-stated primary (the two f54 constructions x 3 horizons: V_primary = 6, tcrit 2.64): SUPPORTED if the best f54 variant has pooled-TRAIN IC >= +0.02 and NW t >= 2.64. Not supported otherwise (REFUTED if all six are <= 0 with the best t <= -1.65... significant negative).
The rival results are reported for attribution; the residual shows what f54 adds beyond the same-window return.
Power simulation (measured noise, work/noise.json; delta = min_useful 0.02; Sidak critical |t| = 3.08 for V = 24 variants; cap 3x):
  sampling h h=1: se 0.0026, power 1.00, alpha(one-sided) 0.0010, w_yes 960.0 -> 3.00, w_no 0.00 -> 0.33
  sampling h h=6: se 0.0044, power 0.93, alpha(one-sided) 0.0010, w_yes 891.8 -> 3.00, w_no 0.07 -> 0.33
  sampling h h=24: se 0.0058, power 0.65, alpha(one-sided) 0.0010, w_yes 628.7 -> 3.00, w_no 0.35 -> 0.35
  sampling d h=1: se 0.0145, power 0.04, alpha(one-sided) 0.0010, w_yes 42.8 -> 3.00, w_no 0.96 -> 0.96
  sampling d h=6: se 0.0133, power 0.06, alpha(one-sided) 0.0010, w_yes 54.8 -> 3.00, w_no 0.94 -> 0.94
  sampling d h=24: se 0.0164, power 0.03, alpha(one-sided) 0.0010, w_yes 30.1 -> 3.00, w_no 0.97 -> 0.97
