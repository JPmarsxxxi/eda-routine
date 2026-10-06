branch: supported
weight_applied: 1

# cell_08 — RESULT (redirect, A54 x -1, C1)

**Branch fired: SUPPORTED.** Deciding number: mean daily cross-sectional rank IC = +0.0521 (se 0.0213, t +2.44, n 329), days 2020-06-09 ..
2021-05-11. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0872). Weight applied to H5: **1** (redirect: never moves the parent).

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): -0.0751 (se 0.0351, t -2.14, n 329)
- net of 1-day reversal: +0.0514 (se 0.0199, t +2.58, n 329); b_rev1's own IC on C1: +0.0302 (se 0.0223, t +1.35, n 329)
- halves of C1: first +0.0425 (se 0.0349, t +1.22, n 164); second +0.0617 (se 0.0245, t +2.52, n 165)
- top-half minus bottom-half spread: -2.4 bp/day (t -0.14); daily half-membership turnover 0.489;
  implied cost 52.4 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) +0.272; with BTC +0.256

**Redirect finding (spawn rule): the flipped statistic IS supported on C1** (flipped IC +0.0521, t +2.44; net of 1-day reversal +0.0514, so it is not the reversal twin; second half of C1 carries it, t +2.52 vs +1.22). -> **child H6 spawned**: -1 x Alpha#54, born_on C1 cell_08, seen_on none (H5 opened no other slice). The raw version points the other way (-0.075 for the flipped sign: the own-return/market part does not share the cross-sectional effect), and the top-minus-bottom spread is ~0 bp/day (t -0.14) despite the rank IC — the effect lives in ranks, not in the tails. Both are recorded, neither changes the spawn.
Plot: `plots/cell_08_a54_c1_flip.png`. Table: `tables/cell_08.json`, `tables/cell_08_daily_ic.csv`.
