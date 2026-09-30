### Cell 04 — EDA: H4 C1, volume-shock x relative-return interaction on CONFIRM

**Sub-claim being tested:** C1(H4): "next-day relative return loads positively on z(rel) x z(volume shock)."

**Why it matters to the hypothesis:** it is all of H4.

**Test(s) used:** daily Fama-MacBeth cross-sectional regression with interaction, NW(2), CONFIRM, 10 coins.

**Decision rule before running:** `cells/cell_04_rule.md`. Weights 10 (capped) / 0.1 (capped) / 1.

**Engine/library APIs used:** guarded loader, `code/panel.py::build`, `code/daily.py::daily`, `code/tests.py::fm_interaction`.

**Decisions I need from you:** none.
