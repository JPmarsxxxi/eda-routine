hypothesis: H6
slice: C3
kind: redirect

# cell_18 rule — mandatory redirect for H6 (H6 signal) on C3

Trigger: H6's only sub-claim was refuted (RUNBOOK_v3 step 8). Question: where does the data actually point instead?
C3 is a slice H6 already opened; no unopened fold is looked at. Weight applied: 1 (a redirect moves no posterior).

Pointers (each = the same 2-bin top-minus-bottom next-day spread, mean bp/day with Newey-West(5) SE, on C3):
- P1 sign flipped (bottom-minus-top).
- P2 horizons h = 2, 3, 5 days: mean per-day spread of the average return over d+1..d+h (response windows overlap: NW(5) SE),
  paper sign and flipped.
- P3 one era only: each calendar year inside C3, both signs.
- P4 re-translation pointed to by the Phase-1 assumption check: Spearman (ranked-in-time) version: correlation of ts-ranks over 6 days, both signs.
- P5 the named rival: 6-day volatility (std of daily log returns), both signs.
**Bar for a pointer:** |mean| >= 20 bp/day AND |t| >= 2.5 (stricter than 1.645 because ~15 looks are taken here).
**Outcome rule:** if one or more pointers clear the bar, the one with the largest |t| becomes ONE new child hypothesis in
BELIEFS.md (born_on C3 cell_18; seen_on = none unless another slice was shown), with its own rule file before any
test; if none clears it, the finding is "absent everywhere looked" and no child is spawned (DECISIONS D13).
