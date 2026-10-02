# REPORT — EDA v3, crypto-panel-1h (run 2026-09-30_crypto-panel-1h)

**Source mode E (Data)**, set explicitly in TARGET.md (no autopick, no inbox item). Data: crypto_panel_2026-09-30, primary target
= Binance spot 1h trade-print bars for 10 coins (open-stamped, knowable at open + 1h). Splits (SPLITS.md, declared from coverage
before any return): EXPLORE 2017-08-17..2021-06-30 · CONFIRM 2021-07-08..2023-03-19 · VAL 2023-03-25..2023-11-30 (opened once).
Stop: **S2** (STOP_REASON.md) after 8 loop cells + 1 VAL cell; guard PASS on every load (ACCESS_LOG.md). EDA only: no signal,
no PnL. Every "supported" below is a statement about a rank correlation, not about a tradeable edge.

## Belief table (prior -> posterior, evidence chain with slice, final state)

| id | hypothesis (short) | prior | posterior | evidence chain (cell: slice, branch, weight) | final state |
|---|---|---|---|---|---|
| H1 | daily time-series reversal | 0.39 | 0.227 | cell_06 CONFIRM refuted (IC -0.047, z -1.38, power 0.56) x0.46; cell_07 EXPLORE redirect (x1) | OPEN (no slice left) |
| H2 | reversal stronger after panel volume-shock days | 0.35 | 0.708 | cell_08 CONFIRM supported (diff IC -0.202, z -2.14) x4.5 | OPEN (no slice left) |
| H3 | same-hour-yesterday 1h reversal (NO-STORY) | 0.28 | 0.795 | cell_03 CONFIRM supported (lag-24 IC -0.035, z -4.38) x10 capped | OPEN, NO-STORY lead |
| H4 | high-volume relative winners continue | 0.21 | 0.026 | cell_04 CONFIRM refuted (FM b3 -14.5 bp, z -2.32, opposite sign) x0.1 capped; cell_05 EXPLORE redirect: absent everywhere (x1) | LOW |
| H5 | intraday 6h-block reversal | 0.39 | 0.985 | cell_01 CONFIRM supported (IC -0.032, z -1.89) x10 capped -> 0.865; cell_09 VAL supported (IC -0.063, z -2.85) x10 capped | HIGH-VAL |
| H6 | 6h reversal stronger in high trailing vol (child of H5) | 0.40 | 0.870 | cell_02 EXPLORE supported (diff IC -0.081, z -2.48) x10 capped | HIGH-EXPLORE (born on CONFIRM; no CONFIRM/VAL, D10) |
| H7 | crash-day rebound (child of H1, from redirect) | 0.42 | 0.42 | spawned by cell_07; not tested (its statistic already seen on CONFIRM, D11) | OPEN (untested lead) |

## Decay-first shape and cost line (everything that reached CONFIRM or VAL)
Costs: FTMO round trip BTC 6.6 .. LTC 36.5 bp, panel median 19.8 bp; + ~8.2 bp per rollover crossed.
- **H5 (6h reversal)** — decay (CONFIRM): 6h -0.032, 12h -0.024, 18h +0.024, 24h -0.054; (VAL): 6h -0.063, 12h +0.026, 18h -0.060,
  24h -0.010. Cost line: implied gross move per 1-sd block 7.3 bp (CONFIRM) / 9.8 bp (VAL) **vs 19.8 bp -> does not clear costs**.
  CONFIRM effect only in 2022-05..2023-03 (first half +0.004).
- **H3 (1h lag-24)** — IC by lag on CONFIRM: 1h -0.033, 2h -0.024, 12h -0.011, 23h -0.011, 24h -0.035, 25h -0.025, 48h +0.003.
  Cost line: ~4-5 bp per 1-sd hour **vs 6.6 bp at the cheapest coin -> uneconomic everywhere**.
- **H1 (daily reversal)** — CONFIRM 1d -0.047, 2d -0.025, 3d +0.043, 7d -0.030. Cost line: 21 bp per 1-sd day vs 28 bp (round
  trip + rollover) -> below costs on average; after bottom-decile days +50 bp next day, after top-decile -28 bp (gross).
- **H2 (volume-shock-conditioned daily reversal)** — IC on top-tercile volume-shock days -0.184 vs +0.027 / -0.005 in the other
  terciles; at 450 bp daily sd that is ~80 bp per 1-sd day on those days vs 28 bp -> **the one effect whose size is above the
  cost line**, but OPEN (0.71), one slice only, and VAL_NOTE (2) warns volume-based leads can fail VAL for structural reasons.
- **H4** — refuted (opposite sign); no cost line.

## K (for downstream DSR deflation)
**K = 18 looks** (ATTEMPTS.md): 9 Phase 0 EXPLORE looks, 5 CONFIRM openings, 3 EXPLORE test/redirect cells, 1 VAL opening. With the
pre-registered descriptives counted as statistics seen, ~120. Deflate against K >= 18, upper bound ~120.

## 1b findings (one per hypothesis that moved off its prior)
- **1b finding — H5.** Claim: consecutive 6h block returns of the 10 Binance spot coins are negatively rank-correlated. Rule:
  z < -1.645 one-sided, pre-registered. CONFIRM IC -0.032 (z -1.89); VAL IC -0.063 (z -2.85; ex-BTC -0.061). Does NOT show: an
  economic effect (1-sd block implies 7-10 bp vs 19.8 bp cost), stability (CONFIRM first half +0.004), or anything about the
  tail-weighted mean (Pearson ICs -0.014 / -0.018, not significant). VAL is weak evidence (VAL_NOTE). Status: HIGH-VAL as a
  data-nature fact; not a strategy.
- **1b finding — H6.** Claim: the 6h reversal is stronger when trailing 7-day panel volatility is high. EXPLORE diff IC -0.081
  (z -2.48); terciles +0.026 / -0.050 / -0.063. Born on CONFIRM's half-split, so tested on EXPLORE only; never on CONFIRM or VAL.
- **1b finding — H3 (NO-STORY lead, never more than a lead).** 1h lag-24 IC -0.035 on CONFIRM (z -4.4), all 10 coins negative,
  but lag 25 is also -0.025 (a smeared "about a day later" reversal) and it cannot pay the cheapest coin's cost. No mechanism.
- **1b finding — H2.** Day->next-day IC on top-tercile panel volume-shock days is -0.20 lower than on other days on CONFIRM (z -2.14),
  and -0.15 lower (z -2.16) after removing the 10% largest moves. One slice only; OPEN at 0.71.
- **1b finding — H1.** A general daily reversal did not pass CONFIRM (IC -0.047, z -1.38, power only 0.56): weak refutation.
  Redirect: on EXPLORE the reversal is confined to extreme days (IC -0.30 vs -0.02) and is a rebound after crashes (+308 bp next
  day after extreme down days, +43 bp after extreme up days).
- **1b finding — H4.** Refuted on CONFIRM with the opposite sign (b3 -14.5 bp, z -2.32); redirect found it absent on EXPLORE
  (+3.6 bp, z 0.40) and the tercile sort disagrees with the regression on the same data: no consistent volume x relative-return
  interaction exists in this panel.

## Still open
H1 (0.227), H2 (0.708), H3 (0.795, NO-STORY), H7 (0.42, untested). None can be tested again inside TRAIN+VAL under the funnel;
they need a fresh slice (TEST is the user's decision, HOLDOUT_RULES rule 3). H6 (HIGH-EXPLORE) likewise.

## Leads (not chased, or NO-STORY — leads only, not findings)
- H3 (NO-STORY): same-hour-yesterday 1h reversal; uneconomic.
- H7: crash-day rebound (child of H1); strongest story, but survivorship-biased panel (no LUNA/FTT) and a few days carry it.
- Calm-market 6h continuation (cell_02 low-vol tercile IC +0.026, z 1.3) — not significant.
- Hourly lag-1/2 reversal and relative 1h reversal (OBS #4, #8) — sits next to the ALREADY TESTED taker-imbalance reversal topic
  and cannot clear 1h costs.
- DOGE trends at 24-168 h (OBS #6: VR 1.19-1.27) while every other coin mean-reverts — single-coin, meme-driven, not chased.
- Data-card discrepancy: zero-gap rate 0.16-0.32 on EXPLORE vs TARGET's "0.3-0.6" (OBS #15) — worth correcting in the card.
- Other families (funding, perp metrics, onchain, macro) were profiled for coverage/knowability only (DATA_CARD.md); positioning
  data is an ALREADY TESTED topic, onchain cm_* and defi are not point-in-time.

## Process notes
- Judge: RUNBOOK_v3 asks for the `eda-v3-judge` agent after gate.py. This run had no agent-spawning tool, so the judge was NOT run;
  a human review should run it (`.claude/agents/eda-v3-judge.md`) before relying on this report.
- Deviations/defaults: DECISIONS.md D4 (matplotlib instead of cellplot's seaborn/plotly, not pre-approved), D10 (CONFIRM-born
  children tested on EXPLORE, no VAL), D11 (no CONFIRM for a child whose statistic CONFIRM already showed), D12 (VAL opened once).
- Weights: every supported branch hit the 10x cap except H2 (4.5); the binary "z < -1.645" rules reward significance, not size —
  H5 passed twice at an effect below its own economic threshold. Future rule files should put the size threshold in the rule.
