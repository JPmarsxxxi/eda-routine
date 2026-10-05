# LEDGER — one row per completed run (RUNBOOK_v3.md "MEMORY"). Append-only; budget 250 lines.

K = scored slice openings of the run (test + val cells; v1 = sweep tests). K_cum = running total for the same `dataset`.
`dataset` names the underlying series, not the folder: the three BTC runs all test Binance BTCUSDT spot 2017-2023
(see DATA_FACTS), so they share one K_cum. methods_score is n/a for runs before v3.2.

| date | run | target | mode | stop | cells | K | dataset | K_cum | methods_score |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-25 | 2026-09-25_btc-spot-1m-clean | btc-spot-1m-clean | v1-sweep | sweep-end | 50 | 50 | BTCUSDT-spot-2017-2023 | 50 | n/a |
| 2026-09-25 | 2026-09-25_btc-spot-1m-clean_v2 | btc-spot-1m-clean | v2-SSRN | refuted-stop | 4 | 4 | BTCUSDT-spot-2017-2023 | 54 | n/a |
| 2026-09-28 | 2026-09-28_btc-perp-various-free | btc-perp-various-free | E | S2 (v3.0) | 10 | 7 | BTCUSDT-spot-2017-2023 | 61 | n/a |
| 2026-09-30 | 2026-09-30_crypto-panel-1h | crypto-panel-1h | E | S2 (v3.0) | 9 | 7 | crypto_panel_2026-09-30 | 7 | n/a |
