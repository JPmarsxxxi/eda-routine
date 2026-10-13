# REPORT — 2026-10-05_crypto-101alphas (EDA routine v3.1, unattended)

**Mode B, one item:** INBOX.md §B `1601.00991v3.pdf`, Kakushadze (2015) *101 Formulaic Alphas*, Appendix A.1. The five alphas TARGET.md
named (#101, #42, #2, #6, #4), verbatim, on Binance UTC daily OHLCV, predicting next-day primary `price` returns, 10 coins.
Paper sample 2010-2013 US equities (no ⚑). One statistic for every test: the next-day return of the top half of coins by the
alpha minus the bottom half (bp/day, NW(5) SE). **Supported** needs >= 20 bp/day AND t >= 1.645 (DECISIONS D7).
**Stop: S2** (three picks in a row worth <= 3 pp; STOP_REASON.md). **gate.py: PASS** (run after this file was written).

## Belief table

| hyp | what | prior -> posterior | evidence chain (cell: slice branch weight) | final state |
|---|---|---|---|---|
| H1 | #101 (close-open)/(high-low+.001), momentum | 0.16 -> **0.852** | 01: C1 supported 10.0 (capped; overstated, D14) · 02: EXPLORE inconclusive 1 · 08: C2 supported 3.311 · 28: **VAL refuted** 0.914 | HIGH-CONFIRM (VAL failed) |
| H2 | #42 rank(vwap-close)/rank(vwap+close), delay-0 reversal | 0.11 -> 0.035 | 03: EXPLORE refuted 0.569 · 04 redirect · 19: C1 inconclusive · 20: C2 inconclusive · 21: C3 refuted 0.51 · 22 redirect -> H7 | LOW |
| H3 | #2 -corr(rank dlog vol, rank (c-o)/o, 6) | 0.11 -> 0.036 | 05: EXPLORE refuted 0.569 · 06 redirect -> H6 · 23: C1 inconclusive · 24: C2 refuted 0.524 · 25 redirect | LOW |
| H4 | #6 -corr(open, volume, 10) | 0.11 -> 0.079 | 07: EXPLORE inconclusive · 10: C1 refuted 0.886 (not the top pick, D16) · 11 redirect · 14: C2 inconclusive · 15: C3 refuted 0.888 · 16 redirect | OPEN (all slices used) |
| H5 | #4 -ts_rank(rank(low), 9) | 0.09 -> 0.090 | 26: C1 inconclusive (92 days) · 27: C2 inconclusive (84 days) | OPEN (C3, EXPLORE left, ~worthless) |
| H6 | child of H3: +corr(raw dlog vol, raw (c-o)/o, 6) | 0.14 -> 0.042 | 09: C1 inconclusive · 12: C2 refuted 0.524 · 13 redirect · 17: C3 refuted 0.51 · 18 redirect | LOW |
| H7 | child of H2: -#42 over 2 days | 0.09 -> 0.09 | born C3 cell_22; seen_on EXPLORE, C1, C2 (D18): no TRAIN slice left | OPEN (lead, needs a fresh slice) |

## Fold table (decay-first shape): mean spread bp/day (t), branch

| hyp | EXPLORE 2019-20 | C1 2020-21 | C2 2021-22 | C3 2022-23 | VAL 2023 |
|---|---|---|---|---|---|
| H1 #101 | +8.2 (0.75) inc | **+56.8 (1.74) sup** | **+33.1 (3.07) sup** | not opened (HIGH-CONFIRM is not pickable) | +4.7 (0.53) **ref** |
| H2 #42 | -6.1 (-0.47) ref | +32.8 (1.13) inc | -0.4 (-0.03) inc | -28.8 (-2.25) ref | — |
| H3 #2 | -1.0 (-0.10) ref | -5.0 (-0.18) inc | -1.8 (-0.18) ref | — | — |
| H4 #6 | +7.6 (0.74) inc | -32.7 (-1.21) ref | +6.8 (0.54) inc | -10.5 (-1.09) ref | — |
| H5 #4 | — | -4.7 (-0.05) inc | -2.3 (-0.04) inc | — | — |
| H6 (child) | born here (+29.5, t 3.06) | -19.0 (-0.67) inc | -6.5 (-0.53) ref | +3.7 (0.38) ref | — |

**H1's shape is a regime story, not a confirmed alpha:** strong only in Jun 2020 - Mar 2022 (C1 carried by 2021's alt-season
tail days: +120 bp/day in Jan-May 2021, rank IC ~0), weak in 2019-20 (+8) and gone in VAL (+4.7, IC -0.03). Its HIGH-CONFIRM
label rests on pre-registered weights whose noise assumptions were wrong: cell_01's 10.0 assumed ~4x too little noise (honest
~3.2), while cell_08 (3.311, honest ~10 capped) and the VAL rule (0.914, honest ~0.47) assumed too much. Correcting the two
that flatter H1 gives ~0.49; correcting all three gives ~0.74. **OPEN either way, not HIGH.** It never opened C3 — the first fold where the response (FTMO mid) is not the same print as the Binance
signal (Obs 3) — because HIGH-CONFIRM is not pickable.

## Cost line (anything that reached HIGH or VAL: H1)

#101's halves turn over almost completely every day: ~2.0 units of one leg traded per day (code/cost_line_h1.py). At TARGET.md
round-trip costs (BTC 18.9 ... XRP 68.6 bp, 24h hold incl. one rollover night) that is **~42-46 bp/day**, against gross
spreads of +8 (EXPLORE), +57 (C1), +33 (C2), +5 (VAL) bp/day. Net of cost: about **-35, +11, -9, -42 bp/day**. Only the
noisiest fold covers costs. DECISIONS D7's 20 bp/day bar assumed a 4.5-day hold, so it was **too lenient for #101**: the
real break-even for a daily-rebalanced #101 is ~45 bp/day.

## K

20 hypothesis slice openings (19 test + 1 VAL), 28 cells including 8 redirects (~140 pointer sorts), plus three null-noise
calibrations (C1, C2, C3) and the Phase-0 EXPLORE profile. Pass this K to any downstream DSR deflation (ATTEMPTS.md).

## 1b findings (one per hypothesis that moved off its prior)

- **H1 (#101):** Claim: range-scaled 1-day cross-sectional momentum continues the next day. Evidence: supported on C1 and C2,
  inconclusive on EXPLORE, refuted on VAL. Mechanism status: alive only as a 2020-22 regime effect, driven by tails. Net of
  ~45 bp/day turnover cost it is negative on 3 of 4 slices. Not a deployable alpha in this form. Weight problems: D14 and the
  cell_28 note.
- **H2 (#42):** The paper's delay-0 reversal sign is wrong here. The spread is negative on C3 (-28.8, IC -0.11, t -5.2) and
  the rank IC is negative on C2. The verbatim ranks mostly sort by price level (D2). Redirect -> H7.
- **H3 (#2):** No effect at any horizon, era or variant on EXPLORE or C2. The raw-value variant pointed the other way on
  EXPLORE (H6) and then failed on C2 and C3.
- **H4 (#6):** Refuted on C1 and C3, inconclusive elsewhere, nothing in three redirects. 0.079 OPEN only because the
  noisy-fold weights are weak.
- **H6 (child of H3):** The 3.06-t EXPLORE pointer did not hold on C1, C2 or C3. It was a selection artefact.

## Still open, and leads

- OPEN: H4 (no slice left), H5 (C3 and EXPLORE left, worth < 2 pp each), H7 (no TRAIN slice left). They need a fresh slice,
  and opening TEST is the user's call. H1 is HIGH-CONFIRM with a failed VAL (see above).
- **H5 (#4) cannot be tested in this universe:** the cross-sectional rank of `low` is a fixed price-level order (Obs 5), so
  #4 is all ties on 71-97% of days (code/signal_coverage.md).
- Leads, not findings: **H7** (-#42 over 2 days, C3 only, max of ~15 pointers). The IC vs spread disagreement of #42 on C2/C3
  (negative IC, flat-to-negative spread) points at the price-level rank inside #42. Same-hour-yesterday hourly reversal
  (Obs 6) is an ALREADY TESTED topic and was not chased.

## Self-applied judge checklist (the eda-v3-judge agent could not be spawned here; DECISIONS D10). A human should run it.

These items would fail or need a human look:
- **B1/B2:** cell_01's power simulation understated noise ~4x (D14), and VAL's overstated it ~4x. Both weights were applied as
  pre-registered.
- **Step 1:** cell_10 ran H4 on C1 when H6 on C2 was the top pick (D16).
- **Mid-run re-calibrations:** D14, D15 and D17 changed the power model for later cells. Each change was written before the
  next rule file, and each used a null that contains no alpha.
- **H7:** seen_on was set conservatively (D18).

Everything else was checked and holds: S2 is backed by three numbered consecutive picks; no NO-STORY entry exists; there is
one mode (B), set explicitly, so autopick did not run; every child came from a redirect cell and has its own rule files.
