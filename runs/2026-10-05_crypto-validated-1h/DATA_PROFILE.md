# DATA_PROFILE — Phase 0, EXPLORE slice only (2019-01-01 -> 2021-07-01)

Cell: `code/p0_profile.py` (one script, seven sections; the rules below were written into this file's skeleton before the
script was first run). Every load through `code/guard.py` (ACCESS_LOG.md). Primary target only, except section 4's
explanatory screen, which profiles the other families only through a lagged, knowable daily feature each (TARGET NOTES).
Facts already listed in TARGET.md CLEANED? are not re-reported as findings.

## 1. Distributions (returns, not levels)
**Question:** what do hourly and daily log returns of `price` look like per coin; is there zero-mass?
**Rule:** fat-tailed if excess kurtosis > 3; skew notable if |skew| > 0.5; zero-mass notable if > 1% of hourly returns
are exactly 0 (stale-print check). Hill index on the top 1% of |r|: < 4 means the 4th moment is unstable.
**Plot:** plots/00_distributions.png. **Table:** tables/00_1_distributions.csv.
**Result:** every coin is fat-tailed at 1h (excess kurtosis 7.5 SOL to 53.5 BTC) and at 1d (3.0 SOL to 30.9 DOGE).
Hourly sd 84 bp (BTC) to 321 bp (DOGE). Skew is negative for the majors (BTC -1.1, ETH -1.3, LTC -1.4, BCH -1.8) and
positive for DOGE (+1.9, 2021 squeeze) and SOL. Zero-mass: only LTC exceeds 1% (1.17% of hourly returns exactly 0); all
others < 0.6%. Hill index 2.8-4.0: tails too heavy for a stable 4th moment -> rank (Spearman) statistics are used below.

## 2. Missingness and gaps
**Question:** where/when are primary hours missing in EXPLORE; anything beyond TARGET's known facts?
**Rule:** an anomaly if a coin-year misses > 0.5% of its hours, or missing hours are coin-specific (not exchange-wide).
**Plot:** plots/00_missingness.png. **Tables:** tables/00_2_missing.csv, tables/00_2_family_coverage_explore.csv.
**Result:** no anomaly. Missing hours are identical across coins (28 in 2019, 18 in 2020, 7 in 2021H1 = Binance-wide
outages, a known fact); max 0.32% per coin-year. new_source flags = gaps (no source switch in EXPLORE). Explanatory
coverage inside EXPLORE: perp premium/funding from 2020-01 (DOGE 2020-07, DOT 2020-08, SOL 2020-09); coinbase for BTC,
ETH, LTC, BCH, XRP (partial), ADA from 2021-03; DOGE/DOT/SOL coinbase only from 2021-06 (~2 weeks); BNB none.

## 3. Autocorrelation
**Question:** are returns, |returns| and volume autocorrelated at lags 1-24h (returns), 1/24/168h (|r|, log volume), 1-5d (daily)?
**Rule:** significant if |ACF| > 2/sqrt(n) (1h: ~0.014 for the long coins; 1d: ~0.067). Hourly ACF(1) economically
notable if |ACF(1)| > 0.05.
**Plot:** plots/00_acf.png. **Table:** tables/00_3_acf.csv.
**Result:** hourly ACF(1) is negative for every coin (-0.015 ETH to -0.063 ADA), significant for 9 of 10, above the
0.05 notability bar only for ADA. ACF(24) is negative and significant for all (-0.028 XRP to -0.116 DOGE). |r| ACF is large and slow
(0.25-0.44 at 1h, 0.03-0.13 at 168h) with a 24h cycle; log volume ACF 0.86-0.96 at 1h, 0.58-0.84 at 168h. Daily ACF(1)
of returns is negative for every coin (-0.01 DOGE to -0.16 BCH; significant for 6 of 10).
(Daily and same-hour reversal are ALREADY TESTED topics: recorded, not chased.)

## 4. Cross-column relationships
**Question:** how do coin returns co-move; is any column secretly a twin of another (floor Q3); which knowable
explanatory series relate to FORWARD primary returns?
**Rules:** impostor pair if daily-return corr > 0.95, or if two series are identical on > 99% of rows. Explanatory
screen: a feature is flagged if |t| > 2 for its IC vs the forward 24h or 72h primary return, TS (panel-average) or XS
(per-day cross-coin Spearman); K looks counted and the chance-expected number of flags (0.046 K) stated beside it.
**Plots:** plots/00_corr.png, plots/00_explanatory_screen.png. **Tables:** tables/00_4_corr_daily.csv,
tables/00_4_twin_primary_vs_binance_spot.csv, tables/00_4_explanatory_screen.csv, tables/00_4_impostor_premium.csv.
**Result:** mean pairwise daily corr 0.55, max BCH-LTC 0.87: no pair > 0.95. **Twin:** in EXPLORE, primary `price` and
`binance_quote_vol` are IDENTICAL to spot/binance_<C> `close` / `quote_vol` on 100% of rows (median gap 0.0 bp) -> the
raw Binance spot file is not an independent explanatory series for EXPLORE/C1 prices; only its other columns are.
**Screen (K = 29 looks, ~1.3 flags expected by chance; 5 flagged):** XS perp premium 72h IC -0.112 (t -3.75; top-third
minus bottom-third coins -170 bp per 72h); XS perp premium 24h IC -0.045 (t -2.61; -24 bp); XS funding 72h IC -0.076
(t -2.43; -128 bp); TS fear&greed 24h IC +0.092 (t +2.75; top-minus-bottom tercile days +84 bp); TS S&P500 prior-session
return 24h IC +0.088 (t +2.18; +37 bp). Nothing else crosses |t| 2 (coinbase premium, kimchi premium, active-address
growth, Deribit funding, VIX change, GDELT attention all |t| < 1.8).
**Impostor check on the strongest flag (XS premium, 72h, every 3rd day, n=154):** premium vs funding cross-sectional
rank corr +0.70 (t 29: funding is largely a smoothed premium -> twin pair, count them as ONE lead); premium vs past-3d
return rank corr -0.01 (not a reversal proxy); past-3d return's own XS IC +0.02 (t 0.5); premium IC after removing the
past-3d-return rank -0.111 (t -3.85): unchanged.

## 5. Regime structure
**Question:** how do vol, co-movement and autocorrelation change across half-years of EXPLORE?
**Rule:** a break is flagged where a statistic moves by > 50% (relative) between adjacent half-years.
**Plot:** plots/00_regimes.png. **Table:** tables/00_5_regimes.csv.
**Result:** median daily vol 4.4% (2019H1) -> 3.8% -> 6.2% (2020H1, COVID crash) -> 4.7% -> 9.1% (2021H1): breaks at
2020H1 and 2021H1. Mean pairwise corr 0.63 -> 0.79 -> 0.91 (2020H1) -> 0.56 -> 0.54: break 2020H1->H2 (-39%, just under
50%) and the alt-season fall. BTC hourly ACF(1) -0.08/-0.06 in 2020 vs ~0 in 2019 and 2021H1 (break). Panel daily ACF(1)
negative in every half-year (-0.05 to -0.23).

## 6. Intraday / weekly shape (descriptive only)
**Question:** how do |r| and volume vary by UTC hour and weekday?
**Rule:** a shape is "material" if max/min across hours (or weekdays) > 1.5.
**Plot:** plots/00_intraday_weekly.png. **Tables:** tables/00_6_intraday.csv, tables/00_6_weekly.csv.
**Result:** material intraday shape: mean |r1| max/min 1.52 (peak 00 UTC 99 bp and 16 UTC 94 bp; trough 19 UTC 65 bp);
volume share max/min 1.87 (peak 16 UTC 5.9%, trough 21 UTC 3.1%). Weekly not material by the rule (1.18): Sat/Sun |r1|
69/73 bp vs 79-81 bp weekdays; weekend median volume ~19% lower.

## 7. What a row physically is
**Question:** is the EXPLORE primary price a trade print, a quote or a mid; how much bounce does it carry?
**Rule (data-hygiene rule 5):** Roll half-spread c = sqrt(-cov(dp_t, dp_t-1)) on hourly returns; if c is far above the
venue's real half-spread (< 1 bp on Binance majors), the negative lag-1 covariance is not bid/ask bounce.
**Plot:** plots/00_roll.png. **Table:** tables/00_7_roll.csv.
**Result:** provenance sentence in DATA_CARD.md. EXPLORE rows are all `binance_trade` last-trade prints. Roll implied
half-spread 13-48 bp (BTC 13.9, ETH 12.8, DOGE 48.3) against a real Binance half-spread of well under 1 bp on the majors:
the hourly negative lag-1 covariance is price reversal, not bounce. C2/C3 FTMO rows are mids (no bounce by
construction), so any hourly effect must be checked across that switch.
