import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
kit.add_h("H16", "Multi-day range position, drawdown and moving-average distance rank the coins", "none",
  "TARGET.md FAMILIES (price-path shape: range position); OBSERVATIONS #2, #11; cell 5 (k=48-168 reversal IC 0.005-0.019 at h1, ~0 at h24)",
  "Do the position of the close inside its trailing 3-30 day range, the drawdown from the trailing high, the rally from the trailing low and the distance to the moving average rank the next 1h/6h/24h returns?",
  "a change in a coin's position in its trailing 72h-720h high-low range, drawdown from the high, rally from the low or distance to the moving average predicts a LOWER cross-sectional rank of its next 6h/24h primary return when high (and a higher one when low) because multi-day extremes are partly given back (range mean reversion)",
  "no position/drawdown/distance feature has a negative IC beyond min_useful at 6h or 24h; positive IC (trend) would refute the mean-reversion claim",
  "the short-horizon reversal (a coin at its range top just rose: cells 5-6, f001/f002); the coin fixed effect (a coin in a long trend sits at the top of its range for months); volatility",
  "EXPLORE #2 #11", 0.20,
  "cell 5 shows the reversal profile falling to ~0 by k=168 at h24; no earlier run tested range position; tracker base 0.30 x0.67 -> 0.20")
tc = kit.tcrit_for(24)
rule = f"""# cell 42 rule - H16: multi-day range position, drawdown, rally and moving-average distance (controls: coin fixed effect via within-coin detrending; conditional: none)
Features (hourly, Binance, trailing-only), windows w in 72, 168, 336, 720 hours: pos_w = (C - min low_w)/(max high_w - min low_w); dd_w = log(C / max close_w) (<= 0); ru_w = log(C / min close_w) (>= 0); madev_w = log(C / mean close_w).
Forms: (a) level; (b) within-coin detrended: minus the coin's own trailing-2160h mean ending at t-1. 4 features x 4 w x 2 forms x 3 h = 96 variants (V = 96); the pre-stated one-sided primary family is the detrended forms at h6 and h24 (4 x 4 x 2 = 32, tcrit {kit.tcrit_for(32):.2f}).
Direction (range mean reversion): NEGATIVE IC for pos_w, ru_w, madev_w (high = near top / far above mean); POSITIVE for dd_w (deep drawdown = lower = more negative value; a higher dd, i.e. near the high, predicts lower, so dd_w is also NEGATIVE; all four scored as -IC).
Pass rule: SUPPORTED if the best detrended (b) primary variant has pooled-TRAIN score (-IC) >= +0.02 and NW t >= {kit.tcrit_for(32):.2f}. Not supported otherwise; wrong-signed significant results count as 'no'. Level (a) is reported for the fixed-effect share.
{fx.rule_power(96)}
"""
ann = """### Cell 42 - EDA: H16 does multi-day range position predict?
**Sub-claim:** (C5) range mean reversion at 6-24h; (Q3 impostor) coin fixed effect, short-horizon reversal. **Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(42, "H16", "TRAIN", "search", "coin fixed effect (persistent range position of trending coins)", "none", rule, ann)
