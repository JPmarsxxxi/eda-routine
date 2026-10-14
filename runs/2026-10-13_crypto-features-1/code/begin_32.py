import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc = kit.tcrit_for(30)
rule = f"""# cell 32 rule - H14: hour-of-day seasonality persistence (controls: coin fixed effect via demeaning across hours of the coin's own average return; conditional: none)
Feature: for each coin and each UTC hour-of-day u, season_N(t) = the mean 1h log return of that coin in bars with the same hour-of-day over the previous N days (the bars at t-24, t-48, ..., t-24N; N = 20, 60), known at the end of bar t-1 for the NEXT bar's hour u = hour(t+1) -
precisely: for the signal stamped at the END of bar t, the next bar has hour u = (hour(t)+1) mod 24, and season_N(t) = mean of the coin's 1h returns at bars t+1-24j, j = 1..N (all strictly in the past).
Forms: (a) raw; (b) demeaned: season_N minus the coin's trailing N*24-hour mean 1h return (removes the coin fixed effect/drift); (c) sign-only: sign of (b) (robust to the fat tails).
Variants: 2 N x 3 forms = 6 features x h = 1, 6, 24 = 18. For h = 6 and 24 the season is still the NEXT-bar seasonality (the horizon return contains it plus later bars). V = 18 (+ same-hour-yesterday lag-24 return as the reference, 3 variants) = 21... counted V = 21.
Pre-stated direction: POSITIVE (the hour-of-day pattern of a coin persists). Pass rule: SUPPORTED if the best (b)/(c) variant has pooled-TRAIN IC >= +0.02 and NW t >= Sidak {kit.tcrit_for(21):.2f} (V = 21); wrong-signed significant counts as 'no'.
{fx.rule_power(21)}
"""
ann = """### Cell 32 - EDA: H14 do coins' own hour-of-day return patterns persist?
**Sub-claim:** (C5) a coin's mean return at the upcoming hour of day over the last 20-60 days predicts its next-bar rank; **side bet:** the fixed effect is removed by demeaning (form b). **Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(32, "H14", "TRAIN", "search", "coin fixed effect (own average return)", "none", rule, ann)
