import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc = kit.tcrit_for(6)
rule = f"""# cell 15 rule - H2: Alpha#54 family, closing strength (controls: close-location alone, (open/close)^5 alone, same-window return; conditional: none)
Seed (sign as in TARGET.md, 'minus #54'): f54 = ((close - low)/(high - low)) * (open/close)^5 on (a) UTC-day OHLC at the 23:00 bar (sampling d) and (b) rolling 24h blocks ending at every hour (open = bar t-23 open, high/low = rolling 24h max/min; sampling h).
Rivals: clv = (close - low)/(high - low) alone; oc5 = (open/close)^5 alone; the 24h return r24' = +(log C_t - log C_(t-24)) (continuation sign, the same-window return) - each a variant. Residual form: f54 (rolling) residualised on the rank of r24' (3 variants).
Horizons 1h, 6h, 24h. Variants: f54 (2) + clv (2) + oc5 (2) + r24' (1) = 7 features x 3 h = 21, + 3 residual variants = 24. V = 24.
Direction (pre-stated, TARGET.md: closing strength continues): POSITIVE IC.
Pre-stated primary (the two f54 constructions x 3 horizons: V_primary = 6, tcrit {tc:.2f}): SUPPORTED if the best f54 variant has pooled-TRAIN IC >= +0.02 and NW t >= {tc:.2f}. Not supported otherwise (REFUTED if all six are <= 0 with the best t <= -1.65... significant negative).
The rival results are reported for attribution; the residual shows what f54 adds beyond the same-window return.
{fx.rule_power(24)}
"""
ann = """### Cell 15 - EDA: H2 does closing strength continue, and is it more than the day's return?
**Sub-claim:** (C5) f54 predicts at 1/6/24h; (Q3 impostor / Q4 attribution) CLV, (O/C)^5 and the day's return are the competing explanations.
**Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(15, "H2", "TRAIN", "search", "close-location alone, (open/close)^5 alone, same-window 24h return", "none", rule, ann)
