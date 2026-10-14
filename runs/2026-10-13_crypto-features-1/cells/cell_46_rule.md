hypothesis: H6
slice: TRAIN
kind: search
controls: Binance bounce (entry delay + rev1/rev3 residual)
conditional: session of the signal (US for Coinbase, ASIA for Upbit)

# cell 46 rule - H6: do the venue-gap residuals live in the home session of the other venue? (controls: Binance bounce via entry delay and residual on rev1, rev3 as in cell 14; conditional: session of the signal)
Features (cell 14 form (c): entry delay 1 and residualised on rev1, rev3 ranks): cb_gap_lvl, cb_retdiff_3, ub_gap_lvl, ub_retdiff_6. Session of the signal t: US 13-16 UTC (Coinbase's home session), ASIA 21-01 UTC (Upbit's home session), other (3). Horizons 1 and 6.
Pairs tested: Coinbase features in US vs other; Upbit features in ASIA vs other: 4 features x 2 h x (home session, other) = 16 variants (V = 16).
Pre-stated primary (V_primary = 8 home-session variants, tcrit 2.73): the gap residual is a home-session lead if a Coinbase feature has pooled-TRAIN IC >= +0.02 in US-hour signals, or an Upbit feature >= +0.02 in ASIA-hour signals, with NW t >= 2.73 and the same sign in C2 and C3.
REFUTED if every home-session variant has IC < 0.01. Else INCONCLUSIVE.
Power: home sessions are 17-21% of the hours (~5,000 rows; Upbit coverage lower): se ~0.0060 (h6), delta 0.02: power at tcrit 2.73 0.63; w_no 0.37; w_yes capped 3.0.
