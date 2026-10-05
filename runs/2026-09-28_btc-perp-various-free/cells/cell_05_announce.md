### Cell 05 — EDA: H2 DVOL vs next-24h realized vol (CONFIRM opening)

**Sub-claim being tested:** H2-C5: "in CONFIRM, DVOL has positive partial Spearman with next-24h log RV after trailing
24h/7d/30d RV."

**Why it matters to the hypothesis:** it is the effect itself; the EXPLORE evidence covers only 9 months of 2021.

**Test(s) used:** partial Spearman via rank residuals; block-bootstrap SE; rival control ladder (signed 24h return, EWMA RV);
quarterly stability.

**Decision rule before running:** `cells/cell_05_rule.md`. SUPPORTED if rho > 0.0869; REFUTED if rho < 0.05; else
INCONCLUSIVE. Weights 10 (capped) / 0.412 / 1.

**Engine/library APIs used:** `eda_guard.load` via `scripts/kit.hourly`, `statsmodels` OLS, numpy bootstrap.

**Slice:** CONFIRM (2022-01-01 .. 2023-03-19), 31 days of warm-up before it for controls only; rows whose forward window crosses
TRAIN_END dropped.

**Decisions I need from you:** none (unattended).
