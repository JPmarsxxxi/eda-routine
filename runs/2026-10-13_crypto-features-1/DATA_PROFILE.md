# DATA_PROFILE - Phase 0 (TRAIN only; code: code/p0_02_profile.py, p0_03_inputs.py, p0_04_noise.py; raw outputs: work/p0_0*_out.txt)

Panel: 10 coins, hourly, primary prices 2019-01-01..2023-03-19 (guard TRAIN bound). No CLEANING_LOG.md is supplied for the panel itself; the
README documents the primary/ cleaning, so no re-cleaning is done and its facts (holes, new_source) are not reported as findings.

## 1. Distributions
Question: are 1h returns fat-tailed enough that raw-return features would be tail-driven? Rule: yes if excess kurtosis > 10 for a majority of coins.
Table (1h log return, TRAIN; sd in bp): BTC sd 77.8 / skew -0.85 / exkurt 46.3; ETH 97.3 / -1.03 / 27.2; BNB 104.6 / -0.96 / 31.6; SOL 159.4 / +0.19 / 13.9;
XRP 117.9 / -0.39 / 38.1; DOGE 185.9 / +2.42 / 87.9; ADA 123.9 / -0.49 / 19.2; LTC 112.1 / -0.99 / 38.6; BCH 123.8 / -1.80 / 45.0; DOT 138.6 / -1.15 / 40.8.
Zero-return mass 0.03% (BTC) to 1.2% (LTC). Result: 10 of 10 coins above 10 -> YES. Plot: plots/00_distributions.png. Consequence: rank/winsorised features.

## 2. Missingness and gaps
Question: how much of each coin's own span is missing and where? Rule: report counts; flag any coin with > 1% missing hours.
Primary missing hours inside the span: BTC 290, ETH 286, BNB 59, SOL 13, XRP 287, DOGE 242, ADA 262, LTC 288, BCH 31, DOT 249 (<= 1.3% each: none flagged);
longest gap 25 h (FTMO fixed Saturday hours; BTC C3 Saturday hours 10-15 and 21-22 UTC are 24-51% missing), BNB 10, SOL 4, BCH 5. Binance spot missing 13-59 hours.
Input-family coverage (non-null % of hourly rows by slice): funding EXPLORE 32-60%, C1-C3 100%; perp klines 32-60% EXPLORE then ~100%; premium index same;
OI / long-short: BTC 33% EXPLORE, 100% C1; every other coin 0% EXPLORE, 18% C1, 100% C2-C3 (hourly snapshot join, see DATA_CARD). Coinbase close covers 9 coins (XRP only 76% of EXPLORE,
0 after); Upbit covers 6 coins. 101 hours have OI == 0 (invalid). See tables in work/p0_03_out.txt.

## 3. Autocorrelation
Question: do 1h returns, |returns| and log volume show serial dependence? Rule: |ACF| > 2/sqrt(n) = 0.0105 counts.
1h return ACF lag 1: BTC -0.017, ETH -0.007, BNB -0.027, SOL -0.020, XRP -0.039, DOGE -0.021, ADA -0.050, LTC -0.044, BCH -0.028, DOT -0.037 (9 of 10 beyond the bound, all negative);
lag 2 -0.012..-0.050 (negative), lags 3 and 6 ~0. |return| ACF lag1 0.26-0.45, lag24 0.15-0.28, lag168 0.09-0.13. Log quote volume ACF lag1 0.88-0.97, lag24 0.78-0.94, lag168 0.70-0.90.
Per fold the lag-1 ACF of BTC/ETH/DOGE: EXPLORE -0.028/-0.015/-0.022; C1 +0.023/+0.005/-0.017; C2 -0.008/-0.012/-0.070; C3 +0.012/+0.038/+0.021.
Result: small short-horizon reversal, unstable by fold; strong vol clustering; volume persistent.

## 4. Cross-column relationships
Question: are any columns twins, and how correlated are the coins? Rule: flag pair corr > 0.9 as an impostor.
Pairwise 1h return correlations 0.39 (DOGE-XRP) to 0.84 (BTC-ETH); none > 0.9. Impostor pairs between series: primary vs Binance close return corr 1.0000 with exact price equality in
EXPLORE and C1 (the response IS the Binance print there); C2 0.9917/0.995/0.9936 (BTC/ETH/DOGE), C3 0.995/0.9946/0.9971 with equality 0-9% -> a different (mid) series after 2022-01-01.
Perp kline vs spot close return corr 0.999 (no lead/lag); Coinbase vs Binance 0.994-0.995. corr(|ret|, log quote vol) pooled 0.258. Taker-buy share of volume 0.49-0.51.
Result: the panel is one dominant market factor plus a thin cross-section; the response switch is real.

## 5. Regime structure
Question: do the properties above change across EXPLORE / C1 / C2 / C3? Rule: report; a change > 30% in a level counts as a structural break.
EW-market 1h vol (bp): 98 / 89 / 100 / 71; mean pairwise corr 0.57 / 0.68 / 0.79 / 0.67; cross-sectional dispersion of 1h returns (bp) 56 / 53 / 45 / 40;
BTC median trades per hour 24.0k / 50.7k / 41.1k / 221.0k; BTC median quote volume per hour $19.9M / $79.2M / $60.9M / $176.5M; perp-spot basis +6.2 / +2.8 / -5.5 / -5.0 bp;
funding on the 0.0001 floor 21% / 52% / 31% / 30%. Result: structural breaks in trade counts (C3, 5x), dispersion (-28% across the sample), correlation (C2 peak) and the response series (2022-01-01).
Plot: plots/00_regime.png.

## 6. Intraday / weekly shape (descriptive only)
Mean |1h return| by UTC hour (bp, pooled): 00h 86.3; 01h 73.5; 02-07h 59-64; 08-11h 64-69; 12-16h 75-82; 17-19h 61-64; 20-23h 66-71. Weekday (Mon..Sun) 71.9, 70.7, 73.4, 71.2, 70.6, 59.7, 61.6.
Quote-volume index (vs trailing 30d mean) by hour: 0.83 (21h) to 1.50 (16h). Plot: plots/00_intraday.png. Result: a stable clock in vol and volume; not yet a claim.

## 7. What a row physically is
Primary: validated hourly close stamped at the bar OPEN (UTC), the value is the bar END, knowable at open + 1h; Binance last-trade close to 2021, FTMO CFD hourly mid from 2022 for
BTC ETH XRP LTC ADA DOGE DOT (BNB, BCH, SOL stay Binance). Stamp check: primary return_t vs Binance close_t/close_{t-1} corr 0.9986; vs neighbours -0.016/-0.018 -> open-stamped, end value confirmed.
Binance spot: trade prints (bar open is the first trade in the bar; open_t == close_{t-1} in 35% of bars). Perp: trade klines (Binance USD-M) + premium-index klines (57% zero volume = an index).
Funding: settled at 00/08/16 UTC, 21-52% on the 0.0001 floor. Metrics: 5-minute snapshots. All raw loads logged in ACCESS_LOG.md; TRAIN bound enforced by eda_guard.

## 8. Noise floor for power simulations (measured, not assumed)
Day-permutation null on EXPLORE (80 permutations of whole UTC days of a 6h-return feature against actual forward returns; code/p0_04_noise.py, work/noise.json):
se(mean IC) = c/sqrt(N): hourly sampling c = 0.44 (1h), 0.74 (6h), 0.96 (24h); daily sampling c = 0.50 / 0.46 / 0.56. Sd of the NW t under the null 0.92-1.11 (calibrated);
mean t +0.36..+0.69 for hourly sampling (a small positive bias from hour-of-day structure shared by feature and return; the pass rules use a size floor of 0.02 beyond the t test).
Consequence: one hourly-sampled 24h-horizon fold (~5,000 hours) has se ~0.014 and a daily-sampled fold ~0.04.
