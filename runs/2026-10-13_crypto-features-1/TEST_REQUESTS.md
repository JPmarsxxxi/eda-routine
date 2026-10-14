# TEST_REQUESTS - VAL-PASS candidates handed to the user (the routine never opens TEST)

## F8 - perp premium crowding (feature f004), horizon h1
spec_sha256: 0780b5fb26a207246bf9121ac731524b2ef658284b26c657a54e4a473b5fa1a0
hypothesis: H5 (NO-STORY: no)
variant_of: F4 (same feature code at the declared h1 horizon after F4 at h24 failed CONFIRM with C1 +0.0186 and C2 +0.0190 just under 0.02; the family has 2 candidates: F4 h24 and F8 h1; plus F10 funding beyond premium, CONFIRM-FAIL)
confirm: C1=supported (+0.0213, t 4.1), C2=supported (+0.0336, t 6.0), C3=inconclusive (+0.0195, t 4.3)
val: cell_37: IC +0.0210 (NW t +4.73, n 5,803 signal hours, 2023-03-25..2023-11-30) against the pass rule (supported if IC >= +0.02 and t >= 1.96); monthly IC -0.025 (Mar), +0.014, +0.031, +0.031, +0.012, +0.016, +0.042, +0.037, -0.004 (Nov). VAL_NOTE: VAL is weak evidence (crossed on this panel by earlier runs, calm 2023 regime, trade counts fell after 2023-04); not out-of-sample proof.
k: K_train 1291, K_val 5, K_cum_train 1415, K_cum_val 6 (this run's counts over all 17 hypotheses and 10 frozen specs, dataset crypto_panel_validated_2026-10-05; the premium family's own looks are cells 10, 11, 12, 34, 40 (search variants 39+30+33+6+18 = 126) and the confirm cells 21, 35, 41, with VAL cell 37)
label: COMBINE-ONLY
turnover: signal re-ranked every hour (a 1h hold re-forms 24x per day; a 24h hold once per day); no PnL or turnover simulation was run (SCOPE: no backtest)
cost_line: TRAIN gross top-3 minus bottom-3 return +2.12 bp per 1h hold (n 25,971) against 2 x 43.7 = 87.3 bp round trip of the six traded names (TARGET.md measured FTMO costs) -> COMBINE-ONLY; the rank IC is real but the extreme-quantile spread is a few bp.
correlations: market: cross-coin mean standardised feature vs EW market forward return +0.002 (CONFIRM folds), +0.007 (VAL). Baselines/candidates (mean XS Spearman, TRAIN): b_rev1 -0.05, b_rev24 0.00, b_mom168 -0.01, b_lowvol 0.00, b_liq +0.01, f001 0.00, f002 +0.01, f003 +0.01, f005 +0.03, f006 0.00, f007 +0.02, f008 0.00; f009 +0.01. No other VAL-PASS exists in this run.
test_check: run features/f004.py unchanged on TEST; response = log of primary `price` from the END of bar t to the END of bar t+1 (invalid across new_source); per signal hour the cross-sectional Spearman rank IC over the coins with a value; SUPPORTED if the mean IC >= +0.02 with NW t (lags 6) >= 1.96, REFUTED if IC < 0 with t <= -1.65, else inconclusive.
