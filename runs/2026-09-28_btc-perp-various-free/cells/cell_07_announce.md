### Cell 07 — EDA: H6 hourly basis change vs next-hour spot return (CONFIRM opening)

**Sub-claim being tested:** H6-C1: "in CONFIRM, partial Spearman(d_basis_t, r_{t+1} | r_t) is negative."

**Why it matters to the hypothesis:** the effect itself. EXPLORE showed -0.033 partial; CONFIRM is the real test and tells apart a separate
basis effect from H5's reversal seen through the spot leg.

**Test(s) used:** rank-residual partial Spearman, moving-block bootstrap SE; r_{t-1} control, 1% trim, by-quarter, gross-vs-cost line.

**Decision rule before running:** `cells/cell_07_rule.md`. SUPPORTED if rho < -0.0168; REFUTED if rho > -0.015; weights 10 (capped) / 0.102 / 1.

**Engine/library APIs used:** `eda_guard.load` via `scripts/kit.hourly` and the half-spread file, scipy.stats.spearmanr.

**Slice:** CONFIRM (2022-01-01 .. 2023-03-19). Pairs whose t+1 hour crosses TRAIN_END are dropped.

**Decisions I need from you:** none (unattended).
