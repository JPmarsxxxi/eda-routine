branch: supported
weight_applied: 5.103

# cell_12 — RESULT (test, A30, C1)

**Branch fired: SUPPORTED.** Deciding number: mean daily cross-sectional rank IC = +0.0371 (se 0.0214, t +1.73, n 329), days 2020-06-09 ..
2021-05-11. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0723). Weight applied to H1: **5.103**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): +0.0442 (se 0.0269, t +1.64, n 329)
- net of 1-day reversal: +0.0341 (se 0.0221, t +1.54, n 329); b_rev1's own IC on C1: +0.0302 (se 0.0223, t +1.35, n 329)
- halves of C1: first +0.0507 (se 0.0334, t +1.52, n 164); second +0.0236 (se 0.0259, t +0.91, n 165)
- top-half minus bottom-half spread: +20.3 bp/day (t +1.02); daily half-membership turnover 0.249;
  implied cost 34.7 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) +0.058; with BTC +0.022


Plot: `plots/cell_12_a30_c1.png`. Table: `tables/cell_12.json`, `tables/cell_12_daily_ic.csv`.
