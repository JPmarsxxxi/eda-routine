# cell_03 RESULT — H3 CONFIRM opening

Script `scripts/cell_03_h3_confirm.py`; tables `tables/03_result.json`, `tables/03_by_quarter.csv`; plot `plots/03_h3_confirm.png`.
Slice: CONFIRM, n = 10,585 hourly rows.

**Branch fired: REFUTED.** Deciding number: partial Spearman (basis vs next-24h log RV | trailing 24h/7d/30d RV) = **+0.0099**
(block-bootstrap SE 0.034), below the 0.05 bar and far below the 0.0689 critical value. Raw Spearman is -0.005. EXPLORE had 0.15.

**Weight applied:** (1-power)/(1-alpha) = 0.228/0.95 = **0.240** (not capped). H3 odds 0.35/0.65 = 0.538 x 0.240 = 0.129 ->
**posterior 0.114**. State: OPEN (0.05 < 0.114 < 0.85).

Unweighted rivals / stability (reported, not scored):
- + log DVOL as an extra control: partial rho **0.054** (higher, not lower, so DVOL is not what explains the absence).
- + log trailing-24h perp volume as an extra control: 0.010 (unchanged).
- By quarter (decay-first): -0.079, +0.079, +0.085, -0.058, +0.029 (2022Q1..2023Q1): sign alternates, no quarter reaches the
  0.0689 bar with any consistency. The pattern is noise around zero, not a regime.

Refutation of H3's core sub-claim -> mandatory redirect cell next (cell_04).
