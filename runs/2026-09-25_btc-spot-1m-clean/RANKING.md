# STEP 5: RANK (Bayes). A ranking of what to check first, not a decision.

Table: tables/23_bayes_ranking.csv; plot: plots/23_bayes_ranking.png; script scripts/s5_rank.py.

**Priors (base rate for the KIND of claim), stated as assumptions:**
- size / volatility claims: **0.50** (odds 1:1). The programme found only the SIZE of moves forecastable.
- direction / mean-return claims: **0.05** (odds 1:19). The programme measured negative out-of-sample R2 for direction and mean across 445 series.

**Likelihood ratio, the smaller of two, both discounted:**
1. p-value bound (Sellke-Bayarri-Berger, LR <= 1/(-e p ln p)) on the Step-4 **twin-controlled** check, with p multiplied by
   K = 50 (Bonferroni, harsher than BH); LR = 1 if K*p >= 1/e.
2. era replication: s of 7 TRAIN eras with the claimed sign; LR = [0.8^s * 0.2^(7-s)] / 0.5^7 (0.8 = assumed chance an era
   shows the sign if the effect is real, 0.5 if it is not).
With 2.9M rows, bound 1 is astronomically large for anything, so bound 2 is what binds except for OBS4.

| rank | lead | prior odds | check t -> p*K | LR (p bound) | eras | LR (eras) | LR used | posterior odds | posterior |
|---|---|---|---|---|---|---|---|---|---|
| 1 | OBS5 |hourly r| by UTC hour (h00 > h05) | 1.00 | 13.29 -> ~0 | 3e35 | 7/7 | 26.8 | 26.8 | 1.00 x 26.8 = 26.8 | **0.96** |
| 2 | OBS6 weekend |daily r| lower | 1.00 | -8.05 -> ~0 | 3e11 | 7/7 | 26.8 | 26.8 | 1.00 x 26.8 = 26.8 | **0.96** |
| 3 | OBS1 5-min reversal | 0.0526 | -8.67 -> ~0 | 5e13 | 6/7 | 6.71 | 6.71 | 0.0526 x 6.71 = 0.353 | **0.26** |
| 4 | OBS4 21-23 UTC mean (known prior) | 0.0526 | 2.64 -> 0.41 | 1.0 | 6/7 | 6.71 | 1.0 | 0.0526 x 1.0 = 0.053 | **0.05** |

Remarks, not re-ranking: OBS1's eras are decaying, with 2023Q1 wrong-signed. OBS4's eras alternate, and it is already a spent
prior hypothesis. The two size leads are "true" in the sense a volatility seasonality usually is. Their value as leads is
for sizing or scheduling, not direction.

Top 3 taken to VAL: **OBS5, OBS6, OBS1** (OBS4 is 4th and its VAL is already spent in pooled form: see VAL_NOTE).
