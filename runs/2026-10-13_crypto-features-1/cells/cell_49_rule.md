hypothesis: H13
slice: TRAIN
kind: search
controls: coin fixed effect in beta (static low-beta ranking)
conditional: sign of the last-6-hours market move

# cell 49 rule - H13: separate the static beta ranking from the market-reversal part (controls: coin fixed effect in beta = the static low-beta component; conditional: sign of the last-k-hours market move)
Decomposition (derived in cell 48): IC(-beta | UP) = a + c and IC(-beta | DOWN) = a - c with a = the state-independent 'low beta wins' component and c = the reversal component (the part whose sign follows the market move).
Features (lagged one bar as in cell 48, k = 6 market window; beta = trailing-720h beta to the EW market, ending at t-2):
 s_static = -beta (every hour, no gating) - the fixed-effect candidate;
 g_rev = -beta x sign(market return over the last 6 hours) / (a ranking that flips with the market move: the reversal-only part);
 g_rev_dt = -(beta - the coin's own trailing 2160h mean beta) x sign(market move) (time-varying beta only, reversal-only).
Scored at h = 1, 6 (3 features x 2 h = 6 variants; plus each residualised on f001 and the market-residual 3h reversal = 6 more; V = 12).
Pre-stated primary (reversal-only form g_rev residualised on f001 and the market-residual reversal, h1 and h6: V_primary = 2, tcrit 2.24): SUPPORTED if the best has pooled-TRAIN IC >= +0.015 with NW t >= 2.24 and the same sign in C2 and C3.
REFUTED if both residual IC < 0.01. Else INCONCLUSIVE. The static ranking s_static is reported (its IC is the fixed-effect size, not a claim).
Power: all-hours sample, se(h6) 0.0044, se(h1) 0.0026; delta 0.015: power 0.88; w_yes capped 3.0; w_no 0.12.
