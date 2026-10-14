hypothesis: H3
slice: TRAIN
kind: search
controls: bid-ask bounce (Roll effect) in the Binance print
conditional: none

# cell 06 rule - H3: how much of the 1-6h reversal is bid-ask bounce? (controls: bid-ask bounce / Roll effect, and the entry-delay version)
Looked at: constructions of the reversal feature on Binance closes, each at k in 1,2,3,6 hours (the strong lookbacks), scored on h = 1, 6, 24:
 (a) base: -(log C_t - log C_(t-k)); entry at the end of bar t (as cell 5);
 (b) skip-1: -(log C_(t-1) - log C_(t-1-k)); drops the last print from the feature (entry still at the end of bar t);
 (c) entry delay d = 1, 2: feature as (a), but the forward return starts at the END of bar t+d (target shifted: log P_(t+d+h) - log P_(t+d)), so the print at t cannot be the start of the response.
Also scored against the Binance-close response (RB) instead of the primary price, for (a) and (c, d=1) at k=2.
Variants: 4 constructions x 4 lookbacks x 3 horizons = 48, plus 6 RB variants -> V = 54.
Hourly sampling; IC + NW (lags h+5+d). Direction +.
Pre-stated primary test: the bounce-free version is (c, d=1) at k=2 or 3, h6 (V_primary = 2, tcrit 2.24): SUPPORTED (a real reversal survives the entry delay) if the pooled-TRAIN IC >= +0.02 with NW t >= 2.24 AND
the C2+C3 (mid-response folds) IC >= +0.02 alone. REFUTED if the pooled TRAIN IC of (c, d=1) k=3 h6 is <= 0.01. Else INCONCLUSIVE. The share of the base IC lost by the delay is reported as the bounce share.
Power: hourly h6, N ~ 28,000 rows, se 0.0044; delta 0.02: power ~1.0 at tcrit 2.24 -> w_yes capped 3.0, w_no capped 0.33 (pooled test, large sample).
