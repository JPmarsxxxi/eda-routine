branch: refuted
weight_applied: 0.223

# cell_07 — RESULT (test, A54, C1)

**Branch fired: REFUTED.** Deciding number: mean daily cross-sectional rank IC = -0.0521 (se 0.0213, t -2.44, n 329), days 2020-06-09 ..
2021-05-11. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here -0.0171). Weight applied to H5: **0.223**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): +0.0751 (se 0.0351, t +2.14, n 329)
- net of 1-day reversal: -0.0506 (se 0.0198, t -2.56, n 329); b_rev1's own IC on C1: +0.0302 (se 0.0223, t +1.35, n 329)
- halves of C1: first -0.0425 (se 0.0349, t -1.22, n 164); second -0.0617 (se 0.0245, t -2.52, n 165)
- top-half minus bottom-half spread: +2.4 bp/day (t +0.14); daily half-membership turnover 0.493;
  implied cost 52.7 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.272; with BTC -0.256


Plot: `plots/cell_07_a54_c1.png`. Table: `tables/cell_07.json`, `tables/cell_07_daily_ic.csv`.
