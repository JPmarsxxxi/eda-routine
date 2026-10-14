hypothesis: H5
slice: TRAIN
kind: search
controls: none
conditional: none

# cell 10 rule - H5: perp positioning (funding, premium index, perp-spot basis, open interest change, long/short ratio) as cross-sectional predictors (controls: none this cell; conditional: none)
Features (hourly, point-in-time; funding = last settled rate with stamp <= bar open; premium index = premium-klines close of bar t; basis = perp kline close / spot close - 1 of bar t; OI and ratios = last 5m snapshot <= open+55min; OI == 0 -> NaN):
 funding_lvl; funding_chg_24 (funding minus funding 24h earlier); prem_lvl (premium index close, bp); prem_chg_6 (change over 6h); basis_lvl; basis_chg_6; oi_chg_6, oi_chg_24 (log change of open interest in coin units); oi_val_chg_24 (log change of OI notional);
 ls_acct_lvl (count_long_short_ratio) and ls_chg_24; ls_top_lvl (top-trader count ratio); taker_ls_lvl (sum_taker_long_short_vol_ratio, log). 13 features x h = 1, 6, 24 = 39 variants (V = 39).
Cross-section: coins with the input available; coverage by fold is reported (OI/ls: BTC only before 2021-12 -> cross-section < 6 coins -> NaN IC until C1 end; EXPLORE and most of C1 are empty for those, so their folds are 'n/a').
Pre-stated directions (crowding story): higher funding / premium / basis / OI growth / long-short ratio -> LOWER return (score = -IC); taker_ls (aggressive buying) -> HIGHER (score = +IC).
Pass rule: SUPPORTED if the best variant in its pre-stated direction has pooled score >= +0.02 and NW t >= Sidak 3.22 (pooled over the folds where it exists) AND the same sign in BOTH C2 and C3 (the only folds with all coins). Not supported otherwise.
Power simulation (measured noise, work/noise.json; delta = min_useful 0.02; Sidak critical |t| = 3.22 for V = 39 variants; cap 3x):
  sampling h h=1: se 0.0026, power 1.00, alpha(one-sided) 0.0006, w_yes 1560.0 -> 3.00, w_no 0.00 -> 0.33
  sampling h h=6: se 0.0044, power 0.91, alpha(one-sided) 0.0006, w_yes 1415.9 -> 3.00, w_no 0.09 -> 0.33
  sampling h h=24: se 0.0058, power 0.60, alpha(one-sided) 0.0006, w_yes 938.1 -> 3.00, w_no 0.40 -> 0.40
  sampling d h=1: se 0.0145, power 0.03, alpha(one-sided) 0.0006, w_yes 51.1 -> 3.00, w_no 0.97 -> 0.97
  sampling d h=6: se 0.0133, power 0.04, alpha(one-sided) 0.0006, w_yes 66.4 -> 3.00, w_no 0.96 -> 0.96
  sampling d h=24: se 0.0164, power 0.02, alpha(one-sided) 0.0006, w_yes 35.3 -> 3.00, w_no 0.98 -> 0.98
Note on N: pooled sample is smaller for OI/ls features (C2+C3 + part of C1, ~11,000 hours, se ~0.009 at h24): power at delta 0.02 is lower than the table above; the cap makes w_yes 3.0 and w_no stays near 0.75-0.9 for them.
