hypothesis: H2
slice: C3
kind: redirect

# cell_12 rule — mandatory redirect after H2's refutation on C3 (RUNBOOK_v3 Phase 2 step 8)

H2 was refuted on C3 (cell_11). This redirect looks only at C3 (already opened by H2), carries **weight_applied 1**, and
any finding becomes a NEW child born on C3 with its own rule file. Recorded as `branch: inconclusive`.

**Fixed menu for every H2 redirect (unchanged from cell_08; DECISIONS D10):**
- R1 opposite sign: is the top-minus-bottom next-day spread significantly NEGATIVE (contrarian)? bar -2 x mean RT24.
- R2 horizon: 72h panel return on a non-overlapping 3-day grid, terciles of Fear & Greed; bar 2 x mean RT72.
- R3 extremes: next-day panel return on days with Fear & Greed >= 75 minus days <= 25; bar 2 x mean RT24.
- R4 change: terciles of the 7-day change in Fear & Greed instead of its level; bar 2 x mean RT24.
- R5 BTC only: next-day BTC return by Fear & Greed tercile; bar 2 x RT24(BTC) = 37.8 bp.
(C3 bars: 2 x RT24 = 84.3 bp; 2 x RT72 = 117.1 bp.)

**Spawn rule:** a child only for |t| >= 2.5 in the stated direction AND an effect clearing that look's bar; otherwise
"absent everywhere on C3", no child.
