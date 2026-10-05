hypothesis: H1
slice: C1
kind: redirect

# cell_02 rule — mandatory redirect after H1's refutation on C1 (RUNBOOK_v3 Phase 2 step 8)

H1 was refuted on C1 (cell_01). This cell asks "where does the data actually point?" on C1 only — a slice H1 has already
opened (allowed for a redirect). It carries **weight_applied 1** and does not move H1. Its finding, if any, becomes a NEW
child hypothesis born on C1 with its own rule file.

**Fixed menu of five looks (no others will be run), all on C1, same block grid and validity rules as cell_01:**
- R1 opposite sign: is the 72h top-minus-bottom spread significantly POSITIVE (t >= +1.645)?
- R2 horizon: 24h tercile spread on a non-overlapping daily grid (cost bar T24 = 2 x mean RT24 = 89.0 bp).
- R3 dispersion: 72h spread in blocks where the cross-sectional premium range (max - min) is above C1's median range vs
  below (t of each half; bar 121.8 bp).
- R4 extremes: single highest-premium coin minus single lowest-premium coin, 72h (bar 121.8 bp).
- R5 era: first half of C1 blocks vs second half (bar 121.8 bp).

**Spawn rule (pre-committed):** a child hypothesis is written only for a look with |t| >= 2.5 (five looks, ~Bonferroni at
0.05 one-sided) AND an effect that clears that look's cost bar in H1's direction (or, for R1, in the opposite direction).
If none qualifies, the redirect reports "absent everywhere on C1" and spawns nothing.

**Branch line for the result file:** a redirect is recorded as `branch: inconclusive`, `weight_applied: 1` whatever it
finds (no evidence weight is applied by a redirect).
