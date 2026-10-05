# EDA RUNBOOK v3: investigative, Bayesian, multi-hypothesis — follow skill 14c-eda.md TO THE LETTER, unattended

THE METHOD FOR EVERY INDIVIDUAL CLAIM IS STILL C:\Users\User\backtest_engine\backtest_engine2\skills\14c-eda.md. This runbook does
NOT replace it. v3 wraps 14c in a session that runs many hypotheses instead of one, from a chosen source mode, through a
Bayesian belief ledger, until a stop rule fires rather than at the first refutation. The full reasoning is
C:\Users\User\eda-routine\DESIGN_v3.md — read it if anything below is unclear; this file is the operational version of it.

Where this runbook, 14c and RUNBOOK.md (v2) seem to differ: 14c wins on method for a single claim; the HOLDOUTS section below
always wins; v3's stop rules and multi-hypothesis rules win over v2 (which stopped at one claim and the first refutation — v3
supersedes that). RUNBOOK.md (v2) and RUNBOOK_v1_sweep.md are kept for reference. Do not follow either.

READ IN FULL FIRST, in this order:
  TARGET.md; DESIGN_v3.md; C:\Users\User\backtest_engine\backtest_engine2\PROTOCOL.md; ...\skills\00-overview.md;
  ...\skills\12-alpha-overview.md; ...\skills\14c-eda.md; C:\Users\User\finding-alphas\data-hygiene.md;
  C:\Users\User\eda-routine\HOLDOUT_RULES.md; INBOX.md; MODES.md (create if absent, see MODE SELECTION below).

UNATTENDED SUBSTITUTIONS (unchanged from v2). Nobody confirms a cell live. Instead:
  - "Announce the cell and wait for confirmation" -> write the full 14c Step-3 announcement to cells\cell_NN_announce.md BEFORE
    any code for that cell exists, then proceed.
  - "Decisions I need from you" / "stop and ask" -> write the question and the CONSERVATIVE default in DECISIONS.md and take the
    default. Heavy dependencies (PyMC, ruptures, deepgraph, ...): DO NOT INSTALL unless TARGET.md's PRE-APPROVED INSTALLS line
    names them; then install only into C:\Users\User\eda-routine\.venv and log versions.
  - "Confirm net status / confirm the stop" -> write it; a human confirms later.
  - Cannot proceed safely -> write STOPPED.md with the reason, set TARGET.md STATUS to STOPPED <run folder>, end.

SCOPE (14c "What does NOT belong here"), unchanged: EDA only. No backtest, no signal, no PnL. Write only inside the run folder
(plus INBOX_PROPOSALS.md, see PHASE 3). Never touch alpha_log.md, live strategies, MT5, or the raw data. Never edit INBOX.md or
MODES.md's counts except as this runbook specifies.

---

## HOLDOUTS (strict, unchanged from v2 — read it there if you skipped it)

TRAIN and VAL only are supplied; there is no TEST here. Data lives only under C:\Users\User\eda-routine\data\<name>\ with a
CUT.json. Never open C:\Users\User\backtest_engine\backtest_engine2\data\. A row later than VAL_END -> STOPPED.md. Crypto: read
HOLDOUT_RULES.md before opening any file; never read backtest_engine2\_SEALED_HOLDOUT.md.

**v3 cuts TRAIN into an EXPLORE slice and several CONFIRM folds, because v3 chases observations and each one needs more than one
clean place to be tested:**

- **EXPLORE, C1, C2, ... Cn** — a chronological split of TRAIN: EXPLORE first, then n CONFIRM folds, an embargo between each
  pair at least as long as the longest horizon the run intends to use. **n = 3 by default; n = 2 only if a three-way cut would
  leave a fold under the minimum length SPLITS.md states (from coverage counts); never fewer than 2.** Declare it in `SPLITS.md`
  from coverage counts only, BEFORE any forward return is measured, and never revise it after one is (same mechanics as the
  x101 runs' `x101_SPLITS.md` / `G.declare_split`). `SPLITS.md` carries the machine-readable block `gate.py` parses:

  ```
  slices:
  - EXPLORE 2017-08-17 2021-07-01
  - C1 2021-07-08 2022-01-01
  - C2 2022-01-08 2022-07-01
  - C3 2022-07-08 2023-03-20
  - VAL 2023-03-25 2023-12-01
  ```
  (from inclusive, to exclusive, UTC dates; slices in this order, non-overlapping.)

- **The slice rules, per hypothesis** (these replace v3.0's "CONFIRM opened once per hypothesis"):
  1. **Never on its birth slice.** A hypothesis is never tested on the slice it was born on (`born_on`), nor on any slice where
     its defining statistic has already been displayed (`seen_on`, e.g. as a descriptive in its parent's cell). EXPLORE-born
     hypotheses therefore start on C1; a child born on C2 may use EXPLORE, C1 and C3.
  2. **Each slice once.** A hypothesis opens each slice at most once. A second test of the same sub-claim on the same slice is
     guard (a) — one piece of evidence.
  3. **No fold shopping.** A hypothesis opens its CONFIRM folds in order: its next CONFIRM test is always on the lowest-numbered
     fold it is still eligible for. It may not skip a fold it could use, because it expects a later one to look better.
  4. **Source-born hypotheses** (modes A/B/C/D, `born_on: SOURCE ...`) were not produced by this data, so EXPLORE is an ordinary
     slice for them: they may open EXPLORE once, then the folds in order, under the same rules.
- **VAL** — unchanged from v2: opened ONCE per session, at Phase 3, for hypotheses that reached HIGH-CONFIRM (below). Rule
  written before opening. VAL_NOTE from TARGET.md quoted beside every VAL number. Never described as out-of-sample proof.

Every slice opening (EXPLORE test, each CONFIRM fold, VAL) is a row in `ATTEMPTS.md` and counts toward K, no exceptions.

---

## MODE SELECTION — read before Phase 0

`SOURCE_MODE` in `TARGET.md` is one of `A`, `B`, `C`, `D`, `E`, or blank.

- **A** = Ideas — one-liners from `INBOX.md` §A, user's own thinking.
- **B** = Papers — one entry from `INBOX.md` §B (SSRN/Substack URL or local file path).
- **C** = Paper groups — one named group from `INBOX.md` §C, read together.
- **D** = Lens — one corpus under `C:\Users\User\finding-alphas\lenses\` (pick by relevance to TARGET.md's data card; every
  claim carries file + section, per `lenses.md` rule 1).
- **E** = Data — free-form; no inbox item; every hypothesis this session tests must trace to a Phase 0 observation.

**If `SOURCE_MODE` is set, use exactly that mode, exactly as given. Autopick never overrides an explicit setting.**

**If `SOURCE_MODE` is blank**, autopick: read `MODES.md` (create with all five modes at 0 if absent), pick the mode with the
fewest completed sessions, ties broken A→B→C→D→E. If that mode has nothing unused in its inbox section (A/B/C only — D and E
always have material), log it in DECISIONS.md and move to the next least-used mode. Write the picked mode into this run's
`DECISIONS.md` with the count table you read. Exactly one mode per session — never mix A with D, etc.

For A/B/C: mark the picked inbox item `used <run folder>` in `INBOX.md` at the end of Phase 3 (only after REPORT.md exists).
Do not consume more than one item (B) or one group (C) per session.

Source material (any mode) is for the CLAIM and MECHANISM only. Its reported RESULTS are never evidence in this run — same
HOLDOUT RULE FOR SOURCES as v2, including the ⚑ flag for any source whose sample overlaps VAL or later.

BROWSER (mode B, C, or D pointing outside the local lens files): same as v2 — ssrn.com and *.substack.com only, read-only, own
new tab, 12 page loads max, log every page in DECISIONS.md. Mode D reading local lens files needs no browser.

---

## PHASE 0 — know the data before any claim (EXPLORE slice only)

Not optional for any mode, including B/C/D where a claim is already in hand — the data-nature facts here feed the Phase 1
"assumption" and "impostor" checks for EVERY hypothesis regardless of where it came from.

Write `DATA_PROFILE.md` with one section per item below. Each section states its own question and pre-committed rule (14c
rule 1 applies to data-nature claims too — e.g. "1-min returns autocorrelated at lag 1: yes if |ACF(1)| > 2/sqrt(n)"), then a
cell, a plot (`plots\00_<slug>.png`), and a table:

1. **Distributions** — each column, on returns not levels: shape, tails, zero-mass.
2. **Missingness and gaps** — where, when, how much (cross-check against CLEANING_LOG.md; do not re-report known cleaning
   facts as findings, same v2 rule).
3. **Autocorrelation** — returns, |returns|, volume, at stated lags.
4. **Cross-column relationships** — correlation matrix on returns; flag impostor pairs (floor Q3: is one column secretly a
   twin of another).
5. **Regime structure** — how 1-4 change across eras; note any structural break.
6. **Intraday / weekly shape** — volume and volatility by time-of-day and day-of-week, as descriptive facts only (not yet a
   claim).
7. **What a row physically is** — from DATA_CARD.md: trade print vs bid/ask/mid, OPEN- or CLOSE-stamped, when knowable.

Close Phase 0 with `OBSERVATIONS.md`: numbered entries, each with its plot/table reference, the slice (always EXPLORE here),
and one line "expected vs saw". This is the raw material Phase 1 mode E draws from, and every mode's Phase 1 "assumption" /
"impostor" checks cite it.

---

## PHASE 1 — hypothesis intake (scientific method, enforced as required fields)

Write up to 6 candidate hypotheses into `BELIEFS.md`, sourced per the picked mode (A: the inbox one-liner(s); B: the one
paper; C: the paper group, which may yield more than one candidate since it's read together; D: the lens corpus; E: Phase 0
observations only). An entry missing any field below is not accepted — fix it or drop the candidate:

- **Observation / source** — file + section, URL, or `OBSERVATIONS.md` number.
- **Question** it answers.
- **Hypothesis**, part-0 form, naming carded columns exactly: *"a change in [column(s)] predicts [response over a stated
  horizon] because [economic reason]."*
- **Prediction that forbids something** — what we would NOT see if it's false. No forbidden outcome -> not a hypothesis
  (lens rule 6).
- **Rivals** — at least two other explanations for the same pattern (volatility, volume, time-of-day, a twin series, or a
  floor-Q3 impostor).
- **Born on** — `SOURCE` + source name, or EXPLORE + the `OBSERVATIONS.md` number it came from (or, for a child, the slice
  and cell that produced it).
- **Prior + anchor + trust arithmetic** — a stated source (tracker base rate at ~30% trust, a published replication rate, an
  uninformative default, a mechanism argument) and the arithmetic that turned it into a number. No anchor -> does not count.

A hypothesis born on EXPLORE with no economic mechanism may still be queued, marked **NO-STORY**, and is never reported as
more than a lead (mirrors part-0's lens rule 6: a story is required to deploy, not to look — but v3 also requires a forbidding
prediction before a NO-STORY lead gets a CONFIRM test, or it's just curve-reading).

### `BELIEFS.md` format — fixed, so `gate.py` can check it, not just a human

One block per hypothesis, in this exact key:value shape (blank lines between blocks, keys in this order). `gate.py` parses
`## H<n>` headings and requires every key below present and non-empty; `state` and `posterior` are the two fields the loop
updates in place, everything else is written once at intake and never edited.

```
## H<n> — <short title>
parent: <H<m> | none>
source: <file+section | URL | OBSERVATIONS.md #k>
question: <...>
hypothesis: <a change in [...] predicts [...] because [...]>
forbids: <what we would NOT see if false | none - NO-STORY>
rivals: <rival 1>; <rival 2>[; ...]
born_on: <SOURCE <name> | EXPLORE #k | C<j> cell_NN | EXPLORE cell_NN>
seen_on: <none | C<j>[, C<k> ...]>
prior: <0.xx>
anchor: <source + trust arithmetic, one line>
posterior: <0.xx>
state: <OPEN | LOW | HIGH | HIGH-CONFIRM | HIGH-VAL>
evidence:
- cell_NN: <slice> <branch> weight=<w> capped=<yes/no> -> posterior <p>
- ...
```

`born_on` starts with the slice name (`SOURCE`, `EXPLORE`, `C1`, ...) — `gate.py` reads that first word. `seen_on` lists every
slice on which this hypothesis's defining statistic was already displayed before it had a rule file of its own (typically a
descriptive printed in its parent's cell); `none` if there is none. Those slices are closed to it, like its birth slice.

`no_story: yes` is written as an extra key (after `state`) only for NO-STORY entries; its absence means the hypothesis has a
mechanism. A NO-STORY entry with `forbids: none - NO-STORY` may still open a CONFIRM fold only once it has been re-written with
a real `forbids` line — until then `gate.py` blocks it from any CONFIRM-fold cell.

---

## PHASE 2 — the loop (repeat until a stop rule fires)

For each iteration:

1. **Pick the next test.** A hypothesis is *pickable* if its state is OPEN or HIGH and it still has an admissible slice:
   EXPLORE or a CONFIRM fold it has not opened, that is not its birth slice and not in its `seen_on` (for CONFIRM, only the
   lowest such fold counts — slice rule 3). Among pickable hypotheses, choose the test with the largest expected belief
   shift; break ties by cheapest test. Write the arithmetic in `cell_NN_rule.md`. HIGH hypotheses stay pickable on purpose:
   one fold is not confirmation, and running the remaining folds is the decay-first check.
2. **Write `cells\cell_NN_rule.md` FIRST** (before any code). It starts with three header lines `gate.py` parses:
   ```
   hypothesis: H<n>
   slice: <EXPLORE | C<j> | VAL>
   kind: <test | redirect | val>
   ```
   then the sub-claim, the 14c menu row + tool named, the decision rule with three branches and numbers, and the **evidence
   weight** for each branch:
   - `weight(supported) = power / alpha`, `weight(refuted) = (1 - power) / (1 - alpha)`, `weight(inconclusive) = 1`.
   - `power` comes from a stated simulation at the smallest economically meaningful effect size, **at this slice's own sample
     size** (a fold is shorter than v3.0's single CONFIRM; its power is lower and the weight must say so) — write the
     simulation's own one-line result in the rule file, not just the number.
   - **The rule must carry a size condition, not just a significance condition.** "supported" requires the effect to clear
     the stated smallest economically meaningful size (or a stated fraction of it, argued in the rule file); a significant
     effect below that size is `inconclusive`, never `supported`. (The first v3 run reached 0.985 on an effect half its own
     economic threshold, because its rules only asked for z < -1.645.)
   - **Guard (a):** if this cell re-tests a sub-claim an earlier cell in this session already tested on the SAME slice, it is
     the same piece of evidence — take the stronger test's weight, do not multiply both in. Tests on DIFFERENT folds are
     separate pieces of evidence and their weights multiply — that is what the folds are for.
   - **Guard (b):** no single cell may move a hypothesis's odds by more than 10x either direction; cap the weight before
     applying it and say you capped it.
3. **Then `cells\cell_NN_announce.md`** in the 14c template, referencing the rule file.
4. **Run the cell** — 14c cell loop, guard for every load, plot + tables, `ATTEMPTS.md` row.
5. **State the result against the pre-committed rule** in `cells\cell_NN_result.md`. It starts with two header lines
   `gate.py` parses:
   ```
   branch: <supported | refuted | inconclusive>
   weight_applied: <w after the cap; 1 for redirect cells>
   ```
   then the deciding number and the weight from step 2 (capped or not). Do not soften it.
6. **Update `BELIEFS.md`**: posterior odds = prior odds × the product of every `weight_applied` in its evidence chain. Convert
   back to a probability and record it; set `state` from the posterior and the fold record (below). `gate.py` recomputes
   this chain from the result files and refuses a posterior that does not match.
7. **Spawn.** Ask "what does this result suggest?" and write any new hypothesis as a CHILD entry in `BELIEFS.md` (same
   required fields as Phase 1, parent hypothesis named, `born_on` = this cell's slice + cell, `seen_on` = any other slice where
   its statistic is already on screen). A child born on fold Cj is tested on EXPLORE and the other folds — it is not stuck.
8. **On refutation of a sub-claim the hypothesis can't survive without** (14c 3.2, scoped per-hypothesis in v3, not
   session-wide): drop that hypothesis's probability toward LOW via steps 6-7, then run a **mandatory redirect cell**
   (`kind: redirect`, `weight_applied: 1`): "where does the data actually point?" — opposite sign? one era/horizon/subset
   only? absent everywhere? It may look at EXPLORE, or at a slice this hypothesis has already opened (that data is already
   seen) — never at a fold it has not opened. Its finding is captured as a NEW spawned hypothesis (step 7), born on the slice
   the redirect looked at, with its OWN rule file — never a rewrite of the dead one, and it does not inherit the dead one's
   identity or arc.

**States**, used only to route what happens next — never reported as a kill (that stays the user's call):
- **LOW** — posterior < 5%. Closed for this session; no further cells against it.
- **OPEN** — posterior 5%-85%. Pickable while it has an admissible slice.
- **HIGH** — posterior > 85%, not yet confirmed. Pickable while it has an admissible slice.
- **HIGH-CONFIRM** — posterior > 85% AND `supported` on at least 2 CONFIRM folds AND `refuted` on none. Queued for VAL. (A
  hypothesis refuted on any fold cannot be HIGH-CONFIRM however high its posterior: an effect that lives in one fold is a
  regime story, and the report says so.)
- **HIGH-VAL** — was HIGH-CONFIRM and its VAL cell came back `supported`. (VAL refuted or inconclusive -> it stays
  HIGH-CONFIRM or drops by its posterior, and the report states the VAL failure.)

---

## STOP RULES — a session ends ONLY when one of these fires; write `STOP_REASON.md` naming which, with the numbers

- **S1 — all resolved.** Every hypothesis in `BELIEFS.md` is LOW or HIGH-VAL.
- **S2 — beliefs have settled.** Three consecutive picks (step 1) where the best available test's expected shift is ≤ 3
  percentage points on every pickable hypothesis. S2 requires that admissible tests still exist — they are just not worth
  running.
- **S3 — hard cap.** 30 test cells (Phase 0 cells don't count) OR 3 wall-clock hours, whichever comes first.
- **S4 — slices exhausted.** No hypothesis is pickable: every one is LOW, HIGH-CONFIRM/HIGH-VAL, or has used every slice it is
  allowed. (The first v3 run reported this case as "S2 with 0.0 pp shifts"; it is its own rule now, and `gate.py` checks it
  by recomputing admissibility rather than taking the claim.) Hypotheses left OPEN or HIGH under S4 are reported as needing a
  fresh slice — opening TEST is the user's call.

**Not allowed:** stopping on a single refutation; stopping with a pickable hypothesis and none of S2/S3 true; stopping because
the inbox item "felt" exhausted without a stated S1-S4.

### `STOP_REASON.md` format — fixed, so `gate.py` can check the claim against `BELIEFS.md`

```
rule: S1 | S2 | S3 | S4
open_count: <n>          # count of BELIEFS.md entries with state: OPEN, at the moment of stopping
low_count: <n>
high_count: <n>          # every state starting HIGH
detail: <one line — S1: nothing to add; S2: the three picks and their expected shifts; S3: cells used / minutes elapsed;
         S4: each non-resolved hypothesis and why it has no admissible slice>
```

`gate.py` recomputes `open_count`/`low_count`/`high_count` from `BELIEFS.md` itself and refuses if they don't match what's
written here — the numbers in this file are a claim, and the gate is what checks the claim rather than trusting it. The counts
are the FINAL state, after the Phase 3 VAL cells.

---

## PHASE 3 — close

1. **VAL pass.** For every HIGH-CONFIRM hypothesis, open VAL once (`kind: val`, `slice: VAL`), rule written first, VAL_NOTE
   quoted beside the result. Every VAL cell is numbered after every test and redirect cell. Report even a failure.
2. **`REPORT.md`**, one page: source mode and item used; the full belief table (hypothesis, prior→posterior, evidence chain
   with slice per step, final state); a fold table for anything that opened a CONFIRM fold (branch and effect per fold — this
   is the decay-first shape); the cost line for anything that reached HIGH or VAL (v2's Step 1b additions, unchanged);
   K = every EXPLORE/fold/VAL look counted, flagged for the downstream DSR deflation; one part-0
   `1b finding` block per hypothesis that moved off its prior; the still-open list; leads (NO-STORY entries, observations not
   chased this session).
3. **`INBOX_PROPOSALS.md`** — any new idea/paper/group worth a future session goes here, never written into `INBOX.md`
   directly (same pattern as `DATA_ADDED.md` in the x101 runs — the human merges it).
4. Mark the consumed inbox item(s) `used <run folder>` in `INBOX.md`. Increment this mode's count in `MODES.md`.
5. Set `TARGET.md` STATUS to `DONE <run folder>` — but only if `gate.py` (see below) passes. If it fails, fix what it names
   and re-run the check; do not write DONE around a failing gate.

---

## ENFORCEMENT

- **`C:\Users\User\eda-routine\gate.py`** — deterministic, modeled on `eda_guard.py`. Run it (`python gate.py <run_dir>`)
  before `STATUS: DONE` may be written; it must print `PASS`. Checks: every required file/section from Phases 0-3 exists;
  `SPLITS.md` declares EXPLORE, at least 2 ordered non-overlapping CONFIRM folds and VAL; every `cell_NN_rule.md` predates its
  `cell_NN_result.md` and carries the hypothesis/slice/kind header; every `BELIEFS.md` entry has all required fields in the
  fixed format (above); the slice rules (never the birth or `seen_on` slice, each slice once, folds in order, redirects only
  on EXPLORE or an already-opened slice, no NO-STORY entry on a fold); every posterior equals its prior times the
  `weight_applied` chain, each weight within the 10x cap; every state matches its posterior and fold record; VAL only for
  HIGH-CONFIRM, after every test cell; `STOP_REASON.md`'s counts and S1-S4 claim match what `BELIEFS.md` and the cells
  actually show. If it prints `FAIL`, fix what it names —
  do not write DONE around a failing gate, and do not edit a result file to make an mtime check pass; fix the process
  defect it's pointing at.
- **`eda-v3-judge` agent** (`C:\Users\User\eda-routine\.claude\agents\eda-v3-judge.md`) — read-only, run AFTER `gate.py`
  passes. Checks what `gate.py` structurally cannot: whether an evidence weight's power/alpha was real and applied
  correctly, whether the stop was actually earned (not a disguised early stop dressed up as S2/S3), whether the
  EXPLORE/fold funnel was really obeyed per hypothesis, whether a spawned "new" hypothesis was a genuine redirect or a
  rewrite of a dead claim, and whether a NO-STORY lead was reported as no more than a lead. Returns PASS/FAIL with numbered
  issues. A FAIL here does not block `STATUS: DONE` mechanically the way `gate.py` does — it is read by the human review
  that follows every `DONE`, same as a `FAIL-MINOR`/`FAIL-MAJOR` from the finding-alphas judges.

Run both at the end of Phase 3, in that order — `gate.py` first since the judge assumes its checks already passed.

---

## NEVER (carried from 14c and v2, plus v3's own)
Run EDA as a "show what you can do" exercise; present a finding with no pre-committed rule; silently ignore a refuted
sub-claim; test a NO-STORY lead on a CONFIRM fold without a forbidding prediction; test a hypothesis on the slice that produced
it or a slice where its statistic was already seen; open the same slice twice for one hypothesis; skip a fold to reach a
later one; call a significant-but-too-small effect "supported"; multiply the same evidence in twice (guard a); let one cell
move a probability past the 10x cap (guard b); stop with a pickable hypothesis and no S2/S3; build a generic `eda.py`.
