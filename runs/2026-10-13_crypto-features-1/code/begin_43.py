import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc = kit.tcrit_for(8)
rule = f"""# cell 43 rule - H16 rival control: the same-window return and the existing reversal features (controls: r3s, r24, r72 trailing returns and f001/f002 ranks; conditional: none)
Features: dd_72, madev_72, dd_168, dd_336 detrended (cell 42 winners), each residualised, per timestamp, on the cross-sectional ranks of r3s = -(log C[t-1]-log C[t-4]), r24 = -(log C[t]-log C[t-24]) and r72 = -(log C[t]-log C[t-72]) (the same-window return in reversal sign),
at h = 6 and 24 (4 features x 2 h = 8 variants, V = 8). Score = -IC for the drawdown-type signs as in cell 42.
Pre-stated primary: SUPPORTED if the best residual variant has pooled-TRAIN score >= +0.015 (incremental) with NW t >= {tc:.2f} and the same sign in C2 and C3; REFUTED if every residual variant has score < 0.01 (the drawdown was the return). Else INCONCLUSIVE.
Power: hourly h6 se 0.0044, h24 0.0060; delta 0.015: power {kit.power(0.0044, 0.015, tc)['power']:.2f} / {kit.power(0.0060, 0.015, tc)['power']:.2f} at tcrit {tc:.2f}; w_yes capped 3.0; w_no {kit.power(0.0044, 0.015, tc)['w_no']:.2f} (h6) / {kit.power(0.0060, 0.015, tc)['w_no']:.2f} (h24).
"""
ann = """### Cell 43 - EDA: H16 rival control (trailing returns)
**Sub-claim:** (Q3 impostor, Q4 attribution) the drawdown/MA-distance signal is the 24h-72h return in disguise. **Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(43, "H16", "TRAIN", "search", "same-window trailing returns r3s, r24, r72 (reversal features)", "none", rule, ann)
