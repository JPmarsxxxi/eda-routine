import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
se = fx.NOISE["d_6"]["c"]/(1170**.5); tc = kit.tcrit_for(2); pw = kit.power(se, 0.02, tc)
rule = f"""# cell 04 rule - H8: session-conditional 24h reversal (controls: none this cell; conditional: anchor session)
Looked at: feature r24 = -(log C_t - log C_{{t-24}}) (reversal direction: past loser ranks high), a rolling 24h trailing return evaluated at EVERY hour (anchor a = 0..23), scored on h = 1, 6, 24 (24 x 3 = 72 variants).
Session groups, collapsed to one daily series by averaging the anchor ICs of the group within each UTC day: ASIA-NIGHT anchors {{21,22,23,0,1}} and US anchors {{13,14,15,16}} (6 group variants). V = 78.
Tool: xs_ic per timestamp, NW t on the daily series (lags h//24+3).
Pre-stated primary test (h6 only, two sides -> tcrit {tc:.2f}): SUPPORTED if IC(ASIA-NIGHT, h6) >= +0.02 with NW t >= {tc:.2f} AND IC(US, h6) <= -0.02 with t <= -{tc:.2f} (reversal overnight, continuation in US hours).
REFUTED if IC(ASIA-NIGHT) <= 0 with t <= -1.65. Else INCONCLUSIVE. (Both sides were glimpsed in cell 2 for the streak, not for r24 at the US anchors.)
Power: daily-sampled h6, N ~ 1170 days, se {se:.4f}; delta 0.02, tcrit {tc:.2f}: power {pw['power']:.2f}, alpha {pw['alpha']:.4f}, w_yes {pw['w_yes']:.1f} -> 3.00, w_no {pw['w_no']:.2f}.
"""
ann = """### Cell 04 - EDA: H8 does the sign of the 24h-return IC depend on the session?
**Sub-claim:** reversal in the 21-01 UTC anchors (next 6h = Asia hours) and continuation in the 13-16 UTC anchors. **Why:** if the profile is flat the cell-2 anchor result was the streak construction only.
**Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(4, "H8", "TRAIN", "search", "none", "anchor session (Asia-night vs US) - time-of-day conditional", rule, ann)
