hypothesis: H1
slice: TRAIN
kind: search
controls: volume-ratio alone; Binance-vs-primary response
conditional: none

# cell 03 rule - H1: does the volume scale add anything, and is the C2/C3 weakness the response switch? (controls: volume-ratio alone, Binance-vs-primary response)
Looked at (daily anchor 23:00, daily sampling, horizons 1h/6h/24h): seed (streak-3 x V5/V20), streak-only, V5/V20 alone (both signs), r24 (reference); each scored against the PRIMARY forward return and against the
BINANCE-close forward return (RB; same bars, no switch). 4 features x 3 h x 2 responses = 24 variants (V = 24).
Pre-stated primary test (H1, one of two horizons h6/h24 -> V_primary = 2, tcrit 2.24): the volume scale ADDS if IC(seed) - IC(streak-only) >= +0.01 (paired per-day difference, NW t >= 2.24).
Not-supported otherwise (and 'refuted' when the difference is <= 0 with t <= -1.65: the scale subtracts).
Secondary, reported, no belief weight: response-switch test = paired daily difference IC(Binance response) - IC(primary response) over C2+C3 for streak-only and r24 at h6/h24 (a positive difference >= +0.01, t >= 1.96,
says the primary-minus-Binance mid-vs-print wedge costs IC).
Power: daily-sampled paired difference, se ~ 0.012 (daily h6 c 0.46 /sqrt(1170) = 0.013; differences of two highly correlated ICs are tighter, using 0.012), delta 0.01: power 0.13, alpha 0.0250, w_yes 5.2 -> 3.00, w_no 0.89.
