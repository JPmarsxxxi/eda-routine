import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc = kit.tcrit_for(2)
rule = f"""# cell 45 rule - H10: does the participation-surprise sign depend on the session of the signal? (controls: none this cell; conditional: session of t, market trend, market volatility)
Feature: f003 (features/f003.py: 1-hour trade-count surprise residualised on the bar's return and |return|), scored at h6 and h24, by session of the signal hour t: ASIA 21-01, EU 07-11, US 13-16, other (4), by market trend up/down (2) and market volatility high/low (2) = 8 conditions x 2 h = 16 variants (V = 16).
Pre-stated primary (session contrast; h24; V_primary = 2 contrasts: ASIA vs other, US vs other; tcrit {tc:.2f}): the sign DEPENDS on the session if the paired-by-day difference IC(session) - IC(other) is <= -0.02 with NW t <= -{tc:.2f} for ASIA or US at h24 (cell 44 saw ASIA/US negative for the 6h-window surprises).
INCONCLUSIVE otherwise; REFUTED (sign does not depend on session) if both differences are within +-0.01.
Power: daily-collapsed paired differences, ~1,000 days, se ~0.012; delta 0.02: power at tcrit {tc:.2f} {kit.power(0.012, 0.02, tc)['power']:.2f}; w_yes capped 3.0; w_no {kit.power(0.012, 0.02, tc)['w_no']:.2f}.
"""
ann = """### Cell 45 - EDA: H10 conditional split (session / trend / market volatility)
**Sub-claim:** (Q8 stability, Q2 assumption) the participation surprise is not one effect; cell 44 found ASIA/US signs opposite to the pooled one. **Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(45, "H10", "TRAIN", "search", "none", "session of the signal, market trend, market volatility", rule, ann)
