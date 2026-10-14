weight_applied: 0.3997
variants: 24
suggests: H13

# cell 30 result - H12 beta x BTC / market move (TRAIN, hourly; 24 variants; cells/cell_30_table.csv, cells/cell_30_output.txt, plots/cell_30_lead.png)
Pre-committed branch: NOT SUPPORTED, and the pre-stated sign is REFUTED: every one of the 24 variants has a NEGATIVE pooled IC (best 'positive' variant lead_btc_1 h24 = -0.0042, t -1.8). weight_applied 0.400 (no-branch at power 0.60 for the best variant's se 0.0060, delta 0.02, tcrit 3.08).
The sign-flipped numbers are large and widespread: beta_mkt x EW-market move over the last k hours predicts a LOWER rank for high-beta coins: lead_mkt_1 h1 -0.0316 (t -12.8; EXPLORE -0.037, C1 -0.035, C2 -0.027, C3 -0.021), lead_mkt_3 h1 -0.0308, lead_mkt_6 h6 -0.0275 (t -6.9), lead_mkt_24 h24 -0.0343 (t -4.4; -0.037/-0.042/-0.016/-0.034); lead_btc_k is weaker (h1 -0.0198..-0.0212).
The market-wide EW move is more informative than BTC's alone (|IC| 0.03 vs 0.02). The sign pattern is the market-level reversal times beta (cell 5 saw it as the 0.010 gap between raw and market-residual reversal).
WARNING recorded before any reading as a signal: lead = beta_i x (market move) ranks the coins by beta whenever the market move has a persistent sign; with a positive average market drift over 2019-2021 the feature contains a fixed 'high-beta coins underperform' component (alts versus BTC/ETH after 2021).
The negative IC could be that fixed effect and not a reversal. The discriminating test is the sign of the IC separately for market-up and market-down states: a fixed effect gives IC of OPPOSITE signs in the two states (the ranking flips with the sign of the move), a reversal gives the SAME sign. Next cell (child hypothesis H13).
