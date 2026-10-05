### Cell 03 — EDA: H3 basis level vs next-24h realized vol (CONFIRM opening)

**Sub-claim being tested:** H3-C5: "in CONFIRM the perp-spot basis has positive partial Spearman with next-24h log RV after
trailing 24h/7d/30d RV."

**Why it matters to the hypothesis:** it is the effect itself; if it is absent outside its 16-month birth window, the
"leverage-premium precedes volatility" story has nothing.

**Test(s) used:** partial Spearman by rank-residualisation, moving-block bootstrap for the SE; side checks with dvol and
volume controls and by quarter.

**Decision rule before running:** see `cells/cell_03_rule.md`. SUPPORTED if rho > 0.0689; REFUTED if rho < 0.05 (and below
0.0689); INCONCLUSIVE between. Weights 10 (capped) / 0.24 / 1.

**Engine/library APIs used:** `eda_guard.load` via `scripts/kit.hourly`, `statsmodels` OLS for rank residuals, numpy bootstrap.

**Slice:** CONFIRM (2022-01-01 .. 2023-03-19), 31 days of warm-up history before it for the trailing controls only. Forward
windows end by 2023-03-19 23:59 (rows whose window would cross are dropped, per SPLITS.md).

**Decisions I need from you:** none (unattended).
