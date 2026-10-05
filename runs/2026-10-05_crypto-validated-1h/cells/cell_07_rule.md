hypothesis: H2
slice: C1
kind: test

# cell_07 rule — H2 (Fear & Greed -> next-day panel return) on C1 (written before any code for this cell is run)

**Pick (Phase 2 step 1)** — tables/pick_07.txt. H1 is no longer pickable (EXPLORE = birth slice, C1-C3 opened).
H2 on C1: prior 0.12, power 0.279: P(sup) 0.078 -> 0.432 (|shift| 0.312); P(ref) 0.922 -> 0.094 (|shift| 0.026);
expected |shift| **4.8 pp**. H3 on C1: 2.0 pp. -> H2 on C1 (its lowest admissible fold; born EXPLORE, seen_on none).

**Sub-claim C2-a:** "On C1, days whose Fear & Greed value (stamped <= d) is in the top tercile are followed by a higher
equal-weight primary panel return over day d+1 than bottom-tercile days, by at least the cost of trading it."

**14c menu row:** "X predicts forward Y" -> tercile sort of next-day panel return by X (Welch t on top vs bottom days);
Spearman IC as a descriptive.

**Design:** every C1 day d whose day d+1 lies inside C1; panel = mean of the valid next-day coin returns, >= 5 coins;
terciles of Fear & Greed within C1.

**Smallest economically meaningful effect:** T = 2 x mean RT24 over C1's 10 coins = **89.0 bp** top-minus-bottom (a
long-on-greed / short-on-fear panel position pays one round trip per day on each side).

**Decision rule:** supported if t >= +1.645 AND spread >= +89.0 bp; inconclusive if t >= +1.645 and spread < 89.0 bp;
refuted if t < +1.645.

**Power (tables/power.csv, code/power_sims.py):** bootstrap of de-meaned EXPLORE panel daily returns (sd 496 bp), random
tercile labels, n = 175 days (58 per tercile), +44.5 bp added to top days and -44.5 bp to bottom days, 20,000 draws:
"P(supported | spread = 89.0 bp) = 0.279; under the null P(supported) = 0.050, P(refuted) = 0.950." alpha 0.05.

**Evidence weights:** supported = 0.279/0.05 = **5.57**; refuted = 0.721/0.95 = **0.759**; inconclusive = **1**. Within cap.
