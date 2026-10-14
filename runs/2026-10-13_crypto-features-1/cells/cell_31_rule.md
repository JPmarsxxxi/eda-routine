hypothesis: H13
slice: TRAIN
kind: search
controls: coin fixed effect in beta (opposite signs in up / down market states)
conditional: market-up vs market-down state of the last k hours

# cell 31 rule - H13: fixed effect or reversal? (controls: coin fixed effect in beta via the sign of the market move; conditional: market-up vs market-down state)
Feature: lead_mkt_k = beta_mkt_i (trailing 720h, ending t-1) x (EW-market log return over the last k hours), k = 1, 3, 6, 24 (cell 30). State at t: UP if the market return over the same k hours is > 0, DOWN if < 0.
IC computed separately inside each state, at h = 1, 6, 24: 4 k x 2 states x 3 h = 24 variants. A second form removes the coin's average: lead minus its own trailing 720h mean (ending t-1) pooled (6 more variants, k=1 and k=6, h=1,6,24 -> hmm 2 k x 3 h = 6): V = 30.
Pre-stated primary (one k, one horizon each side; pair (k=6, h=6) and (k=24, h=24) -> V_primary = 2, tcrit 2.24): the REVERSAL reading is SUPPORTED if, for at least one of the two pairs, the IC is <= -0.015 with NW t <= -2.24 in BOTH the UP and the DOWN state
(the same sign in both states; a fixed effect gives opposite signs). REFUTED (fixed effect) if for both pairs the two states have opposite signs, each with |IC| >= 0.01. Else INCONCLUSIVE.
Direction: NEGATIVE IC (reversal). Power: states are ~50% of hours each (14,000 rows), se(h6) ~0.0062, se(h24) ~0.0085; delta 0.015: power at tcrit 2.24 0.57 (h6) / 0.32 (h24); w_yes capped 3.0; w_no ~0.43-0.69.
