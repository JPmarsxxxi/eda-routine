### Cell 05 — Hypothesis update after EDA

**Original hypothesis:** a change in `close` over the first half-hour of the UTC day (r_first = ln[last `close` 00:00-00:29 of d / last `close` 23:30-23:59 of d-1]) predicts the SAME-SIGN return over the last half-hour of that day (r_last = ln[last `close` 23:30-23:59 / last `close` 23:00-23:29 of d]), because late-informed investors trade near the daily close in the direction of the day's early information (and infrequently-rebalancing investors trade the same way). [Wen, Bouri, Xu & Zhao 2022, SSRN 4080253, momentum leg; Gao, Han, Li & Zhou, SSRN 2440866]

**Sub-claims tested:**
- C1 existence: **supported**. 2,038 of 2,040 TRAIN days usable; 0.00% exact-zero r_last in every year 2018+ (`tables/01_existence_by_year.csv`, `plots/01_existence.png`).
- C2 assumption (00:00 UTC is a focal close): **supported, narrowly and one-sided**. The opening half-hour trades 1.204x the median half-hour (Wilcoxon p 3e-91), but the LAST half-hour, where the story puts the late-informed traders, trades 0.918x, below the median (rank 36/48) (`tables/02_boundary_volume_share.csv`, `plots/02_boundary_volume.png`).
- C8 decay-first: **inconclusive (MIXED)**. Era slopes -0.049 / +0.005 / -0.037 / -0.042 / -0.039, NW t -0.7 / +0.1 / -1.0 / -0.9 / -0.7. No era shows the claimed sign at any strength. Chow p 0.53-0.99, CUSUM p 0.68: stably absent (`tables/03_era_slopes.csv`, `plots/03_decay_first.png`).
- C5 the effect: **REFUTED**. Slope -0.038, NW t -1.23, Spearman +0.006 (p 0.80), hit rate 50.6% (p 0.61), n = 2,038 (`tables/04_effect.csv`, `plots/04_effect.png`).
- C3 impostor, C4 attribution, C6a/C6b side bets, C7 shape, C11 gaps/2017: **not run**. The hunt stopped at C5, as 14c requires.
- C9 economics: **UNTESTED** (round-trip cost unknown; the measured edge is -2.3 bp per day in the claimed direction, so there is no positive edge to price).
- C10 replication (VAL): **not opened**. Its pre-declared condition (C5 supported on TRAIN) failed.

**Net status:** **(c) Hypothesis refuted in this data.** In Binance BTCUSDT spot, 2017-08-18 to 2023-03-19, the first half-hour return of the UTC day does not predict the last half-hour return with positive sign: the pooled slope is negative, in no era is it positive with |t| > 0.2, and the rank IC is zero. No revised hypothesis is proposed from this data (that would be a pick after looking). Negative result logged.

**Observations not in the original hypothesis** (candidate future hunts; NOT chased here):
1. Pearson IC -0.049 (p 0.027) against Spearman +0.006: whatever linear relation exists is carried by a few large |r_first| days and points toward REVERSAL. That matches the source's other ("reversal") leg, which was not taken because its definition could not be read. A future hunt would need the paper's exact reversal predictor, stated before looking.
2. The opening half-hour (00:00-00:29 UTC) carries more volume than the median half-hour (1.20x), while the last half-hour carries less (0.92x). In this market, whatever happens at the UTC day boundary looks like opening activity, not closing activity.
3. The tau = 5 IC (r_first vs 21:30-24:00) is +0.047 (p 0.03), 1 of 3 unscored horizons, and the lead-lag profile has 4 of 47 half-hours outside +/-2/sqrt(n) (about 2 expected). Treat both as multiple-testing noise. The 21:30-24:00 window also borders the ALREADY TESTED 21:00-23:00 topic.

**Decisions I need from you:** confirm the net status (c) before anything further. There is no signal_construction in this routine; this line waits for a human.
