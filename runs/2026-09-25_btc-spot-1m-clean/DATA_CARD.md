# DATA CARD: btc-spot-1m-clean (run 2026-09-25)

**One-line provenance:** these prices are **trade prints** (last-trade OHLC per minute, no bid/ask) from
**Binance BTCUSDT SPOT**, timestamped in **UTC at the bar's OPEN time**, knowable at **stamp + 60 s** (use from the NEXT bar).

| item | value | source |
|---|---|---|
| file | `C:\Users\User\eda-routine\data\btcusdt_spot_1m_clean\btcusdt_spot_1m_clean.parquet` (one file, one feed) | TARGET.md; CUT.json present |
| rows (all) | 3,274,945; 2017-08-17 04:00 -> 2023-11-30 23:59 UTC. Max stamp == VAL_END, **no row after VAL_END** | pyarrow read of index |
| rows TRAIN (<= 2023-03-19 23:59) | 2,906,457 | tables/00_datacard_checks.json |
| timezone | tz-aware UTC in the file (`timestamp[ns, tz=UTC]`); 24/7 market, no DST in the stamps | schema |
| venue / instrument | Binance, BTCUSDT spot (not perp) | TARGET.md, CLEANING_LOG Gate 0 |
| cleaning | clean_btc_spot.py, gates 0-6, 8, 10; no rows dropped; `low` NaN on 11 bars, `quote` NaN on 1,550 | CLEANING_LOG.md |

## Columns: what each IS

| column | is | knowable |
|---|---|---|
| `open` | price of the first trade in [T, T+60s) | T+60 s (treated as bar-complete) |
| `high` / `low` | max / min trade price in the minute (`low` NaN on 11 bars, source had 0) | T+60 s |
| `close` | last trade price in the minute (trade print, carries bid-ask bounce) | T+60 s |
| `vol` | base volume (BTC) traded in the minute | T+60 s |
| `quote` | quote volume (USDT); NaN on 1,550 bars; `quote/vol` = VWAP | T+60 s |
| `n` | number of trades | T+60 s |
| `buy_vol`, `sell_vol` | taker-buy / taker-sell base volume (`buy_vol + sell_vol == vol` on every row). Taker side is an INFERENCE from Binance's kline format (taker-buy base volume), from memory, not checked against documentation | T+60 s |
| `n_buy`, `n_sell` | trade counts by taker side (sum == n) | T+60 s |
| `gap_min` | minutes since previous bar; 1 = consecutive | T |
| `flag_*` | cleaning flags (low_invalid 11, quote_bad 1,550, repeat_prev_bar 37, close_outlier 3, wick_gt3pct 47) | - |

No bid, no ask, no mid, no spread series. **Returns in this run are close-to-close log returns on trade prints, only
where `gap_min == 1`**, never across a missing minute. No fill, no interpolation. One feed only (no pooling).

## Timestamp: OPEN or CLOSE? Re-checked (not assumed)

Test: scheduled activity fires at HH:00:00 (hourly candle closes, bots). If stamps are OPEN times the burst lands in the
bar **stamped :00** (covering HH:00-HH:01); if CLOSE times, the bar stamped :00 covers HH:59-HH:00 (before the event)
and the burst lands in the bar stamped :01.
Result (TRAIN 2018+, plots/00_timestamp_open_check.png, tables/00_activity_by_minute_of_hour.csv): mean log(trades) is
**+0.237** above the minute-of-hour baseline in the bar stamped :00 vs **+0.144** at :01; mean |r| is **1.36x** baseline at :00
vs **1.20x** at :01. The peak is at :00 -> **consistent with OPEN-time stamping**. Also: 2,007 of 2,041 TRAIN days start at
00:00 and 2,018 end at 23:59 (the rest start/end inside a gap). The first bar of the file is 2017-08-17 04:00.
Verdict: OPEN time, supported by two internal checks; still not confirmed against exchange documentation.

## Hygiene checks (data-hygiene.md)

- **Zero-gap rate** (open == previous close, consecutive minutes; tables/00_zero_gap_rate_by_year.csv): 20-46% per year
  (2017 28.6%, 2021 43.7%, 2022 46.1%). Far above the <2% equity guideline, but here `open` is the first TRADE of the next
  minute, and consecutive trades at the same price are normal in a deep book; median |open - prev close| is 0.002-0.4 bp.
  Not a vendor-synthetic open. Any open-vs-prev-close quantity is ~0 by construction: not used.
- **Roll check** (tables/00_roll_corwin_schultz_by_year.csv): lag-1 autocovariance of 1-min returns is NEGATIVE 2017-2020
  (implied Roll spread 24.9 bp in 2017, 4.8 bp 2018, 1.5 bp 2019, 2.4 bp 2020) and POSITIVE 2021-2023Q1 (Roll undefined).
  Corwin-Schultz median 0.8-2.7 bp 2018-2023 (0 in 2017, flat bars). These are statistical estimates, not quotes.
- **Round-trip cost: UNKNOWN** (TARGET.md). Every effect in this run is reported as "cost unknown".
- Regime break at 2023-04 (trades/min fall ~8x, zero-return share 4-12%): lies in VAL, known from CLEANING_LOG Gate 4b. NOT a lead.

## Split used

TRAIN 2017-08-17 -> 2023-03-19 (explore); EMBARGO 2023-03-20 -> 2023-03-24 (ignored); VAL 2023-03-25 -> 2023-11-30 (opened once, Step 6).
