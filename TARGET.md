# TARGET: what the next EDA run should look at

Edit this file, then set STATUS to READY and click "Run now" on the routine. The routine sets STATUS to
`DONE <run folder>` when finished, so a finished target is never re-run by accident.

DATA MUST BE PREPARED FIRST: `python C:\Users\User\eda-routine\prep_target.py <source> <name>` writes a copy that
STOPS at the end of VAL (TEST and sealed rows are never copied). Point DATA at that copy, never at the source.

STATUS: DONE C:\Users\User\eda-routine\runs\2026-09-25_btc-spot-1m-clean_v2

NAME: btc-spot-1m-clean

DATA: C:\Users\User\eda-routine\data\btcusdt_spot_1m_clean\btcusdt_spot_1m_clean.parquet
      Read C:\Users\User\eda-routine\data\btcusdt_spot_1m_clean\CLEANING_LOG.md and CUT.json first, and look at
      plots\ in that folder. 3,274,945 rows, 2017-08-17 04:00 to 2023-11-30 23:59 UTC, index `t` (tz-aware UTC).

PROVENANCE: Trade-based OHLCV bars (last-trade prices, NO bid/ask) from Binance BTCUSDT SPOT, 1-minute, UTC,
            stamped at the bar's OPEN time, so a bar stamped T is knowable only at T + 60 s (use it from the NEXT
            bar). Open-time stamping is INFERRED from month boundaries (every full month runs 00:00..23:59), not
            confirmed against exchange documentation: Step 0 should re-check it.

CLEANED?: yes, by clean_btc_spot.py, following finding-alphas\data-skill\tree-reference.md (gates 0-6, 8, 10; gate 7
          N/A because there are no quotes). NO ROW WAS DROPPED. What the routine must know:
          - `low` is NaN on 11 bars (source had low = 0.0); `quote` is NaN on 1,550 bars (source had quote = 0).
          - Missing minutes (32,495, 0.98%, 74% of them in 2017) are LEFT MISSING. `gap_min` = minutes since the
            previous bar; keep `gap_min == 1` for 1-minute returns.
          - Flags, never altered: `flag_repeat_prev_bar` (37), `flag_close_outlier` (3), `flag_wick_gt3pct` (47).
          - 2017 is a thin market (18.9% of bars are flat: open=high=low=close). Treat it with care.
          - No spread, no cost: ROUND-TRIP COST is UNKNOWN for this file.

TRAIN_END: 2023-03-19
VAL_START: 2023-03-25
VAL_END:   2023-11-30
VAL_NOTE:  Two reasons VAL is weak evidence. (1) BTC VAL was crossed twice by arc #047 (both pre-registered) and overlaps a
           spent pooled row of the 21:00-23:00 UTC seasonality EDA (see _SEALED_HOLDOUT.md): SOFT-clean. (2) VAL is a
           DIFFERENT REGIME from TRAIN: from 2023-04, median trades per minute fall ~8x (about 3,600 to 450, then
           240-360) and the share of zero-return bars rises from <0.3% to 4-12% (CLEANING_LOG.md, Gate 4b; cause not
           established). A lead about trade counts, volume or 1-minute tick behaviour can fail VAL for structural reasons.

HYPOTHESIS: SEARCH
            (Write SEARCH and the routine finds ONE claim itself on SSRN or Substack, following RUNBOOK step 1. Or write your own
            claim in the form "a change in [data] predicts [price response] because [economic reason]", optionally with an SSRN or
            Substack URL or title on a second line.)

ALREADY TESTED (names only, do NOT pick these): BTC hour-of-day seasonality (the 21:00-23:00 UTC window); BTC flow-imbalance and
            positioning / crowd-positioning claims; BTC-dislocation propagation to other coins; short-horizon reversal after taker
            imbalance. (Topic names only, taken from the holdout file; no results. Edit freely.)

PRE-APPROVED INSTALLS: none   (14c says ask before heavy dependencies; the routine cannot ask, so with "none" it installs
                              nothing. To pre-approve, list packages here, e.g. "pymc, arviz", and they go only into
                              C:\Users\User\eda-routine\.venv.)

ROUND-TRIP COST (bp): <blank: cost unknown>

NOTES: This is the routine's first test. Read the report against CLEANING_LOG.md: the routine should NOT re-discover the
       cleaning findings as "leads" (missing minutes, the zero-quote block, the 2017 flat bars, the regime break).
       Other prepared copies sit in data\ (btcusdtperp_5m, btcusdtperp_1m, btcusdt_spot_1m, btcusdt_spot_monthly). They
       are RAW and TRAIN-only or uncleaned: do not use them as the target.
