# DATA CARD - crypto_panel_validated_2026-10-05 (TRAIN <= 2023-03-19 only is read by search cells)

Identity checks done in Phase 0 (code/p0_02_profile.py, p0_03_inputs.py; MEMORY/DATA_FACTS.md consulted first - nothing re-derived that it already holds).

- **primary/validated_<COIN>USD** - "these prices are validated hourly closes: Binance spot last-trade close through 2021 (EXPLORE, C1) and, for
  7 coins from 2022-01-01, FTMO CFD hourly mid; stamped at the bar OPEN (UTC), value is the bar END, knowable at open + 1h."
  Checked: in EXPLORE and C1 the primary price equals the Binance spot close in 100% of rows (return corr 1.0000), so for those years the
  response IS the Binance print. In C2/C3 corr(primary 1h return, Binance close 1h return) = 0.992-0.997 and exact equality 0-9% of bars, so
  the response is a different, smoother series (a mid). Open-stamp check: primary return_t correlates 0.9986 with Binance close_t / close_{t-1} and
  -0.017 with the neighbouring bars, i.e. the stamp is the bar open and the price the bar end (open_t == close_{t-1} in only 35% of bars, so
  Binance bar opens are first trades, not previous closes; only closes are used for returns).
- **spot/binance_<COIN>USD** - "Binance spot hourly OHLC trade prints with base/quote volume, trade count n and taker-buy volume, open-stamped, knowable
  at open + 1h." Missing hours 13-59 per coin inside its span. buy_vol/vol averages 0.49-0.51 (taker-buy share of base volume).
- **perp/perp_klines, perp_premium** - "Binance USD-M hourly klines (perp trade prices) and premium-index klines (volume==0 on 57% of rows, so the premium
  index is an index, not a traded price), open-stamped, knowable at open + 1h." Perp-vs-spot return corr 0.999 same hour; no lead/lag (-0.02).
  Perp-minus-spot close basis (median bp): EXPLORE +6.2, C1 +2.8, C2 -5.5, C3 -5.0 (sign flips with the regime).
- **perp/funding_<COIN>USD** - "settled funding rate, stamped at settlement (00/08/16 UTC; SOL changes interval), knowable at the stamp." Joined as last
  settlement with stamp <= bar OPEN (one hour more conservative than the end-of-bar knowability). Starts 2020 (EXPLORE ~35-60% filled); 21-52% of
  settlements sit exactly on the 0.0001 floor (52% in C1).
- **perp/metrics_<COIN>USD** - "5-minute open-interest, long/short account ratio and taker ratio snapshots stamped at create_time, knowable at the stamp."
  Joined as the last snapshot whose stamp is <= bar open + 55 min. Coverage: BTC from 2020-09 (33% of EXPLORE hours), every other coin from 2021-12-01
  (18% of C1, 100% of C2/C3). 101 hours have OI == 0 (impossible): treated as missing.
- **spot/coinbase_<COIN>USD, spot/upbit_<COIN>KRW** - "other-venue hourly trade closes and volume, open-stamped, knowable at open + 1h." Coinbase vs Binance same-hour
  return corr 0.994-0.995 (BTC, ETH). Coinbase covers 9 coins (XRP absent after 2021 H1; SOL/DOGE/ADA/DOT only from 2021); Upbit KRW covers BTC ETH XRP ADA DOGE SOL.
- **Not used for features (TARGET.md)**: defi/*, onchain/cm_* (backfilled, revised), macro/*, attention/* are not touched in this run; bvol is VAL-only.

Target: forward log return of primary `price` from the END of bar t to the END of bar t+h, h in {1, 6, 24}; invalid if any bar in (t, t+h] has new_source=True
(code/panel.py fwd()). Features are stamped at the bar they are knowable at (end of bar t) and use only bars <= t.
