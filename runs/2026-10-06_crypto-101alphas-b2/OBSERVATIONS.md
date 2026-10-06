# OBSERVATIONS — Phase 0, EXPLORE slice only

Numbered; each with its table/plot, the slice (always EXPLORE here) and one line "expected vs saw". Facts already in TARGET.md
CLEANED? / README (absent coin-years, FTMO Saturday gaps, the source switch) are not observations. Mode B: these feed the
Phase-1 assumption and impostor fields; they are not hypotheses of their own.

1. **#38 is a twin of 1-day reversal.** `tables/p0_04_signal_xs_corr.csv`, `plots/00_crosscorr.png`. EXPLORE. Expected: #38
   (range position x day's move) to overlap reversal partly; saw mean daily cross-sectional rank corr 0.863 with -r(d) — over
   the 0.7 impostor bar. Any #38 result must be read net of plain 1-day reversal (an ALREADY TESTED family).
2. **#53 and #54 read the same thing.** Same table. Expected: related (both use where the close sits in the day's range); saw
   rho 0.50. Their evidence is not independent, and SIGNALS.md must show their correlation if both survive.
3. **#35 leans on reversal too.** Same table. Expected: little overlap (32-day own-history ranks); saw rho 0.43 with -r(d) and
   0.45 with #38, via its (1 - Ts_Rank(returns, 32)) factor.
4. **#30 is the most distinct.** Same table. Expected: overlap with reversal (it fades a 3-day streak); saw <= 0.25 with every
   alpha and baseline — its volume ratio dominates the ranking.
5. **Daily returns reverse at lag 1, pooled.** `tables/p0_03_acf.csv`, `plots/00_acf.png`. Expected: ~0 at daily frequency;
   saw ACF(1) -0.142 (band 0.038), with alternating significant lags 2-4. Pooled own-coin, so it mixes market and
   cross-section; the D7 statistic is cross-sectional.
6. **#53 explodes near the low.** `tables/p0_01_alphas.csv`, `plots/00_distributions.png`. Expected: a bounded ratio; saw
   excess kurtosis ~1,745 and 1.3% of coin-days undefined (close == low). Only its ranks carry information.
7. **EXPLORE is a thin cross-section.** `tables/p0_02_valid_by_month.csv`, `plots/00_missingness.png`. Expected: 7-8 coins;
   saw a median of 5 coins per valid day. Daily cross-sectional ICs on EXPLORE rest on 5 coins: high noise per day.
8. **Coins move together.** `tables/p0_04_return_corr.csv`. Expected: high; saw mean pairwise correlation 0.86, 0.93 in
   2020Q1. Most of each coin's daily move is the market; only the residual is available to a cross-sectional alpha.
9. **The daily boundary is a volume bump.** `tables/p0_06_hour.csv`, `plots/00_clock.png`. Expected: flat-ish; saw 00:00 UTC
   at 4.9% of daily volume (second only to 16:00 at 6.1%). Every alpha here samples its close and open at that bump.
