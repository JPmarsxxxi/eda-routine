hypothesis: H3
slice: C2
kind: redirect
version: neutral

# cell_06 — RULE (redirect, written before any code for this cell runs)

**Why this cell.** H3 was refuted on C2. RUNBOOK v3.2 Phase 2 step 8: "where does the data actually point?" This cell
looks only at C2, which H3 has already opened (a redirect may never look at a fold the hypothesis has not opened, and this
run does not let it look at EXPLORE either unless H3 opened it, so no later test of H3 re-reads a number). Parent cell_05: refuted, IC -0.0192 on C2.

**What it computes (same code as the test, `code/cell_run.py`, on the SIGN-FLIPPED alpha):** the flipped mean daily IC and its
D7 branch; the raw version; the IC net of 1-day reversal; the two halves of C2.

**Pre-committed spawn rule.** A NEW child hypothesis "-1 x A38 (the opposite sign)" is written into BELIEFS.md iff the
flipped statistic is `supported` by D7 on C2 (flipped x >= 0.02 and t >= 1.645): born_on C2 cell_06; seen_on = every
other slice where H3 already displayed this IC (the flipped IC is minus the parent's); prior from the same anchor. Otherwise
the finding is recorded as "no clear opposite-sign effect on C2" with the halves / net-of-reversal numbers, and no child.
Weight applied to H3: 1 (a redirect never moves the parent).
