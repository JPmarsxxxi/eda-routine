### Cell 01 — EDA: H1 funding-clock basis jump (CONFIRM opening)

**Sub-claim being tested:** H1-C5: "In CONFIRM the perp-minus-spot basis rises across the 00/08/16 UTC funding settlement
by more than across the mid-cycle point of the same cycle."

**Why it matters to the hypothesis:** this is the effect itself. If the settlement-specific jump is absent out of the birth
slice, the sawtooth was an EXPLORE artefact and H1 has nothing left.

**Test(s) used:** paired per-settlement difference D (settlement jump minus mid-cycle placebo jump), mean with Newey-West(3)
t, one-sided; side bets by funding bin, by settlement hour, by quarter; cost line from half_bp.

**Decision rule before running:** see `cells/cell_01_rule.md`. SUPPORTED if t >= 2.326; REFUTED if t < 2.326 and mean D <
0.25 bp; INCONCLUSIVE otherwise. Weights 10 (capped) / 0.1 (capped) / 1.

**Engine/library APIs used:** `eda_guard.load` (via `scripts/kit.hourly`), `statsmodels.api.OLS(...).fit(cov_type="HAC",
cov_kwds={"maxlags": 3})`, `scipy.stats.spearmanr`.

**Slice:** CONFIRM (2022-01-01 .. 2023-03-19). Loaded with 1 day of warm-up history, used only to index the snapshot
before the first settlement. No event with S-30m before 2022-01-01 is counted.

**Decisions I need from you:** none (unattended; defaults in DECISIONS.md).
