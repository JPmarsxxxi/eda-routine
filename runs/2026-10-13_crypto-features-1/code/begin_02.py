import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
se = fx.NOISE["d_6"]["c"]/ (1170**.5)
pw = kit.power(se, 0.02, 1.96)
rule = f"""# cell 02 rule - H7: is the streak fade a property of the UTC day-boundary anchor? (controls: trailing 24h return; conditional: anchor hour)
Looked at: the 3-day sign-streak fade (1 - rank(sum of 3 daily-return signs), 24h blocks ending at anchor hour a) for every anchor a = 0..23, horizons 1h/6h/24h (72 variants); a streak-length sweep at anchor 23
(k = 1,2,3,5,7; 15 variants); and the rival control: the streak residualised (cross-sectional rank regression) on the rank of the trailing 24h return at anchor 23 (3 variants). V = 90 variants evaluated.
Tool: xs_ic per timestamp, grouped by anchor hour (each group is a daily series: NW lags h//24+3); the anchor contrast is the per-day paired difference IC(anchor 23) - mean IC(other 23 anchors), NW t.
Direction (pre-stated): positive IC (fade works).
PRE-STATED PRIMARY TEST (one test, h = 6, the horizon of the family's strongest cell-1 result): supported if IC(streak, anchor 23, h6) >= +0.02 AND paired difference vs the other anchors >= +0.02 with NW t >= 1.96.
refuted if the paired difference <= 0 with t <= -1.65 or IC(anchor 23, h6) <= 0; else inconclusive (weight = no-branch). Residual-control result is reported, and read as: partial IC < 0.01 means the 3-day streak adds
nothing beyond the 1-day return.
Power: daily-sampled h6, N ~ 1170 days, c = {fx.NOISE['d_6']['c']:.2f} -> se {se:.4f}; at delta 0.02, tcrit 1.96: power {pw['power']:.2f}, alpha {pw['alpha']:.4f}, w_yes {pw['w_yes']:.1f} -> 3.00 (cap), w_no {pw['w_no']:.2f}.
"""
ann = """### Cell 02 - EDA: H7 anchor-hour dependence of the streak fade
**Sub-claim:** the cell-1 daily-anchor IC (+0.043 at h6) is larger than the any-hour rolling IC (+0.009); is that the 23:00 anchor, and is it more than 1-day reversal?
**Why it matters:** if the IC is flat across anchors the cell-1 gap came from something else (sampling/overlap); if the 3-day streak adds nothing over the last day, H1/H7 collapse into trailing-24h reversal (H3).
**Tests:** IC by anchor hour x horizon, paired anchor contrast, residual-rank control. **Decision rule before running:** see rule file. **Decisions needed:** none.
"""
kit.begin(2, "H7", "TRAIN", "search", "trailing 24h return (r24)", "anchor hour of day (clock)", rule, ann)
