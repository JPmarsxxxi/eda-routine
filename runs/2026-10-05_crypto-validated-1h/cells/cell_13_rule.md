hypothesis: H3
slice: C1
kind: test

# cell_13 rule — H3 (prior-session S&P 500 return -> next-day panel return) on C1 (written before any code is run)

**Pick** — tables/pick_13.txt: H1 and H2 have no admissible slice left. H3 on C1: prior 0.06, power 0.227: P(sup) 0.062
-> 0.225 (|shift| 0.165); P(ref) 0.938 -> 0.049 (|shift| 0.011); expected |shift| **2.0 pp**. This is the only pickable
test, and its expected shift is <= 3 pp: S2 pick count 1 of 3.

**Sub-claim C3-a:** "On C1, days whose prior S&P 500 session return (local_date <= d-1) is in the top tercile are followed
by a higher equal-weight primary panel return over day d+1 than bottom-tercile days, by at least the cost of trading it."

**14c menu row:** "X predicts forward Y" -> tercile sort + Welch t; Spearman IC descriptive.

**Design:** as cell_07, but only days with a defined prior-session return (equity sessions; weekends/holidays NaN).

**Smallest economically meaningful effect:** T = 2 x mean RT24 over C1's 10 coins = **89.0 bp**.

**Decision rule:** supported if t >= +1.645 AND spread >= 89.0 bp; inconclusive if t >= +1.645 and spread < 89.0 bp;
refuted if t < +1.645.

**Power (tables/power.csv):** EXPLORE-bootstrap of de-meaned panel daily returns, n = 120 days (175 x 250/365 session
share), spread 89.0 bp, 20,000 draws: "P(supported) = 0.227; under the null P(supported) = 0.052, P(refuted) = 0.948."
alpha 0.05.

**Evidence weights:** supported = 0.227/0.05 = **4.54**; refuted = 0.773/0.95 = **0.814**; inconclusive = **1**. Within cap.
