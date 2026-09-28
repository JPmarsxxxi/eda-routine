# STEP 4: CHECKS against the boring explanations (TRAIN only; HAC Newey-West 95% CIs throughout)

Script `scripts/s4_checks.py`. (c) luck: Benjamini-Hochberg over the K = 50 sweep p-values (tables/15_bh_adjusted_pvals.csv,
plots/15_bh_adjustment.png): 38 of 50 survive at 5%, which is expected with 2.9M one-minute rows. Almost every small effect is
"significant" here, so BH alone eliminates little and the other checks do the work.
Era classes: decaying / flat / strongest-recent / alternating (the rule is in `classify()` in s4_checks.py: >= 2 sign flips = alternating).

## OBS1 trailing 5-min r -> fwd 5-min r (reversal): SURVIVES (plots/16_obs1_checks.png, tables/16_obs1_checks.csv)
Base: fwd5 top-minus-bottom tr5 decile **-2.06 bp [-2.42, -1.71]**, t -11.4.
- (a) twin, volatility: X scaled by trailing 60-min |r|: -1.17 bp [-1.44, -0.91] (survives). Within trailing-vol terciles:
  low -0.19 [-0.42, +0.04], mid -0.63 [-0.97, -0.29], **high -3.76 [-4.60, -2.93]**: the effect scales with volatility and is ~0 in calm minutes.
  twin, trailing return: the claim IS a trailing-return claim; controlling for the 60-min trailing return and vol leaves
  **-0.35 bp per sd [-0.65, -0.06]** (t -2.3): most of the 5-min effect is shared with the longer trailing return.
- (b) artifact: skip 2 bars instead of 1 (bid-ask bounce): -2.00 bp (unchanged). Ex 2017 (thin market): -1.95. Drop top 1% moves: -2.83 (stronger).
  tr5 != 0 only: -2.07. By UTC session: 00-08 -1.13, 08-16 -2.24, 16-24 -2.77 (all negative). Not one session, not one outlier.
- (c) luck: tr5->fwd5 IC and decile tests survive BH (p_bh < 1e-21).
- (d) eras: 2017 -4.84, 2018 -1.82, 2019 -1.83, 2020 -2.48, 2021 -3.20, **2022 -0.96, 2023Q1 +0.62 [-0.44, +1.67]**.
  Class: **decaying** (flat if 2017 is dropped). The two most recent eras are the weakest, and 2023Q1 has the wrong sign.
- (e) size: ~2 bp top-vs-bottom decile over a 5-minute hold, ~0.2 bp in calm minutes. **Cost unknown.**

## OBS2 taker imbalance -> fwd 5-min r: DIES at (a), twin of the same-bar return (plots/17_obs2_checks.png, tables/17_obs2_checks.csv)
imb alone -0.072 bp/sd [-0.109, -0.035]; **given the same-bar r, tr5 and vol it flips sign to +0.111 [+0.059, +0.163]**.
corr(imb, same-bar r) = 0.30: imbalance is mostly the bar's own return, whose reversal is OBS1. Era by era, given controls:
2018 +0.38, the others -0.02..+0.13 (class alternating). Nothing left to rank.

## OBS3 lag-1 autocorrelation drifts negative -> positive: DIES at (b), tracks liquidity (plots/18_obs3_checks.png, tables/18_obs3_monthly_ar1_vs_liquidity.csv)
Monthly AR(1) vs log median trades/min: Spearman +0.35; vs zero-return share: -0.34. Regressing monthly AR(1) on liquidity,
vol and zero-return share, the post-2020 shift is **-0.0003 [-0.029, +0.028]**: the "break" is fully absorbed by
microstructure covariates (bounce and stale-price share falling as the market deepened). Pre-2020 AR(1) is negative in
every vol tercile (-0.137, -0.067, -0.011); post-2020 ~0 (-0.005, -0.005, +0.014). Drop top 1%: -0.079 vs -0.010. Lag-1 on trade
prints is microstructure; no lead.

## OBS4 21-23 UTC mean return (KNOWN PRIOR): survives (a)-(c) weakly, eras ALTERNATING (plots/19_obs4_checks.png, tables/19_obs4_checks.csv)
Base: window return **+8.56 bp/day [+3.99, +13.14]** (t 3.7); minus the average 2-hour chunk the same day +8.64.
- (a) residual on trailing 24h return +8.61; vol-scaled t 2.64. BUT conditional: after a trailing-24h DOWN day +12.5 [+5.1, +20.0],
  after an UP day +2.1 [-3.8, +8.0]: most of it lives after down days (partly a trailing-return twin, not eliminated).
- (b) drop top 1% days +7.4 [+3.4, +11.3]; ex 2017 +6.9; US DST on (window = 17-19 New York) +10.4 [+5.2, +15.7], DST off (16-18 New York)
  +5.4 [-3.1, +14.0]; weekdays +9.8, weekends +5.4 [-4.0, +14.8]. No spread series exists, so the #016-style spread-clock
  artifact CANNOT be checked on this file (trade prints only): UNTESTED.
- (c) KW hour-mean p 1.3e-4 -> p_bh 1.7e-4 (survives); the conservative p x K = 0.41 (Step 5).
- (d) eras: 2017 +31.3, 2018 +0.7, 2019 +11.2, 2020 +15.2, 2021 +12.1, **2022 -3.8**, 2023Q1 +3.7 (n 78). Class **alternating**.
- (e) ~8.6 bp per day, one 2-hour window. Cost unknown.
Not new: this replicates the prior btc_seasonality_2123 EDA's paper-period row on overlapping data, so it is not independent evidence.

## OBS5 |hourly r| by UTC hour, h00 vs h05: SURVIVES (plots/20_obs5_checks.png, tables/20_obs5_checks.csv)
Measured as |hourly r| / the same day's mean |hourly r| (removes the day's vol level, the (a) twin):
h00 minus h05 **+0.41 [+0.35, +0.47]** day-means, t 13.3.
- (b) drop top 1% hours +0.38; US DST on +0.41, off +0.40. The PEAK hour moves with US DST: 00 UTC under EDT, **15 UTC under EST**
  (a US-equity-open-linked hour, 14:30 UTC in winter); 13 UTC (EDT) and 14 UTC (EST) are 1.14x and 1.17x the day-mean.
  Hour 00 UTC is also the daily-candle boundary and a perp funding time; which of these drives it is unexplained.
- (c) KW on |r| p 1.8e-87, survives BH.
- (d) eras: 2017 +0.08 [-0.11, +0.28], 2018 +0.40, 2019 +0.37, 2020 +0.38, 2021 +0.52, 2022 +0.47, 2023Q1 +0.47. Class **strongest-recent**.
- (e) a size effect (no direction): 0.41 of a day's mean hourly |r|; not a cost comparison. Cost unknown.

## OBS6 weekend |daily r| lower: SURVIVES (plots/21_obs6_checks.png, tables/21_obs6_checks.csv)
Raw: weekend minus weekday **-88 bp [-111, -65]** of |daily r|. Relative to the trailing 4-week mean |daily r| (known before the
day, the (a) twin): **-0.40 [-0.50, -0.30]** of a normal day. (b) drop top 1% days -0.33; ex 2017 -0.42.
(d) eras: 2017 -0.12 (ns), 2018 -0.43, 2019 -0.26 (CI touches 0), 2020 -0.37, 2021 -0.44, 2022 -0.56, 2023Q1 -0.59. Class **strongest-recent**.
(e) size effect; cost unknown.

## OBS7 Hurst disagreement: RESOLVED as estimator bias (plots/22_obs7_hurst_shuffle.png)
2021, 5 shuffles: R/S gives **0.541** on shuffled (memoryless) returns vs 0.535 real, so its > 0.5 reading is bias. Aggregated
variance gives 0.500 +/- 0.003 shuffled vs **0.475 real**: the < 0.5 reading is real and is the same thing as OBS1 (VR < 1).
