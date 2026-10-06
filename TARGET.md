# TARGET: what the next EDA run should look at

Edit this file, then set STATUS to READY and click "Run now" on the routine. The routine sets STATUS to
`DONE <run folder>` when finished, so a finished target is never re-run by accident.

DATA MUST BE PREPARED FIRST: `python C:\Users\User\eda-routine\prep_target.py <source> <name>` writes a copy that
STOPS at the end of VAL (TEST and sealed rows are never copied). Point DATA at that copy, never at the source.

STATUS: READY

NAME: crypto-101alphas-b2

DATA: /home/user/eda-routine/data/crypto_panel_validated_2026-10-05/   (cloud session; on the desktop this is
      C:\Users\User\eda-routine\data\crypto_panel_validated_2026-10-05\). Read README.md, MANIFEST.csv and CUT.json there FIRST.
      234 parquet files in 8 folders, 6,029,906 rows, every file cut at 2023-11-30 23:59:59 UTC (verified per file at build).
      = the 224 files of crypto_panel_2026-09-30 unchanged + primary/ (10 validated hourly price files, one per coin).
      PRIMARY TARGET (the returns every hypothesis must predict): primary/validated_<COIN>.parquet for the 10 coins BTCUSD,
      ETHUSD, BNBUSD, SOLUSD, XRPUSD, DOGEUSD, ADAUSD, LTCUSD, BCHUSD, DOTUSD, column `price`. NEVER take a return across a
      row with new_source=True. Everything else (including the raw spot/binance_* files) is a candidate explanatory series;
      use MANIFEST.csv `knowable` to lag it to its entry-knowable time before ANY join (data-hygiene.md rule).

PROVENANCE: Per file in MANIFEST.csv (source / type / freq / stamp / knowable). Primary target: VALIDATED hourly prices, UTC,
            stamped at the bar OPEN, `price` = value at the bar END, knowable at open + 1h. Binance spot last-trade close in
            years where it was checked against the Binance bid/ask mid (agrees within 2.5 bp); FTMO CFD hourly mid (checked
            against FTMO ticks) from 2022-01-01 for BTC ETH XRP LTC ADA DOGE DOT. BNB, BCH, SOL Binance only. Details README.md.

CLEANED?: PRIMARY: yes (validated; failed coin-years removed as holes, nothing filled). EVERYTHING ELSE: NO, raw pulls.
          Known facts (NOT leads):
          - primary/: coverage starts 2019-01-01 at the earliest; absent years ADA 2019, DOGE 2019-20, SOL 2020; BCH ends
            2021-12-31. A ~0.4-3 bp level offset at the 2022-01-01 Binance -> FTMO switch (flagged by new_source).
            FTMO rows miss fixed Saturday hours (bars closing 06-11 and 18:00 New York). Close only: no OHLC in primary/.
          - Missing hours on raw Binance spot: 20-128 per coin (exchange outages / maintenance).
          - spot/bitstamp_BTCUSD 2011-2013: stale feed, up to ~90% zero-volume hours and flat bars.
          - spot/coinbase_XRPUSD has a delisting gap 2021-01 -> 2023-07.
          - defi/*: vendor-aggregated and BACKFILLED (not point-in-time). onchain/cm_* exchange-flow metrics are
            revised backwards (not point-in-time). macro/cftc_*: knowable 3 days after the stamp. macro/yahoo_*: lag one
            session; Yahoo index opens can be synthetic (close-to-close only).
          - macro/nyfed_rrp `counterparties` is an all-null column.
          - Coverage of explanatory families inside TRAIN is uneven: funding from 2020, perp metrics (OI, long/short) BTC from
            2020-09 and the rest from 2021-12, BVOL only from 2023-06 (VAL only).

TRAIN_END: 2023-03-19
VAL_START: 2023-03-25
VAL_END:   2023-11-30
VAL_NOTE:  VAL is weak evidence. (1) BTC VAL was crossed twice by earlier work and overlaps a spent pooled row of an earlier BTC
           seasonality EDA. (2) VAL has since been opened ONCE more, on all 10 coins, for a pre-registered test of the crash-day
           rebound topic (see ALREADY TESTED): SOFT-clean for every coin for that topic. (3) VAL may be a DIFFERENT REGIME from
           TRAIN (2023 was calm; from 2023-04 BTC's 1-minute trade counts fell ~8x, cause not established).

SOURCE_MODE: B
            (Set by the user's assistant on 2026-10-06 at the user's request: "pick new formulas from the paper" and run the
            EDA again under RUNBOOK_v3 v3.2. Paper = INBOX.md section B entry 2, the same local file 1601.00991v3.pdf, second
            batch of alphas; the first batch's five are in ALREADY TESTED.)

HYPOTHESIS: FIVE NEW alphas from the paper (Appendix A.1), chosen because they need only OHLCV (no vwap, no industry
            neutralisation, no market cap) AND are scale-free across coins (every price enters as a ratio or a per-coin
            time-series rank, so the price-level problem of the first batch, #42/#4, cannot arise), AND are not one of the
            first batch or an ALREADY TESTED topic. Phase 1 = exactly these five, one candidate each (the 6-candidate cap
            still holds). Formulas verbatim from the paper:
            - Alpha#30: (((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) +
                        sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))
                        (3-day up/down streak, faded, scaled by the coin's 5d/20d volume trend; delay-1)
            - Alpha#35: ((Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 - Ts_Rank(returns, 32)))
                        (high own-history volume, low own-history price and return; delay-1)
            - Alpha#38: ((-1 * rank(Ts_Rank(close, 10))) * rank((close / open)))
                        (short a coin at the top of its 10-day range that also rose on the day; delay-1)
            - Alpha#53: (-1 * delta((((close - low) - (high - close)) / (close - low)), 9))
                        (fade the 9-day change in where the close sits in the day's range; paper: delay-0)
            - Alpha#54: ((-1 * ((low - close) * (open^5))) / ((low - high) * (close^5)))
                        (close location in the range times (open/close)^5; paper: delay-0)
            Operators: paper Appendix A.2 (rank = cross-sectional over the coins present; delay / delta / sum / Ts_Rank =
            per-coin time series over the past d DAYS; returns = daily close-to-close). Translation to crypto (24/7): a
            "day" = one UTC calendar day built from the 1h bars of spot/binance_<COIN> (open = first hour's open,
            high/low = max/min, close = last hour's close, volume = sum of vol). The SIGNAL uses those raw Binance daily
            OHLCV; the RESPONSE (forward return) uses primary/validated_<COIN> `price` only. Every alpha: signal from day
            d, response from end of day d to end of day d+1 (00:00 UTC to 00:00 UTC). For the delay-0 pair (#53, #54) the
            paper trades at day d's close; in crypto that close IS day d+1's open, so the same window applies. Note the
            division hazards (#53: close == low; #54: high == low) and how they are handled, in DECISIONS.md.
            The paper's sample is US equities 2010-2013 (pre-dates VAL; no holdout flag).

MIN_USEFUL_IC: 0.02   (rank IC per day; RUNBOOK_v3 v3.2: "supported" = significant AND at least this; cost never decides a
            branch, it sets the STANDALONE / COMBINE-ONLY label in SIGNALS.md)

ALREADY TESTED (names only, do NOT pick these): BTC hour-of-day seasonality (the 21:00-23:00 UTC window); BTC flow-imbalance and
            positioning / crowd-positioning claims; BTC-dislocation propagation to other coins; short-horizon reversal after taker
            imbalance; and the previous run on this panel (runs/2026-09-30_crypto-panel-1h — do NOT open that folder):
            daily time-series reversal; reversal after panel volume-shock days; same-hour-yesterday 1h reversal; high-volume
            relative winners continue; intraday 6h-block reversal; 6h reversal in high trailing vol; crash-day rebound (and a
            volatility-regime filter on it); and runs/2026-10-05_crypto-validated-1h (do NOT open it either): perp premium cross-section,
            Fear & Greed level, prior-session S&P 500 return; and runs/2026-10-05_crypto-101alphas (do NOT open it): the
            first batch of this paper's alphas, #101 intraday-range momentum, #42 vwap-close reversal, #2 volume-change /
            intraday-return correlation, #6 open-volume correlation, #4 time-series rank of the cross-sectional rank of
            low, and their children (raw volume-change / return co-movement; flipped #42 over 2 days). (Topic names only;
            no results.)

PRE-APPROVED INSTALLS: pandas, pyarrow, numpy, scipy, statsmodels, matplotlib   (into /home/user/eda-routine/.venv only)

ROUND-TRIP COST (bp): MEASURED FTMO CFD costs (spread at the trade minute from FTMO quotes 2022+, coin x hour medians applied to
            2019-21; commission 3.25 bp/side), round trip for a 24h hold INCLUDING one rollover night (8.2 bp; subtract it for an
            intraday trade, add 8.2 per extra night, Friday x3): BTC 18.9, ETH 25.4, LTC 36.5, ADA/DOGE/DOT/BNB/SOL ~45-47,
            BCH 65.5, XRP 68.6. Use these, not the `ftmo_spread_rt_bp` column on spot/binance_* (an old single live sample).

NOTES: CLOUD RUN. Map every C:\Users\User\<x> path in RUNBOOK_v3.md to /home/user/<x> (backslashes to slashes).
       Follow RUNBOOK_v3.md (v3.2: several CONFIRM folds; every allowed fold before HIGH-CONFIRM; the SIGNAL CONSTRUCTION
       STANDARD; weak signals kept and handed off in SIGNALS.md). Run gate.py as the runbook says.
       Scope Phase 0 to the PRIMARY TARGET panel first (10 coins, 1h); profile the other families only for coverage,
       knowability and alignment, not as 234 separate studies. This run needs only primary/ and spot/binance_*; the other
       families matter only as rivals (e.g. a volatility or market-wide twin).
       There is no eda_guard.py in this checkout: implement the guard as an assertion at every load that no row is later
       than VAL_END, and log it.
       READ-ONLY method files outside this repo, and ONLY these: backtest_engine/backtest_engine2/PROTOCOL.md,
       skills/00-overview.md, skills/12-alpha-overview.md, skills/14c-eda.md, cellplot.py, data_hygiene.py;
       finding-alphas/data-hygiene.md. Never open anything else in finding-alphas or backtest_engine (no alpha_log.md, no
       hunts/, no notebooks, no data/, no _SEALED_HOLDOUT.md, no x0* files). Inside eda-routine never open runs/ other than
       your own run folder.
