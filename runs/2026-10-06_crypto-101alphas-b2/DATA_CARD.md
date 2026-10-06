# DATA_CARD — crypto_panel_validated_2026-10-05, as used by this run

**Provenance line (data-hygiene rule):** the RESPONSE prices are validated hourly prices — Binance spot last-trade closes
(checked against Binance's own bid/ask mid) up to 2021-12-31 for all coins and through 2023 for BNB/BCH/SOL, and the FTMO CFD
hourly MID from 2022-01-01 for BTC ETH XRP LTC ADA DOGE DOT — stamped at the bar OPEN (UTC), `price` = value at the bar END,
knowable at open + 1h. The SIGNAL inputs are Binance spot hourly trade-print OHLCV bars (no bid/ask), OPEN-stamped (confirmed,
DATA_PROFILE §7), knowable at open + 1h, aggregated to UTC days (DECISIONS D4).

| item | value |
|---|---|
| files used | primary/validated_<COIN>.parquet (response); spot/binance_<COIN>.parquet (signal inputs, Phase 0 clock/row checks) |
| coins | BTC ETH BNB SOL XRP DOGE ADA LTC BCH DOT (USD) |
| rows (primary) | 344,867 hourly rows, 2019-01-01 .. 2023-11-30 23:00 (per-coin table in the bundle README) |
| rows (binance spot, 10 coins) | 444,595 hourly rows, 2017-08-17 .. 2023-11-30 23:00 |
| timezone | UTC throughout |
| response | r(d) = ln(price end of d+1 / price end of d), primary only (D3) |
| signal day | UTC day d, bars 00:00..23:00 (D4); knowable at 24:00 of d = start of the response window |
| type | primary: trade print (validated vs mid) then FTMO mid; binance: trade print OHLCV |
| venue | Binance spot; FTMO CFD (mid) |
| knowable | open + 1h for every hourly bar |
| guard | every load asserts no row after VAL_END (ACCESS_LOG.md) |
| cost (TARGET.md) | FTMO round trip for a 24h hold incl. one rollover night: BTC 18.9, ETH 25.4, LTC 36.5, ADA/DOGE/DOT/BNB/SOL ~45-47, BCH 65.5, XRP 68.6 bp; median coin ~45 bp |

Known and not re-discovered (TARGET.md CLEANED?): absent coin-years (ADA 2019, DOGE 2019-20, SOL 2020, BCH after 2021);
the ~0.4-3 bp Binance -> FTMO level offset at 2022-01-01 (flagged by `new_source`, no return taken across it); FTMO's fixed
Saturday gaps; Binance missing hours. One correction to TARGET.md is NOT claimed here: the zero-gap rate (0.16-0.33 on EXPLORE)
is lower than the "0.3-0.6" TARGET.md quotes, as the first v3 run already noted.

Mid rule (data-hygiene rule 1): the signal is computed on Binance trade prints, not a mid — this is the paper's own input
(OHLCV) and there are no Binance quotes in the bundle. Bounce risk is small at a daily horizon (Roll); the response is on the
validated series. From 2022 the response is a mid and the signal a trade print: their difference is not a signal (§7).
