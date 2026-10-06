# DATA_PROFILE — Phase 0 on EXPLORE (2019-01-01 .. 2020-06-02), primary panel

Each section's question and decision rule was written here BEFORE `code/p0_profile.py` ran (14c rule 1 applies to
data-nature claims). Results are appended under each rule afterwards ("Result:"). EXPLORE only; no forward return is related
to any alpha in this phase (that is a test, and the tests are Phase 2 cells).

## 1. Distributions

Question: what do daily primary log returns, the signal inputs, and the five alphas look like on EXPLORE?
Rule: returns are **fat-tailed** if excess kurtosis > 3 for at least half the coins (-> rank statistics, not Pearson, decide
every test — already the D7 statistic); **zero-mass problem** if > 1% of valid daily returns are exactly 0. An alpha has a
**division problem** if > 1% of its coin-days are NaN from D9's guard; it has a **degenerate cross-section** if on > 20% of days
it takes fewer than 3 distinct values across the coins present.

**Result (`tables/p0_01_returns.csv`, `tables/p0_01_alphas.csv`, `plots/00_distributions.png`).** All 7 coins live on EXPLORE are
fat-tailed: excess kurtosis 15-37 (median 29), skew -1.0 to -3.1 (the 2020-03 crash). Zero mass: max 0.2% of daily returns
(LTC) -> no zero-mass problem. Alphas: #54 has no undefined values; #53's division guard removes 1.3% of live coin-days ->
**division problem flagged (just over 1%)**, and #53 is extremely heavy-tailed (excess kurtosis ~1,745: the ratio explodes when
close sits just above the low) — only ranks of it are usable, which is what every test uses. #30 (15%) and #35 (26%) NaN shares
are warm-up (20- and 32-day windows) and coins entering EXPLORE, not division. No alpha has a degenerate cross-section (#35:
2.6% of days with < 3 distinct values, under the 20% bar). #54 is always <= 0 by construction ((low-close)/(low-high) is in
[0, 1]), which is harmless for a rank.

## 2. Missingness and gaps

Question: where are valid response days and valid daily bars missing on EXPLORE?
Rule: a coin-month is **thin** if < 80% of its days have a valid response; a day is **short** if < 5 coins have a valid
response (it drops out of every statistic, D5). Known cleaning facts (absent coin-years, FTMO Saturday gaps) are not findings.

**Result (`tables/p0_02_valid_by_month.csv`, `plots/00_missingness.png`).** 1.7% of EXPLORE days are short (< 5 coins) and drop
out. Median 5 coins per day on EXPLORE (BTC ETH BNB XRP LTC from 2019-01; BCH from 2019-11; ADA from 2020-01): EXPLORE is a
THIN cross-section, so its ICs will be noisy (power cells use EXPLORE's own day count and coin count). 1 thin coin-month (a coin's
first partial month). Nothing beyond the known absent coin-years.

## 3. Autocorrelation

Question: do daily returns, |returns| and log volume carry memory at lags 1-5?
Rule: pooled per-coin ACF at lag k is **significant** if |ACF| > 2 / sqrt(n). Return autocorrelation matters because #30 and
#38 are built from recent price moves (a reversal or continuation at lag 1 would make them its proxy — see §4 impostors).

**Result (`tables/p0_03_acf.csv`, `plots/00_acf.png`).** Band 2/sqrt(n) = 0.038. Daily returns: lag-1 ACF **-0.142**
(significant reversal), lag 2 +0.067, lag 3 -0.065, lag 4 +0.109 — all significant, alternating. |returns|: +0.150 at lag 1,
+0.166 at lag 4 (volatility clusters). Detrended log volume: +0.60 at lag 1 decaying to +0.14 at lag 5 (volume shocks persist).
The lag-1 reversal is pooled own-coin (it includes the common market move); the tests here are cross-sectional, which removes
the market part — the two can differ.

## 4. Cross-column relationships and impostors

Question: how do the coins co-move, and is any alpha a twin of another alpha or of a simple baseline?
Rule: daily-return correlation matrix reported. An alpha pair, or an alpha and a baseline, is an **impostor pair** if their
mean daily cross-sectional Spearman correlation has |rho| > 0.7 (weaker 0.4-0.7 is "related", reported). Baselines (all known
at the end of day d): b_rev1 = -r(d) (1-day reversal), b_mom20 = 20-day return, b_vol20 = 20-day realised vol, b_volu = log
volume vs its 20-day mean. These are ALSO the `corr_baselines` set for SIGNALS.md. Twin check: Binance daily close-to-close
return vs primary return on the same day, correlation > 0.99 = same print (expected on EXPLORE, where primary IS Binance).

**Result (`tables/p0_04_return_corr.csv`, `tables/p0_04_signal_xs_corr.csv`, `plots/00_crosscorr.png`).** Coins co-move
strongly: mean pairwise daily-return correlation **0.86**. Twin check: Binance close-to-close vs primary return correlation
**1.000** on EXPLORE (same print, as expected: primary IS Binance before 2022). Impostors, by the |rho| > 0.7 rule:
**#38 vs b_rev1 (1-day reversal) rho = 0.863 -> IMPOSTOR PAIR.** #38's ranking is mostly yesterday's cross-sectional reversal.
Related (0.4-0.7): #35 vs #38 0.45, #35 vs b_rev1 0.43, #53 vs #54 0.50 (both read where the close sits in the range). #30 is
related to nothing above 0.25. No alpha is a twin of 20-day momentum or 20-day volatility (|rho| <= 0.28).

## 5. Regime structure

Question: how do volatility, cross-sectional dispersion and average pairwise correlation change across EXPLORE's quarters?
Rule: a **regime shift** is a quarter whose median daily |return| or dispersion differs from the EXPLORE median by > 2x, or a
quarter whose mean pairwise correlation differs by > 0.2.

**Result (`tables/p0_05_regimes.csv`, `plots/00_regimes.png`).** Quarterly median |daily return| 124-265 bp, dispersion
107-226 bp: no quarter is > 2x or < 0.5x the EXPLORE median. Mean pairwise correlation 0.59 (2019Q2) to 0.93 (2020Q1): **2019Q2
is a regime shift by the correlation rule** (0.59 vs median 0.80 — the 2019 spring rally was alt-led), and 2020Q1 (the crash)
is the high-correlation extreme. Cross-sectional signals have least to work with when correlation is high.

## 6. Intraday / weekly shape

Question: when in the UTC day and week do volume and |hourly return| concentrate? (The daily bar boundary is 00:00 UTC.)
Rule: an **hour effect** if the max hour's share of volume (or mean |hourly return|) exceeds the median hour's by > 1.5x; a
**weekday effect** if the max weekday's mean |daily return| exceeds the median weekday's by > 1.3x. Descriptive facts only.

**Result (`tables/p0_06_hour.csv`, `tables/p0_06_weekday.csv`, `plots/00_clock.png`).** Volume share peaks at 16:00 UTC (6.1% of
the day, **1.53x the median hour -> hour effect**, US-session open); a secondary bump at 00:00 UTC (4.9%), the daily-bar boundary
every alpha here is built on. Mean |hourly return| max/median 1.42x (16:00 and 00:00 again) -> under 1.5x, no effect by the
rule. Weekday: max/median |daily return| 1.23x -> no weekday effect (Friday-signal days are the calmest).

## 7. What a row physically is

Question: are the Binance bars OPEN-stamped trade prints (as DATA_CARD/MANIFEST say), and does the primary end-of-day price
equal the Binance daily close on EXPLORE?
Rule: open-stamped is confirmed if the zero-gap rate (open == previous hour's close) is high, as for 24/7 trade prints, AND the
first hour of each UTC month is stamped 00:00 (data-hygiene zero-gap check: here "high" is expected, not a synthetic-open
artifact; it is reported by year). Primary vs Binance daily close are **the same print** if the median |gap| < 5 bp.

**Result (`tables/p0_07_row.csv`, `plots/00_row.png`).** Binance 1h zero-gap rate 0.16-0.33 (median 0.25) — normal for 24/7
trade prints, not synthetic opens (DATA_CARD). Every month's first hour is stamped 00:00 for 6 of 7 coins (BCH's first month
starts 2019-11-28 10:00, its listing) -> **open-stamped confirmed**. Primary end-of-day price vs Binance daily close: median gap
**0.00 bp** for all 7 coins -> **same print on EXPLORE**. (From 2022-01-01, 7 coins' primary is the FTMO mid: the signal's
close and the response's price are then different series; that starts inside C2's last quarter and covers all of C3.)
