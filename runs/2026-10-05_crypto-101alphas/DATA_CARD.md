# DATA_CARD — crypto_panel_validated_2026-10-05 (read README.md, MANIFEST.csv, CUT.json first: done)

**Folder.** /home/user/eda-routine/data/crypto_panel_validated_2026-10-05/ — 234 parquet files, 6,029,906 rows, 8 family folders.
CUT.json: cutoff_inclusive_utc 2023-11-30T23:59:59+00:00; TRAIN_END 2023-03-19; VAL 2023-03-25..2023-11-30; TEST and later
NOT copied. MANIFEST.csv: every file's last row <= VAL_END (re-checked from the manifest here, and asserted again at every
load by the guard in code/run_lib.py, logged in ACCESS_LOG.md).

## What this run uses (only these two families; TARGET.md NOTES)

| role | files | provenance sentence (data-hygiene.md: type / venue / stamp / knowable) |
|---|---|---|
| RESPONSE | primary/validated_<COIN>.parquet, 10 coins | These prices are **validated hourly prices**: Binance spot **last-trade close** (years where it agreed with the Binance bid/ask mid within 2.5 bp) and, from 2022-01-01 for BTC ETH XRP LTC ADA DOGE DOT, the **FTMO CFD hourly mid** (bid + bar spread/2); timestamped at the **bar OPEN (UTC)**, `price` = value at the **bar END**, knowable at **open + 1h**. |
| SIGNAL inputs | spot/binance_<COIN>.parquet, 10 coins | These prices are **Binance spot trade prints** (last-trade OHLC of the USDT pair) with base volume `vol` and quote volume `quote_vol`; timestamped at the **UTC bar open**, knowable at **open + 1h**. |

Columns used. primary: `t, price, source, new_source` (`binance_quote_vol`, `ftmo_spread_bp` described only). binance:
`t, open, high, low, close, vol, quote_vol` (`n`, taker volumes described only; `ftmo_spread_rt_bp` NOT used: TARGET.md says it
is a single old live sample — costs come from TARGET.md's measured ROUND-TRIP COST line).

**The run's day (TARGET.md translation).** Day d = UTC calendar day; Binance daily bar = 24 hourly bars 00:00..23:00 (open of
00:00 bar, close of 23:00 bar = price at 24:00). vwap = sum(quote_vol)/sum(vol). Response for signal day d =
primary price at end of d+1 / at end of d - 1 (bars stamped d 23:00 and d+1 23:00), valid only if all 24 bars of d+1 exist
with no `new_source`. Delay-1 alphas (#101, #2, #6, #4) use day-d data and are entered at 24:00 of d. Delay-0 #42: "the close"
of day d IS 24:00 UTC = the open of d+1, so in 24/7 crypto delay-0-at-the-close and delay-1-at-the-open are the same instant;
same response window. Execution lag between knowing the 23:00 bar's close (24:00) and trading at 24:00 is zero here: an
idealisation stated, not hidden (a live version would trade minutes later).

**Primary coverage (rows / first / last).** BTC ETH LTC XRP BNB 2019-01-01..2023-11-30; ADA from 2020-01-01; DOT from
2020-08-18; SOL, DOGE from 2021-01-01; BCH 2019-11-28..2021-12-31. Holes (failed coin-years) are absent, not filled.
`new_source=True`: BTC 167 rows, ETH 164, DOGE 153 (mostly Saturday 15/16 and 22/23 UTC in FTMO years), BNB 21, SOL 8.

**Binance spot coverage.** BTC, ETH from 2017-08-17; BNB 2017-11; LTC 2017-12; ADA 2018-04; XRP 2018-05; DOGE 2019-07;
BCH 2019-11-28; SOL 2020-08-11; DOT 2020-08-18; all to 2023-11-30. Missing hours 20-128 per coin (TARGET.md known fact).

## Other families — coverage, knowability and alignment only (from MANIFEST.csv; not opened, not studied)

| family | files | rows | earliest first | median first | latest last | knowable (distinct) |
|---|---:|---:|---|---|---|---|
| attention | 16 | 73,812 | 1932-01-01 | 2017-01-01 | 2023-11-30 | nowcast within hours; definitive values revised ~monthly; published ~00:00 UTC for that day; week end; ~15 min after publication; daily value at day end |
| defi | 31 | 39,309 | 2011-06-19 | 2020-10-30 | 2023-11-30 | day end (but BACKFILLED: not PIT) |
| deriv | 14 | 163,883 | 2019-05-01 | 2023-05-12 | 2023-11-30 | at stamp; open + 1h |
| macro | 66 | 391,929 | 1946-01-01 | 2002-09-21 | 2023-11-30 | Friday 15:30 ET (3 days after stamp); Thursday ~16:30 ET (H.4.1 timing); announcement; announcement date; at that session's close; auction day 13:00 ET; dates p |
| onchain | 28 | 891,021 | 2009-01-03 | 2009-01-17 | 2023-11-30 | after day end (~00:00-02:00 UTC next day); at stamp; at stamp; date predictable ahead; day end; period end |
| perp | 42 | 2,929,136 | 2020-01-01 | 2020-04-25 | 2023-11-30 | at settlement; the predicted rate is visible live before it; create_time (a few seconds after); hour end; open + 1h |
| primary | 10 | 344,867 | 2019-01-01 | 2019-06-15 | 2023-11-30 | open + 1h (price = value at bar END) |
| spot | 27 | 1,195,949 | 2011-08-18 | 2018-04-17 | 2023-11-30 | open + 1h |

Alignment/knowability facts that matter if any of these is used as a RIVAL (none is opened in this run unless a rule file
says so): perp funding knowable at settlement (8h); perp metrics 5m knowable at create_time, BTC from 2020-09, others from
2021-12; onchain cm_* daily knowable ~00:00-02:00 UTC next day and exchange-flow metrics NOT point-in-time; defi/* BACKFILLED
(not PIT, unusable as signals); macro/cftc_* knowable 3 days after stamp; macro/yahoo_* lag one session, opens can be synthetic;
macro/nyfed_rrp `counterparties` all-null. These are TARGET.md known facts, not findings.

## Costs (TARGET.md ROUND-TRIP COST, measured FTMO CFD, 24h hold incl. one rollover night 8.2 bp)

BTC 18.9, ETH 25.4, LTC 36.5, ADA/DOGE/DOT/BNB/SOL ~45-47, BCH 65.5, XRP 68.6 bp round trip. Used for the economic size
condition (DECISIONS D7) and the cost line in REPORT.md.
