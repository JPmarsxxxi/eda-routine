branch: inconclusive
weight_applied: 1

# cell_02 — RESULT (test, A35, C2)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = -0.0086 (se 0.0187, t -0.46, n 286), days 2021-05-20 ..
2022-03-20. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0221). Weight applied to H2: **1**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): +0.0978 (se 0.0432, t +2.27, n 287)
- net of 1-day reversal: -0.0126 (se 0.0177, t -0.71, n 286); b_rev1's own IC on C2: -0.0359 (se 0.0197, t -1.82, n 287)
- halves of C2: first -0.0203 (se 0.0242, t -0.84, n 143); second +0.0031 (se 0.0282, t +0.11, n 143)
- top-half minus bottom-half spread: -12.9 bp/day (t -1.48); daily half-membership turnover 0.430;
  implied cost 48.1 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.694; with BTC -0.594


Plot: `plots/cell_02_a35_c2.png`. Table: `tables/cell_02.json`, `tables/cell_02_daily_ic.csv`.
