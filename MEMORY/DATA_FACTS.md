# DATA_FACTS — what each dataset IS (identity, stamping, coverage, twins). Never results. Budget 150 lines.

- btcusdt_perp_bundle: `btcusdt_perp_1m`, `btc_perp_30m`, `btcusdt_perp_hourly` are Binance SPOT, not perp (start 2017, 1m TRAIN rows = spot file's 2,906,457; 0.02% exact match with perp closes). (2026-09-28_btc-perp-various-free)
- btcusdt_perp_bundle: only `btcusdt_metrics_5m` o/h/l/c is perp; its 5m klines are open-stamped (best match to spot 1m at +4 min). (2026-09-28_btc-perp-various-free)
- btcusdt_perp_bundle: perp-minus-spot gap tracks funding (8h corr 0.79); funding pinned at 0.0100% on ~47% of 2020-21 settlements, capped at +/-0.30%. (2026-09-28_btc-perp-various-free)
- btcusdt_perp_bundle: CONFIRM-era 2022-01..2023-03 had only 9 of 1,328 settlements with funding above 0.01%. (2026-09-28_btc-perp-various-free)
- btc_hist_halfspread_hourly: venue and construction undocumented; hourly ACF 0.995, 0.66 corr with trailing RV (a smoothed estimate); coverage 35-79% by year, 32% in 2022-23. (2026-09-28_btc-perp-various-free)
- btcusdt_metrics_5m: OI == 0 on one hour (impossible value); ls_all and ls_top_cnt changes 0.84 correlated; OI value = OI x price. (2026-09-28_btc-perp-various-free)
- btc_dvol_hourly: starts 2021-04-01; no gaps. (2026-09-28_btc-perp-various-free)
- BTCUSDT spot 1m (all bundles): bars OPEN-stamped (complete days run 00:00-23:59); from 2023-04 trades/min fall ~8x and zero-return bars rise to 4-12% (VAL regime differs from TRAIN). (2026-09-25_btc-spot-1m-clean)
