hypothesis: H2
slice: C2
kind: test

# cell_09 rule — H2 on C2 (written before any code for this cell is run)

**Pick** — tables/pick_09.txt: H2 on C2 **3.2 pp** (prior 0.094, power 0.236: P(sup) 0.067 -> 0.329; P(ref) 0.933 ->
0.077); H3 on C1 2.0 pp. H1 not pickable. -> H2 on C2 (lowest admissible fold). Best shift 3.2 pp > 3 pp: not an S2 pick.

**Sub-claim C2-a on C2 (new sample):** "On C2, top-tercile Fear & Greed days are followed by a higher equal-weight primary
panel return over day d+1 than bottom-tercile days, by at least the cost of trading it."

**Design:** as cell_07. C2: 9 coins, 7 on FTMO mids; Saturday-ending days have < 5 valid coins and drop (DECISIONS D5).

**Smallest economically meaningful effect:** T = 2 x mean RT24 over C2's 9 coins = **84.3 bp**.

**Decision rule:** supported if t >= +1.645 AND spread >= 84.3 bp; inconclusive if t >= +1.645 and spread < 84.3 bp;
refuted if t < +1.645.

**Power (tables/power.csv):** EXPLORE-bootstrap, n = 145 days, spread 84.3 bp, 20,000 draws: "P(supported) = 0.236; under
the null P(supported) = 0.049, P(refuted) = 0.951." alpha 0.05.

**Evidence weights:** supported = 0.236/0.05 = **4.72**; refuted = 0.764/0.95 = **0.804**; inconclusive = **1**. Within cap.
