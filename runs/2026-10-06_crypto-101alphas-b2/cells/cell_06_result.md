branch: inconclusive
weight_applied: 1

# cell_06 — RESULT (redirect, A38 x -1, C2)

**Branch fired: INCONCLUSIVE.** Deciding number: mean daily cross-sectional rank IC = +0.0192 (se 0.0197, t +0.97, n 287), days 2021-05-20 ..
2022-03-20. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here +0.0517). Weight applied to H3: **1** (redirect: never moves the parent).

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): +0.0047 (se 0.0103, t +0.45, n 287)
- net of 1-day reversal: -0.0285 (se 0.0189, t -1.51, n 284); b_rev1's own IC on C2: -0.0359 (se 0.0197, t -1.82, n 287)
- halves of C2: first +0.0512 (se 0.0273, t +1.87, n 143); second -0.0125 (se 0.0267, t -0.47, n 144)
- top-half minus bottom-half spread: +26.2 bp/day (t +2.67); daily half-membership turnover 0.427;
  implied cost 47.8 bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) +0.180; with BTC +0.222

**Redirect finding (spawn rule):** the flipped statistic is NOT supported on C2 (flipped IC +0.0192, t +0.97: under 0.02 and under t 1.645) -> **no child**. Where the data points instead: #38's ranking on C2 is carried by its 1-day-reversal twin, which itself pointed to CONTINUATION on C2 (b_rev1 IC -0.036, t -1.82), and the part of #38 orthogonal to that reversal ranked the other way (net-of-reversal IC for the paper's sign +0.035, t +1.93, in cell_05's descriptives). That orthogonal part — the 10-day range position x day's move, with yesterday's move removed — is recorded as a LEAD for a future session (INBOX_PROPOSALS.md), not spawned: the pre-committed spawn rule covers only the sign flip, and C2 is the slice that produced it.
Plot: `plots/cell_06_a38_c2_flip.png`. Table: `tables/cell_06.json`, `tables/cell_06_daily_ic.csv`.
