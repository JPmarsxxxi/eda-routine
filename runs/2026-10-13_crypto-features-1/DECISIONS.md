# DECISIONS (run 2026-10-13_crypto-features-1)

mode: E
job: features

- D1 (installs): TARGET.md allows any PyPI install, but no claim in this run needs a tool the base stack (numpy/pandas/scipy/statsmodels) lacks, so no .venv is created
  and nothing is installed. An install no cell uses is decoration (RUNBOOK_v3). INSTALLS.md is not written. If a later cell needs one, it will be logged here.
- D2 (data): all raw loads through eda_guard (TRAIN bound 2023-03-19 23:59:59); cached derived frames are written only from guard-returned TRAIN rows (work/).
- D3 (slices): SPLITS.md declared from coverage counts before any forward return; same fold labels as earlier runs on this panel.
- D4 (noise): day-permutation null on EXPLORE (code/p0_04_noise.py, work/noise.json) sets the standard error used in every power simulation:
  se(mean IC) = c / sqrt(N rows), c measured per sampling mode and horizon (hourly sampling h1 0.44, h6 0.74, h24 0.96; daily sampling h1 0.50, h6 0.46, h24 0.56).
  NW t calibration under the null: sd(t) 0.92-1.1 (acceptable).
- D5 (alpha level and evidence): a search cell's primary test is the best of its V variants, judged at the Sidak critical |t| = Phi^-1(1 - 0.025/V) (>= 1.96)
  and |mean IC| >= min_useful 0.02 on the stated slice; evidence weight yes = power/alpha, no = (1-power)/(1-alpha), power at delta = min_useful using the
  measured se, capped 3x. Direction pre-stated per hypothesis; a significant IC with the opposite sign counts as `no`.
- D6 (cross-section): rank IC per timestamp across the coins available (>= 6) - market-neutral by construction. Hourly sampling uses every hour; a daily-defined
  feature is evaluated at its UTC-day-end anchor (23:00 bar) and, as a variant, at every hour with rolling-24h windows (the family anchor-hour sweep).
- D7 (supplementary computation outside a cell): cell 34's pre-stated incremental leg for f008 used its two most correlated partners (f006, f007), which exist only at the 23:00 bar, so the residual series had 969 rows and the leg failed on a measurement artifact. The rule was applied as written (weight 0.333). For the registry,
  the incremental IC against dense partners was recomputed in code/supp_f008_inc.py (work/supp_f008_inc.json); it is descriptive only and moved no posterior.
- D8 (cell 40 check-line slip): the cell's printed `supported:` line used `-b.t` and `c2 < 0, c3 < 0` although the series was already the score (-IC), so it printed False. The rule file's own wording (score >= 0.015, t >= 2.64, same sign in C2 and C3) is met (score +0.0172, t +3.04, C2 +0.031, C3 +0.029) and the result was recorded as SUPPORTED; no data or threshold changed.
- drop H6: three search cells (13, 14, 46); the venue gaps are the Binance last-print bounce (cell 14: 60-90% of the h1 IC vanishes with a one-bar delay, the rest is <= +0.014 after residualising on rev1/rev3), no home-session concentration (cell 46); posterior fell below its prior; rival controlled (14, 46), conditional split run (46).
- drop H14: three search cells (32, 33, 34) plus the frozen F9 (CONFIRM-FAIL: C1 +0.0168 t 2.45 and C2 +0.0094 t 1.33 are under the 0.02 bar, only C3 +0.0451 passes); response-artifact rival controlled (cell 33), fold conditional reported; posterior 0.07 is below its prior 0.20. The IC (h1 +0.022 pooled) is real but small and fold-uneven; recorded in REPORT.md as a COMBINE-only lead, not a library feature.
