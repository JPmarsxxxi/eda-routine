import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
tc = kit.tcrit_for(24)
pw = kit.power(0.0060, 0.02, tc)
w, cap = kit.capped(pw["w_no"], "search")
body = f"""# cell 30 result - H12 beta x BTC / market move (TRAIN, hourly; 24 variants; cells/cell_30_table.csv, cells/cell_30_output.txt, plots/cell_30_lead.png)
Pre-committed branch: NOT SUPPORTED, and the pre-stated sign is REFUTED: every one of the 24 variants has a NEGATIVE pooled IC (best 'positive' variant lead_btc_1 h24 = -0.0042, t -1.8). weight_applied {w:.3f} (no-branch at power {pw['power']:.2f} for the best variant's se 0.0060, delta 0.02, tcrit {tc:.2f}).
The sign-flipped numbers are large and widespread: beta_mkt x EW-market move over the last k hours predicts a LOWER rank for high-beta coins: lead_mkt_1 h1 -0.0316 (t -12.8; EXPLORE -0.037, C1 -0.035, C2 -0.027, C3 -0.021), lead_mkt_3 h1 -0.0308, lead_mkt_6 h6 -0.0275 (t -6.9), lead_mkt_24 h24 -0.0343 (t -4.4; -0.037/-0.042/-0.016/-0.034); lead_btc_k is weaker (h1 -0.0198..-0.0212).
The market-wide EW move is more informative than BTC's alone (|IC| 0.03 vs 0.02). The sign pattern is the market-level reversal times beta (cell 5 saw it as the 0.010 gap between raw and market-residual reversal).
WARNING recorded before any reading as a signal: lead = beta_i x (market move) ranks the coins by beta whenever the market move has a persistent sign; with a positive average market drift over 2019-2021 the feature contains a fixed 'high-beta coins underperform' component (alts versus BTC/ETH after 2021).
The negative IC could be that fixed effect and not a reversal. The discriminating test is the sign of the IC separately for market-up and market-down states: a fixed effect gives IC of OPPOSITE signs in the two states (the ranking flips with the sign of the move), a reversal gives the SAME sign. Next cell (child hypothesis H13).
"""
kit.result(30, w, variants=24, suggests="H13", body=body)
kit.add_h("H13", "Beta-weighted market reversal: after a market-wide move over the last k hours, high-beta coins give back more (the sign-flipped H12)", "H12",
  "cells/cell_30_result.md (lead_mkt_1 h1 -0.0316 t -12.8; all 24 variants negative)",
  "Is the negative IC of beta x market move a reversal (same sign after up and after down moves) or the fixed effect 'high-beta coins underperformed' (opposite signs in the two states)?",
  "a change in the product of a coin's trailing beta and the last k-hour equal-weight market return predicts the cross-sectional rank of its next 1h/6h/24h primary return NEGATIVELY in both market-up and market-down states because market-wide moves overshoot and high-beta coins overshoot most",
  "an IC of opposite sign in the market-up and market-down states (a fixed effect); an IC that is concentrated in one state; an IC that vanishes when the coin's own average of the feature is removed",
  "coin fixed effect in beta (high-beta alts underperformed BTC/ETH over 2021-2023); the market reversal itself (a market-timing, not a cross-sectional, effect); the response switch",
  "EXPLORE cell_30", 0.40,
  "cell_30: lead_mkt_k negative IC in all 12 mkt variants, 4/4 folds in lead_mkt_1 h1 (-0.037/-0.035/-0.027/-0.021) but fixed-effect rival unresolved: base 0.30 x2 for consistent sign, x0.67 for the unresolved rival -> 0.40")
kit.attempt(30, "H12", "beta x BTC / EW market move (k=1,3,6,24) x h(3)", "all 24 variants NEGATIVE (refutes diffusion sign); fixed-effect vs reversal unresolved -> H13")
kit.write_beliefs(); print(kit.posterior("H12"), kit.posterior("H13"))
