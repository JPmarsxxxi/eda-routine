"""Write cells/cell_NN_rule.md (FIRST) then cells/cell_NN_announce.md for a kind:test cell, BEFORE any code runs on that
slice for that hypothesis. Usage: write_rule.py NN H SLICE  (the pick table is read from code/pick_NN.md)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import run_lib as L
NN, H, SL = int(sys.argv[1]), sys.argv[2], sys.argv[3]
ALPHA = {"H1": "A101", "H2": "A42", "H3": "A2", "H4": "A6", "H5": "A4"}[H]
FORM = {"A101": "((close - open) / ((high - low) + .001))", "A42": "(rank((vwap - close)) / rank((vwap + close)))",
        "A2": "(-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))",
        "A6": "(-1 * correlation(open, volume, 10))", "A4": "(-1 * Ts_Rank(rank(low), 9))"}[ALPHA]
src = json.load(open(os.path.join(L.RUN, "code", "power_h5.json" if H == "H5" else "power.json")))[SL]
x, w = src["x1.5"], src["weights"]
x1 = src.get("x1.0")
pick = open(os.path.join(L.RUN, "code", f"pick_{NN:02d}.md")).read()
win = L.slices()[SL]
rule = f"""hypothesis: {H}
slice: {SL}
kind: test

# cell_{NN:02d} rule — {H} (Alpha#{ALPHA[1:]}) on {SL} ({win[0].date()} .. {win[1].date()} excl.)

**Sub-claim (the one the hypothesis cannot survive without).** On {SL}, the verbatim Alpha#{ALPHA[1:]} = `{FORM}`, computed
from Binance UTC daily bars of day d, sorts coins so that the next-day primary `price` return (end of d -> end of d+1) of
the top half exceeds the bottom half by at least the economic bar of 20 bp/day (DECISIONS D7), with the paper's sign.

**14c menu row + tool.** "X predicts forward Y" / "X is monotone in Y": quantile sort (2 bins, top vs bottom half by the
alpha, equal weight, ties = average rank, odd middle coin out, days with < 5 coins or an all-tied split skipped) of next-day
returns; statistic = mean daily spread (bp/day) with Newey-West(5) SE. Secondary, descriptive only: mean daily Spearman IC.

**Decision rule (pre-committed, three branches).**
- **supported** if mean spread >= 20 bp/day AND t >= 1.645 (size condition AND significance condition);
- **refuted** if mean + 1.645 x SE < 20 bp/day AND t < 1.645 (the economic effect is excluded at one-sided 95% and there is
  no significant positive effect);
- **inconclusive** otherwise (including a significant spread below 20 bp/day — never `supported`).

**Evidence weight (fixed now).** Power simulation (code/p1_power{'_h5' if H == 'H5' else ''}.py): EXPLORE's empirical daily
cross-sectional residuals, resampled at {SL}'s own size (N = {src['N']} signal days{', mean %.1f coins/day' % src['mean_coins'] if 'mean_coins' in src else ' (only the non-degenerate days of #4, code/signal_coverage.md)'}),
random half split + delta, the rule above applied. Result at noise x1.5 (used): **power {x['power']:.3f} at delta = 20 bp/day, false-
positive alpha {x['alpha']:.3f}** (P(refuted | delta=20) {x['ref_alt']:.3f}, P(refuted | null) {x['ref_null']:.3f}).{(' At noise x1.0: power %.3f, alpha %.3f (not used: the lower-power x1.5 numbers are the conservative choice for both weights).' % (x1['power'], x1['alpha'])) if x1 else ''}
alpha floored at 0.005 for simulation resolution -> alpha used {w['alpha_used']:.3f}.
- weight(supported) = power / alpha = {w['supported_raw']:.3f}{' -> CAPPED at 10 (guard b)' if w['supported_raw'] > 10 else ' (within the 10x cap)'}; applied {w['supported']}
- weight(refuted) = (1 - power) / (1 - alpha) = {w['refuted']}
- weight(inconclusive) = 1

**Guard (a).** First test of this sub-claim for {H} on {SL}; no earlier cell in this session tested it here. Different folds are
separate samples, so their weights multiply.
**Guard (b).** Every weight above is within [0.1, 10] after the cap.

**Slice rules.** {H} is source-born (`born_on: SOURCE`, `seen_on: none`); {SL} is not its birth slice, not in seen_on, not yet
opened by {H}{', and is the lowest CONFIRM fold it is still eligible for (no fold shopping)' if SL.startswith('C') else ' (source-born: EXPLORE may be opened once)'}.

**Why this test now (step 1 arithmetic, code/pick.py).**
{pick}
"""
open(os.path.join(L.RUN, "cells", f"cell_{NN:02d}_rule.md"), "w").write(rule)
ann = f"""### Cell {NN:02d} — EDA: {H} Alpha#{ALPHA[1:]} predicts next-day cross-sectional returns on {SL}

**Sub-claim being tested:** {H}: "the top half of coins by `{FORM}` (day d) out-earns the bottom half over end of d -> end of
d+1 by >= 20 bp/day" (see cell_{NN:02d}_rule.md).

**Why it matters to the hypothesis:** it is the hypothesis's only sub-claim; if it is refuted, {H}'s probability drops and a
redirect cell follows (RUNBOOK_v3 step 8).

**Test(s) used:** 2-bin quantile sort of next-day primary returns by the alpha, mean spread with Newey-West(5) SE; Spearman IC
(descriptive).

**Decision rule before running:** "I will consider it **supported** if mean >= 20 bp/day and t >= 1.645; **refuted** if
mean + 1.645 SE < 20 bp/day and t < 1.645; **inconclusive** otherwise." Weights: supported {w['supported']}, refuted
{w['refuted']}, inconclusive 1 (cell_{NN:02d}_rule.md).

**Engine/library APIs used:** pandas rolling corr / rank (paper A.1 operators), numpy; code/run_lib.py (guarded loaders,
`build_panel`, `alpha`, `half_spread_series`, `nw_se`, `decide`); code/cell_test.py.

**Data loaded:** spot/binance_<COIN> (signal inputs, {SL} plus a 40-day lookback buffer) and primary/validated_<COIN>
(responses strictly inside {SL}); guard asserted at every load (ACCESS_LOG.md).

**Decisions I need from you:** none beyond DECISIONS.md D1-D13 (defaults taken, unattended).
"""
open(os.path.join(L.RUN, "cells", f"cell_{NN:02d}_announce.md"), "w").write(ann)
print("wrote rule + announce for cell", NN)
