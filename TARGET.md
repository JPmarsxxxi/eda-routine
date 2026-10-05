# TARGET: what the next EDA run should look at

Edit this file, then set STATUS to READY and click "Run now" on the routine. The routine sets STATUS to
`DONE <run folder>` when finished, so a finished target is never re-run by accident.

DATA MUST BE PREPARED FIRST: `python C:\Users\User\eda-routine\prep_target.py <source> <name>` writes a copy that
STOPS at the end of VAL (TEST and sealed rows are never copied). Point DATA at that copy, never at the source.

STATUS: DONE C:\Users\User\eda-routine\runs\2026-09-28_btc-perp-various-free

NAME: btc-perp-various-free

SOURCE_MODE: E
            (Data-only. No inbox item. Every hypothesis this session tests must trace to a Phase 0 observation —
            RUNBOOK_v3.md Phase 1, mode E. Do not pull a claim from SSRN/Substack/a lens this run.)

DATA: C:\Users\User\eda-routine\data\btcusdt_perp_bundle_MANIFEST.md
      Read that manifest FIRST — it indexes seven prepared files (1m/30m/hourly perp klines, DVOL, historical
      half-spread, funding, and long/short-ratio + open-interest metrics), each in its own folder under
      C:\Users\User\eda-routine\data\ with its own CUT.json. NOT CLEANED (see manifest) — Phase 0 must do real
      characterisation work, not assume this is pre-cleaned the way btcusdt_spot_1m_clean was.

PROVENANCE: All seven files are BTCUSDT PERPETUAL FUTURES (Binance USD-M) or a BTC derivatives index (Deribit
            DVOL) — a DIFFERENT instrument from every earlier target (which used SPOT). Same underlying data
            arc #047 ("POKER LENS on BTC", alpha_log.md) loaded — see the manifest for exactly which files and
            why two of them needed custom prep instead of prep_target.py. Per-file venue/column/coverage detail
            is in the manifest table, not repeated here.

CLEANED?: NO. Raw VAL-cut copies only — see manifest for what Phase 0 needs to check itself (gaps, coverage
          starts, the 1m file's missing VAL window, the metrics file's overlap with an already-tested signal
          family).

TRAIN_END: 2023-03-19
VAL_START: 2023-03-25
VAL_END:   2023-11-30
VAL_NOTE:  Same VAL weaknesses as every other BTC target here: soft-clean (arc #047 crossed it twice, both
           pre-registered) and a different liquidity regime from TRAIN post-2023-04. Applies to whichever of the
           seven files a hypothesis ends up using — check per-file VAL coverage in the manifest first, since
           btcusdt_perp_1m has NONE.

HYPOTHESIS: (blank — mode E. Hypotheses come only from Phase 0 observations on this bundle, per RUNBOOK_v3.md.
            Do not write a claim here for this run.)

ALREADY TESTED (names only, do NOT pick these): BTC hour-of-day seasonality (the 21:00-23:00 UTC window); BTC flow-imbalance and
            positioning / crowd-positioning claims; BTC-dislocation propagation to other coins; short-horizon reversal after taker
            imbalance. (Topic names only, taken from the holdout file; no results. Edit freely.)
            NOTE for this run specifically: btcusdt_metrics_5m carries count_long_short_ratio and related
            positioning fields — the same signal family as the "flow-imbalance and positioning" line above.
            A Phase-0 observation on this file that turns into a hypothesis needs to say what it's doing
            differently from that already-tested ground, not just re-arrive at it.

PRE-APPROVED INSTALLS: any    (v3.2 default: whatever the claim needs, PyPI/conda-forge only, pinned, into
                              C:\Users\User\eda-routine\.venv, each validated before use - RUNBOOK_v3.md "INSTALLS AND
                              METHODS". Narrow it by listing packages, e.g. "pymc, arviz"; "none" forbids installs.)

ROUND-TRIP COST (bp): <blank — but NOT unknown this time: btc_hist_halfspread_hourly/ carries real hourly
                      half-spread in bp. Price cost from that series at the trade minute, per event, per
                      data-hygiene.md rule 3 — don't reduce it to one pooled number for this field.>

NOTES: Prepared 2026-09-28 for a free-form, data-driven run (mode E) — see DESIGN_v3.md / RUNBOOK_v3.md. This is a
       genuinely different instrument (perp, not spot) from every prior target, so do not assume any of the
       btcusdt_spot_1m_clean findings (CLEANING_LOG.md) transfer here. Full per-file detail, known gaps, and
       exactly how each file was prepared: C:\Users\User\eda-routine\data\btcusdt_perp_bundle_MANIFEST.md.
       Other prepared copies sit in data\ (btcusdtperp_5m, btcusdtperp_1m, btcusdt_spot_1m, btcusdt_spot_monthly,
       btcusdt_spot_1m_clean). They are RAW/uncleaned or a different target already run: do not use them here.
       NAMING TRAP: btcusdtperp_1m (no underscore between usdt/perp; pre-existing, NOT part of this bundle) is
       easy to confuse with btcusdt_perp_1m (underscored; IS part of this bundle, see manifest). Checked both —
       the pre-existing one is also TRAIN-only (2020-01 to 2023-03-19, a different, later-starting source file
       than this bundle's), so it adds nothing this bundle doesn't already have; not worth pulling in.
