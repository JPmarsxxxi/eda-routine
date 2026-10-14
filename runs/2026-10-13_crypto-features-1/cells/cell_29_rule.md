hypothesis: H11
slice: TRAIN
kind: search
controls: coin fixed effect (persistent volatility level)
conditional: none

# cell 29 rule - H11: volatility, extreme-return and risk-shape features (controls: coin fixed effect via within-coin detrending; conditional: none)
Features (hourly, Binance closes, trailing-only; r = 1h log return; all cross-sectionally ranked in the IC):
 rv_168 = std of r over 168h; rv_24 = std over 24h; rv_ratio = log(rv_24/rv_168); max_168 = max r over 168h; min_168 = min r over 168h; skew_168 = skewness of r over 168h; rng_24 = (max high - min low over 24h)/close;
 idio_168 = std over 168h of the residual of r on the EW-market return (trailing-720h beta).
Forms: (a) level; (b) within-coin detrended: level minus the coin's own trailing 2160h (90 day) mean ending at t-1 (kills the persistent coin level, the lesson of cell 11).
Horizons 1h, 6h, 24h. 8 features x 2 forms x 3 h = 48 variants (V = 48).
Pre-stated direction (risk-premium / lottery stories): NEGATIVE IC for rv_168, rv_24, max_168, skew_168, rng_24, idio_168 (high risk -> lower return). rv_ratio and min_168 have no pre-stated direction: they are reported two-sided, exploratory, and are not part of the primary family.
Pass rule (primary family = the 6 one-sided features, forms (a) and (b), 3 horizons: V_primary = 36, tcrit 3.20): SUPPORTED if the best DETRENDED (b) one-sided variant has pooled-TRAIN score (= -IC) >= +0.02 and NW t >= 3.20.
Not supported otherwise; wrong-signed significant results count as 'no'. Level (a) results are reported to show how much is a coin fixed effect.
Power simulation (measured noise, work/noise.json; delta = min_useful 0.02; Sidak critical |t| = 3.28 for V = 48 variants; cap 3x):
  sampling h h=1: se 0.0026, power 1.00, alpha(one-sided) 0.0005, w_yes 1920.0 -> 3.00, w_no 0.00 -> 0.33
  sampling h h=6: se 0.0044, power 0.90, alpha(one-sided) 0.0005, w_yes 1723.1 -> 3.00, w_no 0.10 -> 0.33
  sampling h h=24: se 0.0058, power 0.58, alpha(one-sided) 0.0005, w_yes 1110.5 -> 3.00, w_no 0.42 -> 0.42
  sampling d h=1: se 0.0145, power 0.03, alpha(one-sided) 0.0005, w_yes 55.1 -> 3.00, w_no 0.97 -> 0.97
  sampling d h=6: se 0.0133, power 0.04, alpha(one-sided) 0.0005, w_yes 72.0 -> 3.00, w_no 0.96 -> 0.96
  sampling d h=24: se 0.0164, power 0.02, alpha(one-sided) 0.0005, w_yes 37.7 -> 3.00, w_no 0.98 -> 0.98
