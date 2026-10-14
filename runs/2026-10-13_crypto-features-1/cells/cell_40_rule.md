hypothesis: H5
slice: TRAIN
kind: search
controls: f004 premium crowding feature (incremental test)
conditional: none

# cell 40 rule - H5: do basis and funding add to the premium feature f004? (controls: f004 itself, the premium crowding feature; conditional: none)
Features: basis_dtr = (perp kline close / spot close - 1) minus the coin's trailing-720h mean; funding_dtr = last settled funding minus the coin's trailing-720h mean; each (a) rank only, (b) rank residualised on the ranks of r3s, r24 (as f004), (c) residualised on r3s, r24 AND the f004 rank (features/f004.py) - the incremental piece.
Horizons h = 1, 6, 24. Variants: 2 features x 3 forms x 3 h = 18; V = 18. Direction: score = -IC (crowding sign, as H5).
Pre-stated primary (form c, 2 features x 3 horizons: V_primary = 6, tcrit 2.64): SUPPORTED if any form-(c) variant has pooled-TRAIN score >= +0.015 (the library adds a feature only if incremental IC is a large fraction of min_useful) with NW t >= 2.64 and the same sign in C2 and C3.
REFUTED if every form-(c) variant has score < 0.01. Else INCONCLUSIVE. (The 0.015 incremental bar is lower than min_useful because a combiner can use a half-size independent signal; the candidate, if frozen, is still judged at 0.02 per fold.)
Power: hourly h24 se 0.0060, h6 0.0044, h1 0.0026; delta 0.015: power at tcrit 2.64: 0.45 (h24) / 0.78 (h6); w_yes capped 3.0; w_no 0.56 (h24).
