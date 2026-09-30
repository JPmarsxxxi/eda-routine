# DECISIONS — questions an attended run would have asked, with the conservative default taken

Unattended run (RUNBOOK_v3 UNATTENDED SUBSTITUTIONS). Every "decision I need from you" is written here with the default taken.

## D0. Mode selection
- TARGET.md `SOURCE_MODE: E` is set explicitly -> **mode E (Data)** used exactly as given. Autopick NOT run (it fires only on a
  blank line). MODES.md read for reference only (all counts 0). No inbox item consumed (INBOX.md is empty; mode E needs none).
- Exactly one mode this session. Every hypothesis must trace to an OBSERVATIONS.md number (EXPLORE).

## D1. Cloud path mapping
`C:\Users\User\<x>` -> `/home/user/<x>` everywhere (caller instruction). Run folder `runs/2026-09-30_crypto-panel-1h/`.

## D2. Guard
No eda_guard.py in this checkout (TARGET.md NOTES). Implemented as `code/guarded_load.py::load`: asserts max(time) <= VAL_END at
every load, logs to ACCESS_LOG.md. All 224 files verified in p0_00 (224 PASS, 5,685,039 rows = CUT.json).

## D3. Python environment
`/home/user/eda-routine/.venv`, only the PRE-APPROVED INSTALLS: matplotlib==3.11.2, numpy==2.4.6, pandas==3.0.6,
pyarrow==25.0.1, scipy==1.17.1, statsmodels==0.15.0 (Python 3.11.15).

## D4. Plotting convention
PROTOCOL 5.1 says plots go through `cellplot.py` (plotly/seaborn). seaborn and plotly are NOT pre-approved installs ->
conservative default: do not install them; use matplotlib only, with cellplot.py's palette constants copied verbatim
(`code/plotstyle.py`), one axis, <=4 series, takeaway titles. Plots in `plots/` (Phase 0: `plots/00_<slug>.png`; test cells:
`plots/cell_NN_<slug>.png`).

## D5. "One cell per turn" / "wait for confirmation"
PROTOCOL 1/4 and the finding-alphas CLAUDE.md step rule assume a live user. This is an unattended routine run; RUNBOOK_v3's
UNATTENDED SUBSTITUTIONS replace "announce and wait" with "write cell_NN_announce.md (and cell_NN_rule.md) BEFORE any code for
the cell exists, then proceed". Followed for every test cell. Each cell still runs alone, ends in a printed table + plot, and is
inspected before the next is announced.

## D6. Scope of Phase 0
TARGET.md NOTES: profile the PRIMARY TARGET panel (10 Binance spot coins, 1h) first; other families only for coverage,
knowability and alignment (p0_00 + DATA_CARD.md), not 224 separate studies.

## D7. Split
See SPLITS.md. Default: ~60/40 by coin-hours, quarter boundary, 7-day embargo >= longest horizon (168h).

## D8. Costs used for "smallest economically meaningful effect"
TARGET.md ROUND-TRIP COST: FTMO CFD, constant sample. Panel median ~ 19.8 bp round trip; + ~8.2 bp per rollover crossed.
Default: an effect is economically meaningful only if its gross move over the horizon could plausibly clear the panel's
median round-trip cost; power simulations are run at an effect size tied to that (stated per rule file).

## D9. Topics already tested (TARGET.md ALREADY TESTED) — excluded by construction
BTC hour-of-day (21-23 UTC); BTC flow-imbalance / positioning / crowd positioning (so no funding / long-short / taker-imbalance
hypotheses); BTC-dislocation propagation to other coins (so no BTC-leads-alts hypotheses); short-horizon reversal after taker
imbalance. Any Phase 0 observation that falls into one of these topics is logged but NOT turned into a hypothesis.
