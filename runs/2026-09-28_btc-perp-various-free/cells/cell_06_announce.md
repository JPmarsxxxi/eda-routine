### Cell 06 — EDA: H5 hourly spot return reversal (CONFIRM opening)

**Sub-claim being tested:** H5-C5: "in CONFIRM, Spearman(r_t, r_{t+1}) of hourly spot returns is negative."

**Why it matters to the hypothesis:** the effect itself; EXPLORE showed a pooled -0.078 whose sign alternated by era
(floor Q8 noise signature), so CONFIRM is the real test.

**Test(s) used:** Spearman on consecutive-hour pairs, block-bootstrap SE; crash-hour trim, by-quarter, tercile mechanism check,
gross-vs-cost line.

**Decision rule before running:** `cells/cell_06_rule.md`. SUPPORTED if rho < -0.01526; REFUTED if rho > -0.015; weights
10 (capped) / 0.1 (capped) / 1.

**Engine/library APIs used:** `eda_guard.load` via `scripts/kit.hourly` and the half-spread file, scipy.stats.spearmanr.

**Slice:** CONFIRM (2022-01-01 .. 2023-03-19). Pairs whose t+1 hour crosses TRAIN_END are dropped.

**Decisions I need from you:** none (unattended).
