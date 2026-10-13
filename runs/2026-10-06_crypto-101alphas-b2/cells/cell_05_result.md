branch: refuted
weight_applied: 0.192

# cell_05 — RESULT (test, A38, C2)

**Branch fired: REFUTED.** Deciding number: mean daily cross-sectional rank IC = -0.0192 (se 0.0197, t -0.97, n 287), days 2021-05-20 ..
2022-03-20. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0132). Weight applied to H3: **0.192**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): -0.0047 (se 0.0103, t -0.45, n 287)
- net of 1-day reversal: +0.0347 (se 0.0180, t +1.93, n 287); b_rev1's own IC on C2: -0.0359 (se 0.0197, t -1.82, n 287)
- halves of C2: first -0.0512 (se 0.0273, t -1.87, n 143); second +0.0125 (se 0.0267, t +0.47, n 144)
- top-half minus bottom-half spread: -26.2 bp/day (t -2.67); daily half-membership turnover 0.426;
  implied cost 47.7 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.180; with BTC -0.222


Plot: `plots/cell_05_a38_c2.png`. Table: `tables/cell_05.json`, `tables/cell_05_daily_ic.csv`.
