### Cell 08 — EDA: H4 DVOL level vs next-24h spot return (CONFIRM opening)

**Sub-claim being tested:** H4-C1: "in CONFIRM, Spearman(dvol_t, next-24h spot return) is positive."

**Why it matters to the hypothesis:** the effect itself; EXPLORE covered 9 months of a rising market and needs an out-of-era check.

**Test(s) used:** Spearman with moving-block bootstrap SE; trailing-return partial, by-quarter, best-quarter-out, tercile means.

**Decision rule before running:** `cells/cell_08_rule.md`. SUPPORTED if rho > +0.0669 (weight 7.26); REFUTED if rho < +0.025 (0.671); else INCONCLUSIVE (1).

**Engine/library APIs used:** `eda_guard.load` via `scripts/kit.hourly`, scipy.stats.spearmanr.

**Slice:** CONFIRM (2022-01-01 .. 2023-03-19). Rows whose 24h forward window crosses TRAIN_END are dropped.

**Decisions I need from you:** none (unattended).
