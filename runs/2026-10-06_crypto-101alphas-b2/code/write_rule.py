"""Write cells/cell_NN_rule.md and cell_NN_announce.md BEFORE the cell runs. Usage:
    python write_rule.py NN HYP ALPHA SLICE KIND [SIGN] [WHY...]
The decision rule is D7 (fixed for the whole run); weights come from tables/power.csv (D10). A redirect cell carries
weight 1 and a pre-committed spawn rule instead."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
import common as C

nn, hyp, alpha, sl, kind = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
sign = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
why = " ".join(sys.argv[7:]) if len(sys.argv) > 7 else ""
pw = pd.read_csv(os.path.join(C.RUN, "tables", "power.csv"))
row = pw[(pw.alpha == alpha) & (pw.slice == sl)].iloc[0]
name = f"{'-1 x ' if sign < 0 else ''}Alpha#{alpha[1:]}"
a, b = C.SLICES[sl]
pick = os.path.join(C.RUN, "tables", f"pick_{nn:02d}.txt")
pick_txt = open(pick).read().strip() if os.path.exists(pick) else "(no pick file: this cell is not a step-1 pick)"
cap_s = "capped" if row.w_sup_raw > 10 else "not capped"
cap_r = "capped" if row.w_ref_raw < 0.1 else "not capped"

head = f"hypothesis: {hyp}\nslice: {sl}\nkind: {kind}\nversion: neutral\n\n"
if kind in ("test", "val"):
    body = f"""# cell_{nn:02d} — RULE ({kind}, written before any code for this cell runs)

**Sub-claim.** On {sl} (signal days {a} .. {b}, response window inside the slice), {name} computed from Binance daily
OHLCV (D2, D4) has a mean daily cross-sectional Spearman IC with the next-day primary return of at least MIN_USEFUL_IC = 0.02
in the stated direction (claim version `neutral`, DECISIONS D7). {why}

**14c menu row + tool.** "X predicts forward Y" -> IC at the stated horizon (1 day): daily cross-sectional Spearman IC across
the coins present (>= 5), mean over days, Newey-West(5) SE (`code/common.py::daily_rank_ic`, `summarize`).

**Decision rule (fixed now, D7).** x = mean daily IC, se = its NW(5) SE.
- supported if x >= 0.02 AND x / se >= 1.645;
- refuted if x + 1.645 se < 0.02 (a useful effect in the stated direction is excluded);
- inconclusive otherwise, or if fewer than 150 valid days.
Cost does not enter the branch (RUNBOOK v3.2).

**Evidence weights (fixed now, D10; `tables/power.csv`, row {alpha} / {sl}).** Simulation's own result: daily IC sd
{row.sd_ic_slice:.3f} (measured EXPLORE day-permutation null {row.sd_ic_explore_null:.3f}, lag-1 autocorr {row.ar1_explore_null:+.3f},
scaled to {row.coins_median:.0f} coins/day), {row.n_days:.0f} days, 3,000 runs: P(supported | IC 0.02) = power = {row.power:.3f},
P(supported | IC 0) = alpha = {row.alpha_size:.3f}; P(refuted | 0.02) = {row.P_ref_H1:.3f}, P(refuted | 0) = {row.P_ref_H0:.3f}.
- weight(supported) = power / alpha = {row.w_sup_raw:.3f} ({cap_s}) -> **{row.w_sup:.3f}**
- weight(refuted) = P(ref|0.02) / P(ref|0) = {row.w_ref_raw:.3f} ({cap_r}) -> **{row.w_ref:.3f}**
- weight(inconclusive) = 1
Guard (a): no earlier cell tested this sub-claim on {sl} for {hyp} (slice rule 2, checked by gate.py). Guard (b): applied above.

**Pre-registered descriptives (do not decide the branch):** `raw` version (own-return prediction incl. market, trailing
scaling); IC net of 1-day reversal (alpha ranks residualised on b_rev1 ranks each day) and b_rev1's own IC on this slice
(OBSERVATIONS #1); top-half minus bottom-half spread bp/day, daily half-membership turnover and the cost per day it implies
(D11); the signal's correlation with the same-day panel and BTC return (market share); IC by half of the slice.

**Step-1 pick arithmetic.**
```
{pick_txt}
```
"""
else:
    body = f"""# cell_{nn:02d} — RULE (redirect, written before any code for this cell runs)

**Why this cell.** {hyp} was refuted on {sl}. RUNBOOK v3.2 Phase 2 step 8: "where does the data actually point?" This cell
looks only at {sl}, which {hyp} has already opened (a redirect may never look at a fold the hypothesis has not opened, and this
run does not let it look at EXPLORE either unless {hyp} opened it, so no later test of {hyp} re-reads a number). {why}

**What it computes (same code as the test, `code/cell_run.py`, on the SIGN-FLIPPED alpha):** the flipped mean daily IC and its
D7 branch; the raw version; the IC net of 1-day reversal; the two halves of {sl}.

**Pre-committed spawn rule.** A NEW child hypothesis "-1 x {alpha} (the opposite sign)" is written into BELIEFS.md iff the
flipped statistic is `supported` by D7 on {sl} (flipped x >= 0.02 and t >= 1.645): born_on {sl} cell_{nn:02d}; seen_on = every
other slice where {hyp} already displayed this IC (the flipped IC is minus the parent's); prior from the same anchor. Otherwise
the finding is recorded as "no clear opposite-sign effect on {sl}" with the halves / net-of-reversal numbers, and no child.
Weight applied to {hyp}: 1 (a redirect never moves the parent).
"""
open(os.path.join(C.RUN, "cells", f"cell_{nn:02d}_rule.md"), "w").write(head + body)
ann = f"""### Cell {nn:02d} — EDA: {name} on {sl} ({kind})

**Sub-claim being tested:** see `cells/cell_{nn:02d}_rule.md` ({hyp}, {sl}, version neutral).

**Why it matters to the hypothesis:** {"each fold is a separate piece of evidence; HIGH-CONFIRM needs every allowed fold opened and none refuted" if kind == "test" else ("the VAL check for a HIGH-CONFIRM hypothesis; VAL_NOTE applies" if kind == "val" else "the mandatory redirect after a refutation")}.

**Test(s) used:** daily cross-sectional Spearman IC vs next-day primary return, NW(5) SE; descriptives listed in the rule file.

**Decision rule before running:** {"D7, as written in the rule file (supported / refuted / inconclusive with numbers)." if kind != "redirect" else "the spawn rule in the rule file."}

**Engine/library APIs used:** pandas rank/corr, numpy lstsq; `code/common.py`, `code/cell_run.py`.

**Decisions I need from you:** none (unattended; defaults in DECISIONS.md).
"""
open(os.path.join(C.RUN, "cells", f"cell_{nn:02d}_announce.md"), "w").write(ann)
print(f"wrote rule + announce for cell_{nn:02d}")
