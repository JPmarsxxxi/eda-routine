# TOOL LOG: 14c Step-2 sweep, TRAIN only (2017-08-17 -> 2023-03-19)

Conventions for every row: r = 1-minute close-to-close log return on trade prints, kept only where `gap_min == 1`.
Forward returns start at the close of bar T+1 (one full bar skipped after the bar that makes X knowable), and are NaN
if any minute in the window is missing. Eras = calendar years 2017 (Aug-Dec), 2018 ... 2022, 2023Q1.
Every p-value is written to tables/pvals_registry.csv; K = its row count (Step 4c).

## Pre-declared rules ("counts as an observation if ..."), written BEFORE any sweep script was run

| NN | 14c row | tool / series | counts as an observation if ... |
|---|---|---|---|
| 01 | 1 stationary / mean-reverting | ADF, KPSS, Phillips-Perron on daily log close (level) and on 1-min r | the level REJECTS a unit root (ADF/PP p < 0.01) or KPSS and ADF disagree on r; a level that is I(1) and returns that are I(0) is the null picture, not an observation |
| 02 | 1 | Lo-MacKinlay variance ratio (heteroskedasticity-robust z*) of 1-min r, q = 2, 5, 15, 60, 240, by era | pooled |z*| > 3 at some q AND the same sign of VR-1 in >= 5 of 7 eras |
| 03 | 1 | AR(1) on 1-min r and on 60-min r (OU half-life from AR(1) where coefficient in (0,1)), by era | |phi| has the same sign in >= 5 of 7 eras AND |t_HAC| > 3 pooled |
| 04 | 1 + 2 long memory | Hurst exponent (aggregated-variance on r, and R/S on |r|), by era | H of r outside [0.45, 0.55] in >= 5 of 7 eras (H of |r| > 0.5 is expected vol clustering, logged but it is the row-5 claim) |
| 05 | 2 momentum | ACF / PACF of 1-min r, lags 1..60, by era | any lag other than 1 with |ACF| > 5 x (1/sqrt(n)) in >= 5 of 7 eras with the same sign |
| -- | 3 cointegration | Engle-Granger / Johansen | (N/A, see below) |
| 06 | 4 fat tails | kurtosis, Hill tail index (top 1%), Q-Q vs normal, D'Agostino-Pearson, VaR curve (empirical vs fitted normal) on 1-min r and 60-min r | not an observation by itself (fat tails in 1-min crypto are the null); logged as a fact. Observation only if the LEFT and RIGHT Hill indexes differ by > 0.5 with non-overlapping bootstrap 95% CIs |
| 07 | 5 heteroskedasticity | ARCH-LM (lags 60) on 1-min r; ACF of |r| and r^2 lags 1..1440; rolling 1-day std | logged as a fact (the null for crypto). Observation if ACF(|r|) at lag 1440 (same minute next day) exceeds ACF(|r|) at lag 720 by > 0.02 in >= 5 of 7 eras (a daily periodicity in size) |
| 08 | 6 regime changes | rolling 30-day mean/std of daily r; OLS-CUSUM on daily r; Chow test on daily r at 2020-01-01 (mid-TRAIN, chosen blind); 2-state Markov switching-variance on daily r | CUSUM crosses its 5% band, or Chow p < 0.01 on the MEAN, or the Markov high-vol state has a different mean with |t| > 3 |
| 09 | 7 relationship stability | rolling monthly AR(1) coefficient of 1-min r and rolling monthly slope of fwd 5-min r on taker imbalance; Chow test of each at 2020-01-01 | the coefficient changes SIGN between eras with Chow p < 0.01 (a drifting relationship) |
| 10 | 8 X predicts forward Y | Spearman IC at tau = 1, 5, 20 min, X in {trailing 1-min r, trailing 5-min r, taker imbalance (buy_vol/vol - 0.5), 5-min mean imbalance, log trade-count change}, Y = fwd return; X = trailing 5-min |r|, Y = fwd |r|; lead-lag cross-correlation imbalance vs r, lags -10..+10 | |IC| > 0.01 with HAC |t| > 3 pooled AND the same sign in >= 5 of 7 eras (direction claims); for size, IC > 0.1 is expected (vol clustering) and is logged, not an observation |
| 11 | 9 time-of-day / day-of-week | mean hourly r and mean |r| by UTC hour; mean daily r and |r| by weekday; Kruskal-Wallis across groups (on hourly / daily sums) | KW p < 0.001 AND the top/bottom group keeps its rank sign (above / below the grand mean) in >= 5 of 7 eras |
| 12 | 10 monotone | decile sorts of fwd 5-min r by taker imbalance and by trailing 5-min r; decile sort of fwd 60-min |r| by trailing 60-min |r|; lstsq on basis [1, x, x^3] | the decile profile is monotone (Spearman of decile means vs decile rank |rho| >= 0.9) AND the top-minus-bottom spread has HAC |t| > 3 |
| 13 | 11 distributions differ | KS, Mann-Whitney, Welch t: daily r weekend vs weekday; daily |r| weekend vs weekday; fwd 5-min r after top vs bottom imbalance decile | p < 0.001 in KS or MW AND the direction holds in >= 5 of 7 eras |
| -- | 12 PCA | PCA on returns | (N/A, see below) |
| 14 | 13 outliers beyond data_clamp | run lengths of zero-return bars, gap runs, flag counts, TRAIN, by era | only something NOT already in CLEANING_LOG.md counts (missing minutes, 2017 flat bars, zero-quote block, 2023 regime break are known and are NOT observations) |

## N/A rows (reasons refer to THIS data)

- **Row 3, "X and Y are cointegrated" (Engle-Granger, Johansen): N/A.** The target is ONE instrument (BTCUSDT spot). The
  other copies in `data\` are a different instrument (perp) or uncleaned copies of the same feed, and TARGET.md says not
  to use them; pooling feeds is forbidden (data-hygiene rule 12). There is no second series to cointegrate with.
- **Row 7, Bayesian random-walk coefficient: N/A.** Needs PyMC, which 14c marks "heavy dep, ask first"; the run is
  unattended, so the conservative option is to skip it (DECISIONS.md D3). The rolling-regression and Chow parts of row 7 are run (09).
- **Row 12, "most variance lives in K factors" (PCA on returns): N/A.** PCA needs a cross-section of return series; this
  file has one asset. PCA over features derived from the same price would not test the row's claim.

## Results (appended after each run)

| NN | status | tool / series | plot | one-line result | observation per the pre-rule? |
|---|---|---|---|---|---|
| 01 | RUN | ADF, KPSS, PP; daily log close, daily r, 1-min r by era | plots/01_unit_root.png, tables/01_unit_root_tests.csv | level: ADF p 0.56, PP p 0.54, KPSS p 0.01 (unit root); daily r: ADF p 0, KPSS p 0.10 (stationary). 1-min r in 2017: ADF rejects AND KPSS p 0.038 (mild disagreement, 2017 only) | No (null picture; 2017 KPSS disagreement noted) |
| 02 | RUN | Lo-MacKinlay VR, 1-min r, q=2..240, by era | plots/02_variance_ratio.png, tables/02_variance_ratio.csv | VR(60) < 1 in 6 of 7 eras (0.75-0.95; 2023Q1 1.02); pooled z* -20.8 (q=2) .. -9.8 (q=240); per era |z*| > 3 only in 2017, 2018, 2021 | **Yes -> OBS1** |
| 03 | RUN | AR(1), 1-min and 60-min r, by era, HAC | plots/03_ar1_by_era.png, tables/03_ar1_by_era.csv | 1-min phi: -0.195 (2017), -0.028, -0.006, -0.012, then +0.024 (2021), +0.011, +0.014; pooled t -17.7. Sign negative 4/7 eras: rule not met. 60-min phi negative 2017-2020, ~0 after | No by rule 03 (sign split 4/3); the sign FLIP is picked up by row 09 -> OBS3 |
| 04 | RUN | Hurst: aggregated variance on r, R/S on r and |r|, by era | plots/04_hurst.png, tables/04_hurst.csv | H(r) aggvar 0.44-0.51 (pooled 0.47), R/S 0.51-0.54 (pooled 0.53): inside [0.45,0.55] in 6-7 eras. H(|r|) 0.76-0.86 | No; the two estimators DISAGREE in direction (0.47 vs 0.53) -> OBS7 (method) |
| 05 | RUN | ACF/PACF 1-min r lags 1..60 by era | plots/05_acf_by_era.png, tables/05_acf_by_era.csv | lag 1 flips sign (-0.179 in 2017 .. +0.024 in 2021). Lags passing the rule: 2 (negative 7/7 eras, -0.005..-0.029; pooled HAC t -7.6) and 7 (negative 6/7, t -4.0) | **Yes (lags 2, 7) -> part of OBS1** |
| 06 | RUN | kurtosis, Hill, Q-Q, D'Agostino, VaR curve; 1-min and 60-min r | plots/06_fat_tails.png, tables/06_fat_tails.csv, 06_var_curve_60min.csv | excess kurtosis 83.7 (1-min), 31.0 (60-min); Hill left 3.15 [2.74,3.57] vs right 3.27 [2.88,3.73] (60-min): CIs overlap; 60-min skew -0.55 | No (fat tails = the null; tails symmetric within CI) |
| 07 | RUN | ARCH-LM(60), ACF of |r| to lag 1440, by era | plots/07_vol_clustering.png, tables/07_arch_lm.csv, 07_acf_absr_selected_lags.csv | ARCH-LM p = 0 in every era; ACF(|r|) stays positive to 1 day. ACF(1440)-ACF(720) > 0.02 in 1 of 7 eras | No (vol clustering = the null; no daily bump by the rule) |
| 08 | RUN | rolling 30d mean/std, OLS-CUSUM, Chow at 2020-01-01, 2-state Markov switching variance; daily r | plots/08_regimes.png, tables/08_regime_tests.csv | CUSUM p 0.65; Chow p 0.64; MS: variance states 3.7 vs 37.6 (%^2), state means 0.13% vs 0.00%/day, mean-diff t 0.52 | No (variance regimes, no mean regimes) |
| 09 | RUN | monthly AR(1) and monthly fwd5-on-imbalance slope; Chow (HAC interaction) at 2020-01-01 | plots/09_relationship_stability.png, tables/09_monthly_coefficients.csv, 09_chow_2020.csv | AR(1) -0.099 pre-2020 vs +0.010 post (change t 18.3, p 1e-74); imbalance slope +0.14 bp vs -1.22 bp per unit (t -6.1) | **Yes -> OBS3** (and imbalance part of OBS2) |
| 10 | RUN | Spearman IC tau=1,5,20 (HAC), 5 direction X + 2 size X; lead-lag imbalance vs r | plots/10_ic_leadlag.png, tables/10_ic_table.csv, 10_leadlag_imbalance.csv | tr5->fwd5 IC -0.051 (t -49; negative 6/7 eras, 2017 +0.004); imb->fwd5 -0.014 (t -21, negative 7/7); imb5->fwd5 -0.024 (6/7 < -0.01); dlogn ~0 (p 0.75-0.96). Size IC 0.66 (5-min), 0.83 (60-min). corr(imb_t, r_t) large at k=0, |corr| < 0.003 at k != 0 | **Yes -> OBS1 (tr5, r), OBS2 (imb, imb5)**; size IC logged as the null |
| 11 | RUN | mean r and |r| by UTC hour (hourly sums) and by weekday; Kruskal-Wallis | plots/11_calendar.png, tables/11_hour_of_day.csv, 11_weekday.csv, 11_calendar_summary.json | mean by hour KW p 1.3e-4; top h22 +4.45 bp (above mean 6/7 eras), h21 +4.13, bottom h3 -3.91 (below 5/7). |r| by hour KW p 1.8e-87: peak h0 63 bp, trough h5 44 bp, both 7/7 eras. Weekday mean KW p 0.57; weekday |r| KW p 1.2e-10, Saturday lowest (6/7) | **Yes -> OBS4 (hour mean), OBS5 (hour size), OBS6 (weekday size)**; weekday mean: No |
| 12 | RUN | decile sorts + lstsq [1,x,x^3] | plots/12_decile_sorts.png, tables/12_decile_sorts.csv | tr5->fwd5: monotone (rho -1.00), top-bottom -1.83 bp (t -9.7). imb->fwd5: NOT monotone (rho -0.61), top-bottom +0.02 bp (t 0.28). absr60->fabs60: monotone (rho 1.00), 139 -> 1049 bp. Cubic term adds nothing over linear (MSE equal to 4 dp) | tr5: **Yes (OBS1)**; imbalance: No -> **disagreement with row 10, kept in OBS2**; size: the null |
| 13 | RUN | KS / MW / Welch | plots/13_group_tests.png, tables/13_group_tests.csv | daily r weekend vs weekday: KS p 9e-4 but MW p 0.67, Welch 0.97, direction 4/7 eras (a scale difference, not a location one). |daily r| weekend 213 vs weekday 301 bp: MW p 2e-12, 7/7 eras. fwd5 after top vs bottom imbalance decile: -0.06 vs +0.09 bp, MW p ~0, 5/7 eras | |r| weekend: **Yes (OBS6)**; imbalance: **Yes (OBS2)**; weekend mean: No |
| 14 | RUN | zero-return runs, gaps, flags by era | plots/14_runs_flags.png, tables/14_runs_flags.csv | zero-return share 14.5% (2017), 2.1% (2018), <= 0.7% after; max run 12 bars (2017), <= 7 after; flags and missing minutes = CLEANING_LOG counts | No (all known from CLEANING_LOG) |

K (tests registered in tables/pvals_registry.csv) after the sweep: **50**.
