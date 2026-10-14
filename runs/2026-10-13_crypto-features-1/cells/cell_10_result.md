weight_applied: 3.0000
variants: 39
suggests: not pursued: ls_chg_24, ls_top_lvl, funding_chg_24, basis_chg_6, oi_chg_24 beyond h1 (unstable sign or too thin coverage); rival controls follow in the next H5 cell

# cell 10 result - H5 perp positioning (TRAIN, hourly; 39 variants; cells/cell_10_table.csv, cells/cell_10_output.txt, plots/cell_10_positioning.png)
Pre-committed branch: SUPPORTED (11 variants pass: pooled score >= 0.02, NW t >= Sidak 3.22, same sign in C2 and C3). The crowding sign (higher premium/funding/basis/long-short -> lower return) holds:
 prem_lvl (premium-index close): h1 -0.0315 (t -14.2; EXPLORE -0.036, C1 -0.029, C2 -0.035, C3 -0.023), h6 -0.0329 (t -9.4; -0.039/-0.032/-0.030/-0.023), h24 -0.0378 (t -6.5; -0.046/-0.043/-0.016/-0.029): all folds same sign, all four folds.
 basis_lvl (perp kline close / spot close - 1): h6 -0.0265 (t -7.4), h24 -0.0335 (t -5.5), weaker in C3 (-0.009/-0.018). funding_lvl (settled, pinned floor): h6 -0.0205 (t -4.6), h24 -0.0279 (t -3.7; -0.011/-0.069/-0.039/-0.030).
 ls_acct_lvl (long/short accounts ratio): h24 -0.0716 (t -5.0; C1 -0.039, C2 -0.063, C3 -0.082) and h6 -0.0251 (t -3.3): the largest IC in the cell, but coverage is only C1 end + C2 + C3 (8,850 hourly rows).
 oi_val_chg_24 h1 -0.0236 (t -7.0), oi_chg_6 h1 -0.0154. taker_ls_lvl is NEGATIVE at h1 (-0.0172 t -4.4; wrong sign for the pre-stated positive): the same bounce face as taker_1.
Power: weight_applied 3.0 (w_yes capped).
CAUTION recorded, not resolved here: premium, basis and funding are slow, persistent coin attributes (OBSERVATIONS #8) and follow the trailing return, so (a) they may carry a coin fixed effect (a coin that always trades at a high premium also tended to underperform in this sample - 10 coins, 4 years, mean returns are mostly luck)
and (b) they may be trailing-return reversal re-expressed. Both are rivals; the next H5 cell controls them (de-meaned within coin on a trailing window; residualised on trailing return ranks).
Weak / unstable (not pursued): funding_chg_24, basis_chg_6, oi_chg_24 beyond h1 (|IC| < 0.01-0.016, t < 2.8 or sign flips); ls_chg_24 wrong-signed at h1 (+0.010, t 3.0) and unstable at h24 (C1 -0.063, C2 -0.021); ls_top_lvl (top-trader ratio) covers only 671 C2 hours and 2,157 C3 hours (missing for most coins), IC sign flips between C2 (+0.041) and C3 (-0.044/-0.104): too thin.
