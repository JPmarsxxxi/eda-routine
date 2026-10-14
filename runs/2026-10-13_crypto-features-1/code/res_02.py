import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 02 result - H7 anchor-hour dependence of the streak fade (TRAIN; 90 variants: 72 anchor x horizon + 15 streak-length + 3 residual control)
Pre-stated primary (h6): IC(streak-3, anchor 23) = +0.0441 (t +3.6); paired difference vs the mean of the other 23 anchors = +0.0376 (NW t +3.01) -> SUPPORTED (both bars: IC >= 0.02; diff >= 0.02 with t >= 1.96).
Power at delta 0.02: se 0.0133, power 0.32, w_yes 12.9 -> weight_applied 3.0 (cap).
Anchor profile (streak-3, h6, IC by anchor hour): 22h +0.045 (t 3.9), 23h +0.044 (3.6), 0h +0.036 (3.0), 21h +0.035 (2.8), 1h +0.028 (2.4); anchors 13-16h NEGATIVE (-0.027 at 13h, t -2.2; h24 at 16h +0.040) - the other 14 anchors within +-0.015.
So the effect is a clock window: a 3-day streak fade evaluated 21-01 UTC predicts the following 6 hours (about 22:00-07:00 UTC, the Asia session), not the other hours. h1: flat at anchor 23 (+0.003) but +0.031 at 22h, +0.027 at 4h.
Streak length at anchor 23 (h6 TRAIN IC, t): k=1 +0.036 (2.4), k=2 +0.049 (3.85, best, chosen after the fact), k=3 +0.044 (3.65), k=5 +0.028 (2.4), k=7 +0.021 (1.9): longer streaks add nothing; k=1..3 equivalent.
RIVAL CONTROL (trailing 24h return rank, anchor 23): r24-only h6 IC = +0.0744 (t +6.3; EXPLORE +0.093, C1 +0.040, C2 +0.071, C3 +0.058 - all positive), larger than the streak (+0.044). mean XS Spearman corr(streak3, r24) = 0.30.
Streak residualised on r24: h6 +0.0226 (t +2.0; slices +0.021/+0.025/+0.039/+0.013), h24 +0.0273 (t +2.4), h1 -0.007 (ns). So the 3-day streak keeps a small residual after the 1-day return (above 0.01), but most of the IC is the 1-day cross-sectional reversal into the 00-06 UTC window.
Reading: H7 stands as a clock effect, but its strongest, most parsimonious form is not the streak: it is the trailing-24h return rank (reversal) evaluated at the day-boundary anchor. That is a new hypothesis: H8 (24h reversal conditioned on the anchor hour / session), child of H7, and it overlaps H3 (reversal family, controlled there).
Plot: plots/cell_02_anchor_hour.png. Table above in the cell output (cells/cell_02_output.txt).
"""
kit.result(2, 3.0, variants=90, suggests="H8", body=body)
kit.add_h("H8", "Session-conditional 24h reversal: trailing 24h return rank reverses into the 22-07 UTC window, continues into US hours", "H7",
  "cells/cell_02_result.md (r24-only anchor-23 h6 IC +0.074, t 6.3; anchors 13-16h negative); OBSERVATIONS #6",
  "Does the cross-sectional rank of the trailing 24h return predict the next 1h/6h/24h with a sign that depends on the anchor hour (reversal into the Asia night, continuation into US hours)?",
  "a change in the trailing 24h log-return rank of a coin predicts the cross-sectional rank of its next 6h primary return negatively when measured at the 21-01 UTC anchors and positively at the 13-16 UTC anchors, because overnight (Asia-session) liquidity is thin and daily overshoots revert while US-session flow continues the day's trend",
  "an IC of the same sign at all anchor hours (a flat profile) would refute the clock dependence; a profile that is positive only where the response is the Binance print (EXPLORE/C1) would be the response switch",
  "plain unconditional daily reversal (H3); volatility clock (00 UTC has the highest |ret|); funding settlement at 00/08/16 UTC; weekday",
  "EXPLORE cell_02", 0.55,
  "cell_02: r24-only anchor-23 h6 IC +0.093/+0.040/+0.071/+0.058 on EXPLORE/C1/C2/C3 (4/4 positive, pooled t 6.3) and negative at 13-16h anchors for the streak: base 0.30 x2.5 (4/4 same sign, large t) -> 0.55")
kit.attempt(2, "H7", "streak-3 IC by anchor hour (24) x h (3), streak length sweep, residual on r24", "anchor 23 h6 IC +0.044, diff vs other anchors +0.038 t 3.0 supported; r24-only stronger (+0.074 t 6.3)")
kit.write_beliefs(); print(kit.posterior("H7"), kit.posterior("H8"))
