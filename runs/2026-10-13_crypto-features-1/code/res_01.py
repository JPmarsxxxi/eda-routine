import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 01 result - H1 Alpha#30 seed, TRAIN, 12 variants
Table (mean cross-sectional rank IC, NW t in brackets; cells/cell_01_table.csv; plot plots/cell_01_seed30_ic.png):
seed_daily    h1 +0.004(+0.3) | h6 +0.028(+2.5) | h24 +0.030(+2.6)  [EXPLORE +0.009/+0.052/+0.039; C1 +0.006/+0.029/+0.035; C2 -0.034/+0.006/+0.017; C3 +0.017/-0.008/+0.010]
streak_daily  h1 +0.002(+0.2) | h6 +0.043(+3.6) | h24 +0.031(+2.5)  [h6 by slice: EXPLORE +0.039, C1 +0.057, C2 +0.068, C3 +0.029 - all four positive]
seed_roll24   h1 +0.007(+3.2) | h6 +0.007(+1.7) | h24 +0.008(+1.2)   (IC at every hour of the day, 24h blocks)
streak_roll24 h1 +0.008(+3.4) | h6 +0.009(+2.1) | h24 +0.007(+1.1)
Pre-committed branch: best of 12 = streak_daily h=6 (IC +0.0432, NW t +3.56 >= Sidak 2.87, >= 0.02) -> SUPPORTED. se 0.0145, power 0.07 at delta 0.02 -> w_yes 32.7 -> capped 3.0 (weight_applied 3.0).
Honest reading: the branch is carried by the streak-only leg, not by the seed. The volume scale (V5/V20) LOWERS the daily h6 IC (0.043 -> 0.028) and h24 is flat (0.031 -> 0.030):
attribution (decomposition floor Q4) says the Alpha#30 effect is the sign-streak fade, the volume ratio adds nothing at these horizons. The seed itself (volume-scaled) is below
the Sidak bar in every variant (best seed_daily h24 +0.0296, t 2.6 < 2.87). 
The same features evaluated at EVERY hour of the day (24h-block anchors) give only +0.007..0.009: the daily-anchor IC is not an any-hour effect. It lives at the 23:00 bar with
the next 6h window (00-06 UTC) - a clock/anchor effect (daily candle close; not the Binance-print/FTMO switch, since EXPLORE and C1 (pure Binance print response) are the strongest and C3 is positive but weaker).
Market exposure: corr of cross-coin mean standardised feature with the EW market forward return +0.02 (rolling) / +0.04 (daily): market-neutral by construction.
suggests above: the anchor-hour dependence is a new hypothesis (H7); the volume-ratio rival is controlled in cell 2 (H1); C3 weakness / response-switch test in cell 3 (H1).
"""
kit.result(1, 3.0, variants=12, suggests="H7", body=body)
kit.add_h("H7", "UTC day-boundary anchor: sign-streak fade concentrates at the 23:00 anchor / 00-06 UTC window", "H1",
  "cells/cell_01_result.md (seed_daily/streak_daily vs roll24); OBSERVATIONS #6",
  "Is the streak-fade IC specific to the UTC day boundary (anchor hour 23, next 6h), and what is the mechanism?",
  "a change in the 3-day sign-streak rank of daily closes measured at the UTC day boundary predicts the cross-sectional rank of the next 6h and 24h primary return (down-streak = higher return) because daily-candle-based flows (funding clock, daily rebalancing, 00:00 UTC liquidity) concentrate the overreaction unwind right after the daily close",
  "an IC that is the same at every anchor hour (a flat IC-by-anchor profile) or that sits at a non-boundary hour; an effect present only where the response is the Binance print",
  "volume clock (00 UTC has the highest vol, OBSERVATIONS #6); trailing 24h return alone (reversal); response switch; day-of-week",
  "EXPLORE cell_01", 0.45,
  "cell_01: streak_daily h6 IC +0.039/+0.057/+0.068/+0.029 on EXPLORE/C1/C2/C3 (all positive, t 2.1/2.1/2.0/1.3), pooled t 3.6, but the same feature at the other 23 anchor hours is ~0.008: base 0.30 + uplift for 4/4 same-sign slices (x1.9) -> 0.45")
kit.attempt(1, "H1", "seed #30 + streak-only, daily and rolling-24h anchors, 3 horizons (12 variants)", "streak_daily h6 IC +0.043 t 3.6 supported; seed itself not; anchor-specific")
kit.write_beliefs()
print(kit.posterior("H1"), kit.posterior("H7"))
