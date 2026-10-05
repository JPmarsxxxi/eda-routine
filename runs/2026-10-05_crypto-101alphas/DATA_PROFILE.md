# DATA_PROFILE — Phase 0, EXPLORE slice only (2019-01-01 .. 2020-05-28 excl.)

Scope (TARGET.md NOTES): the PRIMARY TARGET panel (10 coins, 1h; 7 coins exist in EXPLORE: BTC ETH BNB LTC XRP, ADA from
2020-01, BCH from 2019-11-28) plus the Binance spot signal inputs. Other families: coverage/knowability only (DATA_CARD.md).
Per DECISIONS D11, nothing here conditions a forward return on any of the five alphas or on a cross-sectional sort.
Questions and rules below were written BEFORE code/p0_profile.py was run; results follow each, from that script.

## Pre-committed questions and rules (written first)

- **1. Distributions.** Q: are hourly and daily log returns of `price` fat-tailed, and is there zero-mass? Rule: fat-tailed if
  excess kurtosis > 3; zero-mass suspicious if > 2% of hourly returns are exactly 0. Volume (Binance `vol`, log) described.
- **2. Missingness and gaps.** Q: beyond the known holes, how much is missing? Rule: a coin is flagged if > 1% of its expected
  hours inside its own EXPLORE coverage are missing, or > 5% of its days are not valid response days.
- **3. Autocorrelation.** Q: are hourly returns, |returns| and log volume autocorrelated at lags 1, 2, 3, 6, 12, 24 h? Rule:
  significant if |ACF| > 2/sqrt(n). (Hourly TIME-SERIES lags only, D11.)
- **4. Cross-column relationships / impostors.** Q: how correlated are coins' hourly returns; is primary `price` a twin of the
  Binance close (impostor check), and is #101's (close-open) a twin of the close-to-close return? Rule: impostor/twin if
  corr > 0.98. Also: Binance daily open vs previous close gap rate (data-hygiene zero-gap check, inverted for 24/7: a 24/7
  market should show open == previous close almost always) — "24/7-continuous" if > 95% of days have |gap| < 5 bp. And
  price-level ordering: how often does the cross-sectional rank of `low` change from one day to the next? Rule: "rank(low)
  is near-static" if < 10% of coin-days change rank.
- **5. Regime structure.** Q: do 1-4 change across the three EXPLORE half-years (2019H1, 2019H2, 2020H1)? Rule: structural
  break if median-coin hourly vol differs by > 2x between half-years, or mean pairwise correlation moves by > 0.2.
- **6. Intraday / weekly shape.** Q: how are volume and |return| distributed over UTC hour and weekday? Descriptive only, no
  claim; noted: max/min hour ratio.
- **7. What a row physically is.** Q: is primary `price` at stamp t the value at the END of bar t (= Binance close of bar t),
  not its open? Rule: confirmed if median |log(price_t / binance_close_t)| < 1 bp and median |log(price_t / binance_open_t)|
  > 5x that.

## Results
### 1. Distributions

| coin | n_h | sd_h_bp | skew_h | exkurt_h | zero_% | p1_bp | p99_bp | n_d | sd_d_bp | exkurt_d | sd_logvol_h |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 12265 | 82.5 | -1.76 | 88.7 | 0.02 | -233.9 | 224.7 | 503 | 432.0 | 37.3 | 0.75 |
| ETH | 12265 | 96.2 | -2.02 | 60.5 | 0.49 | -267.6 | 268.5 | 503 | 524.0 | 33.0 | 0.83 |
| BNB | 12265 | 102.4 | -2.08 | 52.5 | 0.06 | -273.0 | 262.5 | 503 | 522.0 | 31.1 | 0.74 |
| LTC | 12265 | 106.2 | -0.88 | 33.8 | 1.29 | -297.2 | 297.2 | 503 | 540.0 | 15.3 | 0.89 |
| XRP | 12265 | 89.3 | -1.37 | 36.5 | 0.39 | -249.7 | 251.8 | 503 | 440.0 | 19.5 | 0.87 |
| BCH | 4344 | 127.5 | -2.39 | 61.3 | 0.37 | -344.0 | 325.9 | 177 | 725.0 | 29.7 | 1.0 |
| ADA | 3538 | 124.2 | -1.6 | 34.2 | 1.16 | -354.4 | 316.4 | 143 | 692.0 | 24.0 | 0.9 |

Verdict: excess kurtosis of hourly returns 33.8..88.7 (> 3 for every coin -> FAT-TAILED); daily 15.3..37.3; zero-mass 0.02..1.29% (none suspicious).
Plot: plots/00_distributions.png

### 2. Missingness and gaps

| coin | first | exp_hours | missing_h | missing_% | new_source | days | invalid_resp_day_% | binance_missing_h |
|---|---|---|---|---|---|---|---|---|
| BTC | 2019-01-01 | 12312 | 37 | 0.3 | 10 | 513 | 1.9 | 37 |
| ETH | 2019-01-01 | 12312 | 37 | 0.3 | 10 | 513 | 1.9 | 37 |
| BNB | 2019-01-01 | 12312 | 37 | 0.3 | 10 | 513 | 1.9 | 37 |
| LTC | 2019-01-01 | 12312 | 37 | 0.3 | 10 | 513 | 1.9 | 37 |
| XRP | 2019-01-01 | 12312 | 37 | 0.3 | 10 | 513 | 1.9 | 37 |
| BCH | 2019-11-28 | 4358 | 9 | 0.21 | 5 | 182 | 2.7 | 9 |
| ADA | 2020-01-01 | 3552 | 9 | 0.25 | 5 | 148 | 3.4 | 37 |

Verdict: flagged coins (> 1% hours missing or > 5% invalid response days): none. Invalid response days include the first day of each coin's coverage and days after a new_source/gap row.
Plot: plots/00_missingness.png

### 3. Autocorrelation (hourly time-series lags only)

| coin | n | 2/sqrt(n) | r_l1 | r_l2 | r_l3 | r_l6 | r_l12 | r_l24 | |r|_l1 | |r|_l24 | logvol_l1 | logvol_l24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 12265 | 0.018 | -0.037 | -0.02 | 0.003 | -0.022 | 0.021 | -0.051 | 0.283 | 0.139 | 0.744 | 0.487 |
| ETH | 12265 | 0.018 | -0.042 | -0.016 | 0.016 | -0.003 | 0.018 | -0.055 | 0.252 | 0.127 | 0.745 | 0.498 |
| BNB | 12265 | 0.018 | -0.056 | 0.007 | 0.012 | -0.042 | 0.021 | -0.039 | 0.254 | 0.115 | 0.745 | 0.499 |
| LTC | 12265 | 0.018 | -0.039 | -0.018 | 0.012 | -0.01 | 0.024 | -0.051 | 0.248 | 0.128 | 0.687 | 0.441 |
| XRP | 12265 | 0.018 | -0.063 | -0.003 | 0.009 | -0.018 | 0.028 | -0.043 | 0.264 | 0.13 | 0.77 | 0.513 |
| BCH | 4344 | 0.03 | -0.045 | -0.017 | 0.009 | -0.03 | 0.045 | -0.059 | 0.26 | 0.118 | 0.752 | 0.536 |
| ADA | 3538 | 0.034 | -0.052 | 0.021 | 0.02 | -0.041 | 0.064 | -0.045 | 0.32 | 0.106 | 0.728 | 0.481 |

Verdict: coins with |ACF| of signed hourly returns > 2/sqrt(n), by lag: {1: 7, 2: 1, 3: 0, 6: 3, 12: 6, 24: 7}. |r| and log volume are strongly persistent (|r| lag1 0.248..0.32, log-volume lag1 0.687..0.77): volatility and activity cluster.
Plot: plots/00_acf.png

### 4. Cross-column relationships and impostors

Pairwise correlation of hourly returns (EXPLORE):

| index | BTC | ETH | BNB | LTC | XRP | BCH | ADA |
|---|---|---|---|---|---|---|---|
| BTC | 1.0 | 0.83 | 0.67 | 0.76 | 0.71 | 0.81 | 0.82 |
| ETH | 0.83 | 1.0 | 0.68 | 0.83 | 0.78 | 0.84 | 0.86 |
| BNB | 0.67 | 0.68 | 1.0 | 0.64 | 0.61 | 0.79 | 0.82 |
| LTC | 0.76 | 0.83 | 0.64 | 1.0 | 0.74 | 0.86 | 0.85 |
| XRP | 0.71 | 0.78 | 0.61 | 0.74 | 1.0 | 0.8 | 0.85 |
| BCH | 0.81 | 0.84 | 0.79 | 0.86 | 0.8 | 1.0 | 0.79 |
| ADA | 0.82 | 0.86 | 0.82 | 0.85 | 0.85 | 0.79 | 1.0 |

Mean pairwise hourly-return correlation 0.78 (min 0.61, max 0.86): one common factor dominates.
| coin | corr(primary r, binance close r) 1h | days |open-prevclose|<5bp % | median gap bp | corr(log c/o, log c/prev c) daily |
|---|---|---|---|---|
| BTC | 1.0 | 96.1 | 0.42 | 1.0 |
| ETH | 1.0 | 95.7 | 0.78 | 1.0 |
| BNB | 1.0 | 71.0 | 1.68 | 0.9999 |
| LTC | 1.0 | 84.0 | 1.98 | 1.0 |
| XRP | 1.0 | 90.8 | 1.23 | 1.0 |
| BCH | 1.0 | 85.7 | 1.54 | 1.0 |
| ADA | 1.0 | 67.8 | 2.76 | 0.9999 |

Cross-sectional rank of daily `low` changes on 0.0% of coin-days (rule: near-static if < 10%). Order of the median rank: {'BTC': 6.0, 'BCH': 6.0, 'ETH': 5.0, 'LTC': 4.0, 'BNB': 3.0, 'XRP': 2.0, 'ADA': 1.0}.
Verdict: primary price vs Binance close is a twin in EXPLORE (corr >= 1.0000) — expected, primary IS the Binance trade close in validated years (an impostor pair by construction; the response and the signal share a source until 2022). Binance daily open == previous close (24/7 continuous) on 67.8..96.1% of days; (close-open) is a twin of the close-to-close return (corr 1.000..1.000). rank(low) is NEAR-STATIC.
Plot: plots/00_crosscorr.png

### 5. Regime structure (EXPLORE half-years)

| era | coins | median sd_h bp | median exkurt_h | mean pair corr | median ACF1 |
|---|---|---|---|---|---|
| 2019H1 | 5 | 89.4 | 21.4 | 0.59 | -0.017 |
| 2019H2 | 6 | 76.4 | 23.1 | 0.71 | -0.018 |
| 2020H1 | 7 | 123.6 | 54.5 | 0.84 | -0.069 |

Verdict: vol ratio max/min 1.62 (no break by the 2x rule); correlation range 0.25 (BREAK). 2020H1 contains the March-2020 crash.
Plot: plots/00_regimes.png

### 6. Intraday / weekly shape (descriptive)

By UTC hour (median across coins):

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rel_quote_vol | 0.86 | 0.66 | 0.65 | 0.63 | 0.63 | 0.64 | 0.67 | 0.68 | 0.75 | 0.74 | 0.8 | 0.79 | 0.9 | 0.9 | 0.9 | 0.95 | 1.13 | 0.81 | 0.66 | 0.63 | 0.64 | 0.54 | 0.58 | 0.66 |
| mean_|r|_bp | 78.9 | 67.8 | 57.3 | 56.5 | 58.0 | 54.7 | 57.1 | 55.3 | 62.8 | 64.6 | 71.7 | 60.4 | 71.7 | 67.3 | 67.1 | 69.5 | 78.7 | 58.0 | 54.2 | 51.1 | 58.5 | 57.1 | 57.7 | 67.6 |

By weekday (0=Mon):

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| rel_quote_vol | 0.79 | 0.77 | 0.78 | 0.82 | 0.77 | 0.61 | 0.63 |
| mean_|r|_bp | 67.8 | 61.5 | 66.5 | 69.0 | 69.4 | 52.9 | 58.4 |

Descriptive: relative volume max/min hour ratio 2.08 (peak 16h, trough 21h UTC); |r| ratio 1.54; weekend volume 0.62 vs weekday 0.79.
Plot: plots/00_intraday.png

### 7. What a row physically is

| coin | n | med |price - binance close_t| bp | med |price - binance open_t| bp | med |price - binance open_t+1| bp |
|---|---|---|---|---|
| BTC | 12275 | 0.0 | 25.16 | 0.31 |
| ETH | 12275 | 0.0 | 34.58 | 0.73 |
| BNB | 12275 | 0.0 | 42.61 | 1.44 |
| LTC | 12275 | 0.0 | 41.45 | 1.79 |
| XRP | 12275 | 0.0 | 32.59 | 0.92 |
| BCH | 4349 | 0.0 | 44.87 | 1.35 |
| ADA | 3543 | 0.0 | 51.79 | 2.66 |

Verdict: CONFIRMED — primary `price` stamped t equals the Binance close of bar t (the value at t+1h), i.e. OPEN-stamped, value at bar END, knowable at t+1h. One row = one hour's closing trade print (Binance years) or closing FTMO mid (2022+, 7 coins). Hence the daily response uses the bar stamped 23:00 as 'end of day'.
Plot: plots/00_row_meaning.png


Section 7 also draws on DATA_CARD.md (provenance sentences; FTMO mid rows from 2022 are not in EXPLORE, so the 2022+ response
is a MID while the Binance signal inputs stay trade prints: from C3 on, signal and response come from different venues).
