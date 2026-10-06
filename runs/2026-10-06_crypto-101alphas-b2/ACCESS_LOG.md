# ACCESS_LOG — every data load, guard result (no row after VAL_END 2023-11-30 23:59:59 UTC)

The guard is an assertion inside `code/common.py::load` (TARGET.md NOTES: no eda_guard.py in this checkout). A failing
assertion would stop the cell and this run would write STOPPED.md. Every row below is one load that passed.

| when (UTC) | cell | file | rows | first t | last t | guard |
|---|---|---|---|---|---|---|
| 2026-10-06 10:23:22 | p0_00 | primary/validated_BTCUSD.parquet | 42,642 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:23:22 | p0_00 | primary/validated_ETHUSD.parquet | 42,646 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:23:22 | p0_00 | primary/validated_BNBUSD.parquet | 43,020 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:23:22 | p0_00 | primary/validated_SOLUSD.parquet | 25,522 | 2021-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:23:22 | p0_00 | primary/validated_XRPUSD.parquet | 42,642 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:23:22 | p0_00 | primary/validated_DOGEUSD.parquet | 25,145 | 2021-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:23:22 | p0_00 | primary/validated_ADAUSD.parquet | 33,909 | 2020-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:23:22 | p0_00 | primary/validated_LTCUSD.parquet | 42,643 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:23:22 | p0_00 | primary/validated_BCHUSD.parquet | 18,319 | 2019-11-28 10:00:00+00:00 | 2021-12-31 23:00:00+00:00 | PASS |
| 2026-10-06 10:23:22 | p0_00 | primary/validated_DOTUSD.parquet | 28,379 | 2020-08-18 23:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | spot/binance_BTCUSD.parquet | 54,996 | 2017-08-17 04:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | spot/binance_ETHUSD.parquet | 54,996 | 2017-08-17 04:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | spot/binance_BNBUSD.parquet | 53,059 | 2017-11-06 03:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | spot/binance_SOLUSD.parquet | 28,942 | 2020-08-11 06:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | spot/binance_XRPUSD.parquet | 48,792 | 2018-05-04 08:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | spot/binance_DOGEUSD.parquet | 38,584 | 2019-07-05 12:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | spot/binance_ADAUSD.parquet | 49,204 | 2018-04-17 04:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | spot/binance_LTCUSD.parquet | 52,171 | 2017-12-13 03:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | spot/binance_BCHUSD.parquet | 35,094 | 2019-11-28 10:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | spot/binance_DOTUSD.parquet | 28,757 | 2020-08-18 23:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | primary/validated_BTCUSD.parquet | 42,642 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | primary/validated_ETHUSD.parquet | 42,646 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | primary/validated_BNBUSD.parquet | 43,020 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:13 | p0_build | primary/validated_SOLUSD.parquet | 25,522 | 2021-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:14 | p0_build | primary/validated_XRPUSD.parquet | 42,642 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:14 | p0_build | primary/validated_DOGEUSD.parquet | 25,145 | 2021-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:14 | p0_build | primary/validated_ADAUSD.parquet | 33,909 | 2020-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:14 | p0_build | primary/validated_LTCUSD.parquet | 42,643 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:14 | p0_build | primary/validated_BCHUSD.parquet | 18,319 | 2019-11-28 10:00:00+00:00 | 2021-12-31 23:00:00+00:00 | PASS |
| 2026-10-06 10:24:14 | p0_build | primary/validated_DOTUSD.parquet | 28,379 | 2020-08-18 23:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:25:59 | p0_profile | spot/binance_BTCUSD.parquet | 54,996 | 2017-08-17 04:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:25:59 | p0_profile | spot/binance_ETHUSD.parquet | 54,996 | 2017-08-17 04:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:25:59 | p0_profile | spot/binance_BNBUSD.parquet | 53,059 | 2017-11-06 03:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:25:59 | p0_profile | spot/binance_XRPUSD.parquet | 48,792 | 2018-05-04 08:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:25:59 | p0_profile | spot/binance_ADAUSD.parquet | 49,204 | 2018-04-17 04:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:25:59 | p0_profile | spot/binance_LTCUSD.parquet | 52,171 | 2017-12-13 03:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:25:59 | p0_profile | spot/binance_BCHUSD.parquet | 35,094 | 2019-11-28 10:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | spot/binance_BTCUSD.parquet | 54,996 | 2017-08-17 04:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | spot/binance_ETHUSD.parquet | 54,996 | 2017-08-17 04:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | spot/binance_BNBUSD.parquet | 53,059 | 2017-11-06 03:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | spot/binance_XRPUSD.parquet | 48,792 | 2018-05-04 08:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | spot/binance_ADAUSD.parquet | 49,204 | 2018-04-17 04:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | spot/binance_LTCUSD.parquet | 52,171 | 2017-12-13 03:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | spot/binance_BCHUSD.parquet | 35,094 | 2019-11-28 10:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | primary/validated_BTCUSD.parquet | 42,642 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | primary/validated_ETHUSD.parquet | 42,646 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | primary/validated_BNBUSD.parquet | 43,020 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | primary/validated_XRPUSD.parquet | 42,642 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | primary/validated_ADAUSD.parquet | 33,909 | 2020-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | primary/validated_LTCUSD.parquet | 42,643 | 2019-01-01 00:00:00+00:00 | 2023-11-30 23:00:00+00:00 | PASS |
| 2026-10-06 10:26:00 | p0_profile | primary/validated_BCHUSD.parquet | 18,319 | 2019-11-28 10:00:00+00:00 | 2021-12-31 23:00:00+00:00 | PASS |
