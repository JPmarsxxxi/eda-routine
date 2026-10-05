hypothesis: H2
slice: C3
kind: test

# cell_11 rule — H2 on C3 (written before any code for this cell is run)

**Pick** — tables/pick_11.txt: H2 on C3 **3.4 pp** (prior 0.077, power 0.289: P(sup) 0.068 -> 0.325; P(ref) 0.932 ->
0.059); H3 on C1 2.0 pp -> H2 on C3 (its last admissible fold). 3.4 pp > 3 pp: not an S2 pick.

**Sub-claim C2-a on C3 (new sample):** "On C3, top-tercile Fear & Greed days are followed by a higher equal-weight primary
panel return over day d+1 than bottom-tercile days, by at least the cost of trading it."

**Design:** as cells 07/09. C3: 9 coins, 7 on FTMO mids (Saturday-ending days drop, DECISIONS D5).

**Smallest economically meaningful effect:** T = **84.3 bp** (2 x mean RT24, 9 coins).

**Decision rule:** supported if t >= +1.645 AND spread >= 84.3 bp; inconclusive if t >= +1.645 and spread < 84.3 bp;
refuted if t < +1.645.

**Power (tables/power.csv):** EXPLORE-bootstrap, n = 213 days, spread 84.3 bp, 20,000 draws: "P(supported) = 0.289; under
the null P(supported) = 0.049, P(refuted) = 0.951." alpha 0.05.

**Evidence weights:** supported = 0.289/0.05 = **5.78**; refuted = 0.711/0.95 = **0.748**; inconclusive = **1**. Within cap.
