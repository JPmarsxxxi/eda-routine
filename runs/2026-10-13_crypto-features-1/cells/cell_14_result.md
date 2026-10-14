weight_applied: 0.3333333333
variants: 30
suggests: not pursued: Upbit gap residual at h6 (+0.0137, t 2.6, below min_useful 0.02 and the Sidak bar; C2 ~0)

# cell 14 result - H6 rival control: Binance bounce / own-coin reversal (TRAIN, hourly, min_n 5; 30 variants; cells/cell_14_table.csv, cells/cell_14_output.txt, plots/cell_14_h6_controls.png)
Pre-committed branch: NOT SUPPORTED (inconclusive). The best form-(c) variant (entry delay 1 + residualised on rev1 and rev3 ranks) is ub_gap_lvl at h6: IC +0.0137 (NW t 2.6 < Sidak 2.81; C1 +0.011, C2 +0.000, C3 +0.024); bar was IC >= 0.02. Not refuted either (IC > 0.01 for it).
weight_applied 0.333 (no-branch weight at power 0.95, delta 0.02, se 0.0045).
Attribution - share of the base IC kept by the entry delay / by delay+residual: cb_gap_lvl h1 0.39/0.10, h6 0.45/0.30; ub_gap_lvl h1 0.32/0.14, h6 0.59/0.39; cb_retdiff_3 0.25/0.16 (h1), 0.19/0.29 (h6); ub_retdiff_3 0.24/-0.13 (h1), 0.37/-0.11 (h6); ub_retdiff_6 0.27/0.13 (h1), 0.39/0.41 (h6).
So 60-90% of the venue-gap IC at h1 was the Binance print's own bounce (the feature contains -log C_Binance); at h6 the Upbit gap level keeps 59% after the delay (+0.0210, t 4.1; C3 +0.033, C1 +0.024, C2 +0.009) and 39% after residualising on rev1/rev3 (+0.0137, t 2.6) and
ub_retdiff_6 keeps 0.41 (+0.0093, t 2.1). Coinbase gaps keep little (cb_gap_lvl h6 delay1 +0.0109, resid +0.0073, t 2.0).
Verdict: no venue feature clears the bar once the Binance bounce is controlled. A weak 6-hour Upbit-premium residual (~+0.014, t 2.6, C3-only) is left; it is below min_useful, so no library feature from H6 yet. Coverage caveat: Upbit has 4.8 coins per timestamp on average, which limits ranks.
