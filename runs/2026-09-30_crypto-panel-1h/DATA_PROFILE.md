# DATA_PROFILE — Phase 0, EXPLORE slice only (2017-08-17 .. 2021-06-30), primary panel (10 Binance spot coins, 1h)

Each section: question + pre-committed rule (written in this file BEFORE its cell ran), then cell, plot, table, result.
Known facts from TARGET.md CLEANED? (missing 20-128 h/coin, zero-gap rate 0.3-0.6, bitstamp stale 2011-13, coinbase XRP gap,
defi backfilled, cm revised, nyfed_rrp null column) are NOT findings and are not re-reported as observations.
Returns: r_t = log(close_t/close_{t-1}), NaN across missing hours (DATA_CARD.md). Cells: `code/p0_0N_*.py`.

## 1. Distributions (returns, not levels)
**Questions.** (a) Are 1h returns fat-tailed? (b) Is there zero-mass in returns or volume? (c) What do the activity columns
(log volume, log n, taker-buy share buy_vol/vol) look like?
**Rules (pre-committed).** (a) fat-tailed if excess kurtosis > 3 AND Hill tail index (top 1% of |r|) < 4, per coin.
(b) zero-mass "material" if > 1% of hours have r == 0 exactly, or > 0.5% of hours have vol == 0. (c) descriptive: report
median / IQR; a column is "degenerate" if its IQR is 0.
**Cell** `code/p0_01_distributions.py` · **Plot** `plots/00_distributions.png` · **Table** `tables/p0_01_distributions.csv`
**Result:** (a) **Fat-tailed: yes, 10/10** — excess kurtosis 10.0 (SOL) to 104.2 (DOGE), Hill index (top 1% |r|) 2.40-3.95 (<4 in all
10; SOL 3.95 is at the edge). Skew mixed (-1.84 BCH .. +2.74 DOGE). 1h sd 98 bp (BTC) .. 212 bp (SOL). (b) Zero-mass: r == 0 in
0.08-0.87% of hours for 9 coins; **LTC 1.12% > 1% -> material** (likely price-grid discreteness; not investigated further);
vol == 0 in <= 0.015% of hours (not material). (c) log volume IQR 1.1-2.8, log n IQR 1.2-3.5, taker-buy share median
0.49-0.51 (IQR 0.07-0.14): none degenerate. Table `tables/p0_01_distributions.csv`, plot `plots/00_distributions.png`.

## 2. Missingness and gaps
**Question.** Where, when and how much is missing, beyond the known 20-128 missing hours per coin?
**Rule.** A finding only if (i) a coin's missing hours inside its own EXPLORE life exceed 128, or (ii) > 50% of a coin's missing
hours fall in a single calendar month that is not a whole-exchange outage (i.e. the other live coins are not also missing
then), or (iii) zero-volume bars (vol == 0) exceed 0.5% of a coin's bars. Otherwise "consistent with the known facts".
**Cell** `code/p0_02_missing.py` · **Plot** `plots/00_missingness.png` · **Table** `tables/p0_02_missing.csv`
**Result:** **Consistent with the known facts.** Missing hours inside each coin's EXPLORE life: 13 (SOL, DOT) .. 121 (BTC, ETH), all
<= 128 (rule i not met); the largest month is 2018-02 (33 h, 27-29% of a coin's total) and 100% of every coin's missing hours
occur when every other live coin is also missing (whole-exchange outages; rule ii not met); zero-volume bars <= 0.015%
(rule iii not met). Longest gap 33 h (2018-02). Table `tables/p0_02_missing.csv`, plot `plots/00_missingness.png`.

## 3. Autocorrelation — returns, |returns|, volume, and returns relative to the panel
**Questions.** At lags {1,2,3,6,12,24,48,168} hours: (a) are 1h returns autocorrelated? (b) |r| (vol clustering)?
(c) log volume? (d) returns relative to the equal-weight panel mean (r_i - mean_j r_j) — does a coin's RELATIVE move persist or
revert? (e) variance ratio VR(q) = var(q-hour sum)/(q var(1h)) for q in {2,6,24,72,168}. (f) Roll-implied half-spread from
1h trade prints (data_hygiene.roll_effective_spread logic) vs the FTMO half-spread.
**Rules.** (a-d) lag k is significant if |ACF(k)| > 2/sqrt(n_k) (n_k = pairs used); a lag is a "panel fact" only if
significant with the SAME sign in >= 7 of 10 coins. (e) VR(q) departs from 1 if |VR-1| > 2*sqrt(2(2q-1)(q-1)/(3q n))
(Lo-MacKinlay homoskedastic SE; flagged as optimistic under heteroskedasticity) in >= 7/10 coins with the same sign.
(f) bounce is "material for 1h work" if the Roll half-spread > 25% of the coin's 1h median |r|.
**Cell** `code/p0_03_acf.py` · **Plot** `plots/00_acf.png` · **Table** `tables/p0_03_acf.csv`, `tables/p0_03_vr.csv`
**Result:** (a) 1h returns: **lag 1 and lag 2 negative in 10/10** (median -0.044, -0.041); **lag 24 negative in 10/10 (median
-0.051)**; lags 3, 12, 48, 168 not panel facts; lag 6 negative in 6/10 (short of 7). (b) |r|: positive at every lag to 168 h in
10/10 (0.30 at lag 1, 0.11 at lag 168): volatility clusters for over a week. (c) log volume: 0.85 at lag 1, 0.58 at lag 168,
10/10. (d) relative-to-panel returns: lag 1 negative 10/10 (-0.068), lag 2 negative 9/10, lag 24 negative 9/10 (-0.023), lag
12 positive 7/10 (+0.016). (e) VR(q) of raw r < 1 in 10/10 at q=2 (0.96) and q=6 (0.86); 8/10 at q=24 (0.88); 6/10 at q=72;
2/10 at q=168 (not a panel fact). Relative returns: VR<1 at q=2,6 only (10/10). DOGE is the exception at q>=24 (VR 1.19-1.27,
i.e. trending). (f) Roll-implied half-spread 22.8-36.2 bp vs a Binance/FTMO half-spread of ~0.1-2 bp: ratio to median |r|
0.34-0.85 > 0.25 in 10/10 -> "material" by the rule, but the size (10-30x any real spread) says the lag-1 reversal is NOT
explained by bid-ask bounce; it is price-pressure / outlier reversal. Tables `tables/p0_03_acf.csv`, `p0_03_vr.csv`,
`p0_03_roll.csv`; plot `plots/00_acf.png`.

### 3b. Autocorrelation of DAILY returns (added after section 3 ran; rule written before 3b's cell)
**Why added.** Section 3 showed hourly structure (lag 1, 2, 24 negative) whose magnitudes cannot clear a 6.6-36.5 bp round
trip at 1h; the question that matters for costs is whether anything survives at the 1-day grain.
**Questions.** Daily returns (UTC day, sum of 24 hourly log returns, only days with all 24 present): (a) ACF at lags 1, 2, 3, 7
days, raw and relative to the equal-weight panel mean; (b) cross-sectional quintile sort of next-day relative return on today's
relative return (days with >= 5 coins live).
**Rules.** (a) as section 3: significant if |ACF| > 2/sqrt(n), panel fact if >= 7/10 coins same sign. (b) "monotone
reversal/continuation" if the Q1..Q5 mean next-day relative returns have Spearman rho = -1/+1 with quintile rank (|rho| >= 0.9
counts) AND the daily Q5-Q1 spread has |t| > 2 (one observation per day, so no pooled-row inflation).
**Cell** `code/p0_03b_daily.py` · **Plot** `plots/00_daily_acf.png` · **Table** `tables/p0_03b_daily.csv`
**Result:** (a) Daily raw returns: lag 1 median ACF **-0.089, significant negative in 6/10 coins** (rule needs 7 -> NOT a panel fact,
one short); lag 2 +0.057 (4/10 positive), lags 3, 7 nothing. Daily relative returns: nothing at any lag (<= 4/10).
(b) Cross-sectional quintile sort of next-day relative return: Q1..Q5 = -0.3, -15.8, -3.4, -1.3, +11.8 bp, rho 0.40,
Q5-Q1 +12 bp, t 0.72 over 1,126 days -> **no monotone cross-sectional reversal or continuation** at 1 day. By era the Q5-Q1
spread is +50 bp (t 2.25) in 2017-18 and ~0 afterwards. Tables `tables/p0_03b_daily.csv`, `p0_03b_quintiles.csv`; plot
`plots/00_daily_acf.png`.

## 4. Cross-column relationships (impostor check, floor Q3)
**Questions.** (a) Correlation matrix of 1h returns across the 10 coins — any twin? (b) within a coin, are vol / quote_vol / n
twins of each other (log changes)? (c) is the Binance BTC return a twin of the Coinbase BTC return (i.e. a second venue adds
nothing at 1h)? (d) does |r| co-move with log volume contemporaneously (volume a proxy for volatility)?
**Rules.** Impostor/twin pair if Pearson corr > 0.95 on 1h changes. (d) "volume is a volatility proxy" if Spearman(|r|, log vol
detrended by 30-day median) > 0.5 in >= 7/10 coins.
**Cell** `code/p0_04_crosscol.py` · **Plot** `plots/00_crosscorr.png` · **Table** `tables/p0_04_corr.csv`, `tables/p0_04_within.csv`
**Result:** (a) **No twin coins**: pairwise 1h return correlations 0.26 (SOL-DOGE) .. 0.83 (LTC-BCH), median 0.62; none > 0.95.
DOGE is the least connected (0.26-0.42). (b) Within a coin, **vol and quote_vol are twins (corr of log changes 1.000 in
10/10)** -> treated as one column; vol vs n 0.80-0.93 (< 0.95, not twins). (c) **Binance vs Coinbase BTC 1h returns: corr
0.9525 > 0.95 -> twin at 1h** (a second venue adds almost nothing at this grain). (d) Spearman(|r|, detrended log vol)
0.38-0.50, < 0.5 in 10/10 -> **volume is NOT merely a volatility proxy**. Tables `tables/p0_04_corr.csv`, `p0_04_within.csv`,
`p0_04_venue.csv`; plot `plots/00_crosscorr.png`.

### 4e. Volume x return interaction at the daily grain (added after section 4 ran; rule written before 4e's cell)
**Why added.** Section 4(d) showed volume is NOT a mere volatility proxy (Spearman(|r|, detrended log vol) 0.38-0.50 < 0.5 in
10/10), so volume may carry separate information. Taker-buy imbalance is an ALREADY TESTED topic and is not used; only total
volume.
**Question.** Does the next-day relative return after a big relative move depend on whether that move came on abnormal volume?
Volume shock = log(today's volume / median daily volume over the previous 30 days), per coin; today's relative return sign.
**Rule.** Define each day's cross-section: winners (rel return > 0) / losers, and volume-shock tercile (cross-sectional, among
live coins). "Volume modulates the next-day relative return" if the daily series [mean next-day rel return of winners minus
losers in the HIGH-shock tercile] minus [the same in the LOW-shock tercile] has |t| > 2. Descriptive: report all 6 cells.
**Cell** `code/p0_04e_volume.py` · **Plot** `plots/00_volume_interaction.png` · **Table** `tables/p0_04e_volume.csv`
**Result:** Next-day relative return (bp), by volume-shock tercile x today's sign: high: winners +11.6 / losers -9.5; mid: +6.3 / -8.4;
low: -10.6 / -8.6. Winners-minus-losers: low -9.1, mid +20.4, high +20.7 bp. High-minus-low W-L = **+42 bp, t 1.5 over 402
days -> NOT significant by the rule** (direction: high-volume winners continue, low-volume winners do not). Panel-level
descriptive: corr(EW day t, EW day t+1) = **-0.136 on the top-tercile panel volume-shock days vs -0.066 on the other days**
(n 448 / 895). Table `tables/p0_04e_volume.csv`; plot `plots/00_volume_interaction.png`.

## 5. Regime structure — how 1-4 change across eras
**Question.** Do hourly vol, kurtosis, ACF(1) of r, VR(24), average cross-coin correlation and relative-return ACF change across
eras (2017H2-2018, 2019, 2020, 2021H1)?
**Rule.** A structural change is declared for a statistic if its panel median moves by > 2x (ratio) between adjacent eras, or
(for correlations / ACF) by > 0.15 in absolute terms. A CUSUM of the equal-weight squared return (OLS-CUSUM on |r|) is shown
as the break locator; a break date is named only if the CUSUM crosses its 5% band.
**Cell** `code/p0_05_regimes.py` · **Plot** `plots/00_regimes.png` · **Table** `tables/p0_05_regimes.csv`
**Result:** Panel medians by era (2017H2-18 / 2019 / 2020 / 2021H1): 1h sd 138 / 84 / 112 / 180 bp; excess kurtosis 14.9 / 21.3 /
**53.7** / 13.4 (2020 = the 2020-03 crash; >2x jumps 2019->2020 and 2020->2021H1 -> structural change in tails); ACF(1)
-0.067 / -0.023 / -0.062 / -0.020; **ACF(24) -0.052 / -0.045 / -0.041 / -0.056 (negative and stable in every era)**; VR(24)
0.83 / 0.97 / 0.90 / 0.93; relative ACF(1) -0.100 / -0.105 / -0.078 / -0.039 (weakening); average cross-coin corr 0.71 / 0.61
/ 0.58 / 0.58; log-volume ACF(24) **0.67 -> 0.39** 2018->2019 (> 0.15 change: break). OLS-CUSUM of panel mean |r| peaks at
13.6 (band 1.36) on 2018-04-05: volatility level is not constant (the 2018 bear high-vol era vs 2019 calm). Tables
`tables/p0_05_regimes.csv`, `p0_05_breaks.csv`; plot `plots/00_regimes.png`.

## 6. Intraday / weekly shape (descriptive facts, not claims)
**Question.** How do volume and volatility vary by UTC hour and by weekday (each coin's value divided by its own 30-day
rolling median, to remove trend)?
**Rule.** A clock shape "exists" if max/min of the hour-of-day profile > 1.5 (vol or |r|), and a weekday shape exists if
max/min of the weekday profile > 1.3. Descriptive only; hour-of-day RETURN seasonality for BTC is an ALREADY TESTED topic and
is not examined.
**Cell** `code/p0_06_clock.py` · **Plot** `plots/00_clock.png` · **Table** `tables/p0_06_clock.csv`
**Result:** Hour-of-day (UTC, bar open), each coin / own 30-day median, median of 10: **volume clock shape exists** (max/min 1.88:
peak 16:00, trough 21:00; high 12-16 UTC = US/EU overlap); |r| profile max/min **1.47 (< 1.5: no clock shape by the rule)**,
peaks at 00:00 and 16:00. Weekday: volume 1.20x and |r| 1.19x (< 1.3: no weekday shape by the rule); Sat/Sun are the low days
(volume ~0.87x of weekdays). Descriptive only. Tables `tables/p0_06_clock.csv`, `p0_06_weekday.csv`; plot `plots/00_clock.png`.

## 7. What a row physically is
**Question.** Is each row an OPEN-stamped 1h bar of trade prints, knowable at open+1h, as the card says?
**Rules.** Confirmed if all of: (i) every timestamp is on the exact hour and unique; (ii) the zero-gap rate (open_t ==
close_{t-1}) is within TARGET's known 0.3-0.6 band (a trade-print feed, not a synthetic open); (iii) the Binance BTC return at
bar t correlates with the Coinbase BTC return at the SAME stamp t more than at t-1 or t+1 (same stamping convention across
venues; lag +/-1 corr < 1/3 of lag 0); (iv) high >= max(open, close) and low <= min(open, close) in 100% of bars.
**Cell** `code/p0_07_row.py` · **Plot** `plots/00_row_alignment.png` · **Table** `tables/p0_07_row.csv`
**Result:** (i) every stamp on the exact hour and unique: PASS 10/10. (iii) Binance BTC r_t vs Coinbase BTC r_{t-k}: 0.952 at k=0,
-0.032 / -0.036 at k=-1 / +1 (< 1/3 of lag 0): PASS, same OPEN-stamping on both venues. (iv) high/low consistent with
open/close in 100% of bars: PASS. **(ii) zero-gap rate 0.155 (DOT) .. 0.315 (LTC): BELOW TARGET's stated 0.3-0.6 band in 9/10
coins -> rule (ii) FAILS on the low side; overall "row confirmed" = False by the letter of the rule.** Reading: a low zero-gap
rate is what a real trade-print feed produces (the next bar's first trade usually differs from the last trade); the trap the
check exists for (vendor-synthetic opens) shows up as a HIGH rate, so the row is still a trade print, OPEN-stamped, knowable at
open+1h. The TARGET "0.3-0.6" figure does not hold on EXPLORE; logged as OBSERVATIONS #15 (a card discrepancy, not a defect).
No returns in this run use `open`. Table `tables/p0_07_row.csv`; plot `plots/00_row_alignment.png`.
