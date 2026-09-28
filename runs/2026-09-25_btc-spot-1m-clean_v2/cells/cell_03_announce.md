### Cell 03 — EDA: decay-first gate, era by era (C8), BEFORE any pooled number

**Sub-claim being tested:** C8: "Stability (decay-first gate): the slope is not monotone-decaying and not alternating across TRAIN eras"

**Why it matters to the hypothesis:** part-0's decay-first gate. Monotone decay = crowded away; alternating = noise. Either kills the hunt before the pooled effect is read.

**Test(s) used:** per era (2017-08..2018-12, 2019, 2020, 2021, 2022-01..2023-03-19): OLS slope of r_last on r_first, Newey-West (5 lags) t, n. Then (still no pooled slope printed): rolling 365-day slope; Chow F-test at each of the 4 era boundaries; OLS-residual CUSUM test (statsmodels `breaks_cusumolsresid`).

**Decision rule before running:** era slopes b1..b5, t1..t5, in time order.
- **Monotone decay (KILL)** if t1 >= 2 AND Spearman(era index, b) <= -0.8 AND t5 < 1.
- **Alternating (KILL)** if the sign of b changes >= 2 times across the 5 eras in order AND at least one era of each sign has |t| >= 1.5.
- **Strongest-recent (PASS)** if b5 is the largest of the five, or Spearman(era, b) >= +0.8.
- **Flat (PASS)** if all five b have the same sign and none of the above holds.
- Otherwise **mixed (INCONCLUSIVE)**: flagged; the hunt continues to C5 with this flag carried into the update cell.
Chow / CUSUM are reported beside it; they do not override the shape rule (they test the pooled-regression stability assumption).

**Engine/library APIs used:** `statsmodels.OLS(...).fit(cov_type="HAC", maxlags=5)`, `statsmodels.stats.diagnostic.breaks_cusumolsresid`, Chow F computed from restricted/unrestricted SSR, `scipy.stats.spearmanr`.

**Data:** TRAIN usable days (cell 01).

**Decisions I need from you:** era cut points are calendar years (first era merged 2017-18 because 2017 has only 136 days and is thin; last era runs to TRAIN_END). Fixed here, before running.

Proceeding (unattended).
