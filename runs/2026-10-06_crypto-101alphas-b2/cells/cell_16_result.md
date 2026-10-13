branch: inconclusive
weight_applied: 1

# cell_16 — RESULT (test, A53, C2)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = -0.0042 (se 0.0219, t -0.19, n 287), days 2021-05-20 ..
2022-03-20. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0319). Weight applied to H4: **1**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): -0.0130 (se 0.0255, t -0.51, n 287)
- net of 1-day reversal: -0.0017 (se 0.0213, t -0.08, n 287); b_rev1's own IC on C2: -0.0359 (se 0.0197, t -1.82, n 287)
- halves of C2: first -0.0049 (se 0.0308, t -0.16, n 143); second -0.0035 (se 0.0313, t -0.11, n 144)
- top-half minus bottom-half spread: -7.8 bp/day (t -0.67); daily half-membership turnover 0.490;
  implied cost 52.5 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.303; with BTC -0.274


Plot: `plots/cell_16_a53_c2.png`. Table: `tables/cell_16.json`, `tables/cell_16_daily_ic.csv`.
