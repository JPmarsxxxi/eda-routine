### Cell 06 — EDA: H1 C1, daily reversal on CONFIRM

**Sub-claim being tested:** C1(H1): "a coin's UTC-day return is negatively related to its next UTC-day return."

**Why it matters to the hypothesis:** it is H1's core claim; refuted -> H1 drops and a redirect cell runs.

**Test(s) used:** pooled normal-score IC at 1 day, clustered by day, NW(2), CONFIRM, 10 coins.

**Decision rule before running:** `cells/cell_06_rule.md`. Weights 10 (capped) / 0.4605 / 1.

**Engine/library APIs used:** guarded loader, `code/panel.py`, `code/daily.py`, `code/tests.py::lag_ic`.

**Decisions I need from you:** none.
