### Cell 01 — EDA: H5 C1, 6-hour block reversal on CONFIRM

**Sub-claim being tested:** C1(H5): "on CONFIRM, a coin's 6h block return is negatively related to its next 6h block return."

**Why it matters to the hypothesis:** H5 is only this claim; if refuted, H5 has nothing left (14c 3.2, scoped per hypothesis).

**Test(s) used:** pooled normal-score IC, day-clustered, Newey-West(2) SE, consecutive 6h blocks, 10 coins, CONFIRM.

**Decision rule before running:** see `cells/cell_01_rule.md` — supported if z < -1.645; refuted if z >= -1.645; inconclusive
if < 400 day clusters or a normal-score vs Pearson sign conflict. Weights: 10 (capped) / 0.1 (capped) / 1.

**Engine/library APIs used:** `code/guarded_load.py::spot` (guard), `code/panel.py::build`, `code/tests.py::lag_ic`,
`scipy.stats.norm.ppf`, numpy/pandas; matplotlib (plot).

**Decisions I need from you:** none open; defaults logged in DECISIONS.md (D4 plotting, D8 cost threshold).

Unattended: written before the cell's code, then proceeding (RUNBOOK_v3 UNATTENDED SUBSTITUTIONS).
