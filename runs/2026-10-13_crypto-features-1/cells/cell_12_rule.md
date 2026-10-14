hypothesis: H5
slice: TRAIN
kind: search
controls: none
conditional: market-wide premium regime, hours since funding settlement, session, funding floor share

# cell 12 rule - H5: where does the premium crowding signal live? (controls: none; conditional: market-wide premium regime, time to funding settlement, session)
Feature (fixed from cell 11): prem_dtr = premium-index close minus the coin's trailing-720h mean (ending t-1), cross-sectional rank, residualised on r3s and r24 ranks (form c). Score = -IC (crowded -> lower return). h = 1, 6, 24.
Conditions at t: (1) market premium regime: EW-market mean of the raw premium above / below its own trailing-720h median; (2) funding clock: hours since the last settlement (00/08/16 UTC): bucket 0-2 / 3-5 / 6-7; (3) session of t: ASIA 21-01, EU 07-11, US 13-16, other;
(4) funding floor: market share of coins whose settled funding is exactly 0.0001 above / below 50%. 2+3+4+2 = 11 conditions x 3 h = 33 variants (V = 33).
Pre-stated primary (robustness, h6, two conditions of (1): V_primary = 2, tcrit 2.24): SUPPORTED (the effect is not regime-confined) if the score is >= +0.015 with NW t >= 2.24 in BOTH market-premium regimes (above and below).
REFUTED if one regime has a score <= 0 with t <= -1.65 (wrong sign) . Else INCONCLUSIVE. All other conditions are exploratory and reported only.
Power: each regime ~ half the sample (14,000 rows), se(h6) 0.0062, delta 0.015: power 0.57, w_yes -> 3.0, w_no 0.43.
