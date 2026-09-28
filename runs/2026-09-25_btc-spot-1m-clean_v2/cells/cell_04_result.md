### Cell 04 — result (C5, the effect)
Pooled TRAIN, n = 2,038 days: slope **-0.038**, NW t **-1.23**; Pearson -0.049 (p 0.027); Spearman **+0.006 (p 0.80)**; sign hit
rate 50.6% (binomial p 0.61); mean sign(r_first) x r_last = **-2.3 bp**.
IC by horizon (reported, not scored): tau=1 (23:30-24:00) Spearman +0.006; tau=5 (21:30-24:00) +0.047 (p 0.03); tau=20 (14:00-24:00) -0.022.
Lead-lag profile: r_first vs each of the 47 later half-hours; 4 of 47 exceed +/-2/sqrt(n) (about 2 expected by chance); the
claimed half-hour (47) is +0.006.
**Verdict against the rule: C5 REFUTED** (slope <= 0 AND NW t < 1.0 is not needed; slope <= 0 alone refutes). The hypothesis
cannot survive without C5: **the hunt stops here** (14c Step 3.2). C3, C4, C6a, C6b, C7, C11 are NOT run; C10 (VAL) stays CLOSED
because its opening condition (C5 supported) failed.
Tool disagreement, recorded not averaged: Pearson is negative and nominally significant (p 0.027) while Spearman is ~0 and the
hit rate is 50.6%, so any linear relation is carried by a few large |r_first| days, and it points the OPPOSITE way to the claim
(reversal-like). Not chased (see Observations). Tables `tables/04_effect.csv`, `04_ic_by_tau.csv`, `04_leadlag_profile.csv`; plot `plots/04_effect.png`.
