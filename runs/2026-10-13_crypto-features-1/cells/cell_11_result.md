weight_applied: 3.0000
variants: 45
suggests: none

# cell 11 result - H5 rival controls: coin fixed effect and trailing-return reversal (TRAIN, hourly; 30 variants; cells/cell_11_table.csv, cells/cell_11_output.txt, plots/cell_11_h5_controls.png)
Pre-committed branch: SUPPORTED. Best form-(c) (detrended within coin on trailing 720h AND residualised on the ranks of r3s and r24): prem_lvl at h24 score +0.0250 (NW t 5.0; EXPLORE +0.029, C1 +0.018, C2 +0.020, C3 +0.025 - 4/4 folds), bars: score >= 0.02,
t >= Sidak 3.14, C2 and C3 negative IC: all met. weight_applied 3.0 (power high, capped).
Attribution - share of the raw IC kept (TRAIN): prem_lvl detrend 0.88/0.82/0.74 and detrend+resid 0.76/0.69/0.66 at h1/h6/h24 -> the premium effect is mostly NOT a coin fixed effect and NOT trailing-return reversal. Form (c) prem_lvl: h1 -0.0241 (t -10.9), h6 -0.0227 (t -7.3), h24 -0.0250 (t -5.0).
basis_lvl keeps 0.71/0.57/0.60: h24 -0.0201 (t 3.9; C2 -0.009, C3 -0.031), h6 -0.0151 (t 4.8). funding_lvl keeps 0.30/0.37/0.71: only h24 survives: -0.0199 (t -3.0, just under the Sidak bar 3.14; C1 -0.017, C2 -0.038, C3 -0.033) and loses its EXPLORE/C1 signal when detrended.
ls_acct_lvl was a coin fixed effect: raw h24 -0.0716 (t -5.0) -> detrended -0.0108 (t -0.7), residualised -0.0054, share 0.08-0.15: DEAD as a time-varying feature (the apparent IC came from which coins carry persistently high long ratios; mean returns of 10 coins are luck-dominated).
oi_val_chg_24: detrend keeps 0.97/0.70/0.76 but the trailing-return residual kills it (share 0.20 at h1, negative at h6): open-interest notional change is the price move (OI x price); DEAD.
Lead surviving the controls: the perp premium index level (de-meaned by the coin's own trailing 30-day mean) is a clean crowding feature at 1-24h, equal sign in all folds; basis_lvl is its weaker twin (premium and basis both measure perp vs spot).
The funding floor (OBSERVATIONS #7) may be why funding_lvl underperforms the premium: a clipped variable. Open: which conditional matters (market premium regime, time to funding settlement); the next H5 cell.
