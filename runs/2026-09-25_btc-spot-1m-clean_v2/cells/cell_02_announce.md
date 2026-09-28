### Cell 02 — EDA: is the UTC day boundary a focal "close"? (C2, assumption)

**Sub-claim being tested:** C2: "Assumption: the UTC day boundary is a focal 'close' around which trading concentrates (the late-informed / rebalancing story needs a close)"

**Why it matters to the hypothesis:** the source's reason is trading near the daily close. A 24 h market has no close; if nothing concentrates at 00:00 UTC, the reason given for the effect has no footing here (net status then cannot be (a)).

**Test(s) used:** per TRAIN day, each half-hour's share of the day's `vol`. For the last half-hour (23:30-23:59) and the first (00:00-00:29): ratio of the mean share to the median of the 48 mean shares; per-day paired comparison of the boundary share with that day's median half-hour share: Wilcoxon signed-rank, Mann-Whitney, Welch t, KS.

**Decision rule before running:** "I will consider C2 **supported** if either boundary ratio >= 1.20 with Wilcoxon p < 0.05 (share above the day's median half-hour); **refuted** if both ratios <= 1.00; **inconclusive** otherwise."

**Engine/library APIs used:** `scipy.stats.wilcoxon`, `mannwhitneyu`, `ttest_ind(equal_var=False)`, `ks_2samp`.

**Data:** TRAIN days from cell 01 (usable days only). Note: this is a volume profile, used ONLY to test the story's assumption; it is not a seasonality claim and no return is conditioned on clock time here.

**Decisions I need from you:** none.

Proceeding (unattended).
