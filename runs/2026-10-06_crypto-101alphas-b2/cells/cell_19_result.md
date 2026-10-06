branch: inconclusive
weight_applied: 1

# cell_19 — RESULT (test, A35, EXPLORE)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = +0.0104 (se 0.0268, t +0.39, n 371), days 2019-01-01 ..
2020-05-31. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0545). Weight applied to H2: **1**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): +0.0374 (se 0.0372, t +1.01, n 289)
- net of 1-day reversal: -0.0062 (se 0.0240, t -0.26, n 367); b_rev1's own IC on EXPLORE: +0.0258 (se 0.0247, t +1.04, n 500)
- halves of EXPLORE: first -0.0114 (se 0.0424, t -0.27, n 185); second +0.0322 (se 0.0322, t +1.00, n 186)
- top-half minus bottom-half spread: -2.7 bp/day (t -0.22); daily half-membership turnover 0.468;
  implied cost 50.9 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.666; with BTC -0.587


Plot: `plots/cell_19_a35_explore.png`. Table: `tables/cell_19.json`, `tables/cell_19_daily_ic.csv`.
