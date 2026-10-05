# DATA CARD: btc-perp-various-free (run 2026-09-28_btc-perp-various-free)

Checks: `scripts/cell_00_datacard.py` -> `tables/00_datacard_checks.json`, `tables/00_metrics_c_vs_1m_offsets.csv`,
`plots/00_identity_gap.png`. Structure checks (row counts, first/last stamp, duplicates, step) read every row of each prepared
copy; nothing distributional was computed on embargo or VAL rows. All identity checks are TRAIN rows only.

## HEADLINE: three of the seven "perp" files are SPOT

The manifest and TARGET.md label `btcusdt_perp_1m`, `btc_perp_30m` and `btcusdt_perp_hourly` as Binance USD-M perpetual. **The
evidence says they are Binance BTCUSDT SPOT trade bars:**

1. They start 2017-08-17 04:00 UTC (1m, 30m), which is the Binance **spot** BTCUSDT listing. The Binance USD-M BTCUSDT
   perpetual did not exist until September 2019. Nothing can be a perp bar in 2017-2019.
2. The 1m file has **2,906,457 TRAIN rows, exactly** the TRAIN row count the earlier `btcusdt_spot_1m_clean` run's DATA_CARD
   reports for Binance spot (that card read, not the spot data; the spot data was not opened in this run).
3. `btcusdt_metrics_5m` comes from the Binance USD-M futures endpoint and embeds 5m OHLCV. Its close `c` equals the 1m
   file's close on only **0.02%** of 267,050 stamps at the best alignment (offset +4 min, i.e. metrics klines are
   open-stamped 5m bars). The gap `c - 1m close` has a median |gap| of 4.6 bp and its 8h mean correlates **+0.79 with the
   funding rate** (gap by year: 2021 mean +4.5 bp while funding was strongly positive; 2022 mean -4.3 bp). That is the
   perp-spot basis. Two copies of one series would match exactly.
4. The hourly close equals the 30m close of the second half-hour on 100% of stamps, and both equal the 1m close at
   T+59m / T+29m on 99.997% / 99.999% of stamps. So hourly = 30m = 1m = one spot series at three resolutions.

**Decision (DECISIONS.md D2):** proceed and label correctly rather than stop. The price files are SPOT. The only perp price
in the bundle is `btcusdt_metrics_5m` o/h/l/c (2020-09 onward). Funding, open interest and the ratios are perp quantities.
The perp-minus-spot gap (`basis_bp`, built from metrics `c` and the 1m spot close at the matching minute) is a real
derived series. It is NOT a quote artefact because both legs are trade prints.

## One-sentence provenance per file (data-hygiene rule: type / venue / stamp / knowable)

| file | what a row IS | stamp | knowable at |
|---|---|---|---|
| `btcusdt_perp_1m` (SPOT) | trade-print OHLCV bar, Binance spot BTCUSDT, 1 min; `buy_vol`/`sell_vol` = taker split (inferred) | bar OPEN (all 1,899 complete days run 00:00..23:59) | T + 1 min |
| `btc_perp_30m` (SPOT) | last trade price of the 30 min bar + quote volume | bar OPEN (close = 1m close at T+29m) | T + 30 min |
| `btcusdt_perp_hourly` (SPOT) | last trade price of the hour + quote volume | bar OPEN (close = 1m close at T+59m) | T + 60 min |
| `btcusdt_metrics_5m` (PERP) | OI / OI value / 3 long-short ratios / taker vol ratio snapshot + perp 5m OHLCV | `create_time`; klines open-stamped (best match +4 min) | conservatively T + 5 min for every field (endpoint stamping of the ratio fields is not documented in the bundle; assume the later time) |
| `btcusdt_funding_8h` (PERP) | funding rate applied at the settlement | settlement time 00/08/16 UTC (ms jitter 0-5 ms, rounded to the hour; 0 duplicates after rounding) | at the stamp (the rate is published before settlement; using it from the stamp on is conservative) |
| `btc_dvol_hourly` | Deribit DVOL index (30-day implied vol, annualised %), hourly OHLC | open-stamped hourly (assumed, index close = last value in hour) | T + 60 min |
| `btc_hist_halfspread_hourly` | measured half-spread in bp, hourly; venue is not stated in the bundle (starts 2017-08-20, so it cannot be perp-only) | hour stamp | used only as a COST input, same hour as the event, never as a signal until Phase 0 says what it is |

## Structure (every row of the prepared copy)

| file | rows | first | last | TRAIN | embargo | VAL | dup stamps | modal step | steps > modal |
|---|---|---|---|---|---|---|---|---|---|
| 1m (spot) | 2,906,457 | 2017-08-17 04:00 | 2023-03-19 23:59 | 2,906,457 | 0 | **0** | 0 | 1 min | 11,478 |
| 30m (spot) | 109,973 | 2017-08-17 04:00 | 2023-11-30 23:30 | 97,687 | 238 | 12,048 | 0 | 30 min | 29 |
| hourly (spot) | 43,020 | 2019-01-01 00:00 | 2023-11-30 23:00 | 36,877 | 119 | 6,024 | 0 | 1 h | 19 |
| DVOL | 23,376 | 2021-04-01 00:00 | 2023-11-30 23:00 | 17,232 | 120 | 6,024 | 0 | 1 h | 0 |
| half-spread | 24,302 | 2017-08-20 15:00 | 2023-11-30 23:00 | 21,583 | 69 | 2,650 | 0 | 1 h | 583 |
| funding | 4,290 | 2020-01-01 00:00 | 2023-11-30 16:00 | 3,522 | 15 | 753 | 0 | 8 h | 0 after hour-rounding |
| metrics | 341,064 | 2020-09-01 00:00 | 2023-11-30 23:55 | 267,339 | 1,440 | 72,285 | 0 | 5 min | 152 |

Every file's max stamp <= VAL_END (2023-11-30): **yes**. No TEST row present. Symbol column (where present) is BTCUSDT only.
Exact duplicate rows: 0 in every file. Same-stamp-different-values: 0 (no duplicate stamps).

Notes that matter downstream:
- **half-spread VAL has 2,650 rows for ~6,000 VAL hours** (44% coverage) and 583 TRAIN gaps. Cost at the trade hour will
  often be missing. Phase 0 item 2 measures this. Missing cost is left missing (rule 9), never filled forward silently.
- Funding in TRAIN is clipped at exactly +/-0.0030 (max and min), the exchange cap. Phase 0 item 1 counts cap hits.
- Only the metrics file carries PERP prices; its klines are open-stamped 5m bars (+4 min alignment).
