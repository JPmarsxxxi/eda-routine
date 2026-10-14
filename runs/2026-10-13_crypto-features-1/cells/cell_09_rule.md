hypothesis: H10
slice: TRAIN
kind: search
controls: same-window signed return and absolute return
conditional: none

# cell 09 rule - H10: is the trade-count / volume surprise continuation more than the same-window return? (controls: same-window signed return and absolute return; conditional: none)
Features (as cell 8): nsurp_w and volsurp_w for w = 1, 6, 24 (hours), trailing-720h-norm surprise. Control: each feature residualised, per timestamp, on the cross-sectional RANKS of the same-window signed log return r_w and of |r_w|
(OLS on ranks, residual rank kept; residual_rank in panel.py). Scored at h = 6, 24 (primary forward return, hourly sampling, NW lags h+5): 3 w x 2 families x 2 h = 12 residual variants, plus the taker_1 residual on the 1-hour return rank rev1 at h1 (1 variant). V = 13.
Raw ICs are in cell 8 and are not recounted. Direction pre-stated by cell 8 (post hoc, hence the control): POSITIVE (surprise -> higher return).
Pass rule: SUPPORTED if the best residual variant has pooled-TRAIN IC >= +0.02 and NW t >= Sidak 2.89; REFUTED if every residual variant has IC <= 0.01; else INCONCLUSIVE.
For taker_1: reported only: if the residual IC at h1 is within +-0.005 of 0, the contrarian taker IC was the last bar's return.
Power: hourly h24 se ~ 0.0060 (c 0.96 / sqrt(28000)), delta 0.02, tcrit 2.89: power 0.67, w_yes -> 3.0 (cap), w_no 0.33; for h6 (se 0.0044) power 0.95, w_no 0.05.
