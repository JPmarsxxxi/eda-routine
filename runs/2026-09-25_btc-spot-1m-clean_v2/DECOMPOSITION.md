# DECOMPOSITION (14c Step 1) and TOOLS (14c Step 2)

## Hypothesis
TARGET.md HYPOTHESIS, verbatim: `SEARCH`. Step 1 (DECISIONS.md items 6-9) produced ONE sentence, used verbatim from here on:

> **H: a change in `close` over the first half-hour of the UTC day (r_first = ln[last `close` in 00:00-00:29 of day d /
> last `close` in 23:30-23:59 of day d-1]) predicts the SAME-SIGN return over the last half-hour of that day
> (r_last = ln[last `close` in 23:30-23:59 of d / last `close` in 23:00-23:29 of d]), because late-informed investors trade
> near the daily close in the direction of the day's early information (and infrequently-rebalancing investors trade the
> same way).**
> Source: Wen, Bouri, Xu & Zhao (2022), "Intraday Return Predictability in the Cryptocurrency Markets: Momentum, Reversal,
> or Both", SSRN 4080253, BTC 2013-03-03..2020-05-31 (momentum leg only); definition and mechanism from Gao, Han, Li & Zhou,
> "Market Intraday Momentum", SSRN 2440866, SPY 1993-2013.

Price at the end of a half-hour = the `close` of the LAST bar present in that half-hour (a backward-looking "last" resample,
data-hygiene rule 9; stated, not silent). A half-hour with no bar gives NaN; a day missing any needed anchor is dropped.
r_first is knowable at 00:30 of d; r_last starts at 23:30 of d: 23 hours apart, no shared bar.

## Sub-claims

| # | Sub-claim | Falsifiable by |
|---|---|---|
| C1 | Existence: r_first and r_last exist and vary on enough TRAIN days | refuted if usable TRAIN days < 1,500 of ~2,041, or share of days with r_last == 0 exactly > 5% outside 2017, or std(r_first) = 0 in any era |
| C2 | Assumption: the UTC day boundary is a focal "close" around which trading concentrates (the late-informed / rebalancing story needs a close) | mean share of daily `vol` in 23:30-23:59 and in 00:00-00:29, each / the median half-hour share; supported if either ratio >= 1.20 with Wilcoxon p < 0.05; refuted if both ratios <= 1.00 |
| C3 | Impostor: the effect is special to the 00:00 UTC boundary, not a generic "30-min return predicts the 30-min return 23 h later" autocorrelation at any clock time | slope at the true boundary vs 23 placebo boundaries shifted by 1..23 h; refuted if the true slope is not in the top 4 of the 24 (below the ~83rd percentile) |
| C4 | Attribution: it is the FIRST half-hour that carries the information, not the rest of the day (r_mid = 00:30-23:30 return, everything between the two legs) | joint regression r_last ~ r_first + r_mid; refuted if r_first's NW t < 1.0 while r_mid's NW t >= 2.0 |
| C5 | The effect: r_first predicts r_last with positive sign, at the last half-hour | OLS slope with Newey-West (5 lags) t; Spearman IC; sign hit rate; supported if slope > 0, NW t >= 2.0 and Spearman p < 0.05; refuted if slope <= 0 or NW t < 1.0 |
| C6a | Side bet (source): predictability is stronger on more volatile and higher-volume days (more late information) | slope in top vs bottom tercile of first-half-hour realised vol and of first-half-hour `vol`; supported if top > bottom in both with bootstrap p < 0.10; refuted if top <= bottom for BOTH splits |
| C6b | Side bet (mechanism): if late-informed traders push the close, last-half-hour aggressor flow leans the way r_first points | share of days where sign(buy_vol - sell_vol over 23:30-23:59) == sign(r_first); supported if > 50% with binomial p < 0.05; refuted if <= 50.0% |
| C7 | Shape: monotone across r_first quintiles, not carried by one tail | quintile means of r_last; supported if Q5 > Q1, >= 3 of 4 steps rising, and the slope stays > 0 with NW t >= 1.5 after dropping the top/bottom 1% of r_first; basis fit [1, x, x·abs(x)] vs [1, x] by MSE |
| C8 | Stability (decay-first gate): the slope is not monotone-decaying and not alternating across TRAIN eras | era slopes / NW t over 5 eras (2017-08..2018-12, 2019, 2020, 2021, 2022-01..2023-03-19); numeric rules in the C8 announcement |
| C9 | Economics: effect is the same order as the round trip | mean sign(r_first)*r_last in bp vs cost; cost UNKNOWN -> UNTESTED |
| C10 | Replication (VAL, opened once) | see below |
| C11 | Data-specific: the result is not produced by gap handling or the thin 2017 market | slope on days whose anchors are all exact :29/:59 bars, and slope excluding 2017; refuted if either has NW t < 1.0 while the full sample passes C5 |

## The decomposition floor (14c)
1. Existence -> C1. 2. Assumption -> C2. 3. Impostor -> C3 (placebo boundaries: generic lagged autocorrelation / trailing
return at any clock time). Volatility as impostor: a sign-prediction claim cannot be produced by volatility clustering alone,
but outlier days can dominate an OLS slope; covered by C7's tail trim. Price-level impostor N/A (returns only). 4. Attribution
-> C4. 5. Effect -> C5. 6. Side bets -> C6a (the source's own), C6b (something the correlation alone does not require).
7. Shape -> C7. 8. Stability -> C8 (run BEFORE the pooled C5 number is read: part-0, never pooled first). 9. Economics -> C9,
UNTESTED (cost unknown). 10. Replication -> C10 (out-of-period). Out-of-symbol replication DROPPED: no other asset was given.
Claim-specific rows beyond the floor: C3's placebo-boundary test (is a day boundary special at all in a 24 h market?), C11
(gap handling / thin 2017 market).

C6b uses the aggressor split (buy_vol/sell_vol) only as a MECHANISM check on the last half-hour, not as a predictor. It is not
the ALREADY TESTED "flow-imbalance" claim (DECISIONS.md item 10).

Execution / kill order: C1 -> C2 -> C8 (era-by-era first) -> C5 -> C3 -> C4 -> C7 -> C11 -> C6a -> C6b -> C9 -> update cell -> C10.
C1 refuted -> stop. C8 monotone-decay or alternating -> stop. C5 refuted -> stop. C3 refuted -> the "because of the daily
close" story fails -> stop (net (c) as stated; the generic pattern goes to Observations). C2 refuted -> not a stop by itself,
but net status cannot be (a). C4/C6/C7/C11 refuted -> narrows or flags, stated in the update cell.

## Replication row, declared BEFORE any test (C10)
VAL (2023-03-25 .. 2023-11-30) is opened ONCE, and only if C5 is supported on TRAIN and C8 does not kill. Test: the C5
regression on VAL days, same definitions. **Replicates** if slope > 0 and NW t >= 1.65 (one-sided 5%); **fails** if
slope <= 0; **inconclusive** otherwise. Sign hit rate reported beside it. Quoted with TARGET.md's VAL_NOTE. Never called
out-of-sample proof. If the hunt stops before C10, VAL stays closed.

## Tools (14c Step 2). Every tool in the matching menu row is run, or marked N/A with a reason.
| sub-claim | claim type (menu row) | tools |
|---|---|---|
| C1 | "Outliers exist beyond data_clamp" (coverage part) | gap detection on anchors (dropped days, anchors not on the exact :29/:59 bar), flag-count summary on used days; run-length of clipped bars N/A (no clamp applied) |
| C2 | "Distribution differs between groups" | boundary half-hour share vs median half-hour share per day: Wilcoxon signed-rank (paired twin of Mann-Whitney), Mann-Whitney, Welch t, KS |
| C3 | "X predicts forward Y" (lead-lag) | OLS slope + Pearson/Spearman IC at every one of 24 boundaries |
| C4 | "X predicts forward Y" | joint OLS with NW t; single-leg ICs |
| C5 | "X predicts forward Y" | Pearson and Spearman IC at tau in {1, 5, 20} half-hours ending 24:00 (tau=1 is the claim); lead-lag cross-correlation of r_first with every later half-hour 2..48; OLS slope with NW t; sign hit rate (binomial) |
| C6a | "Distribution differs between groups" + "X predicts forward Y" | tercile slopes; bootstrap of the top-minus-bottom slope (2,000 reps); Welch t / Mann-Whitney / KS on sign(r_first)*r_last, top vs bottom |
| C6b | "Distribution differs between groups" | binomial test on sign agreement; Mann-Whitney / Welch / KS on last-half-hour imbalance, r_first>0 vs r_first<0 days |
| C7 | "X is monotone in Y" (+ fat tails, as far as the trim needs) | quintile sort; lstsq on basis [1,x] vs [1,x,x·abs(x)] judged by MSE and np.allclose; tail-trimmed slope; kurtosis + D'Agostino normaltest on r_first to justify the trim. Hill / VaR curve N/A (no tail-risk claim) |
| C8 | "RELATIONSHIP stable / drifts" + "X has regime changes" | era slopes; rolling 365-day slope; Chow test at each era boundary; OLS-CUSUM (statsmodels breaks_cusumolsresid). Bayesian random-walk beta SKIPPED (PyMC not installed, no pre-approval). Markov-switching N/A (the claim is about one slope; rolling + Chow + CUSUM cover drift) |
| C9 | economics | cost UNKNOWN -> UNTESTED; effect size in bp reported |
| C11 | "Outliers exist beyond data_clamp" | C5 slope re-run on exact-anchor days and on 2018+ days |
