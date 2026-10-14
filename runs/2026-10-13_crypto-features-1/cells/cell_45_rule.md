hypothesis: H10
slice: TRAIN
kind: search
controls: none
conditional: session of the signal, market trend, market volatility

# cell 45 rule - H10: does the participation-surprise sign depend on the session of the signal? (controls: none this cell; conditional: session of t, market trend, market volatility)
Feature: f003 (features/f003.py: 1-hour trade-count surprise residualised on the bar's return and |return|), scored at h6 and h24, by session of the signal hour t: ASIA 21-01, EU 07-11, US 13-16, other (4), by market trend up/down (2) and market volatility high/low (2) = 8 conditions x 2 h = 16 variants (V = 16).
Pre-stated primary (session contrast; h24; V_primary = 2 contrasts: ASIA vs other, US vs other; tcrit 2.24): the sign DEPENDS on the session if the paired-by-day difference IC(session) - IC(other) is <= -0.02 with NW t <= -2.24 for ASIA or US at h24 (cell 44 saw ASIA/US negative for the 6h-window surprises).
INCONCLUSIVE otherwise; REFUTED (sign does not depend on session) if both differences are within +-0.01.
Power: daily-collapsed paired differences, ~1,000 days, se ~0.012; delta 0.02: power at tcrit 2.24 0.28; w_yes capped 3.0; w_no 0.73.
