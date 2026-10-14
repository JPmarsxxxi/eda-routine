import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc = kit.tcrit_for(8)
rule = f"""# cell 46 rule - H6: do the venue-gap residuals live in the home session of the other venue? (controls: Binance bounce via entry delay and residual on rev1, rev3 as in cell 14; conditional: session of the signal)
Features (cell 14 form (c): entry delay 1 and residualised on rev1, rev3 ranks): cb_gap_lvl, cb_retdiff_3, ub_gap_lvl, ub_retdiff_6. Session of the signal t: US 13-16 UTC (Coinbase's home session), ASIA 21-01 UTC (Upbit's home session), other (3). Horizons 1 and 6.
Pairs tested: Coinbase features in US vs other; Upbit features in ASIA vs other: 4 features x 2 h x (home session, other) = 16 variants (V = 16).
Pre-stated primary (V_primary = 8 home-session variants, tcrit {tc:.2f}): the gap residual is a home-session lead if a Coinbase feature has pooled-TRAIN IC >= +0.02 in US-hour signals, or an Upbit feature >= +0.02 in ASIA-hour signals, with NW t >= {tc:.2f} and the same sign in C2 and C3.
REFUTED if every home-session variant has IC < 0.01. Else INCONCLUSIVE.
Power: home sessions are 17-21% of the hours (~5,000 rows; Upbit coverage lower): se ~0.0060 (h6), delta 0.02: power at tcrit {tc:.2f} {kit.power(0.0065, 0.02, tc)['power']:.2f}; w_no {kit.power(0.0065, 0.02, tc)['w_no']:.2f}; w_yes capped 3.0.
"""
ann = """### Cell 46 - EDA: H6 conditional (home sessions of Coinbase and Upbit)
**Sub-claim:** (Q8 stability) the venue lead exists when that venue is the price leader (its own trading day). **Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(46, "H6", "TRAIN", "search", "Binance bounce (entry delay + rev1/rev3 residual)", "session of the signal (US for Coinbase, ASIA for Upbit)", rule, ann)
