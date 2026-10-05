# FINDINGS — hypotheses that moved >= 0.05 off their prior (RUNBOOK_v3.md "MEMORY"). Budget 300 lines.

Format: `### <run> H<n> — title`, then at most 3 lines: claim / state + posterior + slice evidence / what it needs next.
LOW hypotheses: one `- <run> LOW:` line per run. Informs priors and the already-tested list; NEVER evidence in a new run.

- 2026-09-28_btc-perp-various-free LOW: none
- 2026-09-30_crypto-panel-1h LOW: H4 (high-volume winners continue: opposite sign on CONFIRM)

### 2026-09-25_btc-spot-1m-clean L1-L3 — v1 sweep leads (pre-v3, no ledger)
|r| by UTC hour (00 > 05) and weekend < weekday |r|: both supported on VAL (posterior 0.96). 5-min reversal: VAL supported but 72% smaller, decaying.
Needs: these are volatility/seasonality descriptives, already spent on BTC VAL; a fresh slice (2024+) or another venue.

### 2026-09-25_btc-spot-1m-clean_v2 C5 — first-half-hour -> last-half-hour intraday momentum (SSRN 4080253)
Refuted on TRAIN: slope -0.038, NW t -1.23. VAL not opened.
Needs: nothing; dead on this data.

### 2026-09-28_btc-perp-various-free H1 — funding-clock basis jump after 00/08/16 UTC settlement
OPEN 0.13: EXPLORE +0.74bp jump vs placebo; CONFIRM (2022, almost no positive funding) 0.16bp, refuted by size rule.
Needs: a test conditional on funding > 0.01% on a slice with positive-funding periods (2024+ or another venue).

### 2026-09-28_btc-perp-various-free H2 — DVOL predicts next-24h realized vol beyond trailing 24h/7d/30d RV
HIGH-VAL 0.992: CONFIRM partial rho 0.174, VAL 0.299 (soft-clean VAL).
Needs: an HAR/GARCH control (not only trailing RV) before it counts as more than vol persistence.

### 2026-09-28_btc-perp-various-free H3 — perp basis level predicts next-24h realized vol
OPEN 0.114: CONFIRM partial rho 0.010 (EXPLORE 0.15 was the 2021H1 bull regime).
Needs: nothing unless a regime-conditional mechanism is stated.

### 2026-09-28_btc-perp-various-free H4 — high DVOL precedes positive next-24h spot return
OPEN 0.183: CONFIRM Spearman +0.019, below the 0.025 refute bar. Lead: relative DVOL (vs 30d median) z 1.54 on EXPLORE.
Needs: DVOL beyond 2023-11.

### 2026-09-28_btc-perp-various-free H5 — hourly spot return reversal
OPEN 0.714: CONFIRM Spearman -0.064, all 5 quarters negative; Pearson ~0 (extreme hours continue, moderate ones revert).
Needs: a fresh slice; test rank vs size-weighted form separately (non-linear shape).

### 2026-09-28_btc-perp-various-free H6 — hourly basis change leans against next-hour spot return, given own reversal
OPEN 0.638: CONFIRM partial -0.0188 vs crit -0.0168 (thin).
Needs: a fresh slice.

### 2026-09-30_crypto-panel-1h H5 — intraday 6h-block reversal, 10-coin spot panel
HIGH-VAL 0.985: CONFIRM IC -0.032, VAL -0.063; effect about half its own economic threshold (no size rule then).
Needs: re-test under v3.1 size condition; costs 6.6-36.5bp round trip dwarf it.

### 2026-09-30_crypto-panel-1h H3 — same-hour-yesterday 1h reversal (NO-STORY)
OPEN 0.795: CONFIRM lag-24 IC -0.035. Lead only (no mechanism).
Needs: a mechanism before any further test.

### 2026-09-30_crypto-panel-1h H2 — daily reversal stronger after panel volume-shock days
OPEN 0.708: CONFIRM diff IC -0.202. H6 (6h reversal stronger in high trailing vol) 0.87 on EXPLORE only.
Needs: fold tests (v3.1).

### 2026-09-30_crypto-panel-1h H1 — daily time-series reversal
OPEN 0.227: CONFIRM refuted (IC -0.047, z -1.38). Child H7 crash-day rebound untested (0.42).
Needs: H7 on a slice where its statistic was not shown.
