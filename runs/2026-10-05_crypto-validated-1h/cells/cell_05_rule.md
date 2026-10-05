hypothesis: H1
slice: C3
kind: test

# cell_05 rule — H1 on C3 (written before any code for this cell is run)

**Pick (Phase 2 step 1)** — tables/pick_05.txt: H1 on C3 8.3 pp (prior 0.371, power 0.239: P(sup) 0.105 -> 0.738;
P(ref) 0.893 -> 0.321); H2 on C1 4.8 pp; H3 on C1 2.0 pp -> H1 on C3, its last admissible fold (C1, C2 opened).

**Sub-claim C1-a on C3 (new sample, separate evidence):** "On C3, top-third perp-premium coins earn a lower 72h primary
return than bottom-third coins, by at least the cost of trading it."

**Design:** identical to cells 01/03 (C3: 9 coins, 7 on FTMO mids; FTMO Saturday windows void per DECISIONS D5).

**Smallest economically meaningful effect:** T = 2 x mean RT72 over C3's 9 coins = **117.1 bp per 72h**.

**Decision rule:** supported if t <= -1.645 AND spread <= -117.1 bp; inconclusive if t <= -1.645 and spread > -117.1 bp;
refuted if t > -1.645.

**Power (tables/power.csv):** bootstrap of de-meaned EXPLORE block spreads, n = 44, true mean -117.1 bp, 20,000 draws:
"P(supported | effect = -117.1 bp) = 0.239; under the null P(supported) = 0.027, P(refuted) = 0.973." alpha 0.05.

**Evidence weights:** supported = 0.239/0.05 = **4.78**; refuted = 0.761/0.95 = **0.801**; inconclusive = **1**. Within cap.
