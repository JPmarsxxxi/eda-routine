# FINDINGS — candidates that reached CONFIRM-SHOWN or a VAL result (RUNBOOK_v3.md "MEMORY"). Budget 300 lines.

Format (v3.3): `### <run> F<n> — title`, then at most 3 lines: frozen spec / CONFIRM folds + VAL result / what it needs next.
One-line lists per run: `- <run> CONFIRM-FAIL: F..` and `- <run> DROPPED: H..`. Informs picks and the already-tried list;
NEVER evidence in a new run.
Entries before v3.3 are in the old format (H<n>, prior/posterior, LOW lines). Where they say "needs a fresh slice", that
no longer applies to TRAIN: under v3.3 those leads may be searched again on the same TRAIN, then frozen and checked.

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

- 2026-10-05_crypto-validated-1h LOW: H3 (S&P spillover: wrong sign C1)
- 2026-10-05_crypto-101alphas LOW: H2 (#42 reversal), H3 (#2), H6 (#2 raw child)
- 2026-10-06_crypto-101alphas-b2 LOW: H3 (#38), H4 (#53), H5 (#54 opposite sign)

### 2026-10-05_crypto-validated-1h H1 — XS perp premium -> 72h relative underperformance
OPEN 0.321: sign negative on C1/C2/C3 (-23/-118/-19 bp) but EXPLORE's -170 bp shrank ~85%; low power per fold (0.2-0.3).
Needs: under v3.3, search TRAIN for the regime where it holds (C2-like), then freeze and check.

### 2026-10-05_crypto-validated-1h H2 — Fear & Greed level -> next-day panel return
OPEN 0.059: spread fell monotonically C1 +70 -> C2 +41 -> C3 -23 bp; likely a bull-regime impostor.
Needs: nothing unless conditioned on something other than trend.

### 2026-10-05_crypto-101alphas H1 — Kakushadze #101 (close-open)/(high-low), daily, 10 coins
HIGH-CONFIRM 0.852 but VAL refuted (+4.7 bp/day, IC -0.03); C1 +57, C2 +33 bp/day, C3 never opened; regime story (2020-22).
Needs: turnover ~2/day -> break-even ~45 bp/day; dead standalone, possible combine-only input.

### 2026-10-05_crypto-101alphas H7 — -#42 over 2 days (child of H2)
OPEN 0.09, untested (no TRAIN slice left under v3.1). Lead.
Needs: under v3.3, searchable on TRAIN.

### 2026-10-06_crypto-101alphas-b2 H1 — Kakushadze #30 volume-scaled 3-day streak fade
OPEN 0.850: rank IC C1 +0.037, C2 +0.048 supported; C3 +0.001, EXPLORE -0.007. A 2020-22 effect; C3 also changes the response series.
Needs: freeze and check on VAL under v3.3; test whether the C3 fade is the response-series switch.

### 2026-10-06_crypto-101alphas-b2 H6 — -#54, closing strength continues (child of #54)
OPEN 0.490: C2 IC +0.057 supported, C3 +0.023 inc; EXPLORE halves point opposite ways (+0.096 / -0.078).
Needs: same as #30; unstable sign is the risk.
