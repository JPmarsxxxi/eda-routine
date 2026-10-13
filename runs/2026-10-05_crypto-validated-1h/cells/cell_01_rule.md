hypothesis: H1
slice: C1
kind: test

# cell_01 rule — H1 on C1 (written before any code for this cell)

**Pick (Phase 2 step 1)** — tables/pick_01.txt, arithmetic:
- H1 on C1: prior 0.49, power 0.307. P(sup)=0.49x0.307+0.51x0.026=0.164 -> post 0.855 (|shift| 0.365); P(inc)=0.005 -> 0;
  P(ref)=0.49x0.683+0.51x0.973=0.831 -> post 0.412 (|shift| 0.078). Expected |shift| = 12.5 pp.
- H2 on C1: 4.8 pp. H3 on C1: 2.0 pp. -> H1 on C1 (largest). C1 is H1's lowest admissible fold (born EXPLORE, seen_on none).

**Sub-claim C1-a:** "On C1, coins in the top third of the cross-sectional perp-premium rank (daily mean premium over day d)
earn a lower primary 72h log return (d+1 00:00 -> d+4 00:00) than coins in the bottom third, by at least the cost of
trading it."

**14c menu row:** "X predicts forward Y" / "X is monotone in Y" -> quantile (tercile) sort of forward Y by X, plus the
cross-sectional Spearman IC as a secondary descriptive (not part of the decision).

**Design (fixed):** decision days on a fixed every-3rd-day grid starting at the first C1 day whose 72h window lies inside
C1 (non-overlapping 72h blocks); a block needs >= 5 coins with a valid premium and a valid 72h return (no new_source /
hole inside the window); spread_b = mean(top third) - mean(bottom third); statistic = mean over blocks, t = mean / sd x
sqrt(n).

**Smallest economically meaningful effect:** T = 2 x mean RT72 over C1's coins = 2 x mean(RT24 + 2 x 8.2) = **121.8 bp
per 72h** (a $1 long / $1 short book fully turned over each block pays two round trips).

**Decision rule (three branches):**
- **supported** if t <= -1.645 AND mean spread <= -121.8 bp;
- **inconclusive** if t <= -1.645 but mean spread > -121.8 bp (significant but below cost);
- **refuted** if t > -1.645 (not significantly negative, including any positive spread).

**Power (simulation, tables/power.csv, code/power_sims.py):** bootstrap of the 166 de-meaned EXPLORE block spreads (sd
777 bp), n = 57 blocks (C1's count of valid blocks from coverage flags), true mean shifted to -121.8 bp, 20,000 draws:
"P(supported | effect = -121.8 bp) = 0.307; under the null P(supported) = 0.026, P(refuted) = 0.973."
alpha = 0.05.

**Evidence weights:** supported = 0.307 / 0.05 = **6.14**; refuted = (1 - 0.307) / 0.95 = **0.729**; inconclusive = **1**.
None exceeds the 10x cap (guard b). Guard (a): first test of this sub-claim on C1 -> no overlap.
