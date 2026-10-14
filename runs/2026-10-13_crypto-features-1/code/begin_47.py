import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc = kit.tcrit_for(6)
rule = f"""# cell 47 rule - H13: is the h1 UP-state beta reversal just the Binance bounce? (controls: Binance bid-ask bounce via a one-bar entry delay; conditional: market-up state)
Feature: lead_mkt_k = beta_mkt_i x (EW-market log return over the last k hours), k = 1, 3, 6 (cell 31), restricted to market-UP signals (market return over the same k hours > 0), horizon h = 1 (and 6 reported). Scored (a) undelayed (cell 31 reference, IC about -0.05 at h1) and (b) with a one-bar entry delay (response from the end of bar t+1).
Also scored with the coin's own average of the feature removed (detrended minus trailing 720h mean) in the UP state, delayed. Variants: 3 k x 2 timings x 2 forms x h1 = 12, plus h6 delayed 3 = 15 -> V = 15 (reported h6 not in the primary).
Pre-stated primary (V_primary = 3, the delayed + detrended UP-state h1 IC for k = 1, 3, 6; tcrit {tc:.2f}): a real conditional reversal survives the entry delay: SUPPORTED if the best has IC <= -0.015 with NW t <= -{tc:.2f}; REFUTED if all three have |IC| < 0.01 (it was the bounce). Else INCONCLUSIVE.
Power: UP state ~52% of hours (14,000 rows), se(h1) ~0.0035; delta 0.015: power at tcrit {tc:.2f} {kit.power(0.0035, 0.015, tc)['power']:.2f}; w_yes capped 3.0; w_no {kit.power(0.0035, 0.015, tc)['w_no']:.2f}.
"""
ann = """### Cell 47 - EDA: H13 UP-state h1 beta reversal, delay control
**Sub-claim:** (Q3 impostor) the unresolved piece of cell 31: after market-UP hours high-beta coins fall in the next hour (-0.052). **Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(47, "H13", "TRAIN", "search", "Binance bid-ask bounce (one-bar entry delay)", "market-UP state", rule, ann)
