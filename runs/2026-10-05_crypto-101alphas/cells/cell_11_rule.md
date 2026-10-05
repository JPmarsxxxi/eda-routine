hypothesis: H4
slice: C1
kind: redirect

# cell_11 rule — mandatory redirect for H4 (Alpha#6) on C1

Trigger: H4's only sub-claim was refuted (RUNBOOK_v3 step 8). Question: where does the data actually point instead?
C1 is a slice H4 already opened; no unopened fold is looked at. Weight applied: 1 (a redirect moves no posterior).

Pointers (each = the same 2-bin top-minus-bottom next-day spread, mean bp/day with Newey-West(5) SE, on C1):
- P1 sign flipped (bottom-minus-top).
- P2 horizons h = 2, 3, 5 days: mean per-day spread of the average return over d+1..d+h (response windows overlap: NW(5) SE),
  paper sign and flipped.
- P3 one era only: each calendar year inside C1, both signs.
- P4 re-translation pointed to by the Phase-1 assumption check: -correlation(log(close/close.shift(1)), log volume, 10): returns instead of price level, both signs.
- P5 the named rival: 10-day return log(close/close.shift(10)), both signs.
**Bar for a pointer:** |mean| >= 20 bp/day AND |t| >= 2.5 (stricter than 1.645 because ~15 looks are taken here).
**Outcome rule:** if one or more pointers clear the bar, the one with the largest |t| becomes ONE new child hypothesis in
BELIEFS.md (born_on C1 cell_11; seen_on = none unless another slice was shown), with its own rule file before any
test; if none clears it, the finding is "absent everywhere looked" and no child is spawned (DECISIONS D13).
