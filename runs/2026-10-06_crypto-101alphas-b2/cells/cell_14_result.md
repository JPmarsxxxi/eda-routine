branch: inconclusive
weight_applied: 1

# cell_14 — RESULT (test, A30, C3)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = +0.0013 (se 0.0196, t +0.07, n 298), days 2022-03-29 ..
2023-03-18. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0335). Weight applied to H1: **1**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): +0.0011 (se 0.0336, t +0.03, n 298)
- net of 1-day reversal: +0.0195 (se 0.0221, t +0.88, n 298); b_rev1's own IC on C3: +0.0211 (se 0.0242, t +0.87, n 298)
- halves of C3: first +0.0093 (se 0.0276, t +0.34, n 149); second -0.0066 (se 0.0274, t -0.24, n 149)
- top-half minus bottom-half spread: -11.0 bp/day (t -1.14); daily half-membership turnover 0.241;
  implied cost 34.1 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.025; with BTC -0.025


Plot: `plots/cell_14_a30_c3.png`. Table: `tables/cell_14.json`, `tables/cell_14_daily_ic.csv`.
