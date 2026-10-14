hypothesis: H16
slice: TRAIN
kind: search
controls: same-window trailing returns r3s, r24, r72 (reversal features)
conditional: none

# cell 43 rule - H16 rival control: the same-window return and the existing reversal features (controls: r3s, r24, r72 trailing returns and f001/f002 ranks; conditional: none)
Features: dd_72, madev_72, dd_168, dd_336 detrended (cell 42 winners), each residualised, per timestamp, on the cross-sectional ranks of r3s = -(log C[t-1]-log C[t-4]), r24 = -(log C[t]-log C[t-24]) and r72 = -(log C[t]-log C[t-72]) (the same-window return in reversal sign),
at h = 6 and 24 (4 features x 2 h = 8 variants, V = 8). Score = -IC for the drawdown-type signs as in cell 42.
Pre-stated primary: SUPPORTED if the best residual variant has pooled-TRAIN score >= +0.015 (incremental) with NW t >= 2.73 and the same sign in C2 and C3; REFUTED if every residual variant has score < 0.01 (the drawdown was the return). Else INCONCLUSIVE.
Power: hourly h6 se 0.0044, h24 0.0060; delta 0.015: power 0.75 / 0.41 at tcrit 2.73; w_yes capped 3.0; w_no 0.25 (h6) / 0.59 (h24).
