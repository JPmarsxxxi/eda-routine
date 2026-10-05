# OBSERVATIONS — Phase 0, all on EXPLORE (2017-08-17 .. 2021-06-30), primary 10-coin 1h panel

Known facts from TARGET.md CLEANED? are not listed. "10/10" counts coins, which are correlated (median pairwise 0.62), so it is
NOT 10 independent confirmations. Each line: number · plot/table · slice · expected vs saw.

1. `plots/00_distributions.png`, `tables/p0_01_distributions.csv` · EXPLORE · Expected fat tails (kurtosis ~10); saw excess
   kurtosis 10-104 and Hill index 2.4-4.0 in all 10 coins — any mean-based statistic will be driven by a handful of hours.
2. `tables/p0_01_distributions.csv` · EXPLORE · Expected no zero-return mass on liquid coins; saw LTC r == 0 in 1.12% of hours
   (others < 0.9%), vol == 0 in <= 0.015%.
3. `plots/00_missingness.png`, `tables/p0_02_missing.csv` · EXPLORE · Expected the known 20-128 missing hours; saw 13-121, all
   whole-exchange outages (nothing new).
4. `plots/00_acf.png`, `tables/p0_03_acf.csv`, `tables/p0_03_roll.csv` · EXPLORE · Expected a tiny negative lag-1 ACF from
   bid-ask bounce (Binance half-spread ~1 bp); saw lag-1 and lag-2 ACF of 1h returns negative in 10/10 (-0.044, -0.041),
   implying a Roll half-spread of 23-36 bp — 10-30x any real spread, so it is price-pressure/outlier reversal, not bounce.
5. `plots/00_acf.png`, `tables/p0_03_acf.csv`, `tables/p0_05_regimes.csv` · EXPLORE · Expected lag-24 ACF of 1h returns ~0, or
   positive if there were a time-of-day return pattern; saw it NEGATIVE in 10/10 coins (median -0.051) and in every era
   (-0.041 .. -0.056), while lags 12 and 48 are not significant.
6. `tables/p0_03_vr.csv` · EXPLORE · Expected VR ~1 (random walk) beyond 1-2 h; saw VR(6) = 0.86 (10/10 below 1), VR(24) = 0.88
   (8/10), VR(72) 0.86 (6/10): returns over 6-24 h partly undo themselves. DOGE is the exception (VR(24) 1.25, trending).
7. `plots/00_acf.png` · EXPLORE · Expected volatility clustering; saw |r| ACF 0.30 at 1 h still 0.11 at 168 h (10/10).
8. `tables/p0_03_acf.csv`, `tables/p0_03b_quintiles.csv` · EXPLORE · Expected cross-sectional (relative) reversal to carry to the
   daily grain if it exists at 1 h; saw relative ACF(1h) -0.068 (10/10) but at 1 day nothing: quintile sort Q5-Q1 +12 bp, t 0.72
   (only 2017-18 shows +50 bp, t 2.25).
9. `plots/00_daily_acf.png`, `tables/p0_03b_daily.csv` · EXPLORE · Expected daily returns ~uncorrelated; saw daily raw ACF(1)
   median -0.089, significantly negative in 6/10 coins (one short of the 7/10 panel-fact rule), lag 2 +0.057 (4/10 positive).
10. `plots/00_crosscorr.png`, `tables/p0_04_corr.csv`, `p0_04_within.csv`, `p0_04_venue.csv` · EXPLORE · Expected no twins;
    saw none among coins (max 0.83 LTC-BCH), but vol/quote_vol are twins (1.000) and Binance vs Coinbase BTC 1h returns are a
    twin (0.9525 > 0.95).
11. `tables/p0_04_within.csv` · EXPLORE · Expected volume ~ a volatility proxy (Spearman > 0.5); saw 0.38-0.50 in 10/10:
    volume carries information beyond |r|.
12. `plots/00_volume_interaction.png`, `tables/p0_04e_volume.csv` · EXPLORE · Expected volume not to matter for the next-day
    relative return; saw high-volume-shock winners continue (+11.6 bp) while low-volume-shock winners fall (-10.6 bp);
    high-minus-low W-L +42 bp, t 1.5 over 402 days (not significant by the rule).
13. `tables/p0_04e_volume.csv` (printed panel lines), `tables/p0_03b_daily.csv` · EXPLORE · Expected daily reversal (if any) to
    be uniform; saw corr(EW panel day t, day t+1) = -0.136 on top-tercile panel-volume-shock days vs -0.066 on other days
    (448 / 895 days).
14. `plots/00_regimes.png`, `tables/p0_05_regimes.csv` · EXPLORE · Expected stable tails and cross-correlation; saw 2020
    kurtosis 54 vs 13-21 other eras, relative ACF(1) weakening -0.10 -> -0.04, cross-corr 0.71 -> 0.58, log-vol ACF(24) break
    0.67 -> 0.39 in 2018->2019, CUSUM vol-level break (peak 2018-04-05).
15. `plots/00_row_alignment.png`, `tables/p0_07_row.csv` · EXPLORE · Expected the TARGET zero-gap rate 0.3-0.6; saw 0.155-0.315
    (9/10 below the band) — still a real trade print (synthetic opens give HIGH rates); the card figure does not hold on EXPLORE.
16. `plots/00_clock.png`, `tables/p0_06_clock.csv` · EXPLORE · Expected a US/EU-hours volume peak; saw volume peak 16 UTC /
    trough 21 UTC (1.88x); |r| profile 1.47x (under the 1.5 rule), weekday shapes under 1.3x (weekends ~0.87x volume).

Not chased (excluded topics, DECISIONS D9): hourly lag-1/2 reversal (#4) sits next to the ALREADY TESTED "short-horizon reversal
after taker imbalance" and cannot clear a 6.6-36.5 bp round trip at 1 h; it is logged as a lead only. #10, #14, #15, #16 are
data-nature facts used by Phase 1 rivals/impostor checks, not return claims.
