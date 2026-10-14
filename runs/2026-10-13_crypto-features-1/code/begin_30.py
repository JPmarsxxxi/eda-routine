import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc = kit.tcrit_for(24)
rule = f"""# cell 30 rule - H12: BTC / market lead-lag through beta (controls: none this cell; conditional: none)
Features (hourly, Binance closes; beta_i = trailing-720h beta of the coin's 1h return on BTC's (or on the EW-market's) 1h return, ending at t-1; the cross-sectional rank differs only through beta dispersion):
 lead_btc_k = beta_btc_i * (BTC log return over the last k hours), k = 1, 3, 6, 24; lead_mkt_k = beta_mkt_i * (EW-market log return over k hours), k = 1, 3, 6, 24. 8 features x h = 1, 6, 24 = 24 variants (V = 24).
Pre-stated direction (diffusion of market information to high-beta coins with a delay): POSITIVE IC (after a market rise high-beta coins keep rising). The reversal literature (cells 5-6: market-wide hourly reversal exists) argues the opposite; the sign is therefore a genuine test.
Pass rule: SUPPORTED if the best variant (pre-stated positive sign) has pooled-TRAIN IC >= +0.02 and NW t >= Sidak {tc:.2f}; wrong-signed significant results count as 'no'.
{fx.rule_power(24)}
"""
ann = """### Cell 30 - EDA: H12 do BTC / market moves transmit to high-beta coins with a delay?
**Sub-claim:** (C5) beta-weighted market move predicts the cross-section; (Q3 impostor) the sign could be the market reversal x beta already seen in cell 5 (raw vs market-residual reversal differed by 0.010 at h1).
**Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(30, "H12", "TRAIN", "search", "none", "none", rule, ann)
