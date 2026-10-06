branch: inconclusive
weight_applied: 1

# cell_11 — RESULT (test, A54 x -1, EXPLORE)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = +0.0091 (se 0.0234, t +0.39, n 504), days 2019-01-01 ..
2020-05-31. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0475). Weight applied to H6: **1**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): -0.0363 (se 0.0402, t -0.90, n 444)
- net of 1-day reversal: +0.0022 (se 0.0230, t +0.10, n 500); b_rev1's own IC on EXPLORE: +0.0258 (se 0.0247, t +1.04, n 500)
- halves of EXPLORE: first +0.0964 (se 0.0341, t +2.83, n 252); second -0.0783 (se 0.0251, t -3.12, n 252)
- top-half minus bottom-half spread: +11.9 bp/day (t +1.16); daily half-membership turnover 0.593;
  implied cost 60.1 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) +0.305; with BTC +0.234


Plot: `plots/cell_11_a54_explore_flip.png`. Table: `tables/cell_11.json`, `tables/cell_11_daily_ic.csv`.
