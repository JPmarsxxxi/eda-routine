hypothesis: H6
slice: TRAIN
kind: search
controls: none
conditional: none

# cell 13 rule - H6: cross-venue gaps and lead-lag (Coinbase USD and Upbit KRW vs Binance); controls: none this cell; conditional: none
Features (hourly, all knowable at the bar end; cross-sectional ranks cancel the common USDT/USD and KRW/USD basis):
 Coinbase (9 coins; BNB absent; XRP absent after 2021H1): gap_lvl = log(CB close / BN close) minus its trailing-720h mean; gap_chg_1, gap_chg_3, gap_chg_6 = change of the log gap; retdiff_k = (CB k-hour return) - (BN k-hour return), k = 1, 3, 6.
 Upbit (BTC ETH XRP ADA DOGE SOL; the common KRW/USD move cancels in rank): ub_retdiff_k = (UB KRW k-hour return) - (BN k-hour return), k = 1, 3, 6, and ub_gap_lvl = log(UB close / BN close) minus its trailing-720h mean.
 7 + 4 = 11 features x h = 1, 6, 24 = 33 variants (V = 33). min_n for the cross-section: 5 coins (EXPLORE has only 4-5 Coinbase coins, Upbit 5-6), stated deviation from the default 6.
Pre-stated direction: POSITIVE IC for every feature (the venue that moved up more / trades at a premium leads, Binance catches up).
Pass rule: SUPPORTED if the best variant has pooled-TRAIN IC >= +0.02 and NW t >= Sidak 3.17. Wrong-signed significant results count as 'no'. Not supported otherwise.
Power simulation (measured noise, work/noise.json; delta = min_useful 0.02; Sidak critical |t| = 3.17 for V = 33 variants; cap 3x):
  sampling h h=1: se 0.0026, power 1.00, alpha(one-sided) 0.0008, w_yes 1320.0 -> 3.00, w_no 0.00 -> 0.33
  sampling h h=6: se 0.0044, power 0.92, alpha(one-sided) 0.0008, w_yes 1208.3 -> 3.00, w_no 0.08 -> 0.33
  sampling h h=24: se 0.0058, power 0.62, alpha(one-sided) 0.0008, w_yes 818.2 -> 3.00, w_no 0.38 -> 0.38
  sampling d h=1: se 0.0145, power 0.04, alpha(one-sided) 0.0008, w_yes 48.1 -> 3.00, w_no 0.96 -> 0.96
  sampling d h=6: se 0.0133, power 0.05, alpha(one-sided) 0.0008, w_yes 62.2 -> 3.00, w_no 0.95 -> 0.95
  sampling d h=24: se 0.0164, power 0.03, alpha(one-sided) 0.0008, w_yes 33.4 -> 3.00, w_no 0.98 -> 0.98
Note: with 5-8 coins per cross-section the se is a little above the table (fewer coins per timestamp); the cap makes w_yes 3.0 and w_no is shown.
