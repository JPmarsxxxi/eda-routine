branch: inconclusive
weight_applied: 1

# cell_20 — RESULT (test, A30, EXPLORE)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = -0.0069 (se 0.0229, t -0.30, n 429), days 2019-01-01 ..
2020-05-31. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0306). Weight applied to H1: **1**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): -0.0138 (se 0.0260, t -0.53, n 369)
- net of 1-day reversal: -0.0033 (se 0.0214, t -0.15, n 426); b_rev1's own IC on EXPLORE: +0.0258 (se 0.0247, t +1.04, n 500)
- halves of EXPLORE: first -0.0294 (se 0.0344, t -0.85, n 214); second +0.0154 (se 0.0295, t +0.52, n 215)
- top-half minus bottom-half spread: +0.3 bp/day (t +0.03); daily half-membership turnover 0.262;
  implied cost 35.6 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.012; with BTC -0.023


Plot: `plots/cell_20_a30_explore.png`. Table: `tables/cell_20.json`, `tables/cell_20_daily_ic.csv`.
