### Cell 08 — EDA: H2 C1, daily reversal conditional on panel volume shock (CONFIRM)

**Sub-claim being tested:** C1(H2): "day->next-day IC is more negative on top-tercile panel-volume-shock days."

**Why it matters to the hypothesis:** it is all of H2.

**Test(s) used:** difference of per-day normal-score IC, high vs other days, Welch t, CONFIRM.

**Decision rule before running:** `cells/cell_08_rule.md`. Weights 4.5 / 0.816 / 1.

**Engine/library APIs used:** guarded loader, `code/daily.py`, `code/tests.py::diff_ic, lag_ic, nscore`.

**Decisions I need from you:** none.
