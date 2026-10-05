# DATA PROFILE — Phase 0, EXPLORE slice only (TRAIN start .. 2021-12-31)

Cells: `scripts/p0_panel.py` (hourly open-stamped panel -> `tables/p0_panel_EXPLORE.parquet`), `scripts/p0_items.py`
(items 1-6), `scripts/p0_extra.py` (items 4b, 6b). Summary numbers: `tables/p0_summary.json`, `tables/p0_extra.json`.
Panel: one row per UTC hour H = the hour [H, H+1h), knowable at H+1h. Spot return `r` = log close-to-close on consecutive
hours only (from the 30m spot file). `rv_1m` = sqrt(sum of squared true 1-minute spot returns in the hour, >= 30 minutes
present). Perp fields = last 5m snapshot in the hour. `basis_bp` = hourly mean of 1e4*log(perp 5m close / spot 1m close at the
same minute). Gaps are left missing. Impossible values set to NaN with counts: OI == 0 on 1 hour, spot quote volume == 0 on
1 hour.

Each rule below was written into the cell's source before its numbers were printed.

---

## 1. Distributions (returns / changes, not levels)

**Question:** what shape do the columns have: tails, skew, zero mass?
**Rule:** fat-tailed if excess kurtosis > 3 AND D'Agostino-Pearson p < 0.01; zero mass notable if exact-zero share > 5%.
**Cell:** `p0_items.py` item 1. **Plot:** `plots/00_1_distributions.png`. **Table:** `tables/p0_1_distributions.csv`.

| column | n | std | skew | ex.kurt | zero share | fat? |
|---|---|---|---|---|---|---|
| r (spot, 1h) | 38,183 | 0.95% | -0.48 | 29.7 | 0.07% | yes |
| r1 (spot, 1m) | 2,257,058 | 0.14% | 0.10 | 76.0 | 1.78% | yes |
| d_qvol (log) | 38,171 | 0.49 | 0.51 | 2.2 | 0 | no |
| d_log_rv | 37,674 | 0.40 | 0.63 | 2.4 | 0 | no |
| buy_share (spot taker) | 38,218 | 0.074 | -0.40 | 6.5 | 0 | yes |
| log_taker (perp) | 11,643 | 0.145 | 0.98 | 3.3 | 0 | yes |
| d_oi | 11,667 | 1.37% | -2.74 | 38.0 | 0.19% | yes |
| d_ls_all / d_ls_top_cnt / d_ls_top_sum | ~11,636 | 4.0% / 3.5% / 1.1% | | 8.4 / 9.6 / 117.6 | ~0.2% | yes |
| basis_bp (level: a spread, stationary) | 11,655 | 7.26 bp (mean +3.63) | -0.24 | 16.6 | 0 | yes |
| d_basis | 11,639 | 2.84 bp | -10.7 | 1,080 | 0 | yes (one-hour spikes) |
| d_dvol | 6,599 | 0.97% | -0.23 | 79.1 | 1.1% | yes |
| half_bp (level) | 18,137 | 0.17 (median 0.13) | 1.78 | 3.05 | 0 | yes (barely) |
| funding (8h) | 2,193 | 0.034% (mean 0.022%) | 1.73 | 11.3 | 0 | yes |

Result: every return/change series except volume and RV changes is fat-tailed. No zero-mass problem (max 1.8% for 1m
returns). Funding has a **point mass at exactly 0.0100% (46.8% of prints)**, the exchange's default rate, and 2 cap hits
at +/-0.30%.

## 2. Missingness and gaps

**Question:** where, when and how much is missing in each series inside its own coverage span?
**Rule:** a month is notable if < 95% of its hours are present; a gap is notable if >= 24 consecutive missing hours.
**Cell:** `p0_items.py` item 2. **Plot:** `plots/00_2_missingness.png`. **Table:** `tables/p0_2_coverage_by_month.csv`.

| series | first stamp | longest gap (h) | gaps >= 24h | months < 95% |
|---|---|---|---|---|
| spot hourly close | 2017-08-17 04:00 | 34 | 1 | 1 |
| spot 1m (hour fully covered) | 2017-08-21 07:00 | 367 | 14 | 5 |
| metrics OI | 2020-09-01 | 4 | 0 | 0 |
| metrics ls_all | 2020-09-01 | 33 | 1 | 0 |
| basis | 2020-09-01 | 4 | 0 | 0 |
| DVOL | 2021-04-01 | 0 | 0 | 0 |
| **half_bp** | 2017-08-20 15:00 | **598** | **143** | **51 of 53** |
| funding | 2020-01-01 | 8h cadence, 0 missed settlements | | |

Result: **the half-spread series is the only badly gapped file**: present on 79% of 2017 hours, 53% (2018), 35% (2019),
55% (2020), 35% (2021). Any per-event cost number is available for about half the events at best. Everything else is
essentially complete inside its span. The 1m file's 367-hour gap is in 2018 (source cache), and the hourly return series
from the 30m file covers it.

## 3. Autocorrelation

**Question:** how persistent are returns, |returns|, volume and the derivative series?
**Rule:** ACF(k) significant if |ACF(k)| > 2/sqrt(n).
**Cell:** `p0_items.py` item 3. **Plot:** `plots/00_3_acf.png`. **Table:** `tables/p0_3_acf.csv`.

| series | band | lag1 | lag2 | lag3 | lag6 | lag12 | lag24 |
|---|---|---|---|---|---|---|---|
| r (1h) | 0.010 | **-0.053** | **-0.037** | -0.005 | **-0.018** | 0.007 | **-0.046** |
| abs r | 0.010 | 0.300 | 0.282 | 0.265 | 0.242 | 0.237 | 0.209 |
| log qvol | 0.010 | 0.957 | | | | | 0.910 |
| log rv | 0.010 | 0.823 | 0.761 | | 0.698 | | 0.669 |
| basis_bp | 0.019 | 0.923 | 0.882 | 0.862 | 0.833 | 0.803 | 0.774 |
| d_basis | 0.019 | **-0.230** | -0.138 | -0.040 | | | |
| d_oi | 0.019 | 0.080 | 0.018 | | | | 0.044 |
| log_taker | 0.019 | 0.317 | 0.297 | | | | 0.229 |
| half_bp | 0.015 | 0.995 | 0.991 | | 0.977 | 0.958 | 0.925 |
| d_dvol | 0.025 | 0.059 | 0.043 | -0.065 | | | |
| r1 (1m) | 0.001 | -0.060 | -0.019 | -0.005 | | | |
| funding (8h lags) | 0.043 | 0.771 | 0.707 | 0.657 | | | |

Result: hourly spot returns have small but significant **negative** lag-1/lag-2 and lag-24 autocorrelation. The Roll
estimate from the 1m ACF is 3.45 bp (`roll_halfspread_bp_1m`), against a measured median half_bp of 0.13 bp. Bounce can
explain only about -(3.45/95)^2 ≈ -0.001 of the hourly lag-1 ACF, so -0.053 is not bounce. Volatility (|r|, RV) is highly
persistent, as expected. half_bp is almost a random walk at hourly frequency (ACF 0.995), which is **smoother than any
raw spread measurement should be**. It looks like a rolling/smoothed estimate, and its construction is not documented.

## 4. Cross-column relationships (and impostors)

**Question:** which columns are twins of each other; what moves together contemporaneously; which lagged relations exist?
**Rule:** impostor/twin if |Spearman| > 0.9 on changes (reported down to 0.5); lead-lag screen notable if |rho| > 2/sqrt(n).
The screen is a Phase-0 look (counted in K), not a finding. 4b: partial Spearman with next-24h log RV after controlling
trailing 24h and 30d log RV, notable if |partial| > 2/sqrt(n).
**Cell:** `p0_items.py` item 4, `p0_extra.py` 4b. **Plots:** `plots/00_4_corr.png`. **Tables:** `tables/p0_4_corr_spearman.csv`,
`tables/p0_4_leadlag_screen.csv`, `tables/p0_4b_partial_rv.csv`.

Twins / near-twins (|rho| > 0.5, 2020-09..2021-12): d_oi ~ d_oi_val 0.81 (OI value = OI x price, **an impostor of
price**); d_ls_top_cnt ~ d_ls_all 0.84; perp_taker_buy_share ~ log_taker 0.76 (same flow, two encodings); r ~
perp_taker_buy_share 0.69 (flow and price move together contemporaneously); d_qvol ~ d_log_rv 0.74. Funding ~ trailing-8h
basis **0.94**: funding is close to a twin of the price-based basis. None exceeded 0.9 on changes.

Lead-lag screen (Spearman with the FUTURE; selected rows; full 56 rows in the table):

| x (known at t) | next-1h r | next-24h r | next-24h sum abs r | next-24h log RV |
|---|---|---|---|---|
| r | **-0.078** | -0.005 | -0.002 | 0.001 |
| half_bp | 0.013 | 0.027 | **0.622** | **0.622** |
| dvol | 0.022 | **0.064** | **0.437** | **0.427** |
| basis_bp | -0.019 | **-0.058** | **0.240** | **0.286** |
| log_taker | 0.013 | 0.044 | -0.176 | -0.200 |
| d_ls_all | -0.019 | -0.057 | 0.020 | 0.023 |
| d_basis | **-0.041** | -0.014 | 0.006 | 0.009 |
| log_rv (trailing 1h) | 0.024 | 0.037 | 0.706 | — |
| funding (8h rows, n=1,433) | -0.051 (next 8h) | -0.087 | | |

4b, partial Spearman with next-24h log RV:

| x | ctrl: trailing 24h RV | ctrl: + trailing 30d RV | contemporaneous corr with trailing 24h RV | n |
|---|---|---|---|---|
| dvol | 0.204 | **0.174** | 0.489 | 6,373 |
| half_bp | 0.126 | **0.083** | 0.661 | 16,125 |
| basis_bp | 0.153 | **0.150** | 0.251 | 11,203 |

Result: the big raw vol-forecast correlations of half_bp (0.62) and DVOL (0.44) are mostly **the trailing-volatility
impostor**. half_bp in particular is 0.66 correlated with trailing RV and keeps only 0.08 after controls. DVOL and basis each
keep about 0.15-0.17 partial. The derivative series carry little about next-hour spot DIRECTION except known families
(positioning, flow).

## 5. Regime structure (eras)

**Question:** how do items 1-4 change across eras; any structural break?
**Rule:** break noted when a statistic differs from the adjacent era by > 2x, or a signed statistic flips sign.
**Cell:** `p0_items.py` item 5. **Plot:** `plots/00_5_regimes.png`. **Tables:** `tables/p0_5_eras.csv`, `tables/p0_5_eras_derivs.csv`.

| statistic | 2017-18 | 2019 | 2020 | 2021 |
|---|---|---|---|---|
| std r (1h) | 1.20% | 0.71% | 0.80% | 0.92% |
| ex.kurt r | 13.5 | 26.4 | 124.6 (Mar-2020) | 11.1 |
| ACF1 r (1h) | -0.084 | +0.005 | -0.076 | +0.004 |
| ACF1 r (1m) | -0.114 | -0.006 | -0.012 | +0.024 |
| median hourly quote vol | 7.3M | 9.0M | 22.0M | 106.2M |
| median trades/h | 5,962 | 10,962 | 25,505 | 55,202 |
| median half_bp | 0.212 | 0.072 | 0.103 | 0.139 |
| half_bp coverage | 60% | 35% | 55% | 35% |
| basis mean / std (bp) | — | — | 0.93 / 5.8 | 4.53 / 7.5 |

Derivative-side sub-eras: basis mean 0.93 (2020-09..12), **7.29 (2021H1)**, 1.82 (2021H2). Median ls_all 1.36 / 2.14 / 1.70.
DVOL median 94.4 (2021H1) / 88.9 (2021H2).

Result: **breaks by rule.** (a) Hourly lag-1 return ACF alternates in sign era to era (-0.084, +0.005, -0.076, +0.004), the
floor-Q8 "noise" signature, not decay. (b) The 1m bounce (ACF1 -0.114) collapses after 2018 and turns positive in 2021.
(c) Volume grows 15x from 2017-18 to 2021 (> 2x at every step 2019->2020->2021). (d) Median half_bp drops 3x 2017-18 -> 2019.
(e) The basis level is regime-dependent (2021H1 bull ≈ 8x 2020's mean).

## 6. Intraday / weekly shape (descriptive facts only)

**Question:** how do volume, volatility, spread and basis vary by UTC hour and weekday?
**Rule:** a shape is noted if the max/min ratio across hours (or days) > 1.5. 6b: the basis jump across funding settlement
is notable if it differs from the mid-cycle placebo by > 2 SE.
**Cell:** `p0_items.py` item 6, `p0_extra.py` 6b. **Plots:** `plots/00_6_intraday.png`, `plots/00_6b_basis_cycle.png`.
**Tables:** `tables/p0_6_hour_of_day.csv`, `tables/p0_6_day_of_week.csv`, `tables/p0_6b_basis_cycle_profile.csv`,
`tables/p0_6b_jump_by_funding.csv`.

Hour of day (2019-2021): quote volume max/min **1.82** (peak 13-16 UTC and 00 UTC, trough 05 UTC); mean |r| 1.51 (00 UTC
highest at 0.61%); RV 1.48; half_bp **1.06 (flat)**; **basis mean 1.56, with step rises in the hours starting 00, 08 and
16 UTC, the funding settlement hours** (23h 2.86 -> 00h 3.52; 07h 3.26 -> 08h 4.06; 15h 3.20 -> 16h 3.94 bp), then a decline
through each 8h cycle. |d_oi| is also higher in hours 08 and 13-16. Weekday: volume max/min 1.45 (weekend low), |r| 1.28,
half_bp 1.15 (weekend LOWER, 0.094 Sat vs 0.108 Mon).

6b (5-minute resolution, 1,456 settlements, 2020-09..2021-12): mean basis in the 30 min after settlement minus the 30 min
before = **+0.74 bp (SE 0.05)**; the same measure at the non-settlement mid-cycle point = **-0.11 bp (SE 0.05)**. The within-cycle
drift (last 30 min minus first 30 min) = -0.74 bp (SE 0.10). Both scale with the funding just settled (Spearman +0.23 jump,
-0.24 drift): jump +0.27 / +0.53 / +0.61 / **+1.48** bp and drift +0.33 / -0.36 / -0.68 / **-2.12** bp for funding <0.01% / =0.01% /
0.01-0.03% / >0.03%. Under low/negative funding the within-cycle shape inverts (starts low, rises).

## 7. What a row physically is

From `DATA_CARD.md` (identity checks in `scripts/cell_00_datacard.py`):
- **Spot** (NOT perp, despite the folder names): 1m / 30m / hourly Binance BTCUSDT spot trade-print bars, open-stamped,
  knowable at bar end. Returns are on trade prints (last trade), not mid. Bid/ask are not available.
- **Perp**: metrics 5m snapshots (OI, ratios, taker vol ratio) + open-stamped 5m perp klines. Knowable conservatively at
  create_time + 5 min. Funding: rate applied at 00/08/16 UTC settlement.
- **DVOL**: Deribit 30-day implied-vol index, hourly, open-stamped (assumed), knowable at hour end.
- **half_bp**: hourly half-spread in bp of undocumented construction and venue. Item 3 (ACF 0.995) and item 4 (0.66 with
  trailing RV) say it is a smoothed estimate that co-moves with volatility, not a raw quote measurement. It is used as a
  COST input only.
- Clock: all UTC, verified (1m complete days run 00:00-23:59, funding at 00/08/16 exactly after rounding ms jitter).
