# REPORT: EDA of btc-spot-1m-clean (Binance BTCUSDT spot, 1-min trade bars), run 2026-09-25

TRAIN 2017-08-17 -> 2023-03-19 (explored); VAL 2023-03-25 -> 2023-11-30 (opened once). K = 50 sweep tests. **Round-trip cost: unknown.**
Data card: DATA_CARD.md. Stamps re-checked as bar-OPEN times (trades jump +0.24 log in the bar stamped :00 vs +0.14 at :01; plots/00_timestamp_open_check.png).

## Leads (survived Step 4, ranked by Step 5)

| lead | as a testable claim | effect + HAC 95% CI (TRAIN) | K-adj. p (BH) | eras (TRAIN) | posterior | VAL result † | plot |
|---|---|---|---|---|---|---|---|
| **L1 = OBS5** | Distribution of \|hourly return\| differs by UTC hour: hour 00 > hour 05 | raw 63 vs 44 bp mean \|r\| per hour (tables/11_hour_of_day.csv); vol-relative **+0.41 [+0.35, +0.47]** day-means | 5.3e-87 | strongest-recent (2018-23 +0.37..+0.52; 2017 +0.08 ns) | **0.96** | **SUPPORTED**: +0.33 [+0.18, +0.49], n 251 days † | plots/20, 24 |
| **L2 = OBS6** | Distribution of \|daily return\| differs by weekend vs weekday (weekend lower) | raw **-88 bp [-111, -65]**; vol-relative -0.40 [-0.50, -0.30] | 3.2e-12 | strongest-recent (all 7 negative; 2017, 2019 CIs touch 0) | **0.96** | **SUPPORTED**: -0.81 [-1.11, -0.50] rel.; raw -98 bp; 68 weekend days † | plots/21, 24 |
| **L3 = OBS1** | A change in the trailing 5-min return predicts the opposite-sign forward 5-min return (from close T+1) | top-bottom decile **-2.06 bp [-2.42, -1.71]**; ~0 in calm minutes (-0.19), -3.76 in high-vol tercile | 6.3e-22 | **decaying** (2021 -3.20, 2022 -0.96, 2023Q1 +0.62 ns) | **0.26** | **SUPPORTED by the rule, 72% smaller**: -0.58 [-1.04, -0.11] bp; vol-scaled -0.36 [-0.71, -0.01]; 7 of 9 months negative † | plots/16, 24 |
| L4 = OBS4 | Mean return over 21:00-23:00 UTC is positive | **+8.6 bp/day [+4.0, +13.1]**; +12.5 after down days, +2.1 after up days | 1.7e-4 (p x K = 0.41) | **alternating** (2022 -3.8) | 0.05 | not opened: 4th rank; VAL already spent for it (D10) | plots/19 |

† **VAL_NOTE (TARGET.md, verbatim):** "Two reasons VAL is weak evidence. (1) BTC VAL was crossed twice by arc #047 (both pre-registered) and overlaps a
spent pooled row of the 21:00-23:00 UTC seasonality EDA (see _SEALED_HOLDOUT.md): SOFT-clean. (2) VAL is a DIFFERENT REGIME from TRAIN: from 2023-04, median trades per minute fall ~8x (about 3,600 to 450, then 240-360) and the share of zero-return bars rises from <0.3% to 4-12% (CLEANING_LOG.md, Gate 4b; cause not established). A lead about trade counts, volume or 1-minute tick behaviour can fail VAL for structural reasons."
No VAL result here is out-of-sample proof. Rules were written first (VAL_RULES.md); results in tables/24_val_results.json. VAL zero-return share was 6.5%.

**Plain reading.** L1 and L2 are volatility seasonalities: the SIZE of moves depends on the clock. These are the kind of claim the programme has found forecastable. Why hour 00 UTC is the peak is **unexplained**: under US winter time the peak moves to 15 UTC (plots/20). L3 is a direction claim with a low prior. It is about 2 bp, lives in high-vol minutes, decays across TRAIN and shrank 72% in VAL. **Cost is unknown and would have to be well under ~2 bp round trip** for L3 to matter, which is UNTESTED here. L4 replicates a known prior hypothesis on overlapping data, so it adds no new evidence.

## What died (with the number)
- **OBS2 taker imbalance -> forward return**: -0.072 bp/sd alone flips to **+0.111 [+0.059, +0.163]** given the same-bar return, tr5 and vol. corr(imbalance, same-bar r) = 0.30: it is a twin of OBS1. The IC (t -21) and the decile sort (+0.02 bp, t 0.28) also disagreed (plots/17, 12).
- **OBS3 lag-1 autocorrelation flips negative -> positive (2020)**: after controlling for liquidity, vol and zero-return share, the post-2020 shift is **-0.0003 [-0.029, +0.028]**. Microstructure (plots/18).
- **OBS7 Hurst R/S > 0.5**: the R/S estimator gives **0.541 on shuffled data** (bias). Aggregated variance 0.475 vs 0.500 shuffled is real and is OBS1 again (plots/22).
- Not observations by the pre-declared rules: unit root in the level (ADF p 0.56), no mean regimes (CUSUM p 0.65, Chow p 0.64, Markov mean-diff t 0.52), weekday mean (KW p 0.57), trade-count change (IC p 0.75-0.96), tail asymmetry (Hill 3.15 vs 3.27, CIs overlap), daily periodicity in |r| ACF (1/7 eras).
- Not re-discovered as leads (CLEANING_LOG): missing minutes, 2017 flat bars and zero-return runs (plots/14), the zero-quote block, the 2023-04 regime break.
- **UNTESTED**: the spread-clock artifact for L3/L4 (no bid/ask in this file); cost for every lead; any cross-venue or cross-symbol replication (no other data given).

## Tool-log summary (TOOL_LOG.md, 14c Step-2 rows in order)
01 unit roots RUN (null picture) · 02 variance ratio RUN (VR(60) < 1 in 6/7 eras -> OBS1) · 03 AR(1) RUN (lag-1 flip -> OBS3) · 04 Hurst RUN (estimator disagreement -> OBS7) · 05 ACF/PACF RUN (lags 2, 7 negative -> OBS1) · row 3 cointegration **N/A** (one instrument) · 06 fat tails RUN (kurtosis 84 / 31; null) · 07 ARCH/vol clustering RUN (null) · 08 regimes RUN (variance yes, mean no) · 09 relationship stability RUN (-> OBS3, OBS2); Bayesian RW **N/A** (PyMC, D3) · 10 IC / lead-lag RUN (-> OBS1, OBS2) · 11 calendar RUN (-> OBS4, OBS5, OBS6) · 12 decile / lstsq RUN (OBS1 monotone; imbalance not) · 13 KS/MW/Welch RUN (-> OBS6, OBS2) · row 12 PCA **N/A** (one asset) · 14 outliers/runs RUN (nothing beyond CLEANING_LOG). BH: 38/50 survive (plots/15).

## Observations for future hunts (do not chase now)
- Peak |r| hour moves between 00 UTC (US summer time) and 15 UTC (US winter time) (tables/20_obs5_rel_profile.csv). Worth a
  claim of its own about US-clock-linked volatility. UNTESTED beyond this table.
- The 21-23 UTC drift is concentrated after trailing-24h down days (+12.5 vs +2.1 bp). If that seasonality hunt resumes,
  this conditional split is its own pre-registered claim. UNTESTED out of sample.
- The reversal (L3) scales with trailing volatility (calm -0.19, high -3.76 bp). A vol-conditioned version is a different claim. Needs a cost figure first.
- The minute-of-hour activity bursts at :00/:15/:30/:45 (plots/00) were seen only as a timestamp check. They are not a lead yet.

Files: DATA_CARD.md · ATTEMPTS.md · TOOL_LOG.md · OBSERVATIONS.md · CHECKS.md · RANKING.md · VAL_RULES.md · DECISIONS.md · plots/00-24 · tables/ · scripts/.
