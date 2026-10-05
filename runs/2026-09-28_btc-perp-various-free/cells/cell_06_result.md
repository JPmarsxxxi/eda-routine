# cell_06 RESULT — H5 CONFIRM opening

Script `scripts/cell_06_h5_confirm.py`; tables `tables/06_result.json`, `tables/06_by_quarter.csv`, `tables/06_by_abs_tercile.csv`;
plot `plots/06_h5_confirm.png`. Slice: CONFIRM, n = 10,629 consecutive-hour pairs.

**Branch fired: SUPPORTED.** Deciding number: Spearman(r_t, r_{t+1}) = **-0.0640** (block-bootstrap SE 0.0084), below the -0.01526
critical value. EXPLORE pooled was -0.078.

**Weight applied:** power/alpha = 0.946/0.05 = 18.9 -> **capped to 10** (guard b). H5 odds 0.20/0.80 = 0.25 x 10 = 2.5 ->
**posterior 0.714**. State: OPEN (0.05 < 0.714 < 0.85). It did not reach HIGH.

Unweighted rivals / stability / economics (reported, not scored):
- 1% largest |r_t| hours removed: -0.0654 (unchanged), so the rank reversal is not a few crash hours.
- By quarter (decay-first): -0.066, -0.038, -0.044, -0.133, -0.056 (2022Q1..2023Q1). Negative in all five quarters, no fade.
  (EXPLORE alternated in sign by era; CONFIRM does not.)
- Mechanism side bet: reversal is NOT stronger after the largest hours: by |r_t| tercile -0.010 / -0.066 / -0.066 (low / mid / high).
  The bottom tercile has almost none. Reversal after mid and large moves is equal.
- **Pearson (linear) correlation is +0.005 while the rank correlation is -0.064.** The reversal lives in the ranks, i.e. in
  the ordering of moderate moves, not in the size-weighted return. Consistent with that, the naive strategy-shaped statistic
  mean(-sign(r_t) x r_{t+1}) is **-0.44 bp per hour over all 10,629 hours**: fading each hour loses on average before any cost,
  presumably because the largest moves do not reverse. On the 3,446 hours that have a half-spread row (32% coverage, not a
  random subset) the mean gross is +1.48 bp and net of the trade-hour round trip (median 0.17 bp; venue of half_bp unstated)
  +1.27 bp, but that subset cannot be generalised to all hours.

So the CONFIRM finding is a real, stable rank-order reversal that the size-weighted return does not show and that is not, as
measured here, a profitable rule. Deciding number and weight follow the pre-committed rule; the economic caveat stands beside it.

**Spawn (step 7):** the rank/Pearson split and the covered-hours gross suggest two questions; neither can be tested on a fresh
slice (both were born on CONFIRM and CONFIRM was H5's one opening): (a) "reversal confined to non-extreme hours, continuation in
extremes", (b) "half-spread coverage marks a different regime". Recorded as leads, not hypotheses. The Phase 0 observation #10
(basis change leans against next-hour spot) is the rival to H5 that EXPLORE already supplied; it enters as child H6 (own rule file).
