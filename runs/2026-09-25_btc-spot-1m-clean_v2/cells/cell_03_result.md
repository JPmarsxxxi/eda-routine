### Cell 03 — result (C8, decay-first, era by era)
| era | n | slope | NW t | Spearman IC | hit rate |
|---|---|---|---|---|---|
| 2017-08..2018-12 | 499 | -0.049 | -0.70 | -0.013 | 47.9% |
| 2019 | 365 | +0.005 | +0.11 | +0.080 | 54.8% |
| 2020 | 366 | -0.037 | -0.99 | +0.025 | 50.5% |
| 2021 | 365 | -0.042 | -0.91 | -0.032 | 48.5% |
| 2022-01..2023-03-19 | 443 | -0.039 | -0.73 | +0.027 | 51.9% |
Spearman(era, slope) = +0.10; sign flips = 2; no era has |t| >= 1.5 of either sign.
**Verdict against the rule: MIXED (INCONCLUSIVE)** — not monotone decay, not alternating by the pre-set rule (no era reaches |t| 1.5).
Plainly: 4 of 5 era slopes are NEGATIVE (opposite to the claim), none is distinguishable from zero, and the one positive era
(2019) has slope +0.005 (t 0.11). There is no era in which the claimed momentum shows. Chow at the 4 boundaries: p 0.53-0.99;
OLS-CUSUM p 0.68: the (near-zero) relationship is stable, i.e. stably absent. Carried as a flag; the hunt continues to C5 as the
rule says. Tables `tables/03_era_slopes.csv`, `03_chow.csv`, `03_shape.csv`, `03_rolling_slope.csv`; plot `plots/03_decay_first.png`.
