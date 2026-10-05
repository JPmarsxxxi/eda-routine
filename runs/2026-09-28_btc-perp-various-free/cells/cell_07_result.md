# cell_07 RESULT — H6 CONFIRM opening

Script `scripts/cell_07_h6_confirm.py`; tables `tables/07_result.json`, `tables/07_by_quarter.csv`; plot `plots/07_h6_confirm.png`. Slice: CONFIRM, n = 10,628.

**Branch fired: SUPPORTED, thinly.** Deciding number: partial Spearman(d_basis_t, r_{t+1} | r_t) = **-0.0188** (block-bootstrap SE 0.0089),
past the -0.0168 critical value by 0.002. EXPLORE was -0.033.

**Weight applied:** power/alpha = 0.903/0.05 = 18.1 -> **capped to 10** (guard b). Odds 0.15/0.85 = 0.1765 x 10 = 1.765 -> **posterior 0.638**. State OPEN.

Unweighted (reported, not scored), and they argue for caution:
- Controlling r_{t-1} as well: -0.0161; 1% largest |d_basis| removed: -0.0164. Both sit just above the critical value, so the pass is fragile.
- Unpartialled Spearman is -0.0094: the effect appears only after r_t is removed, i.e. it is a small residual of an r_t-contaminated series.
- By quarter (decay-first): -0.012, -0.058, -0.013, +0.015, -0.013. One quarter (2022Q2) carries most of it; 2022Q4 has the wrong sign.
- Economics: mean gross of -sign(d_basis) x r_{t+1} is +0.85 bp/h over all 10,628 hours; on the 3,446 hours with a half-spread row it is -0.39 bp
  gross and -0.60 bp net (median round trip 0.17 bp). Not a usable rule on the covered subset.

Reading: H6 passes its pre-committed rule by a small margin, but the rivals (H5 impostor, one-quarter concentration) are not clearly excluded.
Weight and posterior follow the rule; the fragility is noted beside the number. No spawn: any follow-up (quarter concentration) was born on CONFIRM and H6 has no second opening.
