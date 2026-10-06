# SIGNALS — hand-off to the combination stage (RUNBOOK_v3 v3.2 Phase 3 step 3)

One block for every hypothesis `supported` on at least one CONFIRM fold, whatever its final state: H1 (Alpha#30) and H6
(-1 x Alpha#54). Neither reached HIGH; both are weak and both are below the cost line alone, which is what COMBINE-ONLY means.
All correlations are on TRAIN only (EXPLORE + C1..C3), `code/p3_signals.py` -> `tables/p3_signals.json`. Market and BTC are
the correlation of the signal's cross-sectional mean (trailing z, D7/standard 2) with the same-day panel / BTC return; the
other baselines are mean daily cross-sectional Spearman correlations (DATA_PROFILE §4 definitions). This routine does not
combine signals or fit weights.

## S1 — Alpha#30, volume-scaled 3-day streak fade
hypothesis: H1
definition: ((1 - rank(sign(c - c[-1]) + sign(c[-1] - c[-2]) + sign(c[-2] - c[-3]))) * sum(volume, 5)) / sum(volume, 20) on Binance spot UTC daily bars (open = 00:00 hour's open, close = 23:00 hour's close, volume = sum of hourly base volume; bar valid with >= 20 hours incl. 00 and 23); rank = cross-sectional percentile over the coins present; knowable at 24:00 UTC of day d; universe = the 10 primary coins with >= 5 present
version: neutral (daily cross-sectional rank IC; the raw own-return version was not part of the claim)
horizon: next UTC day (end of d -> end of d+1), primary validated price
folds: EXPLORE IC -0.0069 inconclusive (cell_20); C1 IC +0.0371 supported (cell_12); C2 IC +0.0480 supported (cell_13); C3 IC +0.0013 inconclusive (cell_14); VAL not opened (posterior 0.8497 < 0.85, never HIGH)
turnover: 0.24 of each half-book's names change per day (cells 12-14)
cost_line: top-minus-bottom spread +20.3 / +21.9 / -11.0 bp/day on C1 / C2 / C3 vs 2 x (0.24 x 36.8 + 8.2) = 34 bp/day at the median-coin 45 bp round trip (D11): below cost even on its supported folds
label: COMBINE-ONLY
corr_baselines: market -0.009; btc -0.015; momentum_20d -0.036; volatility_20d +0.011; reversal_1d +0.187; volume_vs_20d +0.216
corr_signals: S2 -0.120 (signal values), -0.123 (daily IC series)

## S2 — -1 x Alpha#54, closing strength continues (redirect child of H5)
hypothesis: H6
definition: +((close - low) / (high - low)) x (open / close)^5, i.e. -1 x Alpha#54, on the same Binance daily bars (NaN when high == low, D9); knowable at 24:00 UTC of day d; same universe
version: neutral (daily cross-sectional rank IC)
horizon: next UTC day (end of d -> end of d+1), primary validated price
folds: C1 IC +0.0521 (birth slice, redirect cell_08 — NOT evidence); C2 IC +0.0567 supported (cell_09); C3 IC +0.0229 inconclusive (cell_10); EXPLORE IC +0.0091 inconclusive (cell_11; halves +0.096 then -0.078); VAL not opened (posterior 0.49)
turnover: 0.48-0.59 of each half-book's names change per day (cells 09-11)
cost_line: spread +27.6 / +6.2 / +11.9 bp/day on C2 / C3 / EXPLORE vs 2 x (0.48 x 36.8 + 8.2) = 52 bp/day (D11): about half the cost on its best fold
label: COMBINE-ONLY
corr_baselines: market +0.307; btc +0.308; momentum_20d +0.014; volatility_20d -0.103; reversal_1d -0.155; volume_vs_20d -0.046
corr_signals: S1 -0.120 (signal values), -0.123 (daily IC series)
