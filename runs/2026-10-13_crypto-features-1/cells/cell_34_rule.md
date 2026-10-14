hypothesis: H14
slice: TRAIN
kind: search
controls: other kept features and simple baselines (library orthogonality)
conditional: none

# cell 34 rule - H14: orthogonality, incremental IC and cost line of f008 (seasonality) and of the h1 horizon of f004 (controls: the other kept features and five baselines; conditional: none)
Looked at: features/f008.py (season60 demeaned, defined in the registry text) and the existing f001..f007 modules computed from the long TRAIN frame (as in cell 17), five baselines (b_rev1, b_rev24, b_mom168, b_lowvol, b_liq).
Orthogonality: mean cross-sectional Spearman correlation of f008 and f004 with every other candidate and baseline on shared timestamps; incremental IC at h1 after partialling out the two most correlated others; cost line at h1: top-3 minus bottom-3 forward 1h return (bp) vs 2 x mean round trip of the traded names.
Variants: f008 at h1/h6/h24 (3) + f004 at h1 (1, already in cells 11-12 under the residualised form: recomputed from features/f004.py) + 2 incremental ICs = 6 (V = 6).
Pre-stated primary (H14, one test, tcrit 1.96): f008 is NOT a duplicate and adds: SUPPORTED if max |corr| of f008 with every other candidate and baseline is < 0.5 AND its incremental IC at h1 is >= +0.015 with NW t >= 1.96. REFUTED if max |corr| >= 0.7. Else INCONCLUSIVE.
Power: hourly h1, se 0.0026; delta 0.015: power ~1.0; w_yes capped 3.0, w_no capped 0.33.
