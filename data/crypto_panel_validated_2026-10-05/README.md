# crypto_panel_validated_2026-10-05

A multi-source crypto and macro panel, cut at VAL_END. Same as `crypto_panel_2026-09-30` (all 224 files unchanged, same
folders) PLUS a new `primary/` folder: one VALIDATED hourly price file per coin. **The primary/ files are the prices every
hypothesis must predict.** The raw `spot/binance_*` files stay as explanatory series (they carry OHLC, trade counts and
taker buy/sell volume, which primary/ does not).

## primary/ (10 files) — how the prices were built

- Columns: `t` (UTC bar OPEN) | `price` (value at bar END) | `source` | `ftmo_spread_bp` | `binance_quote_vol` | `new_source`.
- `source = binance_trade`: Binance spot last-trade close, used only in years where it was checked against Binance's own
  bid/ask mid and agreed (median |gap| <= 2.5 bp, daily-return difference <= 5 bp).
- `source = ftmo_mid`: FTMO CFD hourly mid (bid + bar spread / 2), checked against FTMO ticks. Used from 2022-01-01 for BTC ETH
  XRP LTC ADA DOGE DOT. BNB, BCH and SOL are Binance only. DOT's stored FTMO spread was 10x too small and is corrected here.
- Years that failed the check are ABSENT (left as holes, never patched): ADA 2019, DOGE 2019-20, SOL 2020, BCH 2022-23 (BCH ends
  2021-12-31). Coverage starts 2019-01-01 at the earliest.
- `new_source = True` on the first bar after a source switch (Binance -> FTMO, offset 0.4-3 bp median) or after a gap:
  **never compute a return across it.**
- Only `price` (a close) is given: no open/high/low. `binance_quote_vol` is the raw Binance quote volume for that hour on
  every row (also on ftmo_mid rows). FTMO has fixed missing Saturday hours (bars closing 06-11 and 18:00 New York).
- `ftmo_spread_bp`: FTMO bar spread (the hour's MINIMUM quoted spread, not the spread at a given minute), ftmo_mid rows only.

| file | rows | first | last | rows by source |
|---|---:|---|---|---|
| validated_ADAUSD.parquet | 33,909 | 2020-01-01 00:00:00 | 2023-11-30 23:00:00 | {'binance_trade': 17513, 'ftmo_mid': 16396} |
| validated_BCHUSD.parquet | 18,319 | 2019-11-28 10:00:00 | 2021-12-31 23:00:00 | {'binance_trade': 18319} |
| validated_BNBUSD.parquet | 43,020 | 2019-01-01 00:00:00 | 2023-11-30 23:00:00 | {'binance_trade': 43020} |
| validated_BTCUSD.parquet | 42,642 | 2019-01-01 00:00:00 | 2023-11-30 23:00:00 | {'binance_trade': 26245, 'ftmo_mid': 16397} |
| validated_DOGEUSD.parquet | 25,145 | 2021-01-01 00:00:00 | 2023-11-30 23:00:00 | {'ftmo_mid': 16398, 'binance_trade': 8747} |
| validated_DOTUSD.parquet | 28,379 | 2020-08-18 23:00:00 | 2023-11-30 23:00:00 | {'ftmo_mid': 16397, 'binance_trade': 11982} |
| validated_ETHUSD.parquet | 42,646 | 2019-01-01 00:00:00 | 2023-11-30 23:00:00 | {'binance_trade': 26245, 'ftmo_mid': 16401} |
| validated_LTCUSD.parquet | 42,643 | 2019-01-01 00:00:00 | 2023-11-30 23:00:00 | {'binance_trade': 26245, 'ftmo_mid': 16398} |
| validated_SOLUSD.parquet | 25,522 | 2021-01-01 00:00:00 | 2023-11-30 23:00:00 | {'binance_trade': 25522} |
| validated_XRPUSD.parquet | 42,642 | 2019-01-01 00:00:00 | 2023-11-30 23:00:00 | {'binance_trade': 26245, 'ftmo_mid': 16397} |

## Cutoff and splits

Every file cut at `2023-11-30T23:59:59 UTC` (see CUT.json); every file re-checked at build. TRAIN_END 2023-03-19,
VAL 2023-03-25 -> 2023-11-30. No TEST or later rows exist in this folder.

---

# The 224 files carried over from crypto_panel_2026-09-30 (README of that bundle follows unchanged)

A multi-source crypto and macro panel, cut at VAL_END.

## Cutoff and splits (from CUT.json)

- Cutoff (inclusive, UTC): `2023-11-30T23:59:59+00:00`
- TRAIN_END: 2023-03-19
- VAL_START: 2023-03-25
- VAL_END: 2023-11-30
- Note: TEST (2023-12-06 -> 2024-07-31) and everything from 2024-08-01 were NOT copied. Every file was checked: no row after the cutoff.

Contents: 224 parquet files, 5,685,039 rows, in 7 family folders, plus `MANIFEST.csv` (full per-file metadata: source, stamp, notes, columns) and `CUT.json`.

## Files by family

first/last are the min/max of each file's time column as read at install (they match MANIFEST.csv).

### spot (27 files, 1,195,949 rows)

| file | rows | first | last | freq | knowable |
|---|---:|---|---|---|---|
| binance_ADAUSD.parquet | 49,204 | 2018-04-17 04:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| binance_BCHUSD.parquet | 35,094 | 2019-11-28 10:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| binance_BNBUSD.parquet | 53,059 | 2017-11-06 03:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| binance_BTCUSD.parquet | 54,996 | 2017-08-17 04:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| binance_DOGEUSD.parquet | 38,584 | 2019-07-05 12:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| binance_DOTUSD.parquet | 28,757 | 2020-08-18 23:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| binance_ETHUSD.parquet | 54,996 | 2017-08-17 04:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| binance_LTCUSD.parquet | 52,171 | 2017-12-13 03:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| binance_SOLUSD.parquet | 28,942 | 2020-08-11 06:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| binance_XRPUSD.parquet | 48,792 | 2018-05-04 08:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| bitstamp_BTCUSD.parquet | 107,700 | 2011-08-18 12:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| coinbase_ADAUSD.parquet | 23,691 | 2021-03-18 16:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| coinbase_BCHUSD.parquet | 51,969 | 2017-12-20 01:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| coinbase_BTCUSD.parquet | 73,278 | 2015-07-20 21:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| coinbase_DOGEUSD.parquet | 21,843 | 2021-06-03 16:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| coinbase_DOTUSD.parquet | 21,531 | 2021-06-16 16:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| coinbase_ETHUSD.parquet | 65,869 | 2016-05-18 00:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| coinbase_LTCUSD.parquet | 62,801 | 2016-08-17 04:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| coinbase_SOLUSD.parquet | 21,507 | 2021-06-17 16:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| coinbase_USDTUSD.parquet | 22,579 | 2021-05-04 01:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| coinbase_XRPUSD.parquet | 19,993 | 2019-02-26 17:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| upbit_ADAKRW.parquet | 53,709 | 2017-10-06 08:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| upbit_BTCKRW.parquet | 54,102 | 2017-09-25 03:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| upbit_DOGEKRW.parquet | 24,195 | 2021-02-24 06:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| upbit_ETHKRW.parquet | 53,992 | 2017-09-25 03:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| upbit_SOLKRW.parquet | 18,618 | 2021-10-15 06:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| upbit_XRPKRW.parquet | 53,977 | 2017-09-25 13:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |

### perp (42 files, 2,929,136 rows)

| file | rows | first | last | freq | knowable |
|---|---:|---|---|---|---|
| bvol_BTC.parquet | 3,888 | 2023-06-20 00:00:00 | 2023-11-30 23:00:00 | 1h (resampled from raw ticks) | hour end |
| bvol_ETH.parquet | 3,887 | 2023-06-20 00:00:00 | 2023-11-30 23:00:00 | 1h (resampled from raw ticks) | hour end |
| funding_ADAUSD.parquet | 4,234 | 2020-01-19 16:00:00 | 2023-11-30 16:00:00 | 8h (4h/1h on some coins later) | at settlement; the predicted rate is visible live before it |
| funding_BCHUSD.parquet | 4,290 | 2020-01-01 00:00:00 | 2023-11-30 16:00:00 | 8h (4h/1h on some coins later) | at settlement; the predicted rate is visible live before it |
| funding_BNBUSD.parquet | 4,169 | 2020-02-10 08:00:00 | 2023-11-30 16:00:00 | 8h (4h/1h on some coins later) | at settlement; the predicted rate is visible live before it |
| funding_BTCUSD.parquet | 4,290 | 2020-01-01 00:00:00 | 2023-11-30 16:00:00 | 8h (4h/1h on some coins later) | at settlement; the predicted rate is visible live before it |
| funding_DOGEUSD.parquet | 3,716 | 2020-07-10 08:00:00 | 2023-11-30 16:00:00 | 8h (4h/1h on some coins later) | at settlement; the predicted rate is visible live before it |
| funding_DOTUSD.parquet | 3,593 | 2020-08-20 08:00:00 | 2023-11-30 16:00:00 | 8h (4h/1h on some coins later) | at settlement; the predicted rate is visible live before it |
| funding_ETHUSD.parquet | 4,290 | 2020-01-01 00:00:00 | 2023-11-30 16:00:00 | 8h (4h/1h on some coins later) | at settlement; the predicted rate is visible live before it |
| funding_LTCUSD.parquet | 4,265 | 2020-01-09 08:00:00 | 2023-11-30 16:00:00 | 8h (4h/1h on some coins later) | at settlement; the predicted rate is visible live before it |
| funding_SOLUSD.parquet | 3,595 | 2020-09-13 16:00:00 | 2023-11-30 16:00:00 | 8h (4h/1h on some coins later) | at settlement; the predicted rate is visible live before it |
| funding_XRPUSD.parquet | 4,274 | 2020-01-06 08:00:00 | 2023-11-30 16:00:00 | 8h (4h/1h on some coins later) | at settlement; the predicted rate is visible live before it |
| metrics_ADAUSD.parquet | 210,230 | 2021-12-01 00:00:00 | 2023-11-30 23:55:00 | 5m | create_time (a few seconds after) |
| metrics_BCHUSD.parquet | 210,193 | 2021-12-01 00:00:00 | 2023-11-30 23:55:00 | 5m | create_time (a few seconds after) |
| metrics_BNBUSD.parquet | 210,230 | 2021-12-01 00:00:00 | 2023-11-30 23:55:00 | 5m | create_time (a few seconds after) |
| metrics_BTCUSD.parquet | 341,064 | 2020-09-01 00:00:00 | 2023-11-30 23:55:00 | 5m | create_time (a few seconds after) |
| metrics_DOGEUSD.parquet | 210,230 | 2021-12-01 00:00:00 | 2023-11-30 23:55:00 | 5m | create_time (a few seconds after) |
| metrics_DOTUSD.parquet | 210,230 | 2021-12-01 00:00:00 | 2023-11-30 23:55:00 | 5m | create_time (a few seconds after) |
| metrics_ETHUSD.parquet | 210,230 | 2021-12-01 00:00:00 | 2023-11-30 23:55:00 | 5m | create_time (a few seconds after) |
| metrics_LTCUSD.parquet | 210,187 | 2021-12-01 00:00:00 | 2023-11-30 23:55:00 | 5m | create_time (a few seconds after) |
| metrics_SOLUSD.parquet | 210,230 | 2021-12-01 00:00:00 | 2023-11-30 23:55:00 | 5m | create_time (a few seconds after) |
| metrics_XRPUSD.parquet | 210,229 | 2021-12-01 00:00:00 | 2023-11-30 23:55:00 | 5m | create_time (a few seconds after) |
| perp_klines_ADAUSD.parquet | 33,592 | 2020-01-31 08:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_klines_BCHUSD.parquet | 34,320 | 2020-01-01 00:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_klines_BNBUSD.parquet | 33,352 | 2020-02-10 08:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_klines_BTCUSD.parquet | 34,320 | 2020-01-01 00:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_klines_DOGEUSD.parquet | 29,727 | 2020-07-10 09:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_klines_DOTUSD.parquet | 28,697 | 2020-08-22 07:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_klines_ETHUSD.parquet | 34,320 | 2020-01-01 00:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_klines_LTCUSD.parquet | 34,000 | 2020-01-09 08:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_klines_SOLUSD.parquet | 28,025 | 2020-09-14 07:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_klines_XRPUSD.parquet | 34,072 | 2020-01-06 08:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_premium_ADAUSD.parquet | 33,423 | 2020-01-31 08:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_premium_BCHUSD.parquet | 34,151 | 2020-01-01 00:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_premium_BNBUSD.parquet | 33,183 | 2020-02-10 08:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_premium_BTCUSD.parquet | 34,151 | 2020-01-01 00:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_premium_DOGEUSD.parquet | 29,558 | 2020-07-10 09:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_premium_DOTUSD.parquet | 28,528 | 2020-08-22 07:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_premium_ETHUSD.parquet | 34,151 | 2020-01-01 00:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_premium_LTCUSD.parquet | 33,975 | 2020-01-09 08:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_premium_SOLUSD.parquet | 28,000 | 2020-09-14 07:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| perp_premium_XRPUSD.parquet | 34,047 | 2020-01-06 08:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |

### deriv (14 files, 163,883 rows)

| file | rows | first | last | freq | knowable |
|---|---:|---|---|---|---|
| deribit_dvol_BTC.parquet | 23,568 | 2021-03-24 00:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| deribit_dvol_ETH.parquet | 23,568 | 2021-03-24 00:00:00 | 2023-11-30 23:00:00 | 1h | open + 1h |
| deribit_funding_BTC.parquet | 40,197 | 2019-05-01 01:00:00 | 2023-11-30 23:00:00 | 1h | at stamp |
| deribit_funding_ETH.parquet | 40,197 | 2019-05-01 01:00:00 | 2023-11-30 23:00:00 | 1h | at stamp |
| hyperliquid_funding_ADAUSD.parquet | 954 | 2023-10-22 06:00:00 | 2023-11-30 23:00:00 | 1h | at stamp |
| hyperliquid_funding_BCHUSD.parquet | 3,691 | 2023-06-30 03:00:00 | 2023-11-30 23:00:00 | 1h | at stamp |
| hyperliquid_funding_BNBUSD.parquet | 4,303 | 2023-05-12 00:00:00 | 2023-11-30 23:00:00 | 1h | at stamp |
| hyperliquid_funding_BTCUSD.parquet | 4,303 | 2023-05-12 00:00:00 | 2023-11-30 23:00:00 | 1h | at stamp |
| hyperliquid_funding_DOGEUSD.parquet | 4,303 | 2023-05-12 00:00:00 | 2023-11-30 23:00:00 | 1h | at stamp |
| hyperliquid_funding_DOTUSD.parquet | 1,908 | 2023-09-12 12:00:00 | 2023-11-30 23:00:00 | 1h | at stamp |
| hyperliquid_funding_ETHUSD.parquet | 4,303 | 2023-05-12 00:00:00 | 2023-11-30 23:00:00 | 1h | at stamp |
| hyperliquid_funding_LTCUSD.parquet | 4,303 | 2023-05-12 00:00:00 | 2023-11-30 23:00:00 | 1h | at stamp |
| hyperliquid_funding_SOLUSD.parquet | 4,303 | 2023-05-12 00:00:00 | 2023-11-30 23:00:00 | 1h | at stamp |
| hyperliquid_funding_XRPUSD.parquet | 3,982 | 2023-06-18 00:00:00 | 2023-11-30 23:00:00 | 1h | at stamp |

### onchain (28 files, 891,021 rows)

| file | rows | first | last | freq | knowable |
|---|---:|---|---|---|---|
| bcom_avg_block_size.parquet | 5,431 | 2009-01-17 00:00:00 | 2023-11-30 00:00:00 | day | period end |
| bcom_cost_per_transaction.parquet | 5,431 | 2009-01-17 00:00:00 | 2023-11-30 00:00:00 | day | period end |
| bcom_difficulty.parquet | 5,445 | 2009-01-03 00:00:00 | 2023-11-30 00:00:00 | day | period end |
| bcom_estimated_transaction_volume_usd.parquet | 4,824 | 2010-08-28 00:00:00 | 2023-11-30 00:00:00 | day | period end |
| bcom_hash_rate.parquet | 5,445 | 2009-01-03 00:00:00 | 2023-11-30 00:00:00 | day | period end |
| bcom_median_confirmation_time.parquet | 5,445 | 2009-01-03 00:00:00 | 2023-11-30 00:00:00 | day | period end |
| bcom_mempool_count.parquet | 261,593 | 2016-06-14 14:45:00 | 2023-11-30 23:45:00 | minute | period end |
| bcom_mempool_growth.parquet | 261,572 | 2016-06-11 00:00:00 | 2023-11-30 23:45:00 | minute | period end |
| bcom_mempool_size.parquet | 261,593 | 2016-06-14 14:45:00 | 2023-11-30 23:45:00 | minute | period end |
| bcom_miners_revenue.parquet | 5,431 | 2009-01-17 00:00:00 | 2023-11-30 00:00:00 | day | period end |
| bcom_n_transactions.parquet | 5,431 | 2009-01-17 00:00:00 | 2023-11-30 00:00:00 | day | period end |
| bcom_n_unique_addresses.parquet | 5,420 | 2009-01-03 00:00:00 | 2023-11-30 00:00:00 | day | period end |
| bcom_output_volume.parquet | 5,445 | 2009-01-03 00:00:00 | 2023-11-30 00:00:00 | day | period end |
| bcom_trade_volume.parquet | 5,445 | 2009-01-03 00:00:00 | 2023-11-30 00:00:00 | day | period end |
| bcom_transaction_fees_usd.parquet | 5,431 | 2009-01-17 00:00:00 | 2023-11-30 00:00:00 | day | period end |
| cm_ADA.parquet | 2,260 | 2017-09-23 00:00:00 | 2023-11-30 00:00:00 | 1d | after day end (~00:00-02:00 UTC next day) |
| cm_BCH.parquet | 2,317 | 2017-07-28 00:00:00 | 2023-11-30 00:00:00 | 1d | after day end (~00:00-02:00 UTC next day) |
| cm_BNB.parquet | 2,340 | 2017-07-05 00:00:00 | 2023-11-30 00:00:00 | 1d | after day end (~00:00-02:00 UTC next day) |
| cm_BTC.parquet | 5,445 | 2009-01-03 00:00:00 | 2023-11-30 00:00:00 | 1d | after day end (~00:00-02:00 UTC next day) |
| cm_DOGE.parquet | 3,645 | 2013-12-08 00:00:00 | 2023-11-30 00:00:00 | 1d | after day end (~00:00-02:00 UTC next day) |
| cm_DOT.parquet | 1,556 | 2019-08-28 00:00:00 | 2023-11-30 00:00:00 | 1d | after day end (~00:00-02:00 UTC next day) |
| cm_ETH.parquet | 3,046 | 2015-07-30 00:00:00 | 2023-11-30 00:00:00 | 1d | after day end (~00:00-02:00 UTC next day) |
| cm_LTC.parquet | 4,438 | 2011-10-07 00:00:00 | 2023-11-30 00:00:00 | 1d | after day end (~00:00-02:00 UTC next day) |
| cm_SOL.parquet | 1,329 | 2020-04-11 00:00:00 | 2023-11-30 00:00:00 | 1d | after day end (~00:00-02:00 UTC next day) |
| cm_XRP.parquet | 3,986 | 2013-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d | after day end (~00:00-02:00 UTC next day) |
| mempool_difficulty_adj.parquet | 392 | 2009-01-03 18:15:05 | 2023-11-26 00:16:03 | every 2016 blocks (~2 weeks) | at stamp; date predictable ahead |
| mempool_feerates.parquet | 5,440 | 2009-01-03 18:15:05 | 2023-11-30 12:36:16 | ~daily groups of blocks | at stamp |
| mempool_hashrate.parquet | 5,445 | 2009-01-03 18:15:05 | 2023-11-30 00:00:00 | 1d | day end |

### defi (31 files, 39,309 rows)

| file | rows | first | last | freq | knowable |
|---|---:|---|---|---|---|
| dex_arbitrum.parquet | 822 | 2021-08-31 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| dex_base.parquet | 123 | 2023-07-31 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| dex_bsc.parquet | 1,168 | 2020-09-19 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| dex_ethereum.parquet | 1,855 | 2018-11-02 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| dex_solana.parquet | 787 | 2021-10-02 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| dex_total.parquet | 3,574 | 2014-02-17 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| fees_total.parquet | 2,076 | 2018-03-26 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| hacks.parquet | 622 | 2011-06-19 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| perpdex_oi_total.parquet | 1,009 | 2021-02-25 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| stable_DAI.parquet | 1,473 | 2019-11-19 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| stable_USDC.parquet | 1,907 | 2018-09-11 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| stable_USDT.parquet | 2,193 | 2017-11-29 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| stable_chain_Arbitrum.parquet | 889 | 2021-06-25 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| stable_chain_BSC.parquet | 1,138 | 2020-08-29 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| stable_chain_Base.parquet | 108 | 2023-08-15 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| stable_chain_Ethereum.parquet | 2,193 | 2017-11-29 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| stable_chain_Solana.parquet | 569 | 2021-09-10 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| stable_chain_Tron.parquet | 1,690 | 2019-04-16 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| stable_total.parquet | 2,193 | 2017-11-29 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| tvl_Arbitrum.parquet | 849 | 2021-06-04 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| tvl_BSC.parquet | 1,127 | 2020-10-30 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| tvl_Base.parquet | 699 | 2022-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| tvl_Bitcoin.parquet | 986 | 2021-03-20 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| tvl_Cardano.parquet | 698 | 2022-01-02 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| tvl_Dogechain.parquet | 472 | 2022-08-16 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| tvl_Ethereum.parquet | 2,256 | 2017-09-27 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| tvl_Litecoin.parquet | 562 | 2022-05-18 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| tvl_Polkadot.parquet | 689 | 2021-11-19 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| tvl_Solana.parquet | 989 | 2021-03-17 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| tvl_Tron.parquet | 1,337 | 2020-04-03 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |
| tvl_all.parquet | 2,256 | 2017-09-27 00:00:00 | 2023-11-30 00:00:00 | 1d | day end (but BACKFILLED: not PIT) |

### attention (16 files, 73,812 rows)

| file | rows | first | last | freq | knowable |
|---|---:|---|---|---|---|
| fear_greed.parquet | 2,126 | 2018-02-01 00:00:00 | 2023-11-30 00:00:00 | 1d | published ~00:00 UTC for that day |
| gdelt_timelinetone_bitcoin.parquet | 2,521 | 2017-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d (auto for long spans) | ~15 min after publication; daily value at day end |
| gdelt_timelinetone_crypto_regulation.parquet | 2,521 | 2017-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d (auto for long spans) | ~15 min after publication; daily value at day end |
| gdelt_timelinetone_cryptocurrency.parquet | 2,521 | 2017-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d (auto for long spans) | ~15 min after publication; daily value at day end |
| gdelt_timelinetone_stablecoin.parquet | 2,521 | 2017-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d (auto for long spans) | ~15 min after publication; daily value at day end |
| gdelt_timelinevolraw_bitcoin.parquet | 5,042 | 2017-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d (auto for long spans) | ~15 min after publication; daily value at day end |
| gdelt_timelinevolraw_crypto_regulation.parquet | 5,042 | 2017-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d (auto for long spans) | ~15 min after publication; daily value at day end |
| gdelt_timelinevolraw_cryptocurrency.parquet | 5,042 | 2017-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d (auto for long spans) | ~15 min after publication; daily value at day end |
| gdelt_timelinevolraw_ethereum.parquet | 5,042 | 2017-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d (auto for long spans) | ~15 min after publication; daily value at day end |
| gdelt_timelinevolraw_stablecoin.parquet | 5,042 | 2017-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d (auto for long spans) | ~15 min after publication; daily value at day end |
| hn_bitcoin.parquet | 700 | 2010-07-05 00:00:00 | 2023-11-27 00:00:00 | 7d | week end |
| hn_crypto.parquet | 569 | 2013-01-07 00:00:00 | 2023-11-27 00:00:00 | 7d | week end |
| hn_ethereum.parquet | 517 | 2014-01-06 00:00:00 | 2023-11-27 00:00:00 | 7d | week end |
| kp_geomagnetic.parquet | 33,572 | 1932-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d | nowcast within hours; definitive values revised ~monthly |
| sec_bitcoin.parquet | 569 | 2013-01-07 00:00:00 | 2023-11-27 00:00:00 | 7d | week end |
| sec_digital_asset.parquet | 465 | 2015-01-05 00:00:00 | 2023-11-27 00:00:00 | 7d | week end |

### macro (66 files, 391,929 rows)

| file | rows | first | last | freq | knowable |
|---|---:|---|---|---|---|
| bis_policy_CN.parquet | 9,963 | 1996-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d | announcement |
| bis_policy_GB.parquet | 23,133 | 1946-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d | announcement |
| bis_policy_JP.parquet | 16,473 | 1946-01-01 00:00:00 | 1991-02-06 00:00:00 | 1d | announcement |
| bis_policy_KR.parquet | 6,146 | 1999-05-06 00:00:00 | 2023-11-30 00:00:00 | 1d | announcement |
| bis_policy_US.parquet | 25,355 | 1954-07-01 00:00:00 | 2023-11-30 00:00:00 | 1d | announcement |
| bis_policy_XM.parquet | 9,100 | 1999-01-01 00:00:00 | 2023-11-30 00:00:00 | 1d | announcement |
| cftc_tff_BITCOIN.parquet | 295 | 2018-04-10 00:00:00 | 2023-11-28 00:00:00 | weekly | Friday 15:30 ET (3 days after stamp) |
| cftc_tff_BITCOIN_USD.parquet | 73 | 2017-12-19 00:00:00 | 2019-05-07 00:00:00 | weekly | Friday 15:30 ET (3 days after stamp) |
| cftc_tff_ETHER_CASH_SETTLED.parquet | 139 | 2021-04-06 00:00:00 | 2023-11-28 00:00:00 | weekly | Friday 15:30 ET (3 days after stamp) |
| cftc_tff_MICRO_BITCOIN.parquet | 135 | 2021-05-04 00:00:00 | 2023-11-28 00:00:00 | weekly | Friday 15:30 ET (3 days after stamp) |
| cftc_tff_MICRO_ETHER.parquet | 103 | 2021-12-14 00:00:00 | 2023-11-28 00:00:00 | weekly | Friday 15:30 ET (3 days after stamp) |
| cftc_tff_NANO_ETHER.parquet | 3 | 2023-11-14 00:00:00 | 2023-11-28 00:00:00 | weekly | Friday 15:30 ET (3 days after stamp) |
| cftc_tff_Nano_Bitcoin.parquet | 4 | 2023-11-07 00:00:00 | 2023-11-28 00:00:00 | weekly | Friday 15:30 ET (3 days after stamp) |
| ecb_dfr.parquet | 59 | 1999-01-01 00:00:00 | 2023-09-20 00:00:00 | business day | announcement date |
| fomc_dates.parquet | 102 | 2011-01-26 19:00:00 | 2023-11-01 18:00:00 | ~8/yr | dates published a year ahead |
| nyfed_effr.parquet | 2,241 | 2015-01-02 00:00:00 | 2023-11-30 00:00:00 | 1d | next business day ~08:00 ET |
| nyfed_rrp.parquet | 2,555 | 2013-04-02 00:00:00 | 2023-11-30 00:00:00 | 1d | ~13:15 ET same day |
| nyfed_sofr.parquet | 1,417 | 2018-04-02 00:00:00 | 2023-11-30 00:00:00 | 1d | next business day ~08:00 ET |
| nyfed_soma.parquet | 1,065 | 2003-07-09 00:00:00 | 2023-11-29 00:00:00 | weekly (Wednesday) | Thursday ~16:30 ET (H.4.1 timing) |
| tga.parquet | 13,818 | 2005-10-03 00:00:00 | 2023-11-30 00:00:00 | 1d | next business day ~16:00 ET |
| ust_auctions.parquet | 9,890 | 1979-10-31 00:00:00 | 2023-11-30 00:00:00 | event | auction day 13:00 ET |
| ust_real_yields.parquet | 5,234 | 2003-01-02 00:00:00 | 2023-11-30 00:00:00 | 1d (business days) | that date ~18:00 ET |
| ust_yields.parquet | 8,487 | 1990-01-02 00:00:00 | 2023-11-30 00:00:00 | 1d (business days) | that date ~18:00 ET |
| yahoo_ARKK.parquet | 2,286 | 2014-10-31 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_ARS_X.parquet | 5,278 | 2001-07-12 23:00:00 | 2023-11-30 00:00:00 | 1d | at that session's close |
| yahoo_BITO.parquet | 532 | 2021-10-20 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_BTC_F.parquet | 1,499 | 2017-12-18 05:00:00 | 2023-11-30 05:00:00 | 1d | at that session's close |
| yahoo_CLSK.parquet | 1,771 | 2016-11-16 14:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_CL_F.parquet | 5,843 | 2000-08-23 04:00:00 | 2023-11-30 05:00:00 | 1d | at that session's close |
| yahoo_CNY_X.parquet | 5,592 | 2001-06-24 23:00:00 | 2023-11-30 00:00:00 | 1d | at that session's close |
| yahoo_COIN.parquet | 664 | 2021-04-14 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_DX-Y_NYB.parquet | 13,443 | 1971-01-04 05:00:00 | 2023-11-30 05:00:00 | 1d | at that session's close |
| yahoo_ETH_F.parquet | 711 | 2021-02-05 05:00:00 | 2023-11-30 05:00:00 | 1d | at that session's close |
| yahoo_EURUSD_X.parquet | 5,190 | 2003-12-01 00:00:00 | 2023-11-30 00:00:00 | 1d | at that session's close |
| yahoo_FVX.parquet | 13,497 | 1970-01-02 13:20:00 | 2023-11-30 13:20:00 | 1d | at that session's close |
| yahoo_GBPUSD_X.parquet | 5,202 | 2003-12-01 00:00:00 | 2023-11-30 00:00:00 | 1d | at that session's close |
| yahoo_GBTC.parquet | 2,156 | 2015-05-11 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_GC_F.parquet | 5,835 | 2000-08-30 04:00:00 | 2023-11-30 05:00:00 | 1d | at that session's close |
| yahoo_GLD.parquet | 4,791 | 2004-11-18 14:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_GSPC.parquet | 13,599 | 1970-01-02 14:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_HG_F.parquet | 5,839 | 2000-08-30 04:00:00 | 2023-11-30 05:00:00 | 1d | at that session's close |
| yahoo_HOOD.parquet | 590 | 2021-07-29 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_HYG.parquet | 4,191 | 2007-04-11 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_IRX.parquet | 13,497 | 1970-01-02 13:20:00 | 2023-11-30 13:20:00 | 1d | at that session's close |
| yahoo_JPY_X.parquet | 7,024 | 1996-10-30 00:00:00 | 2023-11-30 00:00:00 | 1d | at that session's close |
| yahoo_KRW_X.parquet | 5,188 | 2003-12-01 00:00:00 | 2023-11-30 00:00:00 | 1d | at that session's close |
| yahoo_LQD.parquet | 5,373 | 2002-07-30 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_MARA.parquet | 2,913 | 2012-05-04 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_MOVE.parquet | 5,201 | 2002-11-12 14:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_MSTR.parquet | 6,411 | 1998-06-11 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_NDX.parquet | 9,620 | 1985-10-01 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_NGN_X.parquet | 5,203 | 2003-12-01 00:00:00 | 2023-11-30 00:00:00 | 1d | at that session's close |
| yahoo_NG_F.parquet | 5,840 | 2000-08-30 04:00:00 | 2023-11-30 05:00:00 | 1d | at that session's close |
| yahoo_NVDA.parquet | 6,256 | 1999-01-22 14:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_QQQ.parquet | 6,224 | 1999-03-10 14:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_RIOT.parquet | 1,932 | 2016-03-31 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_RUT.parquet | 9,129 | 1987-09-10 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_SI_F.parquet | 5,836 | 2000-08-30 04:00:00 | 2023-11-30 05:00:00 | 1d | at that session's close |
| yahoo_SMH.parquet | 5,911 | 2000-06-05 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_SPY.parquet | 7,766 | 1993-01-29 14:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_TLT.parquet | 5,373 | 2002-07-30 13:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |
| yahoo_TNX.parquet | 13,497 | 1970-01-02 13:20:00 | 2023-11-30 13:20:00 | 1d | at that session's close |
| yahoo_TRY_X.parquet | 4,919 | 2005-01-03 00:00:00 | 2023-11-30 00:00:00 | 1d | at that session's close |
| yahoo_TYX.parquet | 11,723 | 1977-02-15 13:20:00 | 2023-11-30 13:20:00 | 1d | at that session's close |
| yahoo_VIX.parquet | 8,545 | 1990-01-02 08:00:00 | 2023-11-30 08:00:00 | 1d | at that session's close |
| yahoo_VVIX.parquet | 4,249 | 2007-01-03 14:30:00 | 2023-11-30 14:30:00 | 1d | at that session's close |

## Point-in-time cautions

Copied from MANIFEST.csv `knowable` / `notes` where they mention backfilled, revised, NOT PIT or lag.

- `attention/kp_geomagnetic.parquet` — knowable: nowcast within hours; definitive values revised ~monthly
- `defi/dex_arbitrum.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/dex_base.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/dex_bsc.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/dex_ethereum.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/dex_solana.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/dex_total.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/fees_total.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/hacks.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/perpdex_oi_total.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/stable_DAI.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/stable_USDC.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/stable_USDT.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/stable_chain_Arbitrum.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/stable_chain_BSC.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/stable_chain_Base.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/stable_chain_Ethereum.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/stable_chain_Solana.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/stable_chain_Tron.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/stable_total.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/tvl_Arbitrum.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/tvl_BSC.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/tvl_Base.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/tvl_Bitcoin.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/tvl_Cardano.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/tvl_Dogechain.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/tvl_Ethereum.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/tvl_Litecoin.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/tvl_Polkadot.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/tvl_Solana.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/tvl_Tron.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `defi/tvl_all.parquet` — knowable: day end (but BACKFILLED: not PIT)
- `macro/cftc_tff_BITCOIN.parquet` — notes: Lag by >= 3 days before use.
- `macro/cftc_tff_BITCOIN_USD.parquet` — notes: Lag by >= 3 days before use.
- `macro/cftc_tff_ETHER_CASH_SETTLED.parquet` — notes: Lag by >= 3 days before use.
- `macro/cftc_tff_MICRO_BITCOIN.parquet` — notes: Lag by >= 3 days before use.
- `macro/cftc_tff_MICRO_ETHER.parquet` — notes: Lag by >= 3 days before use.
- `macro/cftc_tff_NANO_ETHER.parquet` — notes: Lag by >= 3 days before use.
- `macro/cftc_tff_Nano_Bitcoin.parquet` — notes: Lag by >= 3 days before use.
- `macro/yahoo_ARKK.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_ARS_X.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_BITO.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_BTC_F.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_CLSK.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_CL_F.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_CNY_X.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_COIN.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_DX-Y_NYB.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_ETH_F.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_EURUSD_X.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_FVX.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_GBPUSD_X.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_GBTC.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_GC_F.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_GLD.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_GSPC.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_HG_F.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_HOOD.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_HYG.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_IRX.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_JPY_X.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_KRW_X.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_LQD.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_MARA.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_MOVE.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_MSTR.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_NDX.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_NGN_X.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_NG_F.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_NVDA.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_QQQ.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_RIOT.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_RUT.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_SI_F.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_SMH.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_SPY.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_TLT.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_TNX.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_TRY_X.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_TYX.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_VIX.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `macro/yahoo_VVIX.parquet` — notes: Use close-to-close; lag by one session before joining to crypto.
- `onchain/cm_ADA.parquet` — notes: Exchange-flow metrics are label-based and revised backwards (NOT point-in-time).
- `onchain/cm_BCH.parquet` — notes: Exchange-flow metrics are label-based and revised backwards (NOT point-in-time).
- `onchain/cm_BNB.parquet` — notes: Exchange-flow metrics are label-based and revised backwards (NOT point-in-time).
- `onchain/cm_BTC.parquet` — notes: Exchange-flow metrics are label-based and revised backwards (NOT point-in-time).
- `onchain/cm_DOGE.parquet` — notes: Exchange-flow metrics are label-based and revised backwards (NOT point-in-time).
- `onchain/cm_DOT.parquet` — notes: Exchange-flow metrics are label-based and revised backwards (NOT point-in-time).
- `onchain/cm_ETH.parquet` — notes: Exchange-flow metrics are label-based and revised backwards (NOT point-in-time).
- `onchain/cm_LTC.parquet` — notes: Exchange-flow metrics are label-based and revised backwards (NOT point-in-time).
- `onchain/cm_SOL.parquet` — notes: Exchange-flow metrics are label-based and revised backwards (NOT point-in-time).
- `onchain/cm_XRP.parquet` — notes: Exchange-flow metrics are label-based and revised backwards (NOT point-in-time).

## What was verified at install

- All 224 parquet files listed in MANIFEST.csv are present; no extra parquet files.
- Each file's `time_col` (per MANIFEST.csv) exists and is a tz-aware UTC timestamp.
- max(time) <= 2023-11-30 23:59:59 UTC for every file.
- Row count equals MANIFEST.csv `rows` for every file; min/max time match MANIFEST.csv `first`/`last`.
- Schema note: in `macro/nyfed_rrp.parquet` the column `counterparties` has Arrow type `null` (no values).
