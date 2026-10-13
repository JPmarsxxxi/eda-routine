# REPORT — 2026-10-06_crypto-101alphas-b2 (EDA routine v3.2, unattended)

**Mode B, one item:** INBOX.md §B entry 2, Kakushadze (2015) *101 Formulaic Alphas*, second batch: #30, #35, #38, #53, #54
(TARGET.md), verbatim, on Binance UTC daily OHLCV, predicting next-day primary `price` returns across 10 coins. Picked to be
scale-free across coins. Claim per alpha (`neutral` version): mean daily cross-sectional rank IC >= 0.02 (MIN_USEFUL_IC) in
the paper's direction. **Supported = real, not tradeable**: cost never decided a branch (RUNBOOK v3.2).
**Stop: S4**, slices exhausted, after 20 cells (17 tests, 3 redirects). **VAL not opened** (nothing reached HIGH-CONFIRM).
**gate.py: PASS.** EDA only: no signal construction, no PnL; every bp figure below is a top-half-minus-bottom-half descriptive.

## Belief table

| hyp | what | prior -> posterior | evidence chain (cell: slice branch weight) | final state |
|---|---|---|---|---|
| H1 | #30 volume-scaled 3-day streak fade | 0.17 -> **0.850** | 12: C1 sup 5.10 · 13: C2 sup 5.41 · 14: C3 inc · 20: EXPLORE inc | OPEN (all slices used) |
| H6 | -1 x #54, closing strength continues (child of H5) | 0.15 -> **0.490** | born C1 (cell_08) · 09: C2 sup 5.44 · 10: C3 inc · 11: EXPLORE inc | OPEN (all slices used) |
| H2 | #35 high own-volume, low own-price/return | 0.17 -> 0.170 | 01: C1 inc · 02: C2 inc · 03: C3 inc · 19: EXPLORE inc | OPEN (all slices used) |
| H5 | #54 close location x (open/close)^5, reversal | 0.17 -> 0.044 | 07: C1 **ref, opposite sign significant** 0.223 · 08 redirect -> H6 | LOW |
| H3 | #38 top of 10-day range and up today, short | 0.17 -> 0.038 | 04: C1 inc · 05: C2 ref 0.192 · 06 redirect (no child) | LOW |
| H4 | #53 fade 9-day change in close location | 0.15 -> 0.032 | 15: C1 inc · 16: C2 inc · 17: C3 ref 0.189 · 18 redirect (no child) | LOW |

Weights come from a simulation whose noise was MEASURED (EXPLORE day-permutation nulls, `tables/power.csv`, D10): at the
minimum useful IC, power is only 0.21-0.29 per slice, so a supported fold is worth ~4-6x and a refuted one ~0.19-0.27x. Most
cells are inconclusive by design: the folds can see an IC of ~0.04-0.05, not 0.02.

## Fold table (decay-first shape): mean daily rank IC (t), branch

| hyp | EXPLORE 2019-20 | C1 2020-21 | C2 2021-22 | C3 2022-23 | VAL |
|---|---|---|---|---|---|
| H1 #30 | -0.007 (-0.30) inc | **+0.037 (1.73) sup** | **+0.048 (2.29) sup** | +0.001 (0.07) inc | not opened |
| H6 -#54 | +0.009 (0.39) inc | (born: +0.052, 2.44) | **+0.057 (2.35) sup** | +0.023 (1.01) inc | not opened |
| H2 #35 | +0.010 (0.39) inc | +0.010 (0.52) inc | -0.009 (-0.46) inc | +0.003 (0.14) inc | — |
| H5 #54 | — | -0.052 (-2.44) **ref** | — | — | — |
| H3 #38 | — | +0.019 (0.88) inc | -0.019 (-0.97) ref | — | — |
| H4 #53 | — | +0.010 (0.50) inc | -0.004 (-0.19) inc | -0.029 (-1.39) ref | — |

**Both survivors are 2020-22 effects that fade in C3.** H1 is supported on C1 and C2 and flat on C3 (+0.001) and EXPLORE.
H6 is supported on C2, weaker on C3, and on EXPLORE its two halves point in opposite directions (+0.096, t 2.8, then -0.078,
t -3.1). C3 is also the first fold where 7 coins' response is the FTMO mid rather than the Binance print the signal uses, so
a trade-print effect at the 00:00 boundary would fade there for a mechanical reason; this run cannot separate the two.
**On v3.2's fold rule:** H1 ended C1+C2 at 0.8497, a hair under the 0.85 HIGH bar, so the rule did not change its state in
this run. Had it crossed, v3.1 would have sent it to VAL without C3; v3.2 would not — and C3 is exactly where its effect
vanished (+0.001).

## Cost line (SIGNALS.md; D11)

Median-coin round trip 45 bp incl. one 8.2 bp rollover night. H1: spread +20 / +22 bp/day on its supported folds, -11 on C3,
turnover 0.24/day -> cost 34 bp/day. H6: +28 bp/day on C2, turnover 0.48/day -> cost 52 bp/day. **Both COMBINE-ONLY.**
They are mildly NEGATIVELY correlated with each other (signal values -0.12, daily IC series -0.12, TRAIN only), and H1 is
market-neutral (corr with the panel return -0.01) while H6 leans on the market day (+0.31). That pair is the input a
combination stage would look at; this routine does not combine them.

## K (for downstream DSR deflation)

**K = 20 Phase-2 looks** (17 slice openings + 3 redirect re-reads of already-opened slices), each with ~7 pre-registered
descriptive statistics (upper bound ~160 numbers seen). Phase 0: 7 profile sections and 5 x 40 day-permutation nulls on
EXPLORE (no alpha related to a forward return). VAL: 0 looks. Deflate against K >= 20.

## 1b findings (one per hypothesis that moved off its prior)

- **H1 (#30).** Daily rank IC +0.037 (C1) and +0.048 (C2), each over 0.02 with t >= 1.645; flat on C3 and EXPLORE. Net of
  1-day reversal it keeps +0.034 / +0.042, so it is not the reversal twin; it correlates +0.22 with the volume trend. Does NOT
  show: persistence after 2022-03, a standalone edge (20-22 bp/day vs 34 bp/day cost), or anything on VAL.
- **H6 (-#54, a redirect child, never more than its evidence).** Rank IC +0.057 on C2 (t 2.35, spread +28 bp/day), born on
  C1 (+0.052, not counted). Inconclusive on C3 and EXPLORE, with the EXPLORE halves opposite. Sign is the OPPOSITE of the
  paper's: closing strength at 00:00 UTC continued rather than reversed in 2020-22.
- **H5 (#54 as published).** Refuted on C1 with the opposite sign significant (-0.052, t -2.44). LOW.
- **H3 (#38).** Refuted on C2 (-0.019). Phase 0 had flagged it as an impostor of 1-day reversal (rho 0.86); on C2 that
  reversal itself went the wrong way (-0.036), and the part of #38 orthogonal to it pointed the paper's way (+0.035, t 1.93):
  recorded as a lead, not spawned (INBOX_PROPOSALS.md).
- **H4 (#53).** Refuted on C3 (-0.029); flat on C1/C2. The opposite sign lives in late C3 only. LOW.
- **H2 (#35)** did not move: ~0 on every slice. Its raw (own-return) version is positive (+0.08/+0.10 on C1/C2, t 1.8/2.3)
  because the signal's cross-sectional mean is -0.65 to -0.69 correlated with the same-day panel return — that is the
  market's own daily reversal (an ALREADY TESTED topic), not #35's cross-sectional claim.

## Still open / leads

Still open, no slice left: H1 (0.85), H6 (0.49), H2 (0.17). They need a fresh slice; opening TEST is the user's call.
Leads (INBOX_PROPOSALS.md): #38 net of 1-day reversal; the C3 / FTMO-mid question for close-location signals.
Process: the `eda-v3-judge` agent was NOT run in this session (the operator does not spawn agents unasked); run it before
relying on this report. Operator disclosure: DECISIONS D1.

Files: DATA_CARD · SPLITS · DATA_PROFILE · OBSERVATIONS · BELIEFS · ATTEMPTS · DECISIONS · ACCESS_LOG · STOP_REASON ·
SIGNALS · INBOX_PROPOSALS · cells/ · plots/ · tables/ · code/.
