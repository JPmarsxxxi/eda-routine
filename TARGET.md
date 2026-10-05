# TARGET: what the next EDA run should look at

Edit this file, then set STATUS to READY and click "Run now" on the routine. The routine sets STATUS to
`DONE <run folder>` when finished, so a finished target is never re-run by accident.

DATA MUST BE PREPARED FIRST: `python C:\Users\User\eda-routine\prep_target.py <source> <name>` writes a copy that
STOPS at the end of VAL (TEST and sealed rows are never copied). Point DATA at that copy, never at the source.

STATUS: READY

NAME: crypto-101alphas

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
            (Set by the user's assistant on 2026-10-05 at the user's request: "pick about 5 [alphas] that would apply to crypto
            and EDA them". Paper = INBOX.md section B entry 1601.00991v3.pdf, local file in this repo root.)

HYPOTHESIS: The user asked for these FIVE alphas from the paper (Appendix A), chosen because they need only OHLCV + vwap (no
            industry neutralisation, no market cap) and do not repeat an ALREADY TESTED topic. Phase 1 = exactly these five, one
            candidate each (the 6-candidate cap still holds). Formulas verbatim from the paper:
            - Alpha#101: ((close - open) / ((high - low) + .001))        paper: delay-1 MOMENTUM (close > open -> long next day)
            - Alpha#42:  (rank((vwap - close)) / rank((vwap + close)))   paper: delay-0 MEAN-REVERSION, traded at the close
            - Alpha#2:   (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))
            - Alpha#6:   (-1 * correlation(open, volume, 10))
            - Alpha#4:   (-1 * Ts_Rank(rank(low), 9))
            Operators: paper Appendix A.1 (rank = cross-sectional over the 10 coins; correlation/ts_rank = time-series over the past
            d DAYS). Translation to crypto (24/7): a "day" = one UTC calendar day built from the 1h bars of spot/binance_<COIN>
            (open = first hour's open, high/low = max/min, close = last hour's close, volume = sum of vol, vwap = sum(quote_vol) /
            sum(vol)). The SIGNAL uses those raw Binance daily OHLCV; the RESPONSE (forward return) uses primary/validated_<COIN>
            `price` only. delay-1 alphas: signal from day d, return from end of day d to end of day d+1 (00:00 UTC to 00:00 UTC).
            delay-0 (Alpha#42): same response window, and note that in crypto "the close" of day d is the open of day d+1.
            The paper's sample is US equities 2010-2013 (pre-dates VAL; no holdout flag).

ALREADY TESTED (names only, do NOT pick these): BTC hour-of-day seasonality (the 21:00-23:00 UTC window); BTC flow-imbalance and
            positioning / crowd-positioning claims; BTC-dislocation propagation to other coins; short-horizon reversal after taker
            imbalance; and the previous run on this panel (runs/2026-09-30_crypto-panel-1h — do NOT open that folder):
            daily time-series reversal; reversal after panel volume-shock days; same-hour-yesterday 1h reversal; high-volume
            relative winners continue; intraday 6h-block reversal; 6h reversal in high trailing vol; crash-day rebound (and a
            volatility-regime filter on it); and runs/2026-10-05_crypto-validated-1h (do NOT open it either): perp premium cross-section,
            Fear & Greed level, prior-session S&P 500 return. (Topic names only; no results.)

PRE-APPROVED INSTALLS: pandas, pyarrow, numpy, scipy, statsmodels, matplotlib   (into /home/user/eda-routine/.venv only)

ROUND-TRIP COST (bp): MEASURED FTMO CFD costs (spread at the trade minute from FTMO quotes 2022+, coin x hour medians applied to
            2019-21; commission 3.25 bp/side), round trip for a 24h hold INCLUDING one rollover night (8.2 bp; subtract it for an
            intraday trade, add 8.2 per extra night, Friday x3): BTC 18.9, ETH 25.4, LTC 36.5, ADA/DOGE/DOT/BNB/SOL ~45-47,
            BCH 65.5, XRP 68.6. Use these, not the `ftmo_spread_rt_bp` column on spot/binance_* (an old single live sample).

NOTES: CLOUD RUN. Map every C:\Users\User\<x> path in RUNBOOK_v3.md to /home/user/<x> (backslashes to slashes).
       Follow RUNBOOK_v3.md (v3.1: several CONFIRM folds, enforced by gate.py). Run gate.py as the runbook says.
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
