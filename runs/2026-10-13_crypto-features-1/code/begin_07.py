import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc2 = kit.tcrit_for(2)
rule = f"""# cell 07 rule - H3: where is the (bounce-free) reversal stronger? (controls: none; conditional: market-volatility regime, session, own-volatility)
Feature (fixed before looking, from cell 6): rev3s = -(log C_(t-1) - log C_(t-4)), the 3-hour reversal with the last print skipped (bounce-free), Binance closes; and rev24s = -(log C_(t-1) - log C_(t-25)).
Scored on h = 1, 6, 24 (primary forward return, entry at the end of bar t). Conditioning variables, all trailing / point-in-time at t:
 (1) market-vol regime: trailing 168h std of the EW-market 1h return, tercile within TRAIN (cut points from EXPLORE only, applied everywhere);
 (2) session of the anchor hour t: ASIA 21-01, EU 07-11, US 13-16, other;
 (3) own-volatility: coin's trailing-168h vol above/below the cross-sectional median at t (within-cross-section split: IC computed within the top-half-vol and bottom-half-vol coins, >= 3 coins each... with <= 10 coins we need >= 4 per half, hours with fewer are skipped);
 (4) recent market move: EW-market return of the last 3 hours down (< -0.5%) / up (> +0.5%) / flat.
Variants: 2 features x 3 h x (3 + 4 + 2 + 3 = 12 conditional cells) = 72 (V = 72).
Pre-stated primary test (H3, h6 and h1, rev3s only: V_primary = 2, tcrit {tc2:.2f}): reversal is STRONGER in the high-market-vol tercile than in the low: SUPPORTED if IC(high) - IC(low) >= +0.01 (paired by day, NW t >= {tc2:.2f}) for at least one of h1/h6.
REFUTED if the difference <= 0 with t <= -1.65 at both. Else INCONCLUSIVE. Everything else in the table is reported, flagged as exploratory (no belief weight).
Power: paired daily difference of tercile ICs, se ~ 0.010 at h6 (N ~ 380 days per tercile pair...); delta 0.01: power ~0.11, alpha 0.0125 -> w_yes capped 3; w_no ~0.90.
"""
ann = """### Cell 07 - EDA: H3 conditional split (regime, session, own-vol, recent market move)
**Sub-claim:** the bounce-free reversal is a liquidity-overshoot effect and should be larger when volatility is high or after a big market move; session amplitude from cell 4.
**Why it matters:** gives the conditioning set a combiner can use and the effort floor's conditional split. **Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(7, "H3", "TRAIN", "search", "none", "market-volatility regime, session, own-volatility, recent market move", rule, ann)
