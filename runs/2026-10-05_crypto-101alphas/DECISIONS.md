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
