branch: inconclusive
weight_applied: 1

# cell_04 — RESULT (test, A38, C1)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = +0.0191 (se 0.0216, t +0.88, n 329), days 2020-06-09 ..
2021-05-11. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0547). Weight applied to H3: **1**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): -0.0291 (se 0.0205, t -1.42, n 329)
- net of 1-day reversal: -0.0199 (se 0.0209, t -0.95, n 329); b_rev1's own IC on C1: +0.0302 (se 0.0223, t +1.35, n 329)
- halves of C1: first +0.0192 (se 0.0321, t +0.60, n 164); second +0.0189 (se 0.0291, t +0.65, n 165)
- top-half minus bottom-half spread: -14.7 bp/day (t -0.67); daily half-membership turnover 0.440;
  implied cost 48.8 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.066; with BTC -0.168


Plot: `plots/cell_04_a38_c1.png`. Table: `tables/cell_04.json`, `tables/cell_04_daily_ic.csv`.
