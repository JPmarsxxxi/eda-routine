import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 38 result - H15 within-bar shape (TRAIN, hourly; 42 variants; cells/cell_38_table.csv, cells/cell_38_output.txt, plots/cell_38_barshape.png)
Pre-committed branch: SUPPORTED by the letter: best delayed-entry variant body (log C/O of the last bar) at h1: IC -0.0272 (NW t -11.1; EXPLORE -0.033, C1 +0.000, C2 -0.025, C3 -0.035), |IC| >= 0.02 and |t| >= Sidak 3.04. weight_applied 3.0 (cap).
IT IS NOT A NEW FEATURE: the mean cross-sectional rank correlation of body with the 1-hour reversal rank is -0.973 (body is the last hour's return), and body delayed-1 at h1 (-0.0272) equals the delay-1 1h reversal of cell 6 (+0.0272 with the opposite sign convention) to four digits. The rule did not include the own-reversal rival as a control; that is done next (cell 39).
Bounce share: undelayed body h1 -0.0831 (t -35) -> delayed -0.0272 (67% lost); clv1 -0.0598 -> -0.0089; vwap_dev -0.0864 -> -0.0165 (81% lost; t -6.8 after the delay); body_n -0.0655 -> -0.0136; upper_wick +0.0169 -> -0.0013; lower_wick -0.0063 -> +0.0050; gap -0.0026 -> +0.0015 (no content at any horizon).
So the within-bar shape is the last print's bounce plus the last hour's return; after the delay only body, vwap_dev and body_n keep |IC| 0.014-0.027 at h1, all strongly correlated with rev1. The undelayed ICs (up to -0.086 at h1) are exactly the Roll bounce that data-hygiene.md warns about.
"""
kit.result(38, 3.0, variants=42, suggests="none", body=body)
kit.attempt(38, "H15", "within-bar shape (7 features) x h x {undelayed, delay1}", "delayed body h1 -0.0272 t -11 but corr -0.97 with rev1: an impostor; gap has no content")
kit.write_beliefs(); print(kit.posterior("H15"))
