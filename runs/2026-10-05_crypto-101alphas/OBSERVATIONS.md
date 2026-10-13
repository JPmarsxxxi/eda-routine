# OBSERVATIONS — Phase 0, all on the EXPLORE slice (2019-01-01 .. 2020-05-28)

Known cleaning/README facts (holes, Saturday FTMO gaps, Binance outages) are not repeated as observations. None of these
conditions a forward return on an alpha (DECISIONS D11), so they do not open EXPLORE for H1-H5 (`seen_on: none`).

1. **Fat tails everywhere.** plots/00_distributions.png, DATA_PROFILE §1. Slice EXPLORE. Expected excess kurtosis ~10 for
   hourly crypto; saw 34-89 hourly and 15-37 daily. -> Any mean-spread test needs a robust SE and a tail-aware power
   simulation (the power sims resample EXPLORE's empirical cross-sectional residuals rather than assume normality).
2. **One common factor dominates.** plots/00_crosscorr.png, §4. EXPLORE. Expected mean pairwise hourly correlation ~0.6; saw
   0.78 (0.61-0.86), rising to 0.84 in 2020H1. -> Cross-sectional (market-neutral) statistics remove most of the variance;
   the half-vs-half spread is the right unit. Rival for every hypothesis: a market-beta (high-beta coins) twin.
3. **Primary price = Binance close in EXPLORE (impostor pair by construction).** plots/00_row_meaning.png, §4/§7. Expected
   that; saw corr 1.0000 and 0 bp median gap. -> Until 2022 the signal (Binance OHLCV) and the response (primary) are the SAME
   prints: any bid/ask-bounce artefact in Binance closes feeds both. From 2022 (C3) the response is the FTMO mid for 7 coins,
   which breaks that link (data-hygiene Roll trap: a reversal alpha built on trade closes is guilty until a mid-based
   response confirms it).
4. **24/7: the daily open is the previous close.** §4. Expected ~100% of days with |open - prev close| < 5 bp; saw 68-96%
   (median gaps 0.4-2.8 bp; the hour-00 open is the first trade after 24:00, a tick away). (close - open) correlates 1.000
   with the close-to-close log return. -> #101's numerator IS the day's close-to-close return; #2's (close-open)/open likewise.
   #101 is therefore cross-sectional 1-day momentum scaled by the day's range (rival: plain 1-day return sort).
5. **rank(low) is static.** §4. Expected occasional crossings; saw 0.0% of coin-days with a changed cross-sectional rank of
   `low` (BTC > BCH > ETH > LTC > BNB > XRP > ADA every day). -> #4 = -ts_rank(rank(low), 9) is a constant (all ties) in
   EXPLORE: no cross-sectional variation at all, so #4 cannot be tested where coins never cross in price level. Same price-
   level dominance applies to #42's rank(vwap - close) / rank(vwap + close) (DECISIONS D2).
6. **Short-lag hourly reversal and lag-24 reversal.** plots/00_acf.png, §3. Expected ~0; saw ACF(1) -0.04..-0.06 and ACF(24)
   -0.04..-0.06 (all 7 coins beyond 2/sqrt(n)); |r| and log volume strongly persistent (lag-1 0.25-0.32 and 0.69-0.77).
   -> Bounce/reversal at 1h (Roll-type) and same-hour-yesterday reversal (an ALREADY TESTED topic, not chased). Volatility
   clustering means vol-scaled rivals (high-vol coins) matter for #101 (scaled by range) and #6/#2 (volume terms).
7. **Correlation regime shift inside EXPLORE.** plots/00_regimes.png, §5. Expected stable; saw mean pairwise correlation 0.59
   (2019H1) -> 0.84 (2020H1), a BREAK by the 0.2 rule; vol ratio 1.6 (no break by 2x). -> Cross-sectional dispersion (the
   room any cross-sectional alpha has) shrinks when correlation jumps; power differs by era.
8. **Clock shape.** plots/00_intraday.png, §6. Expected US-hours peak; saw relative volume peak 16h UTC, trough 21h; weekend
   volume 0.62 vs 0.79 weekday; |r| 1.5x max/min by hour. -> Descriptive only; the daily (UTC-day) bar's last hours are the
   quietest, so "the close" (24:00 UTC) is a low-activity instant (relevant to #42's delay-0-at-the-close premise).
