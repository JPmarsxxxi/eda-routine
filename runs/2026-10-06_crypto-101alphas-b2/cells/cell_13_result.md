branch: supported
weight_applied: 5.411

# cell_13 — RESULT (test, A30, C2)

**Branch fired: SUPPORTED.** Deciding number: mean daily cross-sectional rank IC = +0.0480 (se 0.0210, t +2.29, n 287), days 2021-05-20 ..
2022-03-20. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0825). Weight applied to H1: **5.411**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): +0.0551 (se 0.0210, t +2.62, n 287)
- net of 1-day reversal: +0.0420 (se 0.0201, t +2.09, n 287); b_rev1's own IC on C2: -0.0359 (se 0.0197, t -1.82, n 287)
- halves of C2: first +0.0484 (se 0.0291, t +1.66, n 143); second +0.0477 (se 0.0302, t +1.58, n 144)
- top-half minus bottom-half spread: +21.9 bp/day (t +2.14); daily half-membership turnover 0.236;
  implied cost 33.8 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) -0.008; with BTC +0.008


Plot: `plots/cell_13_a30_c2.png`. Table: `tables/cell_13.json`, `tables/cell_13_daily_ic.csv`.
