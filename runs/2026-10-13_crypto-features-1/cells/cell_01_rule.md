hypothesis: H1
slice: TRAIN
kind: search
controls: none
conditional: none

# cell 01 rule - H1 seed replication (Kakushadze #30 as written, three horizons, two anchors)
What is looked at: the exact seed f = (1 - rank(sign(c-c1)+sign(c1-c2)+sign(c2-c3))) * sum(vol,5)/sum(vol,20) built (a) on UTC-day OHLCV (decision at the 23:00 bar, sampling d)
and (b) on rolling 24h blocks ending at every hour (step 24 h, sampling h, the "anchor-hour" version), plus the streak-only part (1 - rank(streak)) of each (attribution: is the volume scale doing work?).
Variants: 4 feature definitions x 3 horizons (1h, 6h, 24h) = 12 (V = 12). Slice: TRAIN (EXPLORE + C1..C3, per-slice report). Tool: cross-sectional Spearman IC per timestamp (xs_ic), Newey-West t on the IC series
(lags h+5 hourly, 3 daily). 14c menu row: "X predicts forward Y" -> IC.
Direction (pre-stated): positive IC = fade works (down-streak + volume surge ranks high and earns more).
Pass rule: supported if the best of the 12 variants has pooled-TRAIN mean IC >= +0.02 AND NW t >= Sidak critical (V=12). Else not-supported (also when significant in the opposite sign).
Per-slice IC is reported for stability, not used in the branch. Weight if supported = power/alpha, if not = (1-power)/(1-alpha), at the best variant's own se, capped 3x.
Power simulation (measured noise, work/noise.json; delta = min_useful 0.02; Sidak critical |t| = 2.87 for V = 12 variants; cap 3x):
  sampling h h=1: se 0.0026, power 1.00, alpha(one-sided) 0.0021, w_yes 480.0 -> 3.00, w_no 0.00 -> 0.33
  sampling h h=6: se 0.0044, power 0.95, alpha(one-sided) 0.0021, w_yes 457.7 -> 3.00, w_no 0.05 -> 0.33
  sampling h h=24: se 0.0058, power 0.73, alpha(one-sided) 0.0021, w_yes 350.2 -> 3.00, w_no 0.27 -> 0.33
  sampling d h=1: se 0.0145, power 0.07, alpha(one-sided) 0.0021, w_yes 32.9 -> 3.00, w_no 0.93 -> 0.93
  sampling d h=6: se 0.0133, power 0.09, alpha(one-sided) 0.0021, w_yes 41.2 -> 3.00, w_no 0.92 -> 0.92
  sampling d h=24: se 0.0164, power 0.05, alpha(one-sided) 0.0021, w_yes 23.9 -> 3.00, w_no 0.95 -> 0.95
