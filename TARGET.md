# TARGET: what the next EDA run should look at

Edit this file, then set STATUS to READY and click "Run now" on the routine. The routine sets STATUS to
`DONE <run folder>` when finished, so a finished target is never re-run by accident.

DATA MUST BE PREPARED FIRST: `python C:\Users\User\eda-routine\prep_target.py <source> <name>` writes a copy that
STOPS at the end of VAL (TEST and sealed rows are never copied). Point DATA at that copy, never at the source.

STATUS: READY

NAME: crypto-panel-1h

DATA: /home/user/eda-routine/data/crypto_panel_2026-09-30/   (cloud session; on the desktop this is
      C:\Users\User\eda-routine\data\crypto_panel_2026-09-30\). Read README.md, MANIFEST.csv and CUT.json there FIRST.
      224 parquet files in 7 families, 5,685,039 rows, every file cut at 2023-11-30 23:59:59 UTC (verified per file).
      PRIMARY TARGET (the returns every hypothesis must predict): spot/binance_<COIN>.parquet for the 10 coins BTCUSD,
      ETHUSD, BNBUSD, SOLUSD, XRPUSD, DOGEUSD, ADAUSD, LTCUSD, BCHUSD, DOTUSD. Everything else is a candidate explanatory
      series; use MANIFEST.csv `knowable` to lag it to its entry-knowable time before ANY join (data-hygiene.md rule).

PROVENANCE: Per file in MANIFEST.csv (source / type / freq / stamp / knowable). Primary target: Binance SPOT trade-print
            OHLCV (last-trade prices, NO bid/ask), 1-hour bars, UTC, stamped at the bar OPEN, knowable at open + 1h.

CLEANED?: NO. Raw pulls: no row dropped, gaps LEFT MISSING, nothing filled. Known facts (NOT leads):
          - Missing hours on Binance spot: 20-128 per coin (exchange outages / maintenance).
          - spot/bitstamp_BTCUSD 2011-2013: stale feed, up to ~90% zero-volume hours and flat bars.
          - spot/coinbase_XRPUSD has a delisting gap 2021-01 -> 2023-07.
          - Zero-gap rate (open == previous close) is 0.3-0.6 on the 1h crypto bars: normal for 24/7 trade prints,
            not a synthetic-open artifact.
          - defi/*: vendor-aggregated and BACKFILLED (not point-in-time). onchain/cm_* exchange-flow metrics are
            revised backwards (not point-in-time). macro/cftc_*: knowable 3 days after the stamp. macro/yahoo_*: lag one
            session; Yahoo index opens can be synthetic (close-to-close only).
          - macro/nyfed_rrp `counterparties` is an all-null column.

TRAIN_END: 2023-03-19
VAL_START: 2023-03-25
VAL_END:   2023-11-30
VAL_NOTE:  Two reasons VAL is weak evidence. (1) BTC VAL was crossed twice by earlier work (both pre-registered) and overlaps a
           spent pooled row of an earlier BTC seasonality EDA: SOFT-clean for BTC; clean for the other nine coins as far as
           this file knows. (2) VAL may be a DIFFERENT REGIME from TRAIN: from 2023-04 BTC's 1-minute trade counts fell ~8x
           (cause not established). A lead about trade counts or volume can fail VAL for structural reasons.

SOURCE_MODE: E
            (Set by the user's assistant on 2026-09-30, user away: the user asked for the routine to "get to work" on this
            new dataset; INBOX.md is empty. Mode E = every hypothesis traces to a Phase 0 observation on EXPLORE.)

HYPOTHESIS: none (mode E: hypotheses come from Phase 0 observations only)

ALREADY TESTED (names only, do NOT pick these): BTC hour-of-day seasonality (the 21:00-23:00 UTC window); BTC flow-imbalance and
            positioning / crowd-positioning claims; BTC-dislocation propagation to other coins; short-horizon reversal after taker
            imbalance. (Topic names only; no results.)

PRE-APPROVED INSTALLS: pandas, pyarrow, numpy, scipy, statsmodels, matplotlib   (into /home/user/eda-routine/.venv only)

ROUND-TRIP COST (bp): per coin = spot/binance_<COIN> columns `ftmo_spread_rt_bp` + `ftmo_commission_rt_bp` (6.5). FTMO CFD
            costs, one live sample 2026-09-02, constant (not a history): BTC 6.6, BNB 6.6, ETH 9.0, SOL 9.5, DOGE 17.5,
            XRP 17.6, ADA 21.6, BCH 31.0, DOT 31.9, LTC 36.5. Holding past the daily rollover adds ~8.2 bp per night on every
            coin (-30%/yr swap, both sides, triple on Friday), so horizons that cross a rollover pay it.

NOTES: CLOUD RUN. Map every C:\Users\User\<x> path in RUNBOOK_v3.md to /home/user/<x> (backslashes to slashes).
       Scope Phase 0 to the PRIMARY TARGET panel first (10 coins, 1h); profile the other families only for coverage,
       knowability and alignment, not as 224 separate studies.
       There is no eda_guard.py in this checkout: implement the guard as an assertion at every load that no row is later
       than VAL_END, and log it.
       READ-ONLY method files outside this repo, and ONLY these: backtest_engine/backtest_engine2/PROTOCOL.md,
       skills/00-overview.md, skills/12-alpha-overview.md, skills/14c-eda.md, cellplot.py, data_hygiene.py;
       finding-alphas/data-hygiene.md. Never open anything else in finding-alphas or backtest_engine (no alpha_log.md, no
       hunts/, no notebooks, no data/, no _SEALED_HOLDOUT.md, no x0* files).
