# DECISIONS — unattended defaults (each is a question a human would have been asked; the CONSERVATIVE default was taken)

Run started 2026-10-06 10:22:18 UTC (`tables/run_start_utc.txt`; TARGET.md STATUS READY). Cloud run: every C:\Users\User\<x>
path is read as /home/user/<x>. Method files read in full first, and only the allowed ones (sparse checkout of the user's
public repos): backtest_engine2/PROTOCOL.md, skills/00-overview.md, 12-alpha-overview.md, 14c-eda.md, cellplot.py,
data_hygiene.py; finding-alphas/data-hygiene.md. Nothing else in either repo is on disk.

**D0 — Mode.** TARGET.md `SOURCE_MODE: B` is set explicitly: autopick did not run. Item used: INBOX.md §B entry 2 (the local
paper 1601.00991v3.pdf, Kakushadze "101 Formulaic Alphas", SECOND batch). MODES.md counts read for the record: A 0, B 1, C 0,
D 0, E 2. One mode only. The paper was read from its text (`pdftotext -layout`), no browser, no page loads. Holdout rule for
sources: the paper's sample is US equities 2010-2013 -> predates VAL, no ⚑. Its reported results (Sharpe, turnover,
correlations) are not used in any rule or prior beyond the generic base rate in BELIEFS.md anchors.

**D1 — Operator disclosure (needs a human to weigh).** This session was run by the user's assistant, who, before the run
started and while fixing the routine, read the REPORT.md / STOP_REASON.md / BELIEFS.md summary lines of the two earlier
2026-10-05 runs (to diagnose the v3.1 fold bug). Those runs tested different claims (first-batch alphas #101 #42 #2 #6 #4;
perp premium, Fear & Greed, S&P spillover) on the same bundle. What was seen and could leak: their SPLITS cut points (a
similar equal-coin-day rule — this run derived its own from its own counts, `tables/p0_00_coin_days_by_quarter.csv`), that
first-batch #101 was strong in 2020-22 and gone in VAL, and that price-level ranks were a problem in #42/#4. The last point is
WHY this batch was chosen to be scale-free (TARGET.md). No number from those runs is used in any rule, prior or weight here.
Runs folders other than this one were not opened during this run.

**D2 — Five alphas exactly as TARGET.md names them** (#30, #35, #38, #53, #54), one Phase-1 candidate each, formulas verbatim
from Appendix A.1, operators per A.2: rank = cross-sectional percentile rank over the coins present that day; delay / delta /
sum / Ts_Rank = per-coin time series over the past d days (min_periods = d); returns = daily close-to-close. Ts_Rank(x, d) =
share of the last d values <= today's (in (0, 1]). Code: `code/common.py::alpha30..alpha54`.

**D3 — Responses.** r(d) = ln(primary price at end of d+1 / at end of d), primary/validated_<COIN> `price` only (TARGET.md).
Valid only if the bar ending d exists and day d+1 has all 24 bars with no `new_source=True` among them (TARGET: never take a
return across such a row). Consequence: FTMO coins (from 2022-01-01) lose the days after their fixed Saturday gaps — data
dropped, never bridged.

**D4 — Daily bars for signals** (TARGET.md translation, Binance 1h): open = first hour's open, high/low = max/min, close = last
hour's close, volume = sum(vol) (base units). Valid only with >= 20 of 24 hours AND hours 00 and 23 present; else NaN.

**D5 — Cross-section minimum.** A day enters a statistic only if >= 5 coins have both a signal and a valid response.

**D6 — Lookback buffer.** Signal inputs may use up to 40 days before a slice's start; responses never leave the slice.

**D7 — The decision rule (RUNBOOK_v3 v3.2: supported = REAL, not tradeable).** Claim version = `neutral`: the statistic is the
mean over days of the daily cross-sectional Spearman IC between the alpha and the next-day response (a cross-sectional rank IC
is market-neutral by construction: subtracting the panel return from every coin does not change ranks), Newey-West(5) SE.
Sign: the paper's alpha value is the desired position, so a positive IC means the paper's sign is right. With x = mean IC:
- **supported** if x >= MIN_USEFUL_IC (0.02, TARGET.md) AND x / se >= 1.645;
- **refuted** if x + 1.645 se < 0.02 — the data exclude a useful effect in the paper's direction (this includes a significant
  effect of the opposite sign);
- **inconclusive** otherwise, or fewer than 150 valid days in the slice.
Cost never enters the branch. The `raw` version (own-return prediction including the market, `common.daily_ts_ic`) and the
top-half-minus-bottom-half spread in bp/day are pre-registered descriptives in every cell.

**D8 — Plots.** backtest_engine2/cellplot.py imports seaborn, which is not on TARGET.md's PRE-APPROVED INSTALLS, so it was not
installed. Default: matplotlib only, with cellplot.py's palette (PAL, GRAY) copied into `code/common.py`, saved to `plots/`.

**D9 — Division hazards.** #53 divides by (close - low): when close == low the ratio is undefined; set NaN (the coin sits out
that day), never +-inf. #54 divides by (low - high) * close^5: NaN when high == low. Counts of such cases are reported in
DATA_PROFILE.md §1.

**D10 — Evidence weights for a three-branch rule.** RUNBOOK_v3's formulas weight(supported) = power / alpha and
weight(refuted) = (1 - power) / (1 - alpha) are the likelihood ratios of a TWO-branch rule (supported vs not). This rule has a
separate refute region, so each weight is computed as the likelihood ratio of its own branch from the same simulation:
w(b) = P(b | true IC = 0.02) / P(b | true IC = 0); `power` = P(supported | 0.02) and `alpha` = P(supported | 0), so
w(supported) is exactly power / alpha. w(inconclusive) = 1 (runbook). Cap: [0.1, 10] (guard b). Noise: the daily-IC sd and
lag-1 autocorrelation are MEASURED on EXPLORE from a day-permutation null of each alpha (signal days shuffled against response
days, so the measured spread is the alpha's own noise with any real effect destroyed), and scaled to each slice's day count
(`code/power.py`, `tables/power.csv`). (RUNBOOK v3.2 Phase 2 step 2: noise measured, not assumed.)

**D11 — The cost line (descriptive only; SIGNALS.md label, never a branch).** A long-short book holding the top half against
the bottom half, rebalanced daily, trades a fraction f (the daily half-membership turnover) of each leg and holds every name
overnight. With the TARGET.md median-coin round trip RT = 45 bp for a 24h hold INCLUDING one 8.2 bp rollover night, the cost
per day in the same units as the top-minus-bottom spread is 2 legs x (f x (RT - 8.2) + 8.2). STANDALONE iff the spread clears
it; otherwise COMBINE-ONLY.

**D12 — Redirect scope.** A redirect looks only at the slice its refuted parent just opened (or another slice the parent already
opened), never at EXPLORE or a fold the parent has not opened, so no later test of the parent re-reads a number. Its
pre-committed spawn rule: a sign-flipped child iff the flipped statistic is `supported` by D7 on that slice.
Cached daily panels (tables/_daily_*.parquet, tables/_response.parquet) were deleted before commit: they are copies of the bundle (responses include VAL rows) and are rebuilt by `code/p0_build.py`.
