# ATTEMPTS (every look, recorded, never capped; counts toward K)

Slices (SPLITS.md): EXPLORE <= 2021-12-31; CONFIRM 2022-01-01..2023-03-19; embargo 2023-03-20..24 unused; VAL 2023-03-25..2023-11-30.

| # | when (UTC) | cell | slice | what was looked at | K counted as |
|---|---|---|---|---|---|
| 1 | 2026-09-28 20:37 | 00 data card | ALL rows structure; TRAIN for identity | row counts, first/last, dups, steps (all rows); perp-vs-spot identity, stamping (TRAIN) | structure (no return stats on VAL) |
| 2 | 2026-09-28 20:45 | 00b splits | TRAIN coverage counts | non-null counts per slice at 3 candidate boundaries | none (no values) |
| 3 | 2026-09-28 20:50 | p0 items 1-6 | EXPLORE | distributions (17 cols), coverage, ACF (17 series), Spearman matrix (15), lead-lag screen (56 pairs), funding 8h (4 pairs), eras, intraday/weekday | Phase-0 looks: 56 + 4 lead-lag correlations with the future |
| 4 | 2026-09-28 21:00 | p0 extra 4b/6b | EXPLORE | partial Spearman x->next-24h RV (3 x 2), basis cycle profile, jump by funding (4 bins), placebo, DVOL by quarter (3) | Phase-0 looks: 6 partials + 1 jump test + 4 bins + 3 quarters |
| 5 | 2026-09-28 21:05 | power_all | EXPLORE | power simulations (noise calibration) for H1-H5 tests; EXPLORE D mean 1.01bp re-seen | calibration (EXPLORE, already spent) |
| 6 | 2026-09-28 21:10 | 01 H1 CONFIRM | **CONFIRM** (opening 1 of 1 for H1) | D per settlement, NW t; side bets by funding/hour/quarter; cost | K +1 (scored) -> REFUTED |
| 7 | 2026-09-28 22:06 | 02 H1 redirect | EXPLORE (birth slice, not evidence) | D per settlement by funding LE/HI, NEG side, quarter (3 group looks); weight 1 | Phase-0-type looks: 1 HI-vs-LE test + 1 NEG mean + 6 quarter shares |
| 8 | 2026-09-28 22:06 | 03 H3 CONFIRM | **CONFIRM** (opening 1 of 1 for H3) | partial Spearman basis vs next-24h log RV | K +1 (scored) -> REFUTED; + dvol and volume control looks + 5 quarter looks (reported, unscored) |
| 9 | 2026-09-28 22:08 | 04 H3 redirect | EXPLORE (birth slice, not evidence) | basis-level partial by 5 quarters + pooled-ex-best + 2 transforms (24h change, extremity) | Phase-0-type looks: 5 + 1 + 2 |
| 10 | 2026-09-28 22:09 | 05 H2 CONFIRM | **CONFIRM** (opening 1 of 1 for H2) | partial Spearman dvol vs next-24h log RV | K +1 (scored) -> SUPPORTED; + signed-return and EWMA control looks + 5 quarter looks (reported, unscored) |
| 11 | 2026-09-28 22:10 | 06 H5 CONFIRM | **CONFIRM** (opening 1 of 1 for H5) | Spearman(r_t, r_t+1) hourly spot; crash-trim, 5 quarters, 3 terciles, gross/cost | K +1 (scored) -> SUPPORTED; other looks reported, unscored |
| 12 | 2026-09-28 22:18 | 07 H6 CONFIRM | **CONFIRM** (opening 1 of 1 for H6) | partial Spearman d_basis_t vs r_t+1 given r_t | K +1 (scored) -> SUPPORTED (thin: -0.0188 vs crit -0.0168); r_t-1 control, 1% trim, 5 quarters, gross/cost reported, unscored |
| 13 | 2026-09-28 22:24 | 08 H4 CONFIRM | **CONFIRM** (opening 1 of 1 for H4) | Spearman dvol vs next-24h spot return | K +1 (scored) -> REFUTED (0.0194 < 0.025); partial-on-r24b, 5 quarters, best-quarter-out, terciles reported, unscored |
| 14 | 2026-09-28 22:26 | 09 H4 redirect | EXPLORE (birth slice, not evidence) | quarterly raw rho (3), relative-DVOL 24h, raw 72h, raw 168h | Phase-0-type looks: 3 + 1 + 2 |
| 15 | 2026-09-28 22:41 | 10 H2 VAL | **VAL** (opening 1 of 1 for the session) | partial Spearman dvol vs next-24h log RV given 24h/7d/30d RV | K +1 (scored) -> PASS (0.2985 > 0.1213); signed-return, EWMA controls and 2 segments reported, unscored |
| 16 | 2026-09-28 22:36 | power_h6, power_val_h2 | EXPLORE | power simulations (noise calibration) for H6's CONFIRM test and H2's VAL test | calibration (EXPLORE, already counted in Phase 0) |
