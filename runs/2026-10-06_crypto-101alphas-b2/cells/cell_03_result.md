branch: inconclusive
weight_applied: 1

# cell_03 — RESULT (test, A35, C3)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = +0.0034 (se 0.0243, t +0.14, n 297), days 2022-03-29 ..
2023-03-18. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0433). Weight applied to H2: **1**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): +0.0918 (se 0.0552, t +1.66, n 298)
- net of 1-day reversal: +0.0045 (se 0.0216, t +0.21, n 297); b_rev1's own IC on C3: +0.0211 (se 0.0242, t +0.87, n 298)
- halves of C3: first +0.0238 (se 0.0328, t +0.73, n 148); second -0.0169 (se 0.0351, t -0.48, n 149)
- top-half minus bottom-half spread: -14.7 bp/day (t -1.42); daily half-membership turnover 0.464;
  implied cost 50.6 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.774; with BTC -0.718


Plot: `plots/cell_03_a35_c3.png`. Table: `tables/cell_03.json`, `tables/cell_03_daily_ic.csv`.
