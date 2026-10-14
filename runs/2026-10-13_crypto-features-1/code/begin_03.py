import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
se = 0.012
pw = kit.power(se, 0.01, 1.96)
rule = f"""# cell 03 rule - H1: does the volume scale add anything, and is the C2/C3 weakness the response switch? (controls: volume-ratio alone, Binance-vs-primary response)
Looked at (daily anchor 23:00, daily sampling, horizons 1h/6h/24h): seed (streak-3 x V5/V20), streak-only, V5/V20 alone (both signs), r24 (reference); each scored against the PRIMARY forward return and against the
BINANCE-close forward return (RB; same bars, no switch). 4 features x 3 h x 2 responses = 24 variants (V = 24).
Pre-stated primary test (H1, one of two horizons h6/h24 -> V_primary = 2, tcrit {kit.tcrit_for(2):.2f}): the volume scale ADDS if IC(seed) - IC(streak-only) >= +0.01 (paired per-day difference, NW t >= {kit.tcrit_for(2):.2f}).
Not-supported otherwise (and 'refuted' when the difference is <= 0 with t <= -1.65: the scale subtracts).
Secondary, reported, no belief weight: response-switch test = paired daily difference IC(Binance response) - IC(primary response) over C2+C3 for streak-only and r24 at h6/h24 (a positive difference >= +0.01, t >= 1.96,
says the primary-minus-Binance mid-vs-print wedge costs IC).
Power: daily-sampled paired difference, se ~ {se:.3f} (daily h6 c 0.46 /sqrt(1170) = 0.013; differences of two highly correlated ICs are tighter, using 0.012), delta 0.01: power {pw['power']:.2f}, alpha {pw['alpha']:.4f}, w_yes {pw['w_yes']:.1f} -> 3.00, w_no {pw['w_no']:.2f}.
"""
ann = """### Cell 03 - EDA: H1 attribution + response-switch control
**Sub-claim:** (C4) the volume ratio V5/V20 is the second leg of Alpha#30; (C6 side bet) if the MEMORY story (C3 fade) were the response switch, scoring against the Binance close in C2/C3 should recover IC.
**Why it matters:** decides whether the seed is a feature (vol-scaled) or only the streak/reversal part is.
**Tests:** paired per-day IC differences, NW; xs_ic. **Decisions needed:** none.
"""
kit.begin(3, "H1", "TRAIN", "search", "volume-ratio alone; Binance-vs-primary response", "none", rule, ann)
