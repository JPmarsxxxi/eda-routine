# LEDGER — one row per completed run (RUNBOOK_v3.md "MEMORY"). Append-only; budget 250 lines.

K_train = specs evaluated on TRAIN (search `variants:` + confirm runs); K_val = VAL checks. K_cum_* = running totals for the
same `dataset`. `dataset` names the underlying series, not the folder: the three BTC runs all test Binance BTCUSDT spot
2017-2023 (see DATA_FACTS), so they share one K_cum. methods_score is n/a for runs before v3.2.
`job` is - for runs before v3.4 (one engine, no jobs). Rows before v3.3 (2026-10-13) had one K; it is split here from each run's ATTEMPTS.md (test cells -> K_train, VAL openings ->
K_val). Those runs counted one per test cell, not per variant, so their K_train is a floor.

| date | run | job | target | mode | stop | cells | K_train | K_val | dataset | K_cum_train | K_cum_val | methods_score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-25 | 2026-09-25_btc-spot-1m-clean | - | btc-spot-1m-clean | v1-sweep | sweep-end | 50 | 50 | 3 | BTCUSDT-spot-2017-2023 | 50 | 3 | n/a |
| 2026-09-25 | 2026-09-25_btc-spot-1m-clean_v2 | - | btc-spot-1m-clean | v2-SSRN | refuted-stop | 4 | 4 | 0 | BTCUSDT-spot-2017-2023 | 54 | 3 | n/a |
| 2026-09-28 | 2026-09-28_btc-perp-various-free | - | btc-perp-various-free | E | S2 (v3.0) | 10 | 6 | 1 | BTCUSDT-spot-2017-2023 | 60 | 4 | n/a |
| 2026-09-30 | 2026-09-30_crypto-panel-1h | - | crypto-panel-1h | E | S2 (v3.0) | 9 | 6 | 1 | crypto_panel_2026-09-30 | 6 | 1 | n/a |
| 2026-10-05 | 2026-10-05_crypto-validated-1h | - | crypto-validated-1h | E | S4 (v3.1) | 14 | 77 | 0 | crypto_panel_validated_2026-10-05 | 77 | 0 | n/a |
| 2026-10-05 | 2026-10-05_crypto-101alphas | - | crypto-101alphas | B | S2 (v3.1) | 28 | 27 | 1 | crypto_panel_validated_2026-10-05 | 104 | 1 | n/a |
| 2026-10-06 | 2026-10-06_crypto-101alphas-b2 | - | crypto-101alphas-b2 | B | S4 (v3.2-cloud) | 20 | 20 | 0 | crypto_panel_validated_2026-10-05 | 124 | 1 | n/a |
| 2026-10-13 | 2026-10-13_crypto-features-1 | features | crypto-features-1 | E | S2 (v3.4) | 50 | 1291 | 5 | crypto_panel_validated_2026-10-05 | 1415 | 6 | 1 |
