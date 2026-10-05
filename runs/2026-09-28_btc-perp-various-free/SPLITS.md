# SPLITS — declared from coverage counts only, before any forward return was measured

Written after `scripts/cell_00b_splits.py` (usable-row census in `tables/00b_split_census.csv`; `eda_guard.declare_split`
records in `HYGIENE.jsonl`). At this point no return, change or distribution of any column had been computed, only
non-null counts per slice. **This split is never revised after a forward return is measured.**

| slice | range (UTC) | used for |
|---|---|---|
| EXPLORE | TRAIN start .. **2021-12-31 23:59** | Phase 0, every observation, every data-born hypothesis's development |
| CONFIRM | **2022-01-01 00:00** .. 2023-03-19 23:59 | opened ONCE per data-born hypothesis, rule written first |
| embargo | 2023-03-20 .. 2023-03-24 | nothing |
| VAL | 2023-03-25 .. 2023-11-30 | once per session, Phase 3, only for HIGH-CONFIRM hypotheses |

Boundary rule for forward windows: an EXPLORE event whose forward window would end after 2021-12-31 23:59 is dropped from
EXPLORE (not truncated). A CONFIRM event whose window would cross TRAIN_END is dropped too. No window straddles two slices.

## Why 2021-12-31 (usable rows, EXPLORE / CONFIRM)

| file (key column) | 2021-06-30 | **2021-12-31 (chosen)** | 2022-06-30 |
|---|---|---|---|
| spot hourly (close) | 21,877 / 15,000 | **26,245 / 10,632** | 30,589 / 6,288 |
| spot 30m (close) | — | **76,423 / 21,264** | 85,111 / 12,576 |
| DVOL (close) | 2,184 / 15,048 | **6,600 / 10,632** | 10,944 / 6,288 |
| half-spread | 16,697 / 4,886 | **18,137 / 3,446** | 19,402 / 2,181 |
| funding | 1,641 / 1,881 | **2,193 / 1,329** | 2,736 / 786 |
| metrics (c, OI) | 86,862 / 180,477 | **139,755 / 127,584** | 191,883 / 75,456 |

The derivatives-side series (metrics from 2020-09, DVOL from 2021-04) are what a data-born hypothesis on this bundle will
most likely need. 2021-12-31 is the only candidate that gives both of them a usable EXPLORE (DVOL 6,600 h ≈ 9 months,
metrics ≈ 16 months) AND a CONFIRM at least as large for DVOL (14.5 months) and near-equal for metrics. 2021-06-30 leaves DVOL
3 months to explore on; 2022-06-30 leaves CONFIRM under 9 months for everything. Spot prices get a long EXPLORE (2017-2021)
and 14.5 months of CONFIRM.

Known property of the chosen CONFIRM, stated before looking at it: 2022-01..2023-03 is one calendar block containing the
2022 bear market (LUNA May-22, FTX Nov-22). CONFIRM is a harder, different-regime test than a random block would be. That
is accepted, not tuned away.

**Half-spread coverage in CONFIRM is thin: 3,446 of ~10,600 hours (32%).** Cost priced at the trade hour will be missing for
most CONFIRM events. Rule, fixed now: cost statistics are reported only on events that have a same-hour half-spread row, with
the covered count stated. Missing is never filled.
