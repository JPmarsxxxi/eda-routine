# MODES — completed-session counts per source mode, for autopick

Read by MODE SELECTION in RUNBOOK_v3.md ONLY when `TARGET.md`'s `SOURCE_MODE` line is left blank. Autopick chooses the mode
with the lowest count below, ties broken A -> B -> C -> D -> E. The routine increments the picked mode's count by 1 at the
end of Phase 3, after `REPORT.md` and `STATUS: DONE` are written — never before, and never for a session that ended in
STOPPED.md (a stopped run did not complete, so it does not count toward balancing the modes).

| mode | what it is | completed sessions |
|---|---|---|
| A | Ideas (INBOX.md §A) | 0 |
| B | Papers (INBOX.md §B) | 0 |
| C | Paper groups (INBOX.md §C) | 0 |
| D | Lens (finding-alphas\lenses\) | 0 |
| E | Data (Phase 0 observations only) | 2 |

## Log (one row per completed session, newest last)

<!-- appended by the routine, one line per DONE session:
YYYY-MM-DD  mode  run folder
-->
2026-09-30  E  runs/2026-09-30_crypto-panel-1h
2026-10-05  E  runs/2026-10-05_crypto-validated-1h
