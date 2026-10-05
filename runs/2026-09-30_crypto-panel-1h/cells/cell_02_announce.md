### Cell 02 — EDA: H6 C1, 6h reversal conditional on trailing volatility (EXPLORE)

**Sub-claim being tested:** C1(H6): "6h->next-6h normal-score IC is more negative on top-tercile trailing-vol days."

**Why it matters to the hypothesis:** it is the whole of H6; refuted -> H6 drops, redirect cell follows.

**Test(s) used:** day-clustered IC difference (high-vol days minus others), Welch t, 6h blocks, EXPLORE.

**Decision rule before running:** `cells/cell_02_rule.md` — supported z < -1.645; refuted z >= -1.645; inconclusive if a
group < 300 days or sign conflict. Weights 10 (capped) / 0.1 (capped) / 1.

**Engine/library APIs used:** guarded loader, `code/panel.py::build`, `code/tests.py::diff_ic_clustered`, `lag_ic`; matplotlib.

**Decisions I need from you:** the CONFIRM-born child is tested on EXPLORE and cannot reach VAL (DECISIONS D10, default taken).
