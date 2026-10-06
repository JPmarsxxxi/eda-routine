branch: refuted
weight_applied: 0.189

# cell_17 — RESULT (test, A53, C3)

**Branch fired: REFUTED.** Deciding number: mean daily cross-sectional rank IC = -0.0291 (se 0.0209, t -1.39, n 298), days 2022-03-29 ..
2023-03-18. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0052). Weight applied to H4: **0.189**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): +0.0004 (se 0.0472, t +0.01, n 298)
- net of 1-day reversal: -0.0217 (se 0.0169, t -1.29, n 298); b_rev1's own IC on C3: +0.0211 (se 0.0242, t +0.87, n 298)
- halves of C3: first +0.0018 (se 0.0304, t +0.06, n 149); second -0.0600 (se 0.0274, t -2.19, n 149)
- top-half minus bottom-half spread: -16.3 bp/day (t -1.35); daily half-membership turnover 0.563;
  implied cost 57.8 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.343; with BTC -0.323


Plot: `plots/cell_17_a53_c3.png`. Table: `tables/cell_17.json`, `tables/cell_17_daily_ic.csv`.
