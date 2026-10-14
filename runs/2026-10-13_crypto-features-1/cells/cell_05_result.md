weight_applied: 3.0000
variants: 108
suggests: not pursued: k=48 h24 bump (t 1.9, below the Sidak bar 3.50); bounce rival is controlled in the next H3 cell

# cell 05 result - H3 lookback x scaling sweep of the cross-sectional reversal (TRAIN, hourly sampling, 108 variants; cells/cell_05_table.csv, cells/cell_05_output.txt, plots/cell_05_reversal_profile.png)
Pre-committed branch: SUPPORTED. Best: raw 2-hour reversal at h1: IC +0.0842 (NW t +35.6; EXPLORE +0.106, C1 +0.061, C2 +0.062, C3 +0.065), Sidak bar 3.50, size bar 0.02. Power ~1.0 (se 0.0026); w_yes capped -> weight_applied 3.0.
Profile (TRAIN IC, raw): h1: k1 +0.083, k2 +0.084, k3 +0.082, k6 +0.065, k12 +0.050, k24 +0.037, k48 +0.019, k72 +0.016, k168 +0.009. h6: k1 +0.048, k2 +0.056, k3 +0.058 (peak), k6 +0.054, k12 +0.040, k24 +0.032, k48 +0.017, k72 +0.012, k168 +0.005.
h24: k2 +0.023 (peak), k3 +0.022, k1 +0.017, all others <= 0.016, k168 -0.001. So the reversal decays smoothly with lookback and with horizon (h1 0.084 > h6 0.058 > h24 0.023): it is a 1-6 hour phenomenon with 1-3 hour lookbacks. No momentum (k168 h24 -0.010 for the residual versions, t -1.1: not significant).
Transforms: RAW rank is the best at every k and h; volatility scaling LOWERS the IC (k2 h1: 0.084 -> 0.070) and beta-residualising lowers it too (-> 0.074; mres_vs 0.0735). So (a) vol-scaling is not a feature here; (b) part of the raw IC (0.010 at h1 k2) is the market-reversal x beta component and
the idiosyncratic residual keeps most of it (88%) at +0.074. Fold stability (raw k2 h1): 0.106 / 0.061 / 0.062 / 0.065 - level drops from EXPLORE to C1 and then is stable; k3 h6: 0.068 / 0.033 / 0.061 / 0.052.
FLAG (to be controlled in the next H3 cell, not reported as a finding yet): EXPLORE and C1 score against the primary price = the Binance print itself, the same print that sets the feature's last point; a 1h-2h reversal at IC 0.1 in a pure-print response is the signature of bid-ask bounce (Roll 1984; data-hygiene.md). The drop to ~0.06 in C2/C3
(response = FTMO mid for 7 of 9 coins) is in the direction a bounce component would produce. The cell does not separate bounce from true reversal.
Leads: the lookback-48 uptick at h24 (+0.016 vs +0.011 at k24, t 1.9) is below the Sidak bar (3.50): not pursued. The bounce question is the next H3 cell (controls rival).
