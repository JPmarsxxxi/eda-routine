# REPORT — btc-perp-various-free (mode E: data only) — run 2026-09-28

**Source:** Mode E. Every hypothesis traces to a Phase 0 observation on EXPLORE (`OBSERVATIONS.md`). Slices (`SPLITS.md`): EXPLORE <= 2021-12-31; CONFIRM 2022-01-01..2023-03-19;
embargo 03-20..24; VAL 2023-03-25..2023-11-30 (VAL_NOTE: soft-clean VAL, different liquidity regime). Ten test cells, stop rule **S2** (see the caveat under "Stop").

**Data flag for the human:** `TARGET.md` PROVENANCE calls the price files "perp". `DATA_CARD.md` (identity check) shows they are Binance **SPOT**; only the `metrics` file carries perp `c`, OI and ratios.
Basis here = 1e4 x log(perp `c` / spot 30m close).

## Belief table

| id | hypothesis | prior -> posterior | evidence chain (slice) | state |
|---|---|---|---|---|
| H1 | funding-clock basis sawtooth | 0.60 -> **0.130** | born EXPLORE #1; cell_01 CONFIRM REFUTED (D 0.163 bp, t 2.18; weight 0.0303 capped to 0.1); cell_02 redirect (EXPLORE) B4 diffuse | OPEN |
| H2 | DVOL adds next-day RV info beyond trailing RV | 0.60 -> **0.992** | born EXPLORE #2; cell_05 CONFIRM SUPPORTED (partial +0.174; weight 12.2 capped to 10; -> 0.938); cell_10 VAL PASS (partial +0.2985, crit +0.1213; weight 8.28) | **HIGH-VAL** |
| H3 | basis level vs next-day RV beyond trailing RV | 0.35 -> **0.114** | born EXPLORE #4; cell_03 CONFIRM REFUTED (partial +0.0099; weight 0.240); cell_04 redirect (EXPLORE) B3 | OPEN |
| H4 | DVOL level vs next-24h spot return (fear premium) | 0.25 -> **0.183** | born EXPLORE #8; cell_08 CONFIRM REFUTED (Spearman +0.0194 < +0.025; weight 0.671); cell_09 redirect (EXPLORE) B1 lead | OPEN |
| H5 | hourly spot return reversal | 0.20 -> **0.714** | born EXPLORE #6; cell_06 CONFIRM SUPPORTED (Spearman -0.0640; weight 18.9 capped to 10) | OPEN |
| H6 | hourly basis change leans against next-hour spot return beyond r_t (child of H5) | 0.15 -> **0.638** | born EXPLORE #10; cell_07 CONFIRM SUPPORTED, thinly (partial -0.0188 vs crit -0.0168; weight 18.1 capped to 10) | OPEN |

Priors are anchored in `BELIEFS.md`. Weights follow the rule files, written before each cell; three of the four supports/refutes hit the 10x cap (guard b) and are marked as such.

## What moved, per hypothesis (decay-first shape, then cost)

- **H2 (the one HIGH-VAL).** Partial Spearman by slice: EXPLORE 0.17; CONFIRM quarters 0.33, 0.38, 0.22, 0.31, 0.18; VAL 0.32 (2023Q2 hours) / 0.28 (2023H2 hours). No fade; the last CONFIRM quarter is the lowest, VAL is high again.
  Controls for signed return and an EWMA-of-squared-returns (HAR) rival leave it unchanged (0.176/0.180 in CONFIRM; 0.296/0.322 in VAL). **What this says:** DVOL, an options-implied vol index, carries information on
  next-day realised vol beyond trailing windows. That is a known property of implied vol, so its value is that the data behaves as expected. It has no direction, so cost is N/A. VAL_NOTE applies: a pass on a soft-clean slice in a different liquidity regime, not proof of out-of-sample behaviour.
- **H5 (reversal, OPEN 0.714).** Spearman -0.064 in CONFIRM, negative in all five quarters (-0.066, -0.038, -0.044, -0.133, -0.056), unchanged with the 1% largest hours removed (-0.065). **But Pearson is +0.005**
  and the naive fade of each hour's sign loses 0.44 bp/hour gross over all 10,629 hours. On the 3,446 hours that have a half-spread row (32% coverage, not a random subset) the mean gross is +1.48 bp and net +1.27 bp (median round trip 0.17 bp;
  venue of `half_bp` unstated). A real, stable rank-order reversal, not shown to be monetisable.
- **H6 (OPEN 0.638, thin).** Partial -0.0188 passes the -0.0168 bar by 0.002. With r_{t-1} also controlled it is -0.0161 and with the 1% largest |d_basis| removed -0.0164 (both above the bar); the unpartialled Spearman is -0.0094; by quarter -0.012, -0.058, -0.013,
  +0.015, -0.013 (2022Q2 carries it, 2022Q4 has the wrong sign). Cost: on covered hours gross -0.39 bp, net -0.60 bp. Treat as a lead in H5's neighbourhood, not a finding.
- **H1 (OPEN 0.130).** Funding-clock jump minus placebo: EXPLORE +1.48 bp when funding > 0.03%, CONFIRM mean D 0.163 bp; by quarter 0.10, 0.34, 0.27, 0.09, 0.01: **decays**, and CONFIRM held almost no positive-funding settlements
  (9 of 1,328), so the regime that made the jump large did not occur. Two-leg cost median 0.34 bp on the covered 432 settlements (jump 0.08 bp is a quarter of it).
- **H3 (OPEN 0.114).** Partial +0.0099 vs EXPLORE 0.15; quarters alternate sign (-0.079, +0.079, +0.085, -0.058, +0.029). Not a regime, noise around zero. Direction-free, so cost N/A.
- **H4 (OPEN 0.183, weak refutation).** Pooled +0.0194 (SE 0.044), power only 0.363, so the refutation moved belief little (weight 0.671). By quarter +0.213, +0.094, +0.182, +0.062, -0.017: positive in four of five but the pooled value is ~0 (best quarter removed: -0.015).
  Terciles of next-24h return (bp): -2.3 / -42.8 / +7.9, not monotone. No cost line (level relation, not a signal).

## 1b findings (one per hypothesis that moved off its prior)

- **H2 1b finding:** DVOL level has a partial rank correlation of about +0.17 to +0.32 with next-24h log RV after trailing 24h/7d/30d RV, positive in every slice (EXPLORE, five CONFIRM quarters, two VAL segments); rivals (signed return, EWMA) do not remove it. Known-property confirmation, no trade, cost N/A.
- **H5 1b finding:** hourly spot return has a negative Spearman correlation (-0.064) with the next hour in CONFIRM, stable by quarter and by trimming; the size-weighted return shows none (Pearson +0.005). Cost line on covered hours: +1.27 bp net of a 0.17 bp median round trip, on 32% of hours; over all hours fading loses 0.44 bp gross.
- **H6 1b finding:** hourly basis change has a partial correlation of -0.019 with next-hour spot return after r_t, barely past the pre-committed bar and not robust to a second lag or trimming. Cost: net -0.60 bp on covered hours.
- **H1, H3, H4 1b findings:** each moved down on a pre-committed refutation (0.60 -> 0.130, 0.35 -> 0.114, 0.25 -> 0.183); the refuting numbers and their quarter shapes are in the table above. These are reported as evidence moves, not kills.

## K (look count for downstream DSR deflation)

Scored confirmatory looks: **7** (six CONFIRM openings, one per H1..H6, plus one VAL opening for H2). Every CONFIRM and VAL slice was opened once per hypothesis and once for VAL. Additional reported-but-unscored looks on those slices
(rival controls, quarter and tercile splits, cost lines) are itemised in `ATTEMPTS.md` rows 6-15. EXPLORE looks (Phase 0 distributions for 17 columns, ACF of 17 series, a 15-column Spearman matrix, a 56-pair lead-lag screen, partial-RV screens,
funding/basis profiles, and the redirect cells 02/04/09) are itemised in rows 3, 4, 9, 14 and are birth-slice looks, not confirmations. Note that H5, H6 and H2 share CONFIRM hours, so their supports are not independent evidence.

## Stop (S2, with a stated caveat)

`STOP_REASON.md`: S2, open 5, low 0, high 1. Ten of the 30 test cells and under 3 hours of wall clock by the system clock (first access 20:37, close about 22:30; the clock advanced slowly during the run) were used. **This is not a "beliefs have settled by evidence" stop:** H1, H3, H4, H5 and H6 have each spent the one CONFIRM opening a data-born
hypothesis gets, and VAL is opened only for HIGH-CONFIRM (D13). Their best available test is worth 0 pp, so the pick step had nothing eligible. Five hypotheses ending OPEN, two of them (H5, H6) supported but below 0.85, is a fact about the funnel and the slice sizes.

## Still open, leads, and notes

- Still OPEN: H1 0.130, H3 0.114, H4 0.183, H5 0.714, H6 0.638. A fresh slice (later data) is the only way to move H5 and H6.
- Leads, not hypotheses: decay of the funding-clock jump; fading of the basis-level vs RV link; extreme-hour continuation in the hourly reversal (Pearson +0.005 vs Spearman -0.064); half-spread coverage regime; relative DVOL vs next-24h return (EXPLORE 0.109, z 1.54); H4's 4-of-5 positive CONFIRM quarters against a ~0 pooled value.
- Not chased: #3 (half_bp is a volatility impostor), #11 and #12 (descriptive), and #5/#7/#9, which belong to the ALREADY-TESTED families (positioning, time-of-day, flow imbalance).
- Process notes: the B3/B4/B1 redirects (cells 02, 04, 09) spawned nothing (D11, D12); the RUNBOOK reads a redirect's finding as captured "as a NEW spawned hypothesis", and these were pre-committed as leads when the branch found no localised effect or an era-conditional one. H6 was spawned as a child of H5 by the CONFIRM cell (born on EXPLORE #10).
- Proposals for a future session are in `INBOX_PROPOSALS.md`. Nothing was written to `INBOX.md`, `alpha_log.md`, live strategies, MT5, raw data or `backtest_engine2\data\`.

## Judge verdict

(eda-v3-judge, verbatim)

```
VERDICT: PASS
REASON: All six checklists pass. The S2 stop is legitimate: H1/H3/H4/H5/H6 have each spent their single CONFIRM opening and no VAL eligibility exists for the non-HIGH hypotheses, resulting in E|shift|=0.0 pp for all OPEN hypotheses. Redirect cells 02/04/09 correctly fired pre-committed branches and recorded findings as leads (not spawned hypotheses), which is appropriate because they require fresh slices unavailable in the funnel. H6 is genuinely new (tests d_basis vs r_{t+1} given r_t, distinct from H5's r_t vs r_{t+1}) with own rule file. All evidence weights computed correctly from stated power/alpha simulations and capped appropriately; no double-counting of H6 evidence against H5's CONFIRM slice because the partial controls for r_t. Mode E used exclusively, all hypotheses traceable to Phase 0 observations, CONFIRM opened once per hypothesis with no re-testing on birth slice, VAL opened only for H2 (the only HIGH-CONFIRM).
```
