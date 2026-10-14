hypothesis: H2
slice: VAL
kind: val
controls: none
conditional: none
candidate: F5
spec_sha256: 7cca95cde8a1075f41a8c838426f0f759fb53854dc0247b3106c90b6cee79b02

# cell 28 rule - VAL check of candidates/F5.md (f005); the spec is frozen, its sha256 is in the header
VAL_NOTE (TARGET.md, quoted): "VAL is weak evidence. (1) BTC VAL was crossed twice by earlier work. (2) VAL was opened once more, on all 10 coins, for the crash-day rebound topic, and once by runs/2026-10-05_crypto-101alphas (#101): SOFT-clean. (3) VAL may be a DIFFERENT REGIME from TRAIN (2023 was calm; from 2023-04 BTC's 1-minute trade counts fell ~8x)."
The cell runs features/f005.py unchanged on 2023-03-25 .. 2023-11-30 (code/confirm.py run_val); nothing is tuned on what it shows. History before 2023-03-25 (from 2022-12-01) is loaded only to fill trailing windows.
pass_rule (copied verbatim from candidates/F5.md): per fold (C1, C2, C3) and for VAL: supported if the primary-horizon mean rank IC >= +0.02 and NW t >= 1.96; refuted if IC < 0 and NW t <= -1.65; else inconclusive. CONFIRM-SHOWN needs >= 2 supported folds and none refuted. VAL judged with the same rule on 2023-03-25..2023-11-30.
min_useful: 0.02. One VAL check per frozen spec.
Evidence weights (cap 10x): VAL-sample se = c/sqrt(N) = 0.0120 (c from work/noise.json, N ~ 6,400 signal hours x coin share); power at delta 0.02 and tcrit 1.96 = 0.38, alpha(one-sided) 0.0250;
w_yes = 15.3 -> capped 10; w_no = 0.63. weight_applied = w_yes if branch supported else w_no.
