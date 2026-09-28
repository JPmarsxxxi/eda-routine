# STEP 3: OBSERVATIONS (TRAIN only), from the pre-declared rules in TOOL_LOG.md

Not observations (logged facts / the null picture for 1-min crypto; the pre-rules said so in advance): price level I(1)
(01), fat tails with symmetric Hill indexes (06), volatility clustering and size forecastability (07, 10 size IC 0.66/0.83,
12 |r| sort), variance regimes without mean regimes (08), no weekday effect on the MEAN (11, KW p 0.57), trade-count change
predicts nothing (10, IC p 0.75-0.96). Known from CLEANING_LOG and NOT leads: missing minutes, 2017 flat bars / zero-return
runs (14), zero-quote block, the 2023-04 regime break.

| OBS | what looks non-random | tools that show it | number |
|---|---|---|---|
| OBS1 | Short-horizon **reversal**: the trailing 5-min return predicts the opposite sign over the next 5 min | 02 VR < 1 at q 15-240; 05 ACF lags 2 and 7 negative; 10 IC; 12 decile sort | IC tr5->fwd5 -0.051 (HAC t -49), negative 6/7 eras; decile top-bottom -1.83 bp (t -9.7, monotone rho -1.00); VR(60) < 1 in 6/7 eras; ACF lag 2 negative 7/7 (tables/10_ic_table.csv, 12_decile_sorts.csv, 02_variance_ratio.csv, 05_acf_by_era.csv) |
| OBS2 | Taker **imbalance** (buy_vol/vol) predicts a slightly NEGATIVE forward return | 10 IC; 13 MW/KS; 09 slope drift | IC imb->fwd5 -0.014 (t -21), 7/7 eras negative; fwd5 after top vs bottom decile -0.06 vs +0.09 bp (MW p 1e-59) |
| OBS3 | The **lag-1 autocorrelation** of 1-min returns drifts from negative to positive | 03 AR(1); 05 ACF; 09 Chow | AR(1) -0.099 before 2020 vs +0.010 after (change t 18.3); -0.195 in 2017, +0.024 in 2021 (tables/09_chow_2020.csv, 03_ar1_by_era.csv) |
| OBS4 | **21:00-23:00 UTC** mean return is positive; hour 2-3 negative | 11 KW by hour | KW p 1.3e-4; h22 +4.45, h21 +4.13 bp/hour; h22 above the mean in 6/7 eras, h3 below in 5/7 (tables/11_hour_of_day.csv). **This is the known prior** of the btc_seasonality_2123 EDA (SSRN 4581124), not a new finding |
| OBS5 | **|return| has a UTC-hour profile**: peak at 00 UTC, trough at 05 UTC | 11 KW on |r| | KW p 1.8e-87; h00 63 bp vs h05 44 bp per hour; peak and trough hold 7/7 eras |
| OBS6 | **Weekend days are quieter** | 11 KW on |daily r|; 13 MW | weekend 213 vs weekday 301 bp |daily r|, MW p 2e-12, 7/7 eras; Saturday lowest 6/7 |
| OBS7 | Tool disagreement: **Hurst estimators disagree** in direction (aggregated variance 0.47 < 0.5, R/S 0.53 > 0.5) | 04 | tables/04_hurst.csv |

## Disagreements between tools (reported, not averaged)

- **OBS2, IC vs decile sort.** IC imb->fwd5 is negative (t -21) but the decile top-minus-bottom is +0.02 bp (t 0.28)
  and the decile profile is hump-shaped (rho -0.61; tables/12_decile_sorts.csv). The IC is carried by the middle of the
  distribution, not the tails.
- **OBS1 vs 03 in 2017.** VR says 2017 is the most mean-reverting era (VR(2) 0.79), but the IC of the trailing 1-min
  return on fwd1 is POSITIVE in 2017 (+0.025) while negative in every other era. The 2017 VR is dominated by lag-1
  (bounce, -0.179), which the forward-return definition skips.
- **OBS7.** See Step 4.
- **Weekend daily r (13):** KS p 9e-4 but MW p 0.67 and Welch p 0.97: the distributions differ in scale, not location.
  Consistent with OBS6, not a separate observation.
