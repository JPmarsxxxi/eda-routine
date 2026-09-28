# DATA CARD: btc-spot-1m-clean (run 2026-09-25_btc-spot-1m-clean_v2)

Checks: `scripts/cell_00_datacard.py` -> `tables/00_datacard_checks.json`. Cleaning facts are from the data folder's
CLEANING_LOG.md and are NOT re-reported here as findings.

**One-sentence provenance (data-hygiene):** these prices are **trade prints aggregated to 1-minute OHLCV bars**
(first/max/min/last trade price in the minute) from **Binance BTCUSDT SPOT**, timestamped in **UTC at the bar's OPEN**,
knowable at **open + 60 s**, so a bar stamped T is used from bar T+1 onward.

| item | value |
|---|---|
| file | `C:\Users\User\eda-routine\data\btcusdt_spot_1m_clean\btcusdt_spot_1m_clean.parquet` (one file, one feed, one venue) |
| rows | 3,274,945 (TRAIN 2,906,457; embargo 2023-03-20..24: 7,048, not used; VAL 361,440) |
| range | 2017-08-17 04:00 to 2023-11-30 23:59 UTC. Max stamp <= VAL_END: **yes** (no TEST row present) |
| index | `t`, datetime64[ns, UTC], sorted, unique, whole minutes |
| timezone | UTC, tz-aware (verified) |
| open/close stamp | **OPEN time.** Re-checked: all 2,154 complete days run 00:00..23:59 (a close-stamp would run 00:01..00:00); 74/76 months start 01 00:00 and 75/76 end 23:59; the exceptions are 2017-08 (partial first month, starts 17 04:00, last minute 23:58 missing) and 2017-09 (00:00 missing, starts 00:01): missing minutes in the thin 2017 market, not a stamping shift. Not confirmed against exchange docs; the NEXT-bar rule below is safe under either stamping. |
| open vs previous close | open == previous close on only 34.8% of consecutive TRAIN bars; p99 gap 22 bp. Expected for trade bars (open = first trade of the minute, not a carry of the last). Returns here use close-to-close. |

| column | what it IS |
|---|---|
| open, high, low, close | trade prices (last-trade based), USDT. NOT bid, ask or mid. `low` NaN on 11 bars (source had 0). |
| vol | base volume (BTC) traded in the minute |
| quote | quote volume (USDT); NaN on 1,550 bars |
| n | number of trades |
| buy_vol / sell_vol | volume split by aggressor side (buy_vol + sell_vol == vol on every row); labelled taker-buy / taker-sell by inference from the Binance kline format, not verified |
| n_buy / n_sell | trade counts by aggressor side |
| gap_min | minutes since previous bar; `gap_min == 1` keeps true 1-minute returns |
| flag_* | cleaning flags (low_invalid 11, quote_bad 1,550, repeat_prev_bar 37, close_outlier 3, wick_gt3pct 47); never altered |

Rules applied in every cell:
- No quotes exist, so no mid can be formed. Returns are **close-to-close log returns of trade prices**; this carries
  bid-ask bounce (Roll 1984) at fine scales. The data-hygiene "mid" rule cannot be met; it is recorded as a limitation,
  and fine-scale (1-minute) reversal-type readings are treated as bounce-suspect.
- Returns, never levels. One feed. No fills: missing minutes stay missing; multi-minute gaps are excluded or handled
  by building returns from last available close at fixed clock stamps (stated per cell).
- Nothing at time T uses a bar stamped T or later for a prediction made at T.
- ROUND-TRIP COST: UNKNOWN (TARGET.md). Economics row is UNTESTED.
- Splits (from TARGET.md): TRAIN_END 2023-03-19, VAL_START 2023-03-25, VAL_END 2023-11-30.
