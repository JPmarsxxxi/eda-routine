weight_applied: 0.3333333333
variants: 48
suggests: none

# cell 50 result - H17 perp aggressive flow and derivatives intensity (TRAIN, hourly; 48 variants; cells/cell_50_table.csv, cells/cell_50_output.txt, plots/cell_50_perpflow.png)
Pre-committed branch: NOT SUPPORTED. Best form-(b) variant (detrended, residualised on the same-window return and |return|): pgap_6 (perp minus spot 6h taker imbalance) at h6: IC -0.0132 (NW t -3.6; folds -0.011 / -0.028 / -0.024 / -0.000), under the 0.02 bar; Sidak 3.28. weight_applied 0.333 (power 0.90, floor 1/3).
Perp taker imbalance behaves exactly like the spot one (cell 9): ptaker_1 detrended h1 -0.0308 (t -13.9) is the bounce - residualised on the 1h return it is -0.0089 (t -4.1) and zero by h6 (-0.0015); ptaker_6 -0.0186 -> -0.0013; ptaker_24 ~0. The perp-versus-spot gap and the perp share of dollar volume (pshare h6 -0.0161 detrended -> -0.0125 residual, C2-heavy: C1 -0.015, C2 -0.031, C3 -0.013)
and the perp trade-count surprise (pnsurp_6 h24 +0.0106, sign flips between C2 -0.040 and C3 +0.029) carry no stable IC; nothing reaches 0.02 in the residual form.
So derivatives activity beyond the premium/funding level (f004, f009) adds no feature in this panel; the premium itself already carries the leveraged-crowding information. No library feature from H17.
