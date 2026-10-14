hypothesis: H14
slice: TRAIN
kind: search
controls: coin fixed effect (own average return)
conditional: none

# cell 32 rule - H14: hour-of-day seasonality persistence (controls: coin fixed effect via demeaning across hours of the coin's own average return; conditional: none)
Feature: for each coin and each UTC hour-of-day u, season_N(t) = the mean 1h log return of that coin in bars with the same hour-of-day over the previous N days (the bars at t-24, t-48, ..., t-24N; N = 20, 60), known at the end of bar t-1 for the NEXT bar's hour u = hour(t+1) -
precisely: for the signal stamped at the END of bar t, the next bar has hour u = (hour(t)+1) mod 24, and season_N(t) = mean of the coin's 1h returns at bars t+1-24j, j = 1..N (all strictly in the past).
Forms: (a) raw; (b) demeaned: season_N minus the coin's trailing N*24-hour mean 1h return (removes the coin fixed effect/drift); (c) sign-only: sign of (b) (robust to the fat tails).
Variants: 2 N x 3 forms = 6 features x h = 1, 6, 24 = 18. For h = 6 and 24 the season is still the NEXT-bar seasonality (the horizon return contains it plus later bars). V = 18 (+ same-hour-yesterday lag-24 return as the reference, 3 variants) = 21... counted V = 21.
Pre-stated direction: POSITIVE (the hour-of-day pattern of a coin persists). Pass rule: SUPPORTED if the best (b)/(c) variant has pooled-TRAIN IC >= +0.02 and NW t >= Sidak 3.04 (V = 21); wrong-signed significant counts as 'no'.
Power simulation (measured noise, work/noise.json; delta = min_useful 0.02; Sidak critical |t| = 3.04 for V = 21 variants; cap 3x):
  sampling h h=1: se 0.0026, power 1.00, alpha(one-sided) 0.0012, w_yes 840.0 -> 3.00, w_no 0.00 -> 0.33
  sampling h h=6: se 0.0044, power 0.93, alpha(one-sided) 0.0012, w_yes 784.8 -> 3.00, w_no 0.07 -> 0.33
  sampling h h=24: se 0.0058, power 0.67, alpha(one-sided) 0.0012, w_yes 562.4 -> 3.00, w_no 0.33 -> 0.33
  sampling d h=1: se 0.0145, power 0.05, alpha(one-sided) 0.0012, w_yes 40.7 -> 3.00, w_no 0.95 -> 0.95
  sampling d h=6: se 0.0133, power 0.06, alpha(one-sided) 0.0012, w_yes 51.9 -> 3.00, w_no 0.94 -> 0.94
  sampling d h=24: se 0.0164, power 0.03, alpha(one-sided) 0.0012, w_yes 28.8 -> 3.00, w_no 0.97 -> 0.97
