import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 43 result - H16 rival control: trailing returns (TRAIN, hourly; 8 variants; cells/cell_43_table.csv, cells/cell_43_output.txt, plots/cell_43_range_resid.png)
Pre-committed branch: SUPPORTED (incremental). Best residual variant: dd_336 (log of the close over its trailing 14-day maximum close, detrended, then residualised on the ranks of r3s, r24, r72) at h24: score +0.0220 (NW t +2.94; EXPLORE +0.0245, C1 +0.0104, C2 +0.0301, C3 +0.0198),
bars: score >= 0.015, t >= Sidak 2.73, same sign in C2 and C3. weight_applied 3.0 (cap).
How much was the return: dd_72 detrended at h6 drops from +0.0317 to +0.0159 after the residualisation (50% kept; t 4.2), madev_72 h6 from +0.0261 to +0.0101 (39%), dd_168 h6 +0.0250 -> +0.0139, dd_336 h6 +0.0252 -> +0.0161 (64% kept; t 4.0). The longer the window the more survives (dd_336 keeps 84% of its h24 IC: +0.0262 -> +0.0220).
mean XS correlations of the 72h drawdown (detrended) with r3s -0.20, r24 -0.48, r72 -0.40 (the drawdown is a reversal-signed return).
What is left is a slow piece: the depth below the 14-day high beyond what the last 3/24/72 hours explain, worth ~0.016 at h6 and ~0.022 at h24. It is a pooled-sample signal: the per-fold se of an hourly h24 IC is about 0.017, so no single fold can show t >= 1.96 at +0.022 (fold values +0.010/+0.030/+0.020, t 0.6-1.4).
Not frozen (a candidate is judged per fold at 0.02 / t 1.96 and would be CONFIRM-FAIL on power, not on content); recorded as a lead in REPORT.md. Fixed-effect and reversal rivals are now both controlled (cells 42-43).
"""
kit.result(43, 3.0, variants=8, suggests="not pursued: dd_336 incremental piece (+0.022 at h24, t 2.9) is not frozen: per-fold se ~0.017 means no fold can reach t 1.96; listed as a lead in REPORT.md", body=body)
kit.attempt(43, "H16", "dd/madev detrended, raw vs residual on r3s,r24,r72, h6/h24", "dd_336 h24 residual +0.0220 t 2.9: supported incremental; not frozen (power)")
kit.write_beliefs(); print(kit.posterior("H16"))
