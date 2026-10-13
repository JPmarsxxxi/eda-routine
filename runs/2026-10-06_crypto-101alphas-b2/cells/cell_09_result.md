branch: supported
weight_applied: 5.443

# cell_09 — RESULT (test, A54 x -1, C2)

**Branch fired: SUPPORTED.** Deciding number: mean daily cross-sectional rank IC = +0.0567 (se 0.0241, t +2.35, n 287), days 2021-05-20 ..
2022-03-20. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0964). Weight applied to H6: **5.443**.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): +0.0432 (se 0.0309, t +1.40, n 287)
- net of 1-day reversal: +0.0593 (se 0.0233, t +2.54, n 287); b_rev1's own IC on C2: -0.0359 (se 0.0197, t -1.82, n 287)
- halves of C2: first +0.0740 (se 0.0343, t +2.16, n 143); second +0.0395 (se 0.0335, t +1.18, n 144)
- top-half minus bottom-half spread: +27.6 bp/day (t +2.22); daily half-membership turnover 0.477;
  implied cost 51.5 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) +0.372; with BTC +0.430


Plot: `plots/cell_09_a54_c2_flip.png`. Table: `tables/cell_09.json`, `tables/cell_09_daily_ic.csv`.
