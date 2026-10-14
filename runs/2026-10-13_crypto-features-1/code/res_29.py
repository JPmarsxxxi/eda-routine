import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
pw = kit.power(0.0060, 0.02, kit.tcrit_for(36))
w, cap = kit.capped(pw["w_no"], "search")
body = f"""# cell 29 result - H11 risk-shape features (TRAIN, hourly; 48 variants; cells/cell_29_table.csv, cells/cell_29_output.txt, plots/cell_29_risk.png)
Pre-committed branch: NOT SUPPORTED. Best detrended one-sided variant: skew_168 at h24 score +0.0144 (NW t 1.58) vs bar 0.02 and Sidak {kit.tcrit_for(36):.2f}. weight_applied {w:.3f} (no-branch at power {pw['power']:.2f}, se 0.0060, delta 0.02).
THE FIXED-EFFECT TRAP, quantified: the LEVEL features have huge ICs with the pre-stated sign - rv_168 h24 -0.0843 (t -8.2), idio_168 h24 -0.0931 (t -9.6), max_168 -0.0715, rng_24 -0.0685, min_168 +0.0743 - positive in every fold. After subtracting the coin's own trailing-90-day mean they all collapse:
rv_168 -0.0068, rv_24 -0.0048, idio_168 -0.0139, max_168 -0.0111, rng_24 +0.0040 (wrong sign), min_168 -0.0087 at h24. So the apparent risk premium (high-vol coins underperformed: DOGE, SOL) was entirely which coins are volatile, not when a coin is volatile: a coin fixed effect on 10 coins over 4 years,
exactly what cell 11 found for the long/short ratio. No level feature is registered for that reason. Time variation of risk carries no IC beyond |0.0144|.
Exploratory (no weight): rng_24 detrended at h6 has the WRONG sign (+0.0180, t 3.8; EXPLORE +0.033, C1 +0.011, C2 -0.018, C3 +0.013: sign-unstable); rv_ratio and min_168 detrended |IC| <= 0.0154.
Consequences for the library: (1) risk-shape level features are fixed effects and excluded; (2) the within-coin detrend step used for f004 was necessary and is the right construction rule for slow variables (premium/basis/funding/OI/vol); (3) f003 (trailing-720h ratio) and the price-based features (f001, f002, f005, f006) do not carry a level.
"""
kit.result(29, w, variants=48, suggests="not pursued: rng_24 detrended h6 positive IC (+0.0180, t 3.8, wrong sign vs story, sign-unstable by fold, below min_useful)", body=body)
kit.attempt(29, "H11", "8 risk features x {level, detrended} x 3 h", "levels IC -0.07..-0.09 at h24 are coin fixed effects; detrended |IC| <= 0.0144: not supported")
kit.write_beliefs(); print(kit.posterior("H11"))
