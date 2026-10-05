### Cell 09 — EDA: Phase 3 VAL check for H5 (6h reversal)

**Sub-claim being tested:** C1(H5) on VAL (same statistic as cell_01).

**Why it matters to the hypothesis:** the one VAL look; decides HIGH-VAL vs not. VAL_NOTE quoted in the rule file and beside
the result: VAL is weak evidence (BTC soft-clean; possible regime change from 2023-04).

**Test(s) used:** pooled normal-score IC, 6h blocks, day clusters, NW(2), VAL.

**Decision rule before running:** `cells/cell_09_rule.md`. Weights 10 (capped) / 0.1 (capped) / 1.

**Engine/library APIs used:** guarded loader (slice VAL), `code/panel.py`, `code/tests.py::lag_ic`.

**Decisions I need from you:** opening VAL at all (DECISIONS D12; default: open once, H5 only).
