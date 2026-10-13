branch: inconclusive
weight_applied: 1

# cell_15 — RESULT (test, A53, C1)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = +0.0096 (se 0.0192, t +0.50, n 329), days 2020-06-09 ..
2021-05-11. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0411). Weight applied to H4: **1**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): +0.0198 (se 0.0290, t +0.68, n 329)
- net of 1-day reversal: -0.0015 (se 0.0192, t -0.08, n 329); b_rev1's own IC on C1: +0.0302 (se 0.0223, t +1.35, n 329)
- halves of C1: first +0.0455 (se 0.0282, t +1.61, n 164); second -0.0261 (se 0.0243, t -1.08, n 165)
- top-half minus bottom-half spread: -15.2 bp/day (t -0.83); daily half-membership turnover 0.522;
  implied cost 54.8 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.399; with BTC -0.329


Plot: `plots/cell_15_a53_c1.png`. Table: `tables/cell_15.json`, `tables/cell_15_daily_ic.csv`.
