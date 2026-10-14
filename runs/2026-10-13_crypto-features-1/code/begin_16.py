import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
se = 0.012
pw = kit.power(se, 0.02, 1.96)
rule = f"""# cell 16 rule - H2: is the h24 continuation of closing strength a bull-regime impostor? (controls: market trend; conditional: trailing 30-day market trend, anchor session)
Feature: f54_roll (rolling-24h closing strength x (open/close)^5, fixed in cell 15), h = 24 (primary) and 6, 1 (reported). Conditioning at t (trailing only): market trend = EW-market 30-day log return (sum of 720 hourly returns ending at t) >0 (up) or <0 (down); the split is 'up' vs 'down' pooled over TRAIN.
Also reported: the same split by session of the anchor hour (ASIA 21-01, EU 07-11, US 13-16, other) and a split by fold. Variants: 2 trend states x 3 h + 4 sessions x 3 h + residual-on-r24 trend split (2 x 3) = 24 (V = 24).
Direction: positive (continuation) at h24.
Pre-stated primary (h24, one test): the continuation is NOT a bull-only impostor if the IC in the 'down' trend state is >= +0.02 with NW t >= 1.96. Impostor (refuted) if the down-state IC <= 0.01 and the up-state IC >= +0.02. Else INCONCLUSIVE.
Power: down state ~ 40% of hours (about 11,000 rows), h24 se ~0.0092; delta 0.02: power at tcrit 1.96 {kit.power(0.0092, 0.02, 1.96)['power']:.2f}, alpha {kit.power(0.0092, 0.02, 1.96)['alpha']:.4f}, w_yes -> 3.0, w_no {kit.power(0.0092, 0.02, 1.96)['w_no']:.2f}.
"""
ann = """### Cell 16 - EDA: H2 conditional split by market trend and session
**Sub-claim:** (Q2/Q8) the 2021H2 concentration (C1 +0.077) says the continuation may need an up-trending market.
**Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(16, "H2", "TRAIN", "search", "market trend (bull-regime impostor)", "trailing 30-day market trend (up/down) and anchor session", rule, ann)
