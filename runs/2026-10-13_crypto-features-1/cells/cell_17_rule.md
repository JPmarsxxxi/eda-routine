hypothesis: H3
slice: TRAIN
kind: search
controls: other kept features and simple baselines (library orthogonality)
conditional: none

# cell 17 rule - H3: orthogonality and cost line of the candidate set, run through the features/ code (controls: the other kept features and five simple baselines; conditional: none)
Looked at: the seven feature modules features/f001.py..f007.py (the code that will be registered) computed from the long TRAIN frame, checked equal to the search-cell versions (f001 = rev3s, f005 = a54_roll; max abs diff reported), at their primary horizons:
 f001 rev3s h6; f002 rev24s (21-06 UTC) h6; f003 nsurp_1 residual h24; f004 -prem_dtr residual h24; f005 f54_roll h24; f006 3-day streak fade at 23:00 h6; f007 Alpha#30 at 23:00 h24 (all other horizons 1/6/24 also reported for the table). Baselines: b_rev1 = -(r1), b_rev24 = -(r24), b_mom168 = +r168, b_lowvol = -std of 1h returns over 168h, b_liq = log trailing-720h mean quote volume.
Orthogonality: the mean over shared timestamps of the cross-sectional Spearman correlation between every pair (12 x 12); max |corr| per feature vs all others and vs the baselines; incremental IC = IC at the primary horizon of the feature's rank residualised on the ranks of its two most correlated others (library features and baselines).
Cost line: per feature at its primary horizon h, mean top-3 minus bottom-3 forward return (bp) over TRAIN, against the round-trip cost of the traded legs (TARGET.md: BTC 18.9, ETH 25.4, LTC 36.5, ADA/DOGE/DOT/BNB/SOL 45-47, BCH 65.5, XRP 68.6 bp; a long and a short leg each pay it) -> STANDALONE if the net spread is positive after 2 x (mean RT cost of the 6 traded names), else COMBINE-ONLY.
Variants: 7 features x 3 horizons = 21 IC evaluations + 7 incremental IC = 28 (V = 28). Hourly sampling (f006/f007 only at 23:00).
Pre-stated primary (H3, one test, tcrit 1.96): f001 is NOT a duplicate: SUPPORTED if max |corr| of f001 with every other candidate and baseline is < 0.7, OR its incremental IC (primary h6) >= +0.02 with NW t >= 1.96. REFUTED if max |corr| >= 0.7 AND incremental IC < 0.01. Else INCONCLUSIVE.
Power: hourly h6 se 0.0044; delta 0.02: power ~1.0; w_yes capped 3.0, w_no capped 0.33.
