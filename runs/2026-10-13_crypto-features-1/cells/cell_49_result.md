weight_applied: 0.3333333333
variants: 12
suggests: none

# cell 49 result - H13 static beta ranking versus the reversal part (TRAIN, hourly; 12 variants; cells/cell_49_table.csv, cells/cell_49_output.txt, plots/cell_49_beta.png)
Pre-committed branch: NOT SUPPORTED (not refuted). The reversal-only form g_rev = -beta x sign(last-6h market move), residualised on f001 and the market-residual reversal, has pooled-TRAIN IC +0.0128 at h1 (NW t 5.7) and +0.0131 at h6 (t 4.3; C2 +0.019, C3 +0.011): under the 0.015 bar, above the 0.01 refute line.
weight_applied 0.333 (no-branch at power 0.88, floor 1/3).
THE DECOMPOSITION: the static ranking s_static = -beta (every hour, no market gating) has IC +0.0234 at h1 (t 10.4) and +0.0400 at h6 (t 7.7) in all four folds (h6: +0.033 / +0.060 / +0.044 / +0.040), and by market state: UP +0.0409 (h1) / +0.0585 (h6) versus DOWN +0.0031 (h1, t 0.9) / +0.0186 (h6, t 2.8).
So most of the cell-47/48 effect is a state-independent 'low-beta coins outperform' component (BTC/ETH versus DOGE/SOL over 2019-2023) - the persistent coin attribute with 10 coins and ~4 years of luck-dominated mean returns - modulated in size by the market state. The time-varying beta (coin's beta minus its own 90-day mean) x market sign keeps nothing (h1 +0.0055 residualised, t 2.6; h6 +0.0027).
Not frozen and not registered: the static component is a fixed effect (same trap as the volatility and long/short levels, cells 11 and 29); the market-reversal component is +0.013 once the own-return reversal is removed, below min_useful. It is recorded as a lead: a low-beta tilt exists in this sample but cannot be separated from which coins were low-beta.
