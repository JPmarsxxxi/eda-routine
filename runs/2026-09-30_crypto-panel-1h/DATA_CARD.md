# DATA_CARD — crypto_panel_2026-09-30 (as used by this run)

Source: `/home/user/eda-routine/data/crypto_panel_2026-09-30/` (README.md, MANIFEST.csv, CUT.json read first). 224 parquet, 7
families, 5,685,039 rows, cut at 2023-11-30 23:59:59 UTC; re-verified per file by this run's guard (p0_00, 224/224 PASS).
Raw pulls: nothing dropped, gaps left missing, nothing filled (TARGET.md CLEANED?: NO). There is no CLEANING_LOG.md; the
"known facts" list in TARGET.md CLEANED? plays its role (they are not re-reported as findings).

## Provenance sentence (data-hygiene.md checklist item 1)
**These prices are last-trade prints (OHLC of trades, no bid/ask/mid) from Binance spot <COIN>USDT, 1-hour bars, timestamped
at the bar OPEN (UTC), knowable at open + 1h.** (MANIFEST `type`=trade print (last-trade OHLC), `stamp`=UTC bar open,
`knowable`=open + 1h.) USDT-quoted; the files call them <COIN>USD.

## PRIMARY TARGET: spot/binance_<COIN>.parquet, 10 coins
BTCUSD, ETHUSD, BNBUSD, SOLUSD, XRPUSD, DOGEUSD, ADAUSD, LTCUSD, BCHUSD, DOTUSD. Time column `t` (tz-aware UTC).

| column | what it is | knowable |
|---|---|---|
| open, high, low, close | first / max / min / last TRADE price in [t, t+1h) | t+1h (open alone is known at t, but only as a print) |
| vol, quote_vol | base / quote (USDT) volume traded in the bar | t+1h |
| n | number of trades in the bar | t+1h |
| buy_vol, buy_quote_vol | taker-BUY base / quote volume (MANIFEST note) | t+1h |
| sell_vol | vol - buy_vol (checked: max abs diff 1.8e-12 on BTC EXPLORE) | t+1h |
| ftmo_spread_rt_bp, ftmo_commission_rt_bp | FTMO CFD round-trip spread / commission in bp; ONE live sample 2026-09-02, constant in every row; NOT a history | cost constants only, never a feature |

Row = one 1-hour bar of trades. Because it is a trade print with no quotes, fine-scale returns carry bid-ask bounce (Roll 1984;
data-hygiene.md): any 1-2 bar reversal is guilty until the Roll-implied spread is sized (p0 item 3). The trading costs used here
are the FTMO CFD round trips from TARGET.md (BTC 6.6 ... LTC 36.5 bp) + ~8.2 bp per daily rollover crossed.

## Returns convention in this run
r_t = log(close_t / close_{t-1}) only when bar t-1 exists (one hour earlier); across a missing hour -> NaN (never bridged).
Forward return at horizon h from decision time T (= end of bar t, i.e. t+1h, when bar t is knowable):
fwd_h = log(close_{t+h} / close_t), NaN if any bar in (t, t+h] is missing. Computed only inside one slice (loader slices first).

## Other families (candidate explanatory series) - coverage, knowability, alignment only (TARGET NOTES)
From MANIFEST `knowable`; lag to the knowable time before ANY join (data-hygiene rule 4).

| family | files | freq | knowable -> lag rule before joining to a 1h bar decided at T |
|---|---|---|---|
| spot (other venues: bitstamp, coinbase, upbit KRW) | 17 | 1h | open + 1h (same as primary). bitstamp BTC 2011-13 stale (known). coinbase XRP delist gap 2021-01..2023-07 (known). |
| perp (Binance USD-M) | 42 | funding 8h (4h/1h later); metrics 5m; klines/premium 1h; bvol 1h (2023-06+ only, VAL-only coverage) | funding at settlement; metrics at create_time; klines open+1h. Funding / long-short / OI = positioning: topic EXCLUDED (DECISIONS D9). |
| deriv | 14 | 1h | dvol open+1h; deribit/hyperliquid funding at stamp. hyperliquid from 2023-05 = VAL-only coverage. |
| onchain | 28 | day / minute / ~2wk | bcom period end; cm_* after day end ~00:00-02:00 UTC next day AND exchange-flow metrics revised backwards (NOT PIT) -> unusable for prediction without a PIT source. |
| defi | 31 | 1d | day end but BACKFILLED (not PIT) -> descriptive only. |
| attention | 16 | 1d / 7d | fear_greed ~00:00 UTC same day; gdelt day end; hn/sec week end; kp revised monthly. |
| macro | 66 | 1d / weekly / event | yahoo_*: close-to-close only, lag one session (index opens can be synthetic); cftc_*: lag >= 3 days; nyfed_rrp.counterparties all-null (known). |

Coverage vs this run's slices (p0_00 table): only spot/perp-klines/perp-premium/funding/deriv dvol and the daily macro/attention
series cover EXPLORE; bvol and hyperliquid start inside VAL (unusable for EXPLORE/CONFIRM); perp `metrics_*` start 2020-09
(BTC) / 2021-12 (others) i.e. mostly CONFIRM-only.
