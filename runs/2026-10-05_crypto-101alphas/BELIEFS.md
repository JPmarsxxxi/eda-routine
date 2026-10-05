# BELIEFS — Bayesian ledger (fixed format, RUNBOOK_v3 Phase 1)

Mode B, one paper: Kakushadze (2015) "101 Formulaic Alphas", 1601.00991v3.pdf (local). Five candidates = the five alphas
TARGET.md names (DECISIONS D1). Every hypothesis is tested with the same pre-registered sub-claim and statistic (DECISIONS
D7): the next-day (end of d -> end of d+1, primary `price`) return of the top half of coins by the alpha minus the bottom
half, mean over days, bp/day; the paper's sign says it is POSITIVE (alpha value = desired position) and the economic bar is
20 bp/day.

**Shared prior anchor (trust arithmetic).** Base rate: published replication rate of equity anomalies ~0.35 (Hou, Xue &
Zhang 2020, "Replicating Anomalies": ~65% of 452 fail at |t| >= 1.96), x 0.5 transfer discount (US equities -> 10-coin crypto
cross-section, a significance bar -> a 20 bp/day economic bar) = 0.175, carried at 30% trust. The remaining 70% is a
per-alpha mechanism argument (stated in each anchor). prior = 0.3 x 0.175 + 0.7 x m = 0.0525 + 0.7 m.

## H1 — Alpha#101 intraday-range momentum
parent: none
source: 1601.00991v3.pdf Appendix A.1 Alpha#101 + §2 ("delay-1 momentum alpha: if the stock runs up intraday ... the next day one takes a long position"); TARGET.md HYPOTHESIS
question: Does a coin's (close - open)/((high - low) + .001) on UTC day d rank it for the next day's return, with the paper's momentum sign, at >= 20 bp/day top-minus-bottom?
hypothesis: a change in Binance daily (close - open)/((high - low) + .001) (from spot/binance_<COIN> open, high, low, close) predicts the cross-sectional rank of the next-day primary `price` return (end of d -> end of d+1) with a positive sign because a day that closes near its high signals sustained buying pressure / slow information diffusion that continues into the next day (paper: delay-1 momentum).
forbids: on a fold with its own pre-registered rule, a top-minus-bottom half spread whose one-sided 95% upper bound is below 20 bp/day without a significant positive effect (refuted); in particular we would NOT see the top-#101 half underperform the bottom half on average.
rivals: plain 1-day cross-sectional momentum (Obs 4: close-open IS the close-to-close return; the range scaling adds nothing); high-beta / volatility twin (Obs 2, 6: coins with big up-days in rising markets are high-beta, the spread is market beta); bid-ask bounce in shared Binance closes until 2022 (Obs 3) — would push the other way (reversal); the +.001 price-unit term (D2) reorders low-priced coins.
born_on: SOURCE Kakushadze 2015 101 Formulaic Alphas
seen_on: none
prior: 0.16
anchor: 0.3 x 0.175 (base rate) + 0.7 x 0.15 (mechanism: crypto cross-sectional momentum is documented at weekly horizons in large cross-sections, e.g. Liu-Tsyvinski-Wu 2022, but 1-day continuation in 10 large, 0.78-correlated coins at >= 20 bp/day is ambitious; Obs 6 shows short-lag reversal, not continuation) = 0.0525 + 0.105 = 0.1575 -> 0.16
posterior: 0.16
state: OPEN
evidence:

## H2 — Alpha#42 vwap-close delay-0 reversal
parent: none
source: 1601.00991v3.pdf Appendix A.1 Alpha#42 + §2 ("essentially a delay-0 mean-reversion alpha ... The contrarian position is taken close to the close"); TARGET.md HYPOTHESIS
question: Does rank(vwap - close)/rank(vwap + close) at the UTC close of day d rank coins for the next day's return with the paper's sign, at >= 20 bp/day?
hypothesis: a change in Binance daily rank(vwap - close)/rank(vwap + close) (vwap = sum(quote_vol)/sum(vol), close = last hour's close) predicts the cross-sectional rank of the next-day primary `price` return (end of d -> end of d+1) with a positive sign because coins that slid below their day's vwap late in the day (close < vwap) were pushed by temporary order-flow pressure that reverts, and the denominator down-weights richer coins (paper).
forbids: on a fold with its own pre-registered rule, a top-minus-bottom spread whose one-sided 95% upper bound is below 20 bp/day without a significant positive effect (refuted); we would NOT see the high-#42 half underperform the low-#42 half.
rivals: price-level sort (Obs 5, D2: rank(vwap+close) is the price-level rank, BTC always top, so #42 largely sorts by price level x the sign of vwap-close — a size/price-level effect, not reversal); plain 1-day reversal (close vs vwap ~ the day's late return, ALREADY TESTED topic daily TS reversal is a cousin); bid-ask bounce in shared Binance closes until 2022 (Obs 3) — would manufacture a reversal; time-of-day: 24:00 UTC is the quietest hour (Obs 8), not an auction close.
born_on: SOURCE Kakushadze 2015 101 Formulaic Alphas
seen_on: none
prior: 0.11
anchor: 0.3 x 0.175 (base rate) + 0.7 x 0.08 (mechanism: the delay-0 "contrarian at the close" premise needs a closing auction; 24:00 UTC is the quietest hour (Obs 8) and the verbatim ranks are price-level dominated (Obs 5, D2)) = 0.0525 + 0.056 = 0.1085 -> 0.11
posterior: 0.11
state: OPEN
evidence:

## H3 — Alpha#2 volume-change vs intraday-return correlation
parent: none
source: 1601.00991v3.pdf Appendix A.1 Alpha#2; TARGET.md HYPOTHESIS
question: Does -correlation(rank(delta(log(volume), 2)), rank((close - open)/open), 6) rank coins for the next day's return with the paper's sign, at >= 20 bp/day?
hypothesis: a change in the 6-day per-coin correlation between the cross-sectional rank of Binance delta(log(volume), 2) and the cross-sectional rank of (close - open)/open predicts the cross-sectional rank of the next-day primary `price` return with a positive sign of -correlation because coins whose relative up-days come with relative volume surges (high correlation) are being pushed by flow that overshoots and reverts, while volume-light moves are information that persists.
forbids: on a fold with its own pre-registered rule, a top-minus-bottom spread whose one-sided 95% upper bound is below 20 bp/day without a significant positive effect (refuted); we would NOT see coins with a negative volume-return correlation (high #2) underperform.
rivals: plain reversal/momentum of recent returns (the correlation co-moves with the recent return path); volume-level or liquidity twin (persistent log volume, Obs 6: high-volume coins differ in beta); market-wide volume shocks (a panel-volume-shock reversal is an ALREADY TESTED topic) acting through all coins at once.
born_on: SOURCE Kakushadze 2015 101 Formulaic Alphas
seen_on: none
prior: 0.11
anchor: 0.3 x 0.175 (base rate) + 0.7 x 0.08 (mechanism: a plausible flow-overshoot story, but a 6-day correlation of two ranks over 5-10 coins is a very noisy estimator, and volume/return links in crypto are dominated by the common factor, Obs 2) = 0.0525 + 0.056 = 0.1085 -> 0.11
posterior: 0.11
state: OPEN
evidence:

## H4 — Alpha#6 open-volume correlation
parent: none
source: 1601.00991v3.pdf Appendix A.1 Alpha#6; TARGET.md HYPOTHESIS
question: Does -correlation(open, volume, 10) rank coins for the next day's return with the paper's sign, at >= 20 bp/day?
hypothesis: a change in the 10-day per-coin correlation of Binance daily `open` with daily `volume` (sum of vol) predicts the cross-sectional rank of the next-day primary `price` return with a positive sign of -correlation because a coin whose price level rose together with volume (high correlation) is in a crowded, attention-driven run that mean-reverts, while a coin rising on falling volume is not.
forbids: on a fold with its own pre-registered rule, a top-minus-bottom spread whose one-sided 95% upper bound is below 20 bp/day without a significant positive effect (refuted); we would NOT see low-correlation (high #6) coins underperform high-correlation coins.
rivals: 10-day price trend (open-volume correlation is high in trends with rising volume: the statistic may be a 10-day momentum/reversal twin); volatility (volume and |return| cluster together, Obs 6); market-wide volume regime (all coins' volumes co-move with the common factor, Obs 2).
born_on: SOURCE Kakushadze 2015 101 Formulaic Alphas
seen_on: none
prior: 0.11
anchor: 0.3 x 0.175 (base rate) + 0.7 x 0.08 (mechanism: attention-run reversal is plausible in crypto, but a 10-day level-vs-volume correlation mostly reflects the shared trend, Obs 2) = 0.0525 + 0.056 = 0.1085 -> 0.11
posterior: 0.11
state: OPEN
evidence:

## H5 — Alpha#4 time-series rank of the cross-sectional rank of low
parent: none
source: 1601.00991v3.pdf Appendix A.1 Alpha#4; TARGET.md HYPOTHESIS
question: Does -Ts_Rank(rank(low), 9) rank coins for the next day's return with the paper's sign, at >= 20 bp/day?
hypothesis: a change in the 9-day time-series rank of the cross-sectional rank of Binance daily `low` predicts the cross-sectional rank of the next-day primary `price` return with a positive sign of -Ts_Rank because a coin whose relative price level sits at the top of its own recent range is relatively overbought and reverts.
forbids: on a fold with its own pre-registered rule, a top-minus-bottom spread whose one-sided 95% upper bound is below 20 bp/day without a significant positive effect (refuted); we would NOT see coins at the bottom of their relative range (high #4) underperform.
rivals: degeneracy (Obs 5: rank(low) is a static price-level order, so #4 is all ties on most days; signal-coverage check, code/signal_coverage.md: non-degenerate days EXPLORE 16, C1 94, C2 86, C3 52 — the statistic is defined only on days when two coins cross in price level); short-term reversal of relative returns (the ALREADY TESTED daily reversal topic's cross-sectional cousin); price-level / size (crossings happen among the low-priced coins).
born_on: SOURCE Kakushadze 2015 101 Formulaic Alphas
seen_on: none
prior: 0.09
anchor: 0.3 x 0.175 (base rate) + 0.7 x 0.05 (mechanism: the relative-overbought story is fine in equities with thousands of price-level crossings, but in 10 coins the input is static on >= 75% of days (Obs 5), leaving almost nothing to predict with) = 0.0525 + 0.035 = 0.0875 -> 0.09
posterior: 0.09
state: OPEN
evidence:
