import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc = kit.tcrit_for(108)
rule = f"""# cell 05 rule - H3: lookback x scaling sweep of the cross-sectional reversal (controls: none this cell; conditional: none)
Looked at: reversal feature -(log C_t - log C_{{t-k}}) on Binance closes (trailing, knowable at the end of bar t), k in 1,2,3,6,12,24,48,72,168 hours, four transforms: raw; vol-scaled (divided by the coin's trailing
168h std of 1h returns); market-residual (minus trailing-720h beta x equal-weight-market return over the same k hours); market-residual and vol-scaled. Horizons 1h, 6h, 24h. 9 x 4 x 3 = 108 variants (V = 108).
Hourly sampling (all hours), cross-sectional Spearman IC vs primary forward return, NW t (lags h+5). Slice TRAIN with per-slice report. Direction pre-stated: positive IC (past loser outperforms).
Pass rule: SUPPORTED if the best of the 108 variants has pooled-TRAIN IC >= +0.02 and NW t >= Sidak {tc:.2f}. Not supported otherwise. Lookback profile (the k at which IC peaks) is reported for each transform and horizon.
{fx.rule_power(108)}
"""
ann = """### Cell 05 - EDA: H3 where in lookback x scaling space does the cross-sectional reversal live?
**Sub-claim:** reversal exists and its profile over k (1h..168h) and transforms. **Why:** the family sweep defines which transforms/lookbacks to freeze; a flat profile would mean no feature. Hourly sampling = power (se 0.003-0.006).
**Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(5, "H3", "TRAIN", "search", "none", "none", rule, ann)
