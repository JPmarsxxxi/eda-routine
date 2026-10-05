hypothesis: H1
slice: C2
kind: test

# cell_03 rule — H1 on C2 (written before any code for this cell is run)

**Pick (Phase 2 step 1)** — tables/pick_03.txt: H1 on C2 6.8 pp (prior 0.412, power 0.199: P(sup) 0.098 -> 0.736;
P(ref) 0.901 -> 0.371); H2 on C1 4.8 pp; H3 on C1 2.0 pp -> H1 on C2. C2 is H1's lowest admissible fold (C1 opened).

**Sub-claim C1-a (same as cell_01, NEW sample):** "On C2, top-third perp-premium coins earn a lower 72h primary return
than bottom-third coins, by at least the cost of trading it." Different fold from cell_01 -> separate evidence (guard a
does not apply).

**14c menu row / design:** identical to cell_01 (tercile sort, every-3rd-day grid from C2's first eligible day, >= 5
coins per block, t on block spreads). C2 specifics: 9 coins (no BCH), 7 on FTMO mids; FTMO Saturday new_source flags
void most 72h windows that contain a Saturday for those 7 coins (DECISIONS D5), so blocks fall to ~32.

**Smallest economically meaningful effect:** T = 2 x mean RT72 over C2's 9 coins = **117.1 bp per 72h**.

**Decision rule:** supported if t <= -1.645 AND spread <= -117.1 bp; inconclusive if t <= -1.645 and spread > -117.1 bp;
refuted if t > -1.645.

**Power (tables/power.csv):** bootstrap of de-meaned EXPLORE block spreads, n = 32, true mean -117.1 bp, 20,000 draws:
"P(supported | effect = -117.1 bp) = 0.199; under the null P(supported) = 0.026, P(refuted) = 0.974." alpha 0.05.

**Evidence weights:** supported = 0.199/0.05 = **3.98**; refuted = 0.801/0.95 = **0.843**; inconclusive = **1**. Within
the 10x cap.

Note (states, RUNBOOK): H1 was refuted on C1, so it cannot become HIGH-CONFIRM this session whatever C2/C3 show; this
test still updates its posterior and is the decay-first record.
