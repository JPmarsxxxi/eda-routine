# cell_07 — RULE (mandatory REDIRECT after H1's refutation; written before any code for this cell exists)

**Why this cell:** RUNBOOK_v3 Phase 2 step 8. H1 C1 refuted on CONFIRM (cell_06, IC -0.047, z -1.38); H1 posterior 0.227,
CONFIRM spent. "Where does the data actually point?" Candidates the CONFIRM descriptives raised: extreme days only (IC -0.227 on
the top-10% |r| days vs -0.027 elsewhere), one era, or nowhere. Moves NO hypothesis's odds (weight 1 on every entry).
**Step-1 pick arithmetic:** not a pick (step 8 makes the redirect mandatory).
**Slice:** EXPLORE (where H1 was born). Not a re-test of H1 (no weight to H1). The CONFIRM numbers are cell_06's, re-used as given.

## Sub-claim looked at
R(H1): on EXPLORE daily returns, the normal-score day->next-day IC split into days whose |r| is in the coin's top 10% (over
EXPLORE) vs the rest, overall and by era (2017H2-18, 2019, 2020, 2021H1).

## 14c menu row + tool
"Distribution differs between groups" / "X predicts forward Y": products of per-coin normal scores (day d, day d+1), averaged
within day over the group's coin-days, NW(2) over days. `code/tests.py::nscore`, `nw_se`.

## Decision rule (decides only what gets spawned)
- **extreme-days only** if big-day IC z < -1.645 AND other-day IC |z| <= 1.645.
- **everywhere** if both z < -1.645 (then the CONFIRM failure is a power problem, not a location one; no child).
- **opposite sign** if the all-day IC z > +1.645.
- **absent everywhere** otherwise.

## Power / weights
Power simulation (`code/power.py R7`, `R7min`, 200 sims, 1,400 days x 6 coins; only top-10% |r| days reverse by phi_big):
**"cell_07 big-day IC size: 0.065"; "cell_07 big-day IC power (phi_big=-0.024): 0.3"; "(phi_big=-0.2): 1.0".**
Smallest economically meaningful: a top-10% day is ~1.8 sd = ~1,170 bp on EXPLORE; predicting the 28 bp cost line needs
|phi_big| >= 28/1170 = 0.024 (power 0.30 there; the CONFIRM descriptive magnitude ~ -0.2 is detected with power 1.0).
Weights: **1 for all branches on every BELIEFS entry** (redirect; no update). Guard (a)/(b): n/a.
