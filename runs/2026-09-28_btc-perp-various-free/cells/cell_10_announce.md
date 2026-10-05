### Cell 10 — EDA: Phase 3 VAL check for H2 (DVOL adds next-day RV information)

**Sub-claim being tested:** partial Spearman(dvol, next-24h log RV | 24h/7d/30d trailing log RV) > 0 in VAL.

**Why it matters:** the only HIGH-CONFIRM hypothesis; VAL is opened once per session, and a failure would be reported.

**Test(s) used:** rank-residual partial Spearman, moving-block bootstrap SE.

**Decision rule before running:** `cells/cell_10_rule.md`. PASS > +0.1213 (weight 8.28, HIGH-VAL); FAIL < +0.05 (0.617); else INCONCLUSIVE (1).

**VAL_NOTE:** soft-clean VAL, different liquidity regime post-2023-04 (quoted beside the result).

**Engine/library APIs used:** `eda_guard.load` via `scripts/kit.hourly`.

**Slice:** VAL 2023-03-25 .. 2023-11-30, once.

**Decisions I need from you:** none (unattended).
