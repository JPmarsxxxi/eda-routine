# DATA_CARD — crypto_panel_validated_2026-10-05 (as used by this run)

Source: /home/user/eda-routine/data/crypto_panel_validated_2026-10-05/ (README.md, MANIFEST.csv, CUT.json read first).
Cut: every file ends <= 2023-11-30 23:59:59 UTC (CUT.json); re-asserted at every load by code/guard.py (ACCESS_LOG.md).

## Provenance sentence (data-hygiene.md checklist)
"These prices are **validated hourly prices** — Binance spot **last-trade prints** (checked against Binance bid/ask mid,
<= 2.5 bp) through 2021, and **FTMO CFD hourly mids** from 2022-01-01 for BTC ETH XRP LTC ADA DOGE DOT (BNB, BCH, SOL stay
Binance trades) — timestamped at the **bar OPEN (UTC)**, `price` = value at the bar END, **knowable at open + 1h**."

## PRIMARY TARGET — `primary/validated_<COIN>.parquet`, column `price`
| column | meaning | use in this run |
|---|---|---|
| t | UTC bar open | index |
| price | close (value at bar end) | the response; returns = log(price_t / price_{t-1h}) |
| source | binance_trade / ftmo_mid | slice provenance (EXPLORE, C1 all binance_trade; C2/C3 7 coins ftmo_mid) |
| new_source | True on first bar after a source switch or a gap | a return is NEVER taken across it (DECISIONS D5) |
| binance_quote_vol | raw Binance spot quote volume of the hour | descriptive only |
| ftmo_spread_bp | FTMO bar minimum spread, ftmo_mid rows | not used (TARGET: use the measured RT costs instead) |

Coverage (TRAIN): tables/00_coverage_primary_by_quarter.csv. ADA from 2020, DOGE/SOL from 2021, DOT from 2020-08-18,
BCH 2019-11-28 -> 2021-12-31.

## Explanatory families used, with the lag applied (decision time tau = 00:00 UTC of day d+1)
| family / file | MANIFEST knowable | value used for decision at tau |
|---|---|---|
| perp/perp_premium_<C> (Binance premium index klines, `close`) | open + 1h | mean of the 24 hourly closes of bars stamped d 00:00..23:00 |
| perp/funding_<C> (`last_funding_rate`) | at settlement | mean of settlements stamped in (d 00:00, tau) — the tau settlement itself excluded |
| spot/coinbase_<C> vs spot/binance_<C> `close` | open + 1h | daily mean of hourly log(coinbase/binance) over day d |
| spot/upbit_<C>KRW, macro/yahoo_KRW_X | open + 1h; session close, lag one session | log(upbit close d 23:00 / (binance close d 23:00 x USDKRW of session local_date <= d-1)) |
| onchain/cm_<C> `AdrActCnt` | after day end (~00-02 UTC next day) | day d-1 value (log 7d/28d mean) |
| deriv/deribit_funding_BTC `interest_8h` | at stamp | mean over stamps of day d |
| attention/fear_greed `value` | published ~00:00 UTC for that day | value stamped <= d |
| macro/yahoo_GSPC, yahoo_VIX `close` | session close; TARGET: lag one session | session local_date <= d-1 |
| attention/gdelt_timelinevolraw_bitcoin | day end + 15 min | day d-1 (log 3d/30d mean) |

Not used, and why: defi/* (BACKFILLED, not PIT); onchain cm_* exchange-flow columns (revised backwards); perp/metrics
(non-BTC only from 2021-12, outside EXPLORE; BTC positioning already tested — TARGET ALREADY TESTED); taker buy/sell
(flow imbalance already tested); bvol (VAL only); hyperliquid (2023 only); macro/nyfed_rrp `counterparties` (all null).

## Costs (TARGET.md, measured FTMO): RT bp for a 24h hold incl. one night — BTC 18.9, ETH 25.4, LTC 36.5,
ADA/DOGE/DOT/BNB/SOL ~46, BCH 65.5, XRP 68.6; +8.2 per extra night; -8.2 for intraday.
