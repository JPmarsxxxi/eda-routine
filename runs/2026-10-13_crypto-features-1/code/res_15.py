import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 15 result - H2 Alpha#54 family (TRAIN; 24 variants; cells/cell_15_table.csv, cells/cell_15_output.txt, plots/cell_15_f54.png)
Pre-committed branch: SUPPORTED. Best f54 variant: rolling-24h (any-hour) f54 at h24: IC +0.0287 (NW t +4.7; EXPLORE +0.016, C1 +0.077, C2 +0.026, C3 +0.026), Sidak bar 2.64 for 6 variants, size bar 0.02. weight_applied 3.0 (cap; power 0.76 at delta 0.02, se 0.0060).
The daily-anchor f54 at h24 is +0.0247 (t 2.0; C1 +0.100): below the bar. HONEST SHAPE: the sign flips with the horizon - f54_roll is NEGATIVE at h1 (-0.0350, t -15.5, 4/4 folds) and h6 (-0.0211, t -5.0), POSITIVE only at h24. At h1/h6 f54 behaves like the continuation of strength
being punished next hour (reversal): it is mostly the same reversal as H3 in another coat (r24_cont h1 -0.0368; clv_roll h1 -0.0481, the strongest). Only the h24 continuation is H2's claim; and ~60% of that h24 IC is the C1 fold (2021H2): the per-fold h24 ICs are +0.016 (t 1.9) / +0.077 (5.1) / +0.026 (1.6) / +0.026 (1.8): positive in all four,
large in one. A confirm cell would find one clearly supported fold (C1) at the 0.02/1.96 bars.
Attribution: CLV alone has the same h1/h6 reversal (-0.048/-0.030) and weaker h24 (+0.015, t 2.3): the (open/close)^5 factor ADDS at h24 (f54 +0.0287 vs clv +0.0154); (open/close)^5 alone is the reversal-signed 24h move: oc5_daily h6 +0.0743 (t 6.3) is the r24 reversal (corr identical to cell 2/4), oc5_roll h1 +0.0365.
Residualised on the 24h return rank: f54_roll|r24 h24 +0.0293 (t 5.3; +0.021/+0.084/+0.013/+0.019): not the same-window return; h1 -0.0332 (reversal of strength survives r24: it is the close-location part). Market exposure: corr(cross-coin mean feature z, EW market fwd return) +0.01.
Reading: H2's real content is a 24h continuation of closing strength concentrated in 2021H2 (bull), with an offsetting 1-6h reversal that belongs to H3/H9. Next H2 cell: is the h24 continuation a bull-regime impostor (conditional on the trailing market trend)?
"""
kit.result(15, 3.0, variants=24, suggests="not pursued: h1/h6 negative IC of f54/clv (it is the H3 reversal in another coat: corr with rev features checked at the freeze/orthogonality stage)", body=body)
kit.attempt(15, "H2", "f54 daily/rolling, clv, oc5, r24 x h(3) + residual on r24", "f54_roll h24 +0.029 t 4.7 supported but C1-driven; h1/h6 negative (reversal)")
kit.write_beliefs(); print(kit.posterior("H2"))
