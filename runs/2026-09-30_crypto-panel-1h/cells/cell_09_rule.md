# cell_09 — RULE (Phase 3 VAL check; written before any code for this cell exists)

**Hypothesis:** H5 (Intraday 6-hour reversal), state HIGH-CONFIRM after cell_01 (posterior 0.865). This is the session's ONE
VAL opening (DECISIONS D12), for H5 only. Not a pick: Phase 3 step 1 ("for every hypothesis queued HIGH-after-CONFIRM").
**Slice:** VAL 2023-03-25 .. 2023-11-30 (loader slice "VAL"; guard asserts no row > VAL_END).

**VAL_NOTE (TARGET.md, quoted verbatim):** "Two reasons VAL is weak evidence. (1) BTC VAL was crossed twice by earlier work (both
pre-registered) and overlaps a spent pooled row of an earlier BTC seasonality EDA: SOFT-clean for BTC; clean for the other nine
coins as far as this file knows. (2) VAL may be a DIFFERENT REGIME from TRAIN: from 2023-04 BTC's 1-minute trade counts fell ~8x
(cause not established). A lead about trade counts or volume can fail VAL for structural reasons."

## Sub-claim
C1(H5) on VAL: a coin's 6h block return is negatively related to its next 6h block return — the SAME statistic as cell_01.

## 14c menu row + tool
"X predicts forward Y": pooled normal-score IC, consecutive 6h blocks, day clusters, NW(2). `code/tests.py::lag_ic(B, 1, day)`.

## Decision rule
- **supported** if z < -1.645 with >= 150 day clusters.
- **refuted** if z >= -1.645 with >= 150 day clusters, no sign conflict.
- **inconclusive** if < 150 day clusters or sign conflict (normal-score z < -1.645, Pearson z > +1.645).

## Evidence weights
Power simulation (`code/power.py VAL5`, 300 sims, 250 days x 4 blocks x 10 coins, phi = -0.065, same DGP as cell_01):
**"VAL H5 size: 0.0733", "VAL H5 power (phi=-0.065): 0.94".** Smallest economically meaningful effect as in cell_01 (0.065).
alpha = max(0.05, 0.0733) = 0.0733.
- weight(supported) = 0.94/0.0733 = 12.8 -> **capped 10** · weight(refuted) = 0.06/0.9267 = 0.065 -> **capped 0.1** ·
  inconclusive 1.
Guard (a): cell_01 was CONFIRM (different sample) -> independent pieces of evidence, both applied. Guard (b): capped as stated.
State after: supported -> posterior > 0.85 -> **HIGH-VAL**; refuted -> posterior via the capped weight, state by band.

## Descriptive (does not decide)
Same statistic without BTC (VAL_NOTE 1); per coin; decay lags 2-4; cost line (implied 1-sd move vs 19.8 bp).
