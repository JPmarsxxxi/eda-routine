### Cell 01 — EDA: existence of the inputs (C1)

**Sub-claim being tested:** C1: "Existence: r_first and r_last exist and vary on enough TRAIN days"

**Why it matters to the hypothesis:** with too few usable days, or with degenerate (zero) half-hour returns, there is nothing to measure and the hunt stops.

**Test(s) used:** build the TRAIN half-hour series (last `close` in each UTC half-hour, `vol`, `buy_vol`, `sell_vol`, bar count, sum of squared 1-minute log returns on `gap_min == 1` bars); from it r_first(d), r_mid(d), r_last(d) per UTC day. Gap detection on the three anchors (dropped days; anchors that are not the exact :29/:59 bar); share of exact-zero returns by year; std of r_first by era; flag counts on used days.

**Decision rule before running:** "I will consider C1 **supported** if usable TRAIN days >= 1,500 AND the share of days with r_last == 0 exactly is <= 5% in every year 2018+ AND std(r_first) > 0 in each of the 5 eras; **refuted** if usable days < 1,500 OR any 2018+ year has > 5% exact-zero r_last OR std(r_first) = 0 in some era; **inconclusive** if only 2017 fails the zero-share bound (then 2017 is flagged and C11 decides)."

**Engine/library APIs used:** `pandas.read_parquet`, `DataFrame.resample('30min', label='left', closed='left').last()` (backward-looking: the value is the last trade price inside the half-hour), `numpy.log`.

**Data:** TRAIN only (t <= 2023-03-19 23:59 UTC). VAL and the embargo are masked out before any computation.

**Decisions I need from you:** none; half-hour length is the source's; "last" resample stated in DECOMPOSITION.md.

Proceeding (unattended).
