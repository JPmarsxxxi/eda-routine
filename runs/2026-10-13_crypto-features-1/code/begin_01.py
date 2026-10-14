import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
rp = fx.rule_power(12)
rule = f"""# cell 01 rule - H1 seed replication (Kakushadze #30 as written, three horizons, two anchors)
What is looked at: the exact seed f = (1 - rank(sign(c-c1)+sign(c1-c2)+sign(c2-c3))) * sum(vol,5)/sum(vol,20) built (a) on UTC-day OHLCV (decision at the 23:00 bar, sampling d)
and (b) on rolling 24h blocks ending at every hour (step 24 h, sampling h, the "anchor-hour" version), plus the streak-only part (1 - rank(streak)) of each (attribution: is the volume scale doing work?).
Variants: 4 feature definitions x 3 horizons (1h, 6h, 24h) = 12 (V = 12). Slice: TRAIN (EXPLORE + C1..C3, per-slice report). Tool: cross-sectional Spearman IC per timestamp (xs_ic), Newey-West t on the IC series
(lags h+5 hourly, 3 daily). 14c menu row: "X predicts forward Y" -> IC.
Direction (pre-stated): positive IC = fade works (down-streak + volume surge ranks high and earns more).
Pass rule: supported if the best of the 12 variants has pooled-TRAIN mean IC >= +0.02 AND NW t >= Sidak critical (V=12). Else not-supported (also when significant in the opposite sign).
Per-slice IC is reported for stability, not used in the branch. Weight if supported = power/alpha, if not = (1-power)/(1-alpha), at the best variant's own se, capped 3x.
{rp}
"""
ann = """### Cell 01 - EDA: does the Alpha#30 seed predict at 1h/6h/24h on TRAIN, and is the volume scale doing the work?
**Sub-claim:** H1 / C5 (effect) and C4 (attribution: streak-only vs volume-scaled) of the decomposition; decomposition floor Q1 existence (coverage), Q3 impostor (volume ratio alone is cell 2), Q8 stability (per slice).
**Why it matters:** if neither anchor shows a pooled-TRAIN IC >= 0.02 the seed is a regime effect (C1/C2 only, per MEMORY) and cells 2-3 must find which regime.
**Tests:** xs_ic (Spearman per timestamp, cross-section of the coins available, >= 6), NW t. **Decision rule before running:** see rule file. **APIs:** pandas rank/rolling, scipy.stats; eda_guard via code/panel.py.
**Decisions needed:** none (defaults in DECISIONS.md D5/D6).
"""
kit.begin(1, "H1", "TRAIN", "search", "none", "none", rule, ann)
print("written")
