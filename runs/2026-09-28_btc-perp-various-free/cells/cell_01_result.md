# cell_01 RESULT — H1 CONFIRM opening

Script `scripts/cell_01_h1_confirm.py`; tables `tables/01_result.json`, `tables/01_per_settlement.csv`, `tables/01_by_*.csv`;
plot `plots/01_h1_confirm.png`. Slice: CONFIRM, 1,328 settlements.

**Branch fired: REFUTED.** Deciding numbers: mean D = **0.163 bp** (< 0.25 bp threshold), NW(3) t = **2.18** (< 2.326).
Settlement jump +0.083 bp, mid-cycle placebo -0.080 bp. The difference is positive and near-significant but only a third of
the 0.5 bp minimum economic effect, so by the rule written first this is a refutation, not an inconclusive.

**Weight applied:** (1-power)/(1-alpha) = 0.030/0.99 = 0.0303 -> **capped to 0.1** (guard b). H1 odds 1.5 x 0.1 = 0.15 ->
**posterior 0.130** (from 0.60). State: OPEN (0.05 < 0.130 < 0.85).

Unweighted side bets / rivals (reported, not scored):
- Mechanism side bet (funding scaling): Spearman(jump, funding settled) = **+0.011** (EXPLORE +0.23). By funding bin:
  <0.01% n=848 D +0.17, =0.01% n=471 D +0.16, 0.01-0.03% n=8 D -1.57, >0.03% n=1. **CONFIRM contains almost no positive-funding
  settlements** (9 of 1,328 above the 0.01% default, vs 547 of 1,456 in EXPLORE). The regime in which the EXPLORE jump was
  large (+1.48 bp at >0.03%) never occurred in CONFIRM, so the side bet could not really be exercised. That is a fact
  about the sample, and the pre-committed weight stands anyway.
- Session-open rival: D at 00 / 08 / 16 UTC = 0.13 / 0.26 / 0.10 bp (all small). Nothing separates the session-open rival
  from the funding mechanism here.
- Stability (decay-first): D by quarter 0.10, 0.34, 0.27, 0.09, 0.01. No quarter reaches 0.5 bp. Fading into 2023Q1.
- Economics: two-leg round trip (4 x half_bp) median **0.34 bp** on the 432 settlements with a same-hour half_bp row (32%
  coverage; venue of half_bp unstated). The CONFIRM jump (0.08 bp) is a quarter of that.

Refutation of H1's core sub-claim -> mandatory redirect cell next (cell_02).
