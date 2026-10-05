# DECISIONS — unattended run; every question a human would have been asked, with the conservative default taken

Run folder: runs/2026-10-05_crypto-validated-1h. Started 2026-10-05 12:22:52 UTC. Runbook: RUNBOOK_v3.md (v3.1).

## D1 — Source mode
TARGET.md `SOURCE_MODE: E` is set explicitly -> mode E used exactly as given; autopick NOT run (it fires only on a
blank line). MODES.md counts read for the record: A 0, B 0, C 0, D 0, E 1. No inbox item consumed (mode E needs none).

## D2 — Cloud path mapping
Every `C:\Users\User\<x>` in the runbook mapped to `/home/user/<x>`. Venv at /home/user/eda-routine/.venv with only the
PRE-APPROVED INSTALLS: pandas 3.0.6, pyarrow 25.0.1, numpy 2.4.6, scipy 1.17.1, statsmodels 0.15.0, matplotlib 3.11.2
(Python 3.11.15).

## D3 — Holdout guard
No eda_guard.py exists in this checkout (TARGET.md NOTES). Implemented as `code/guard.py: load()`: every parquet read
goes through it; it asserts max(time column from MANIFEST.csv) <= 2023-11-30 23:59:59 UTC and appends a row to
ACCESS_LOG.md. A failure would raise -> STOPPED.md. Slice cutting is done after the load, in `code/panel.py`.

## D4 — Plot styling (cellplot.py needs seaborn/plotly, which are not pre-approved)
Question: install seaborn/plotly so `cellplot` can be imported? Conservative default: NO install. Plots are drawn
with matplotlib only, using cellplot.py's palette constants copied verbatim (PAL, GRAY, DIV, SURFACE, GRID), saved as
plots/00_<slug>.png (Phase 0) and plots/cell_NN_<slug>.png (cells). No notebook: each cell is a script in code/.

## D5 — Returns never cross new_source=True
Hourly return at bar t is valid only if bar t-1h exists and bar t has new_source=False. A daily (or 72h) return is
valid only if both end bars exist and NO bar inside the window has new_source=True. Because FTMO rows miss fixed
Saturday hours and the first bar after each such gap is flagged, FTMO coins (C2, C3, VAL) lose most Saturday-ending
windows. Conservative default: drop them (never patch); stated in every cell that uses C2/C3.

## D6 — Day convention
Decision time tau = 00:00 UTC. "Day d close" = `price` of the bar stamped d 23:00 (value at d+1 00:00). Every
explanatory series is lagged to be knowable at or before tau using MANIFEST.csv `knowable` (data-hygiene rule 4);
the per-family lag is written in DATA_CARD.md.

## D7 — Costs
TARGET.md ROUND-TRIP COST (bp, 24h hold incl. one rollover night): BTC 18.9, ETH 25.4, LTC 36.5, ADA/DOGE/DOT/BNB/SOL
~46 (midpoint of "~45-47"), BCH 65.5, XRP 68.6. 72h hold = 24h figure + 2 x 8.2. Not the `ftmo_spread_rt_bp` column.
