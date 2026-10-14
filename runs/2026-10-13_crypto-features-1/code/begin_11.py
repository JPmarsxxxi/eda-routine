import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc = kit.tcrit_for(24)
rule = f"""# cell 11 rule - H5: persistent coin attribute and trailing-return rivals (controls: coin fixed effect; trailing returns r3s and r24; conditional: none)
Features: the five H5 survivors of cell 10 - prem_lvl, basis_lvl, funding_lvl, ls_acct_lvl, oi_val_chg_24 - each in three forms:
 (a) raw level (cell 10 reference, not recounted);
 (b) within-coin detrended: x_t minus the coin's own trailing-720h mean of x (ending at t-1) - removes the persistent coin level, keeps time variation;
 (c) detrended AND residualised, per timestamp, on the cross-sectional ranks of the bounce-free 3h reversal r3s = -(log C_(t-1) - log C_(t-4)) and the 24h reversal r24 (so what is left cannot be trailing-return reversal re-expressed).
Scored at h = 1, 6, 24, hourly sampling. Variants: 5 features x 2 forms (b, c) x 3 h = 30 -> V = 30 (cell-10 raw forms not recounted). Pass direction: crowding sign negative, score = -IC.
Pass rule: SUPPORTED if the best form-(c) variant has pooled-TRAIN score >= +0.02 and NW t >= Sidak {kit.tcrit_for(30):.2f}, with the same sign in C2 and C3. REFUTED if every form-(c) variant has score <= 0.01. Else INCONCLUSIVE.
Reported: share of the raw IC kept by (b) and (c) per feature (attribution to the fixed effect and to trailing returns).
Power: hourly sample, h24 se 0.0060 (ls_acct/oi: coverage ~9-10k rows -> se 0.010), delta 0.02, tcrit {kit.tcrit_for(30):.2f}: power {kit.power(0.0060, 0.02, kit.tcrit_for(30))['power']:.2f} (h24, full sample) / {kit.power(0.010, 0.02, kit.tcrit_for(30))['power']:.2f} (limited coverage); w_yes -> 3.0; w_no {kit.power(0.0060, 0.02, kit.tcrit_for(30))['w_no']:.2f} / {kit.power(0.010, 0.02, kit.tcrit_for(30))['w_no']:.2f}.
"""
ann = """### Cell 11 - EDA: H5 rival controls (coin fixed effect; trailing returns)
**Sub-claim:** (Q3 impostor, Q4 attribution) is the positioning IC more than a persistent coin attribute or trailing-return reversal? **Why it matters:** premium/basis/funding are slow variables; with 10 coins a fixed effect is easy to mistake for a signal.
**Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(11, "H5", "TRAIN", "search", "coin fixed effect (persistent level) and trailing-return reversal (r3s, r24)", "none", rule, ann)
