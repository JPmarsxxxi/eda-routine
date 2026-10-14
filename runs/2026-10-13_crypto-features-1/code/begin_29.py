import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
H = kit
tc = kit.tcrit_for(48)
rule = f"""# cell 29 rule - H11: volatility, extreme-return and risk-shape features (controls: coin fixed effect via within-coin detrending; conditional: none)
Features (hourly, Binance closes, trailing-only; r = 1h log return; all cross-sectionally ranked in the IC):
 rv_168 = std of r over 168h; rv_24 = std over 24h; rv_ratio = log(rv_24/rv_168); max_168 = max r over 168h; min_168 = min r over 168h; skew_168 = skewness of r over 168h; rng_24 = (max high - min low over 24h)/close;
 idio_168 = std over 168h of the residual of r on the EW-market return (trailing-720h beta).
Forms: (a) level; (b) within-coin detrended: level minus the coin's own trailing 2160h (90 day) mean ending at t-1 (kills the persistent coin level, the lesson of cell 11).
Horizons 1h, 6h, 24h. 8 features x 2 forms x 3 h = 48 variants (V = 48).
Pre-stated direction (risk-premium / lottery stories): NEGATIVE IC for rv_168, rv_24, max_168, skew_168, rng_24, idio_168 (high risk -> lower return). rv_ratio and min_168 have no pre-stated direction: they are reported two-sided, exploratory, and are not part of the primary family.
Pass rule (primary family = the 6 one-sided features, forms (a) and (b), 3 horizons: V_primary = 36, tcrit {kit.tcrit_for(36):.2f}): SUPPORTED if the best DETRENDED (b) one-sided variant has pooled-TRAIN score (= -IC) >= +0.02 and NW t >= {kit.tcrit_for(36):.2f}.
Not supported otherwise; wrong-signed significant results count as 'no'. Level (a) results are reported to show how much is a coin fixed effect.
{fx.rule_power(48)}
"""
ann = """### Cell 29 - EDA: H11 do volatility / lottery / risk-shape features rank the cross-section?
**Sub-claim:** (C5) high recent risk predicts lower returns; (Q3 impostor) persistent coin level (fixed effect) is the main rival - controlled by detrending in the same cell.
**Why it matters:** the standard cross-sectional risk anomalies are absent from the library; a family check at one stroke. **Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(29, "H11", "TRAIN", "search", "coin fixed effect (persistent volatility level)", "none", rule, ann)
