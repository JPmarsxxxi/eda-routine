hypothesis: H4
slice: TRAIN
kind: search
controls: none
conditional: none

# cell 08 rule - H4: volume, trade-count, trade-size and taker-flow surprises (controls: none this cell; conditional: none)
Features (hourly, Binance spot, trailing-only normalisation; w = window in hours of the numerator):
 volsurp_w = log( sum(quote_vol, w) / (w * mean(quote_vol over the trailing 720h ending at t-w)) ), w = 1, 6, 24;
 nsurp_w = same with the trade count n; sizesurp_w = log(quote_vol/n over w) minus its trailing-720h mean (average trade size surprise); taker_w = sum(buy_vol, w)/sum(vol, w) - 0.5 (taker-buy imbalance), w = 1, 6, 24;
 volratio_d = log( sum(quote_vol, 120) / sum(quote_vol, 480) ) (the Alpha#30 volume ratio at hourly anchors).
13 features x h = 1, 6, 24 = 39 variants (V = 39). Hourly sampling, cross-sectional Spearman IC, NW t (lags h+5), TRAIN with per-slice report.
Pre-stated directions (from cell 3 and the story): surprises in volume / trade count / size: NEGATIVE IC for the surprise (high-attention coin underperforms), score = -IC; taker imbalance: POSITIVE (buy-heavy flow continues).
Pass rule: SUPPORTED if the best variant in its pre-stated direction has pooled-TRAIN score >= 0.02 and NW t >= Sidak 3.22; the wrong-signed significant ones count as 'no'. Per-slice sign stability is reported (4 slices).
Power simulation (measured noise, work/noise.json; delta = min_useful 0.02; Sidak critical |t| = 3.22 for V = 39 variants; cap 3x):
  sampling h h=1: se 0.0026, power 1.00, alpha(one-sided) 0.0006, w_yes 1560.0 -> 3.00, w_no 0.00 -> 0.33
  sampling h h=6: se 0.0044, power 0.91, alpha(one-sided) 0.0006, w_yes 1415.9 -> 3.00, w_no 0.09 -> 0.33
  sampling h h=24: se 0.0058, power 0.60, alpha(one-sided) 0.0006, w_yes 938.1 -> 3.00, w_no 0.40 -> 0.40
  sampling d h=1: se 0.0145, power 0.03, alpha(one-sided) 0.0006, w_yes 51.1 -> 3.00, w_no 0.97 -> 0.97
  sampling d h=6: se 0.0133, power 0.04, alpha(one-sided) 0.0006, w_yes 66.4 -> 3.00, w_no 0.96 -> 0.96
  sampling d h=24: se 0.0164, power 0.02, alpha(one-sided) 0.0006, w_yes 35.3 -> 3.00, w_no 0.98 -> 0.98
