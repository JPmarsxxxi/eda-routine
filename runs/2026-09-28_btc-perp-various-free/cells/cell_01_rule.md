# cell_01 RULE — H1 CONFIRM opening (written before any code for this cell exists)

**Hypothesis:** H1, funding-clock basis sawtooth (born EXPLORE #1). This is H1's ONE CONFIRM opening.

**Pick arithmetic (Phase 2 step 1):** expected |shift| = P(sup)*|post_sup - p| + P(not)*|post_ref - p| (`scripts/shift.py`):
H1 0.392 (p .60, power .97, alpha .01) > H3 0.314 > H2 0.264 > H5 0.253 > H4 0.117. H1 has the largest expected shift -> picked.

**Sub-claim (14c floor Q5, the effect):** in CONFIRM, the perp-minus-spot basis rises across the funding settlement by more
than it changes across the mid-cycle point of the same cycle.

**14c menu row + tool:** "Distribution differs between groups" -> paired difference of means per settlement, Newey-West
(maxlags 3) t on the mean, one-sided.

**Statistic:** for each settlement S in CONFIRM (S-30m >= 2022-01-01 00:00 and S+4h30m <= 2023-03-19 23:59):
b(X) = 1e4*log(perp metrics `c` of the 5m bar ending at X / spot 30m close of the bar ending at X) (`scripts/kit.py`);
D_S = [b(S+30m) - b(S-30m)] - [b(S+4h30m) - b(S+3h30m)]. Test mean(D) > 0.

**Smallest economically meaningful effect:** 0.5 bp. A basis trade crosses two legs twice. At the EXPLORE median half_bp of
0.13 bp, a round trip is about 4 x 0.13 ≈ 0.5 bp, so an effect below that could never be expressed.

**Power (stated simulation, `scripts/power_all.py`, `tables/power_all.json` "H1"):** 2,000 moving-block (21 settlements)
bootstrap samples of the EXPLORE D series, demeaned then shifted by +0.5 bp, n = 1,329 (CONFIRM settlements), NW(3) t >
2.326 -> **power = 0.970**; same with no shift -> empirical size 0.0115. **alpha = 0.01.**

**Decision rule (three branches) and evidence weights:**
- **SUPPORTED** if NW t >= 2.326 (one-sided p < 0.01). weight = power/alpha = 0.970/0.01 = 97 -> **capped to 10** (guard b).
- **REFUTED** if t < 2.326 AND mean(D) < 0.25 bp (half the minimum effect). weight = (1-power)/(1-alpha) = 0.030/0.99 =
  0.0303 -> **capped to 0.1** (guard b).
- **INCONCLUSIVE** otherwise (t < 2.326 but mean(D) >= 0.25 bp). weight = 1.

**Guard (a):** first test of this sub-claim on CONFIRM. No earlier cell in this session tested it on CONFIRM. Phase 0 6b was
the EXPLORE observation that gave birth to it and is not evidence.

**Reported, NOT weighted (side bets and rivals, 14c floor Q4/Q6/Q7/Q8/Q9):**
- Q6 mechanism side bet: Spearman(jump across settlement, funding settled at S) > 0; jump by funding bin (<0.01%, =0.01%,
  0.01-0.03%, >0.03%).
- Rival "session opens": D separately at 00, 08, 16 UTC settlements. 16 UTC is not a major venue open, so an effect of similar
  size at 16 weakens the session-open rival.
- Q8 stability: mean D by calendar quarter in CONFIRM (decay-first shape).
- Q9 economics: half_bp at the settlement hour where present (count stated). The two-leg round trip = 4 x half_bp compared
  with mean jump.
