# cell_09 — RESULT (Phase 3 VAL check, H5; rule: cells/cell_09_rule.md)

> **VAL_NOTE (TARGET.md):** "Two reasons VAL is weak evidence. (1) BTC VAL was crossed twice by earlier work (both
> pre-registered) and overlaps a spent pooled row of an earlier BTC seasonality EDA: SOFT-clean for BTC; clean for the other
> nine coins as far as this file knows. (2) VAL may be a DIFFERENT REGIME from TRAIN: from 2023-04 BTC's 1-minute trade counts
> fell ~8x (cause not established). A lead about trade counts or volume can fail VAL for structural reasons."

**Branch fired: SUPPORTED.** Deciding number: pooled normal-score 6h->next-6h IC on VAL = **-0.0627, NW se 0.0220, z = -2.85**
(< -1.645), 251 day clusters (>= 150). Pearson -0.0175 (z -0.63): same sign, no conflict (but much weaker: the effect is in the
ranks, not in the tail-weighted means). Without BTC (VAL_NOTE 1): **-0.061, z -2.77** — the result does not rest on the
soft-clean coin.
**Weight applied: 10 (capped from 12.8, guard b).** H5 posterior: odds 6.39 x 10 = 63.9 -> **0.985** -> state **HIGH-VAL**.
This is a VAL pass, NOT out-of-sample proof (VAL_NOTE; and the effect is below costs, next paragraph).

Descriptive: per coin all 10 negative (-0.022 ADA .. -0.110 BCH); halves -0.044 / -0.084; decay lag 12h +0.026, 18h -0.060,
24h -0.010 (the 24h echo seen on CONFIRM is absent here). Cost line: VAL median 6h sd 156 bp -> implied 1-sd move 9.8 bp vs
the 19.8 bp median round trip: **below costs**; next block after the bottom decile +17.0 bp, after the top decile -3.6 bp.
Table `tables/cell_09_h5_val.csv`, `cell_09_h5_val_primary.csv`; plot `plots/cell_09_h5_val_6h_reversal.png`.
