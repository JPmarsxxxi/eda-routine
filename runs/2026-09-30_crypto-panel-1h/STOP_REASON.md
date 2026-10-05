rule: S2
open_count: 4
low_count: 1
high_count: 2
detail: S2 - picks #9, #10, #11 (after cell_08, tables/picks_9_11.txt) each found best expected shift 0.0 pp on every OPEN hypothesis (H1 0.227, H2 0.708, H3 0.795, H7 0.42): no admissible test remains (H1/H2/H3 spent their one CONFIRM opening and were born on EXPLORE; H7's statistic was already seen on CONFIRM, DECISIONS D11); S1 impossible with OPENs left; S3 not reached (8 test cells before stopping, ~45 min).

# STOP_REASON — notes (not parsed)

- Written after cell_08 and BEFORE the Phase 3 VAL cell (cell_09). The counts above are the BELIEFS.md state at the stop:
  OPEN H1, H2, H3, H7; LOW H4; HIGH H5 (HIGH-CONFIRM, queued for VAL), H6 (HIGH-EXPLORE, not VAL-eligible, D10).
- Why S2 and not a longer loop: every open hypothesis is data-born and has used the only slice it may be tested on; the next three
  picks are necessarily identical because nothing can change between them (no admissible cell exists to run). This is the
  "beliefs have settled" case in its limiting form: the best available test moves nothing because no test is available, not
  because tests were judged too weak. More looks at EXPLORE or CONFIRM for these ids would be the self-confirmation the funnel
  forbids.
- Not a stop on a single refutation: two refutations (H4 cell_04, H1 cell_06) were each followed by their mandatory redirect
  (cell_05, cell_07) and by further picks (cell_06 after cell_05; cell_08 after cell_07).
- If the VAL cell changes H5's state, the counts above are updated to the final BELIEFS.md state (gate.py compares against the
  final file) and the change is noted here.
- After cell_09 (VAL): H5 moved HIGH-CONFIRM -> HIGH-VAL; open/low/high counts unchanged (4/1/2), so the parsed fields above equal the final BELIEFS.md state.
