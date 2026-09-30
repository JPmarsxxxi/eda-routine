### Cell 03 — EDA: H3 C1, lag-24 reversal of 1h returns on CONFIRM

**Sub-claim being tested:** C1(H3): "r(t) negatively related to r(t+24h), and lag 24 more negative than lags 23/25."

**Why it matters to the hypothesis:** it is all of H3 (a NO-STORY lead with a forbidding prediction).

**Test(s) used:** pooled normal-score IC at lags 23/24/25, day-clustered, NW(2), CONFIRM, 10 coins.

**Decision rule before running:** `cells/cell_03_rule.md`. Weights 10 (capped) / 0.1 (capped) / 1.

**Engine/library APIs used:** guarded loader, `code/panel.py::build`, `code/tests.py::lag_ic`; matplotlib.

**Decisions I need from you:** none; contamination from cell_01's descriptive lag-24h number disclosed in the rule file.
