# cell_02 RESULT — redirect after H1's refutation (EXPLORE only)

Script `scripts/cell_02_h1_redirect.py`; tables `tables/02_*.csv|json`; plot `plots/02_h1_redirect.png`. 1,435 EXPLORE settlements.

**Branch fired: B4 (diffuse / no localised effect).** Checked in the pre-committed order:
- B1 funding-conditional: D(HI) 1.50 bp (n=540) vs D(LE) 0.72 bp (n=895); difference **0.78 bp < 1.0 bp** (t = 3.11). Fails
  the size bar (and D(LE) 0.72 >= 0.5 bp fails the third clause). Not fired.
- B2 opposite sign at low funding: D(funding < 0.01%) = +0.33 bp (t = +1.65, n=228). The sign is positive, not negative. Not fired.
- B3 one era: the largest quarter (2021Q1) carries 33.0% of sum(D) < 60%. Not fired.

**What the data actually points to** (descriptive, EXPLORE): the settlement-specific jump is positive at every funding level
(0.33 / 0.85 / 0.61 / 1.90 bp across the four bins), larger when funding is high, and it is spread over six quarters but
**shrinks over time**: mean D by quarter 0.53, 1.32, 1.81, 0.92, 0.43, 0.76 (2020Q3..2021Q4), then, from cell_01 on CONFIRM,
0.10, 0.34, 0.27, 0.09, 0.01 (2022Q1..2023Q1). This is a decay, not a localised regime, so it is not one of the redirect
shapes the rule listed (opposite sign / one era / one funding regime).

**Spawn decision (pre-committed B4):** no new funding-clock hypothesis is spawned. The decay pattern is recorded as a lead
(`REPORT.md` leads; `INBOX_PROPOSALS.md`): a "spread-capture decay" claim would need a fresh slice, and the only slice
left is VAL, which this session opens only for HIGH-CONFIRM hypotheses. **Weight applied: 1 (birth data, no evidence).**
H1 stays at posterior 0.130, state OPEN, with no eligible next test on EXPLORE (its birth slice) or CONFIRM (its one
opening is spent), so its next-test expected shift is 0 for the S2 count.
