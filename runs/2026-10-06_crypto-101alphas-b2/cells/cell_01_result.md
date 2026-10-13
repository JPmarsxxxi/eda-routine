branch: inconclusive
weight_applied: 1

# cell_01 — RESULT (test, A35, C1)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = +0.0101 (se 0.0194, t +0.52, n 328), days 2020-06-09 ..
2021-05-11. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0419). Weight applied to H2: **1**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): +0.0791 (se 0.0451, t +1.75, n 329)
- net of 1-day reversal: -0.0118 (se 0.0175, t -0.68, n 328); b_rev1's own IC on C1: +0.0302 (se 0.0223, t +1.35, n 329)
- halves of C1: first +0.0213 (se 0.0297, t +0.72, n 164); second -0.0011 (se 0.0246, t -0.04, n 164)
- top-half minus bottom-half spread: -7.7 bp/day (t -0.37); daily half-membership turnover 0.428;
  implied cost 47.9 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.653; with BTC -0.534


Plot: `plots/cell_01_a35_c1.png`. Table: `tables/cell_01.json`, `tables/cell_01_daily_ic.csv`.
