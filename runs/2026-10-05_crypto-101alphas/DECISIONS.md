# DECISIONS — unattended defaults (each is a question a human would have been asked; the CONSERVATIVE default was taken)

Run started 2026-10-05 14:26 UTC (TARGET.md read, STATUS READY). Cloud run: every C:\Users\User\<x> path read as /home/user/<x>.

**D0 — Mode.** TARGET.md `SOURCE_MODE: B` is set explicitly, so autopick did NOT run (RUNBOOK_v3 MODE SELECTION). Item used:
INBOX.md §B entry 1 `1601.00991v3.pdf` (Kakushadze, "101 Formulaic Alphas", 2015), local file, read with `pdftotext -layout`
(no browser, no page loads). MODES.md counts read for the record: A 0, B 0, C 0, D 0, E 2. One mode only.
Holdout rule for sources: the paper's sample is US equities 2010-01-04..2013-12-31 (paper §3) -> predates VAL, no ⚑ flag.
Its reported results (Sharpe, turnover, correlations) are not evidence here and are not used in any prior beyond the
generic base rate in BELIEFS.md anchors.

**D1 — Five alphas exactly as TARGET.md names them** (#101, #42, #2, #6, #4), one Phase-1 candidate each, formulas verbatim
from Appendix A.1 (checked against the extracted text, code/paper.txt lines 452 (#42), 652 (#101) and the #2/#4/#6 lines),
operators per the paper's function list (rank = cross-sectional percentile rank over the coins present that day;
correlation / ts_rank = per-coin time series over the past d days, min_periods = d). No variants, no parameter changes.

**D2 — Verbatim formulas that are price-level dependent in crypto (needs human confirmation).** #42's `rank(vwap - close)`
and `rank(vwap + close)` and #4's `rank(low)` are cross-sectional ranks of PRICE LEVELS / price differences. Across 10 coins
whose prices span ~0.002 (DOGE 2019) to ~60,000 (BTC), these ranks are dominated by the price level, not by the intraday
move (paper: "the denominator weights down richer stocks" — the same is true here, but far more extreme). #101's `+ .001`
is in price units and is not negligible for DOGE (2021-23 price ~0.06-0.7; daily range ~0.005-0.05). DEFAULT: test the
verbatim formulas as the user specified (TARGET.md says "Formulas verbatim from the paper"); flag the scale dependence as a
Phase-1 assumption failure and let the data say whether it matters. A scale-free re-translation would be a new hypothesis
(only via a redirect cell, never a rewrite).

**D3 — new_source on Saturdays.** FTMO rows (7 coins, 2022-01-01 on) carry `new_source=True` after the fixed Saturday gaps
(hours 15/16 and 22/23 UTC). TARGET.md: never take a return across such a row. DEFAULT: a coin's response day is valid only
if all 24 bars exist and none is flagged; so most Saturday response days (signal day = Friday) drop out for FTMO coins
in C3 (and VAL), leaving < 5 coins -> the day is skipped. Conservative (drops data rather than bridging a gap).

**D4 — Daily bar construction** (TARGET.md translation, Binance 1h): open = first hour's open, high/low = max/min, close = last
hour's close, volume = sum(vol) (base units), vwap = sum(quote_vol)/sum(vol). DEFAULT: a day's bar is valid only with >= 20
of 24 hours AND hour 00 and hour 23 present (so open and close really are 00:00 and 24:00 UTC); otherwise the day is NaN
(not filled).

**D5 — Cross-section minimum.** A day enters a cross-sectional statistic only if >= 5 coins have both a signal and a valid
response. EXPLORE (2019 - May 2020) has 5-7 coins; C1-C3 8-10.

**D6 — Lookback buffer for signal inputs.** Signal inputs (Binance OHLCV) may use 40 days before a slice's start so that the
operators are defined from the slice's first day; RESPONSES are taken strictly inside the slice (signal day d, response
ends at d+2 00:00 <= slice end). The buffer days are only ever used as signal inputs, never as an outcome.

**D7 — The economic size condition (supported needs it).** Statistic for every test: mean over days of the next-day
(end of d -> end of d+1) primary-price return of the TOP half of coins by the alpha minus the BOTTOM half (equal weight,
ties = average rank, odd middle coin left out), in bp/day; positive = the paper's sign is right (alpha value = desired
position). Smallest economically meaningful effect = 20 bp/day: TARGET.md round-trip costs are ~19-69 bp (median coin ~45 bp,
24h hold incl. one rollover night); a dollar-neutral long-short that turns each leg over every ~4.5 days pays about
2 legs x 45 bp / 4.5 days = 20 bp/day (the paper's own alphas hold 0.6-6.4 days, median 2.1, so 4.5 days is a lenient,
i.e. low, bar). A significant spread under 20 bp/day is `inconclusive`, never `supported`.

**D8 — Plots.** backtest_engine2/cellplot.py imports seaborn, which is not installed and is not on TARGET.md's
PRE-APPROVED INSTALLS line, so it was not installed. DEFAULT: matplotlib only, with cellplot.py's palette and styling
copied into code/run_lib.py; plots saved to plots/00_<slug>.png (Phase 0) and plots/cell_NN_<slug>.png (cells).

**D9 — Run-specific helper module.** code/run_lib.py holds the guarded loaders, the TARGET.md day/response translation,
the five formulas and the one test statistic. It is specific to this hunt (not a generic eda.py); each cell's own script
(code/cell_NN.py) states its claim and calls it.

**D10 — The judge agent.** RUNBOOK_v3 asks to run the `eda-v3-judge` agent after gate.py passes. This unattended session has
no agent-spawning tool. DEFAULT: not run; the judge's checklist A-F was self-applied and the result is written in REPORT.md;
a human should run the real judge.

**D11 — Phase 0 never shows a hypothesis statistic.** To keep EXPLORE an ordinary (unseen) slice for the five source-born
hypotheses, Phase 0 never computes a forward return conditioned on any of the five alphas or on a cross-sectional sort of
coins: its autocorrelation section uses HOURLY time-series lags only, and its daily-bar section describes signal INPUTS
(open-vs-previous-close gaps, price-level rank crossings) without any outcome. So every H1-H5 has `seen_on: none`.

**D12 — Cell budget for S3.** RUNBOOK_v3 S3 caps "30 test cells". DEFAULT (conservative): every Phase-2 cell (test AND
redirect) counts toward the 30.

**D13 — Redirect children.** A redirect spawns at most one child (the strongest pre-registered pointer), and only if a
pointer clears its pre-registered bar; "absent everywhere" is recorded as the redirect's finding with no child. A redirect
runs after the FIRST refutation of a hypothesis and again only if a later refutation drops it to LOW and the later slice
adds a new place to look (DEFAULT to keep the session inside its cap; RUNBOOK says a redirect follows a refutation of a
sub-claim the hypothesis cannot survive without — here every fold test is the same single sub-claim).

**D14 — Power simulation re-calibrated after cell_01 (written before cell_02's rule; needs human review).** cell_01 (H1 on
C1) realised a Newey-West SE of 32.7 bp for the mean spread; the Phase-1 power simulation (EXPLORE residual pool) assumed
~8.1 bp at noise x1.0 and ~12 bp at x1.5. A NULL calibration on C1 (already opened by cell_01; random half splits of C1's
own next-day returns, no alpha; code/p2_noise_c1.py) gives a median SE of 31.0 bp = **3.83 x** the EXPLORE-pool simulation:
the 2020-21 cross-section (alt season, more coins) is far more dispersed than 2019 - May 2020. Consequences:
(1) cell_01's PRE-REGISTERED weight (supported 10.0, capped from 12.7) stands — gate.py and RUNBOOK forbid editing a result
to change it — but it is OVERSTATED: at the realised noise the same rule has power ~0.16 / alpha 0.05, i.e. a supported
weight ~3.2. H1's posterior after cell_01 (0.656) is therefore too high by roughly that factor in odds (~0.37 at the honest
weight). Flagged in REPORT.md. (2) DEFAULT for every rule file from cell_02 on: power and alpha come from code/power_v2.json
= the same rule evaluated on a normal sampling distribution of the mean spread with SE = (EXPLORE-pool simulated SE at the
slice's size) x (noise scale), noise scale = 1.5 for EXPLORE (its own pool, as before) and the largest measured fold ratio
(3.83, C1) for every CONFIRM fold (C2/C3 not measured — they are unopened; assumed like C1). This is the conservative
direction: lower power -> smaller supported AND closer-to-1 refuted weights. The noise scale only rises if a later opened fold
shows a larger null ratio. (3) The C1 null calibration is a look at C1 returns without any alpha; it is logged in
ACCESS_LOG.md and noted in ATTEMPTS.md but is not a hypothesis test.

**D15 — Fold-specific noise once a fold has been measured (written before cell_09's rule).** cell_08 (H1 on C2) realised SE
10.8 bp where D14 assumed 30.4 bp: C1's noise (2020-21, incl. the DOGE/alt mania of Jan-May 2021) is not typical. A null
calibration on C2 (already opened by cell_08; random splits, no alpha; code/p2_noise_c2.py — its output key says
`C1_random_split_se` by a copy slip, the value is C2's) gives 11.6 bp = 1.47 x the EXPLORE-pool simulation. DEFAULT from
cell_09 on (code/power_v3.json, same normal-sampling method as D14): noise scale = the MEASURED null ratio for a fold that has
been opened and calibrated (C1 3.83, C2 1.47), and the LARGEST measured ratio (3.83) for a fold nobody has opened (C3);
EXPLORE stays x1.5. Keeping C2 at 3.83 would understate C2's power ~3x and make S2 ("beliefs settled") fire on an
artefact of the noise assumption; using the measured value is the accurate choice, and C3 stays on the conservative side.
Cells 01-08 keep the weights their rule files fixed (cell_08's weight is conservative, cell_01's is overstated: D14).

**D16 — Process deviation in cell_10 (operator error, disclosed).** After cell_09 the pick table (code/pick_10.md, also
pasted in cell_10_rule.md) ranked **H6 on C2 first at 7.92 pp**; cell_10 nevertheless ran **H4 on C1 (1.22 pp)** because the
pick was chosen before the refreshed table was read. RUNBOOK_v3 step 1 says to run the largest expected shift. The cell
itself was pre-registered (rule before result, H4's lowest admissible fold, no slice rule broken) and its result stands
(changing it would be worse), but it was not the optimal pick. Consequences: K is one higher than a strict run would have
reached at this point, and the S2 counter is reset (the best pick before cell_10 was 7.92 pp > 3 pp). Next cells return to
the pick order (H6 on C2 next).

**D17 — C3 measured; redirects after every refutation (written before cell_17's rule).** (1) cell_15 opened C3 (H4). Per D15,
a null calibration on C3 (code/p2_noise_c3.py; random splits, no alpha) gives 9.4 bp = 1.15 x the EXPLORE-pool simulation, so
from cell_17 on C3 uses its measured ratio (code/power_v4.json; C1 3.83, C2 1.47, C3 1.15, EXPLORE x1.5). (2) D13's second
clause is relaxed: a redirect cell now follows EVERY refutation while the 30-cell budget allows (cell_16 is H4's second
redirect, on C3), which is closer to RUNBOOK_v3 step 8 than D13 was.

**D18 — H7's seen_on (EXPLORE, C1, C2).** H7's defining statistic is the flipped #42 spread at h = 2. Exactly that number was
displayed on EXPLORE (redirect cell_04, P2 flipped h=2: +9.8 bp/day, t 1.0). On C1 and C2 its first half — the flipped h=1
spread — was displayed by H2's own tests (cell_19: -32.8 flipped; cell_20: +0.4 flipped). The h=2 average shares day d+1
with h=1, so a test of H7 on C1/C2 would re-read a number already on screen. DEFAULT (conservative): seen_on = EXPLORE, C1,
C2, so H7 has NO admissible TRAIN slice; it is reported as a lead needing a fresh slice (TEST is the user's call). It is not
spawned to close slices: no other hypothesis's admissibility depends on it.
