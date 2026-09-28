# REPORT — btc-spot-1m-clean, run 2026-09-25_btc-spot-1m-clean_v2 (method: 14c-eda, RUNBOOK v2)

**Hypothesis (from SSRN, DECISIONS.md items 6-9):** a change in `close` over the first half-hour of the UTC day (r_first) predicts the same-sign return over the last half-hour of that day (r_last), because late-informed investors trade near the daily close in the direction of the day's early information. Source: Wen, Bouri, Xu & Zhao (2022), SSRN 4080253 (BTC 2013-03..2020-05), momentum leg; definition and mechanism from Gao, Han, Li & Zhou, SSRN 2440866.

**Net status: (c) REFUTED in TRAIN.** The hunt stopped at C5. VAL was not opened. This needs a human to confirm (`cells/cell_05_hypothesis_update.md`).

| # | sub-claim | verdict | deciding number | evidence |
|---|---|---|---|---|
| C1 | inputs exist and vary | supported | 2,038 / 2,040 TRAIN days usable; 0.00% zero r_last 2018+ | `plots/01_existence.png`, `tables/01_existence_by_year.csv` |
| C2 | 00:00 UTC is a focal close | supported, narrowly | first half-hour 1.204x the median half-hour's volume; **last half-hour 0.918x** | `plots/02_boundary_volume.png`, `tables/02_boundary_volume_share.csv` |
| C8 | decay-first | MIXED (inconclusive) | era slopes -0.049/+0.005/-0.037/-0.042/-0.039, all abs(t) <= 1.0 | `plots/03_decay_first.png`, `tables/03_era_slopes.csv` |
| C5 | r_first predicts r_last (+) | **REFUTED** | slope **-0.038**, NW t **-1.23**, Spearman +0.006 (p 0.80), hit 50.6% | `plots/04_effect.png`, `tables/04_effect.csv` |
| C3, C4, C6a, C6b, C7, C11 | impostor, attribution, side bets, shape, gaps | UNTESTED | hunt stopped at C5 | — |
| C9 | economics | UNTESTED | cost unknown; edge in the claimed direction = -2.3 bp/day | `tables/04_effect.csv` |
| C10 | replication on VAL | NOT OPENED | the opening condition (C5 supported) failed | DECOMPOSITION.md |

**Decay-first shape:** MIXED. Four of five eras are negative and none reaches abs(t) 1.5. Chow p 0.53-0.99 and CUSUM p 0.68 say the relationship is stable, and what is stable is its absence (`tables/03_chow.csv`, `tables/03_shape.csv`).

**Cost:** round-trip cost UNKNOWN (TARGET.md). The economics row is UNTESTED. In any case there is no positive edge to price: -2.3 bp/day in the claimed direction.

**What died, and the number that killed it:** the claim that intraday momentum runs from the first half-hour to the last half-hour of the UTC day. Slope -0.038 (NW t -1.23, n 2,038), against the pre-committed rule that a slope <= 0 refutes it.

**Still untested:** the source's REVERSAL leg (definition unreadable; the Pearson/Spearman split in cell 04 hints at reversal on large-move days); conditioning on volatile, high-volume or jump days (C6a). The source says predictability changes on such days, and a subset result could exist even though the pooled claim fails. Other day boundaries. The paper's exact predictor definitions (the PDF could not be read, so the definitions are my operationalisation, DECISIONS.md item 8). Anything on VAL.

**Observations not chased:** see `cells/cell_05_hypothesis_update.md` (tail-driven negative Pearson; opening-heavy, not closing-heavy, volume at the boundary; tau=5 IC p 0.03 read as multiple-testing noise).

**Not re-discovered as leads:** the missing minutes, the zero-quote block, the 2017 flat bars and the 2023 regime break come from CLEANING_LOG.md. They are used only as data facts (DATA_CARD.md) and are not reported as findings.

```
1b finding - BTC first-half-hour return (UTC day) predicts same-sign last-half-hour return   [source: SSRN 4080253 via TARGET.md SEARCH]   [ledger: ALPHA]
  C1 inputs exist and vary - supported (2,038/2,040 TRAIN days)
  C2 00:00 UTC is a focal close - supported narrowly (first half-hour 1.204x volume; last half-hour 0.918x)
  C5 r_first predicts r_last (+) - REFUTED (slope -0.038, NW t -1.23, Spearman +0.006 p 0.80, hit 50.6%, n 2,038)
  decay-first: MIXED  eras -0.049 / +0.005 / -0.037 / -0.042 / -0.039 (t -0.7 / +0.1 / -1.0 / -0.9 / -0.7)
  cost: edge/cost = UNKNOWN (edge in claimed direction -2.3 bp/day)     K so far: 1 claim, 4 scored cells     notebook: C:\Users\User\eda-routine\runs\2026-09-25_btc-spot-1m-clean_v2
  still untested: the source's reversal leg with its exact definition; the volatile/high-volume-day subset (C6a); the paper's own predictor definitions; VAL (never opened)
```
This is a FINDING, not a verdict (part-0): nothing here is written to alpha_log.md.
