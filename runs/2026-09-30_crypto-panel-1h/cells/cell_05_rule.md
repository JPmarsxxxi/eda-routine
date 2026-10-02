# cell_05 — RULE (mandatory REDIRECT after H4's refutation; written before any code for this cell exists)

**Why this cell:** RUNBOOK_v3 Phase 2 step 8. H4 was refuted on CONFIRM (cell_04, b3 -14.5 bp, z -2.32, opposite sign) and is
LOW/closed. This cell asks "where does the data actually point?" — opposite sign? one era / subset only? absent everywhere?
It moves NO hypothesis's odds (H4 is closed; no cell may be run against it), so every branch has weight 1 on every entry. Its
finding, if any, becomes a NEW hypothesis with its own rule file and its own first test on a slice it was not born on.

**Step-1 pick arithmetic:** not a pick — step 8 makes the redirect mandatory before the next pick.

**Slice:** EXPLORE (where H4's observation #12 was born; this is a look for direction, not a re-test of H4 — no weight to H4).
It is the only slice where the redirect can look without spending another CONFIRM opening on H4's family; CONFIRM's own
breakdown (halves, tercile table) was already produced by cell_04 and is re-used below as given, not recomputed.

## Sub-claim looked at
R(H4): the sign and location of the daily cross-sectional interaction b3 (next-day relative return on z(rel) x z(volume shock))
on EXPLORE, overall and by era (2018, 2019, 2020, 2021H1), days with >= 6 coins; plus the rank-regressor version.

## 14c menu row + tool
"X predicts forward Y" (cross-sectional) -> daily Fama-MacBeth with interaction, NW(2). `code/tests.py::fm_interaction(min_n=6)`.

## Decision rule (three branches; decides only what gets spawned)
- **opposite sign** if EXPLORE b3 z < -1.645 overall -> the CONFIRM sign is the data's direction -> spawn a reversal-type child.
- **subset only** if |z overall| <= 1.645 but exactly one era has |z| > 2, OR z overall > +1.645 (original sign on EXPLORE,
  opposite on CONFIRM = a regime-specific effect) -> spawn a regime-conditioned child only if a mechanism names that regime.
- **absent everywhere** if |z overall| <= 1.645 and no era has |z| > 2 -> nothing to spawn; the EXPLORE tercile pattern (OBS #12)
  was statistic-specific noise.

## Power / weights
Power simulation (`code/power.py R5`, 200 sims, 1,100 days x 7 coins, b3 = 28 bp, same DGP as cell_04):
**"cell_05 FM on EXPLORE size: 0.045", "cell_05 FM on EXPLORE power (b3=28bp): 0.82".** alpha 0.05.
Weights: **1 for all three branches on every BELIEFS entry** (a redirect generates hypotheses; it is not evidence for or against
any open one, and H4 is closed). Guard (a)/(b): n/a (no update).
