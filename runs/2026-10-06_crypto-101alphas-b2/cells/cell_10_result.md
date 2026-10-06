branch: inconclusive
weight_applied: 1

# cell_10 — RESULT (test, A54 x -1, C3)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = +0.0229 (se 0.0226, t +1.01, n 298), days 2022-03-29 ..
2023-03-18. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0600). Weight applied to H6: **1**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): -0.0218 (se 0.0453, t -0.48, n 298)
- net of 1-day reversal: +0.0266 (se 0.0200, t +1.33, n 298); b_rev1's own IC on C3: +0.0211 (se 0.0242, t +0.87, n 298)
- halves of C3: first +0.0057 (se 0.0319, t +0.18, n 149); second +0.0400 (se 0.0317, t +1.26, n 149)
- top-half minus bottom-half spread: +6.2 bp/day (t +0.59); daily half-membership turnover 0.529;
  implied cost 55.3 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) +0.540; with BTC +0.512


Plot: `plots/cell_10_a54_c3_flip.png`. Table: `tables/cell_10.json`, `tables/cell_10_daily_ic.csv`.
