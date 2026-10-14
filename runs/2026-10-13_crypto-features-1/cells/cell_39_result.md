weight_applied: 0.3333333333
variants: 20
suggests: none

# cell 39 result - H15 rival control: own 1-hour reversal (TRAIN, hourly; 20 variants; cells/cell_39_table.csv, cells/cell_39_output.txt, plots/cell_39_shape_resid.png)
Pre-committed branch: REFUTED. Every residual delayed-entry variant has |IC| < 0.01: body_n|rev1 h1 +0.0070 (t 3.2), clv1|rev1 h1 +0.0060 (2.7), vwap_dev|rev1 h1 -0.0027, upper_wick|rev1 -0.0024, lower_wick|rev1 +0.0010 (h6 all |IC| <= 0.0042). weight_applied 0.333 (power ~1, no-branch floor).
Once the hour's own reversal is removed the within-bar shape carries nothing tradable. The UNDELAYED residuals are large and are the pure last-print bounce beyond the return: vwap_dev|rev1 at h1 = -0.0419 (t -18.4; 4/4 folds, -0.057/-0.034/-0.018/-0.028), clv1|rev1 -0.0233, upper_wick|rev1 +0.0189 (all vanish with a one-bar delay).
This is the Roll/PIN picture of data-hygiene.md at the bar level: the print's position vs the bar VWAP is the bounce information, usable only by someone who can trade at the close print, which no later stage can.
No library feature from H15.
