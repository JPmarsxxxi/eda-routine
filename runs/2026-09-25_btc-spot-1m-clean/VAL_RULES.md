# STEP 6: VAL rules, written BEFORE VAL is opened

VAL = 2023-03-25 00:00 -> 2023-11-30 23:59 UTC, opened ONCE by `scripts/s6_val.py`, for the top 3 leads below. Only VAL rows
are used: no TRAIN or embargo row enters any VAL statistic, including trailing windows (they start inside VAL, and the
first days without a full window are dropped). The measurement code is the same as Step 4 (same functions, same HAC lags).

> **VAL_NOTE (TARGET.md, verbatim):** "Two reasons VAL is weak evidence. (1) BTC VAL was crossed twice by arc #047 (both pre-registered) and overlaps a
> spent pooled row of the 21:00-23:00 UTC seasonality EDA (see _SEALED_HOLDOUT.md): SOFT-clean. (2) VAL is a
> DIFFERENT REGIME from TRAIN: from 2023-04, median trades per minute fall ~8x (about 3,600 to 450, then
> 240-360) and the share of zero-return bars rises from <0.3% to 4-12% (CLEANING_LOG.md, Gate 4b; cause not
> established). A lead about trade counts, volume or 1-minute tick behaviour can fail VAL for structural reasons."

| lead | testable claim | TRAIN value | SUPPORTED if | REFUTED if | INCONCLUSIVE if |
|---|---|---|---|---|---|
| L1 = OBS5 | The distribution of |hourly r| differs by UTC hour: |r| in hour 00 exceeds hour 05, measured as (|r_h00| - |r_h05|) / same-day mean |hourly r|, per day | +0.41 [+0.35, +0.47] | VAL mean > 0 AND HAC 95% CI lower bound > 0 | VAL mean <= 0 | mean > 0 but CI includes 0 |
| L2 = OBS6 | The distribution of |daily r| differs by weekend vs weekday: weekend |daily r| / trailing 28-day mean |daily r| (VAL days only, >= 14 days of history) is lower than on weekdays | -0.40 [-0.50, -0.30] | VAL coefficient < 0 AND CI upper bound < 0 | coefficient >= 0 | < 0 but CI includes 0 |
| L3 = OBS1 | A change in the trailing 5-min return predicts the opposite-sign 5-min forward return (from the close of bar T+1): fwd5 mean, top minus bottom tr5 decile (deciles formed within VAL) | -2.06 bp [-2.42, -1.71] | VAL effect < 0 AND CI upper bound < 0 | effect >= 0 | < 0 but CI includes 0 |

Also reported for L3, NOT part of the rule: the vol-scaled version and the effect by VAL month (the regime break is in VAL).
A VAL result is not out-of-sample proof. VAL is SOFT-clean, and it is a different regime (VAL_NOTE).
