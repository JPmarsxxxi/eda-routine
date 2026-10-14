hypothesis: H4
slice: TRAIN
kind: search
controls: same-window signed return and |return|
conditional: session, market trend, market volatility

# cell 44 rule - H4: do the pre-stated (overheating / aggressive-buying) directions appear in any regime once the same-window return is removed? (controls: same-window signed return and |return|; conditional: session, market trend, market volatility)
Features (as cell 8, w = 6): volsurp_6, nsurp_6 (pre-stated direction NEGATIVE: score = -IC) and taker_6, taker_24 (pre-stated POSITIVE: score = +IC), each residualised on the cross-sectional ranks of the same-window signed return and |return| (cell 9 construction).
Conditions (point-in-time at t): session of t: ASIA 21-01, EU 07-11, US 13-16, other; market trend: EW-market 30-day return up / down; market volatility: trailing-168h std of the EW-market 1h return above / below its EXPLORE median. 4 + 2 + 2 = 8 conditions;
7 conditions? count: sessions 4, trend 2, vol 2 = 8. Horizons 6 and 24. 4 features x 8 conditions x 2 h = 64 variants (V = 64).
Pre-stated primary: SUPPORTED if any variant has pooled-TRAIN score (pre-stated sign) >= +0.02 and NW t >= Sidak 3.36. Not supported otherwise; wrong-signed significant results count as 'no' and are reported as leads.
Power (conditions hold 15-50% of the hours; se 0.006-0.012 at h24): delta 0.02, tcrit 3.36: power 0.20; w_no ~0.81.
