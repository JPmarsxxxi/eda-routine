# TARGET: what the next EDA run should look at

Edit this file, then set STATUS to READY and click "Run now" on the routine. The routine sets STATUS to
`DONE <run folder>` when finished, so a finished target is never re-run by accident.

DATA MUST BE PREPARED FIRST: `python C:\Users\User\eda-routine\prep_target.py <source> <name>` writes a copy that
STOPS at the end of VAL (TEST and sealed rows are never copied). Point DATA at that copy, never at the source.

STATUS: DONE C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1

JOB: features
            (v3.4. data = find outside data that predicts the target (JOB_DATA.md); features = engineer predictive,
            non-redundant features from DATA (JOB_FEATURES.md); methods = apply toolbox methods or try new algorithms on
            DATA (JOB_METHODS.md). The target is the forward return of DATA's main instrument(s) unless named below.)

NAME: crypto-features-1

DATA: C:\Users\User\eda-routine\data\crypto_panel_validated_2026-10-05\   Read README.md, MANIFEST.csv and CUT.json there FIRST.
      234 parquet files in 8 folders, every file cut at 2023-11-30 23:59:59 UTC (verified per file at build).
      PRIMARY TARGET: primary/validated_<COIN>.parquet for the 10 coins BTCUSD, ETHUSD, BNBUSD, SOLUSD, XRPUSD, DOGEUSD,
      ADAUSD, LTCUSD, BCHUSD, DOTUSD, column `price`. NEVER take a return across a row with new_source=True. Everything else
      (including the raw spot/binance_* files) is an input series; use MANIFEST.csv `knowable` to lag it to its
      entry-knowable time before ANY join (data-hygiene.md rule).

TARGET RETURN: forward return of primary `price`, cross-sectional across the 10 coins. Horizons to declare in SPLITS.md:
      next 1h, next 6h, next 24h (every horizon tried counts in K).

PROVENANCE: Per file in MANIFEST.csv (source / type / freq / stamp / knowable). Primary target: VALIDATED hourly prices, UTC,
            stamped at the bar OPEN, `price` = value at the bar END, knowable at open + 1h. Binance spot last-trade close in
            years where it was checked against the Binance bid/ask mid (agrees within 2.5 bp); FTMO CFD hourly mid (checked
            against FTMO ticks) from 2022-01-01 for BTC ETH XRP LTC ADA DOGE DOT. BNB, BCH, SOL Binance only. Details README.md.

CLEANED?: PRIMARY: yes (validated; failed coin-years removed as holes, nothing filled). EVERYTHING ELSE: NO, raw pulls.
          Known facts (NOT leads):
          - primary/: coverage starts 2019-01-01 at the earliest; absent years ADA 2019, DOGE 2019-20, SOL 2020; BCH ends
            2021-12-31. A ~0.4-3 bp level offset at the 2022-01-01 Binance -> FTMO switch (flagged by new_source).
            FTMO rows miss fixed Saturday hours (bars closing 06-11 and 18:00 New York). Close only: no OHLC in primary/.
          - The response switches from the Binance print to the FTMO mid for 7 coins from C3 (2022-07) on (MEMORY/DATA_FACTS):
            a feature built on Binance prints may fade in C3 for that mechanical reason. Report it per fold.
          - Missing hours on raw Binance spot: 20-128 per coin (exchange outages / maintenance).
          - defi/*: vendor-aggregated and BACKFILLED (not point-in-time). onchain/cm_* exchange-flow metrics are revised
            backwards (not point-in-time). DO NOT build features from these two families. macro/cftc_*: knowable 3 days
            after the stamp. macro/yahoo_*: lag one session; Yahoo index opens can be synthetic (close-to-close only).
          - Coverage of input families inside TRAIN is uneven: funding from 2020, perp metrics (OI, long/short) BTC from
            2020-09 and the rest from 2021-12, BVOL only from 2023-06 (VAL only: unusable for features).

TRAIN_END: 2023-03-19
VAL_START: 2023-03-25
VAL_END:   2023-11-30
VAL_NOTE:  VAL is weak evidence. (1) BTC VAL was crossed twice by earlier work. (2) VAL was opened once more, on all 10 coins,
           for the crash-day rebound topic, and once by runs/2026-10-05_crypto-101alphas (#101): SOFT-clean. (3) VAL may be
           a DIFFERENT REGIME from TRAIN (2023 was calm; from 2023-04 BTC's 1-minute trade counts fell ~8x).

SOURCE_MODE: E
            (Data-only: feature families come from Phase 0 observations on this panel, plus the seeds below.)

SEEDS (start the library with these two; both are OPEN leads from runs/2026-10-06_crypto-101alphas-b2, see MEMORY/FINDINGS):
            - Kakushadze Alpha#30, a volume-scaled fade of the 3-day up/down streak:
              (((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) +
              sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))
              Daily rank IC +0.037 (C1), +0.048 (C2), +0.001 (C3).
            - minus Alpha#54, closing strength continues: ((low - close) * (open^5)) / ((low - high) * (close^5)), sign
              flipped. Daily rank IC +0.057 (C2), +0.023 (C3); EXPLORE halves point opposite ways.
            Daily OHLCV = UTC calendar days built from spot/binance_<COIN> 1h bars (open = first hour's open, high/low =
            max/min, close = last hour's close, volume = sum). Treat each seed as a FAMILY: sweep its lookbacks,
            normalisations and horizons, test whether the C3 fade is the response switch, then freeze what holds.

FAMILIES TO EXPLORE (a starting list, not a cap; Phase 0 observations may add more):
            price-path shape (streaks, range position, close location, gaps between sessions); reversal / momentum at
            1h-24h scaled by trailing volatility; volume and trade-count surprises; funding rate and basis (perp vs spot,
            from 2020); open interest and long/short changes (BTC from 2020-09); cross-coin lead-lag (BTC/ETH leading alts);
            market-wide (equal-weight panel) return and volatility conditioning; time-of-day / day-of-week interactions
            with any of the above.

ALREADY EXPLORED (v3.3: may be searched again on TRAIN, but say so and build on it, don't rediscover it): daily time-series
            reversal; reversal after panel volume-shock days; same-hour-yesterday 1h reversal; high-volume relative winners
            continue; intraday 6h-block reversal; 6h reversal in high trailing vol; crash-day rebound; perp premium
            cross-section; Fear & Greed level; prior-session S&P 500 return; Kakushadze #101 #42 #2 #6 #4 #35 #38 #53.

MIN_USEFUL_IC: 0.02   (mean rank IC per period; "supported" = significant AND at least this. Cost never decides a branch;
            it sets the STANDALONE / COMBINE-ONLY label.)

PRE-APPROVED INSTALLS: any   (PyPI/conda-forge only, pinned, into C:\Users\User\eda-routine\.venv, each validated before
            use - RUNBOOK_v3.md "INSTALLS AND METHODS". .venv does not exist yet: create it as the runbook says.)

ROUND-TRIP COST (bp): MEASURED FTMO CFD costs (spread at the trade minute from FTMO quotes 2022+, coin x hour medians applied to
            2019-21; commission 3.25 bp/side), round trip for a 24h hold INCLUDING one rollover night (8.2 bp; subtract it for an
            intraday trade, add 8.2 per extra night, Friday x3): BTC 18.9, ETH 25.4, LTC 36.5, ADA/DOGE/DOT/BNB/SOL ~45-47,
            BCH 65.5, XRP 68.6. Use these, not the `ftmo_spread_rt_bp` column on spot/binance_* (an old single live sample).

NOTES: Follow RUNBOOK_v3.md (v3.4 core) and JOB_FEATURES.md. Run gate.py as the runbook says.
       Use C:\Users\User\backtest_engine\backtest_engine2\eda_guard.py for every data load (the guard), and log it.
       Phase 0: profile the PRIMARY panel (10 coins, 1h) and the input families you will build from, for coverage,
       knowability and alignment; not 234 separate studies.
       READ-ONLY method files outside this repo, and ONLY these: backtest_engine\backtest_engine2\PROTOCOL.md,
       skills\00-overview.md, skills\12-alpha-overview.md, skills\14c-eda.md, cellplot.py, data_hygiene.py, eda_guard.py;
       finding-alphas\data-hygiene.md. Never open anything else in finding-alphas or backtest_engine (no alpha_log.md, no
       hunts\, no notebooks, no data\, no _SEALED_HOLDOUT.md, no x0* files). Inside eda-routine never open runs\ other than
       your own run folder (MEMORY\ carries what earlier runs found).
