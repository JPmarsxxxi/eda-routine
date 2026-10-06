branch: inconclusive
weight_applied: 1

# cell_18 — RESULT (redirect, A53 x -1, C3)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = +0.0291 (se 0.0209, t +1.39, n 298), days 2022-03-29 ..
2023-03-18. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0634). Weight applied to H4: **1** (redirect: never moves the parent).

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): -0.0004 (se 0.0472, t -0.01, n 298)
- net of 1-day reversal: +0.0226 (se 0.0168, t +1.35, n 298); b_rev1's own IC on C3: +0.0211 (se 0.0242, t +0.87, n 298)
- halves of C3: first -0.0018 (se 0.0304, t -0.06, n 149); second +0.0600 (se 0.0274, t +2.19, n 149)
- top-half minus bottom-half spread: +16.3 bp/day (t +1.35); daily half-membership turnover 0.572;
  implied cost 58.5 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) +0.343; with BTC +0.323

**Redirect finding (spawn rule):** the flipped statistic is NOT supported on C3 (flipped IC +0.0291, t +1.39, under t 1.645) -> **no child**. Where the data points: across H4's three folds the paper-sign IC went +0.010 (C1), -0.004 (C2), -0.029 (C3); the flipped effect is confined to the second half of C3 (t +2.19 vs -0.06 in the first half), i.e. late 2022 - early 2023, and survives removing 1-day reversal (+0.023, t +1.35). Recorded as 'absent until late C3, sign opposite to the paper's there' — not a lead strong enough for INBOX_PROPOSALS.
Plot: `plots/cell_18_a53_c3_flip.png`. Table: `tables/cell_18.json`, `tables/cell_18_daily_ic.csv`.
