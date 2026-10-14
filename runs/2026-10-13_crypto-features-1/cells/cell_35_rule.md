hypothesis: H5
slice: CONFIRM
kind: confirm
controls: none
conditional: none
candidate: F8

# cell 35 rule - confirm of candidates/F8.md (F8), frozen before this cell, run unchanged on C1, C2 and C3
The frozen spec is candidates/F8.md (not edited after its freeze; this cell's code is code/confirm.py importing features/F8.py). Primary horizon h = 1 (h sampling). Slice CONFIRM = each of C1, C2, C3 separately.
pass_rule (copied from the candidate file, per fold): per fold (C1, C2, C3) and for VAL: supported if the primary-horizon mean rank IC >= +0.02 and NW t >= 1.96; refuted if IC < 0 and NW t <= -1.65; else inconclusive. CONFIRM-SHOWN needs >= 2 supported folds and none refuted. VAL judged with the same rule on 2023-03-25..2023-11-30.
min_useful: 0.02.
Evidence weights (cap 10x): outcome CONFIRM-SHOWN (>= 2 of 3 folds supported, none refuted). Per-fold power at delta = 0.02 from the measured noise (work/noise.json: se = c/sqrt(N), fold powers [0.85, 0.83, 0.95]);
P(CONFIRM-SHOWN | effect at min_useful in every fold) = 0.960; under the null each fold is 'supported' with probability 0.025, P(CONFIRM-SHOWN | null) = 0.0018;
w_yes = 520.9 -> capped 10.0; w_no = 0.04 (floor 0.1). weight_applied = w_yes if CONFIRM-SHOWN else w_no.
