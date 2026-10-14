weight_applied: 3.0000
variants: 18
suggests: none

# cell 47 result - H13 UP-state beta x market-move reversal with a one-bar entry delay (TRAIN, hourly; 15 variants; cells/cell_47_table.csv, cells/cell_47_output.txt, plots/cell_47_up_delay.png)
Pre-committed branch: SUPPORTED. Delayed (entry at the end of bar t+1) and detrended UP-state IC at h1: k=1 -0.0425 (NW t -12.7), k=3 -0.0375 (-11.4), k=6 -0.0386 (-11.9); bars IC <= -0.015 and t <= -2.64 (Sidak, V_primary = 3). weight_applied 3.0 (cap).
The bounce explains little of it: undelayed k=1 level -0.0524 -> delayed -0.0438 (84% kept) -> delayed and detrended -0.0425; folds (delayed, detrended, k=1): -0.041 / -0.057 / -0.045 / -0.033 (4/4 strongly negative). At h6 (delayed, detrended) the UP-state IC is LARGER: k=1 -0.0496, k=3 -0.0529, k=6 -0.0531 (t -8.6 to -9.0; folds -0.041..-0.074).
So after the equal-weight market rose over the last 1-6 hours, high-beta coins (ranked by trailing-720h beta) underperform the low-beta coins over the next 1-6 hours, in all four folds. Combined with cell 31 (DOWN-state IC at h6 is +0.0135, not a symmetric mirror) this is a state-dependent beta effect with a reversal component, not the pure fixed effect that cell 31 diagnosed for the all-state product.
Caveat that decides what it is worth: within the UP state the cross-sectional ranking of lead_mkt_k is simply the ranking of beta (the market move is one scalar per timestamp), so the feature is 'minus beta, defined only when the market has just risen'. It overlaps the market component of the plain own-return reversal (f001 / f002 rank coins by -r_i = -(beta_i m + idiosyncratic)); whether it adds anything beyond f001/f002 is the orthogonality question of the next H13 cell.
