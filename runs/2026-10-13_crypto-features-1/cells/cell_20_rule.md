hypothesis: H10
slice: CONFIRM
kind: confirm
controls: none
conditional: none
candidate: F3

# cell 20 rule - confirm of candidates/F3.md (f003), frozen before this cell, run unchanged on C1, C2 and C3
The frozen spec is candidates/F3.md (not edited after its freeze; this cell's code is code/confirm.py importing features/f003.py). Primary horizon h = 24 (h sampling). Slice CONFIRM = each of C1, C2, C3 separately.
pass_rule (copied from the candidate file, per fold): per fold (C1, C2, C3) and for VAL: supported if the primary-horizon mean rank IC >= +0.02 and NW t >= 1.96; refuted if IC < 0 and NW t <= -1.65; else inconclusive. CONFIRM-SHOWN needs >= 2 supported folds and none refuted. VAL judged with the same rule on 2023-03-25..2023-11-30.
min_useful: 0.02.
Evidence weights (cap 10x): outcome CONFIRM-SHOWN (>= 2 of 3 folds supported, none refuted). Per-fold power at delta = 0.02 from the measured noise (work/noise.json: se = c/sqrt(N), fold powers [0.27, 0.26, 0.36]);
P(CONFIRM-SHOWN | effect at min_useful in every fold) = 0.214; under the null each fold is 'supported' with probability 0.025, P(CONFIRM-SHOWN | null) = 0.0018;
w_yes = 115.9 -> capped 10.0; w_no = 0.79 (floor 0.1). weight_applied = w_yes if CONFIRM-SHOWN else w_no.
