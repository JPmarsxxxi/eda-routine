# EDA ROUTINE v3 — DESIGN (spec only; not yet a runbook)

Status: DRAFT for the user to read. RUNBOOK.md (v2) is untouched and stays the live one until v3 is approved and built.
Written 2026-09-28.

## Why v3 exists (evidence from v2, run 2026-09-25_btc-spot-1m-clean_v2)

v2 tested ONE claim, ran 4 scored cells, hit its first refutation (C5) and stopped. Six sub-claims were left UNTESTED
(C3, C4, C6a, C6b, C7, C11) and a lead it wrote down was never chased (Pearson and Spearman disagree, hinting at reversal on
large-move days). That is not a bug: RUNBOOK v2 says "exactly ONE claim" (step 1), "do NOT test claims outside the hypothesis"
(step 3) and "refuted -> STOP THE HUNT" (step 4e). v3 changes those three rules and adds what is missing around them.

| v2 | v3 |
|---|---|
| one claim, from SSRN/Substack only | many claims from ONE source mode per session (5 modes, below) |
| no look at the data before the claim | Phase 0: get to know the data first, on a declared EXPLORE slice |
| refutation stops the hunt | refutation lowers a probability and forces "where does the data point instead" |
| observations are logged, never chased | observations become new hypotheses, tested on a slice they were not born on |
| no probabilities | every hypothesis has a prior, a stated evidence weight per test, a posterior |
| stop = the list ran out | stop = every hypothesis resolved, or the best remaining test would not move beliefs, or a hard cap |

## What does NOT change
14c stays the method for each individual claim (decompose, ten-question floor, tools from the menu, pre-committed rule, one cell
per sub-claim, hypothesis-update cell). Holdout rules, the unattended substitutions, no installs, the browser rule (SSRN and
*.substack.com only, 12 page loads), write scope (run folder only), findings-not-verdicts, never write to alpha_log.md.
Everything in RUNBOOK.md not mentioned below carries over.

**Two deliberate deviations from 14c, stated so nobody has to discover them:**
1. 14c Step 3.2 "refuted -> stop the hunt" applies PER HYPOTHESIS. The session continues with the others.
2. 14c "do not chase observations outside the hypothesis" is replaced by "chase them only through the funnel below". 14c itself
   allows this route: "When to load ... starting from raw data with no hypothesis and need to derive one from observation".

## One source mode per session
`INBOX.md` (in eda-routine\, edited by the user) has:
- **A. Ideas** — one-liners from the user's own thinking
- **B. Papers** — one per line (SSRN/Substack URL, or a local file path)
- **C. Paper groups** — a name plus a list of papers, read together
Plus two modes that need no inbox entry:
- **D. Lens** — a corpus under `finding-alphas\lenses\` (each has an INDEX.md). Every claim carries file + section (lens rule 1).
- **E. Data** — free-form: hypotheses come only from what Phase 0 shows.

Choice: `TARGET.md` line `SOURCE_MODE: A|B|C|D|E|` (blank allowed). If the user sets it, that mode is used as given — no
override. **Autopick fires ONLY when the line is left blank** — it is a fallback for "nothing supplied", not a sixth option
alongside the other five. Autopick = the mode with the fewest completed sessions (kept in `MODES.md`), ties in A-E order; if the
picked mode has nothing unused in the inbox, log it and take the next least-used mode. Exactly one mode per session, never
mixed. Each inbox item is marked `used <run folder>` after a session takes it.
Source results are for the CLAIM and METHOD only, never evidence (RUNBOOK HOLDOUT RULE FOR SOURCES stays).

## The funnel: three slices, each opened by rule
`EXPLORE -> CONFIRM -> VAL`. EXPLORE and CONFIRM are a chronological split of TRAIN, declared from coverage counts only, before
any forward return is measured, never revised after (x101 rule; `G.declare_split`). Every exploratory look and every hypothesis
is born and developed on EXPLORE. CONFIRM is opened ONCE PER HYPOTHESIS, for a test whose rule was written first; every opening
counts in K. VAL is opened once per session at the end, for hypotheses that passed CONFIRM, VAL_NOTE quoted beside the number.
Why: looking is free but every look raises the chance of a false find. The funnel is what lets it look a lot and still be believed.

## Phases

### Phase 0 — know the data (before any claim)
Cells here answer "what is this data like?" and each is written as a question with a pre-committed rule, per 14c rule 1 (a data-nature
claim, e.g. "1-minute returns are autocorrelated at lag 1: yes if |ACF| > 2/sqrt(n)"). EXPLORE slice only. Required outputs, in `DATA_PROFILE.md`,
one section each, each with a plot and a table:
1. distribution of each column (returns not levels): shape, tails, zeros
2. missingness and gaps: where and when
3. autocorrelation of returns, |returns| and volume, at stated lags
4. cross-column relationships on returns: correlation matrix, and which pairs are impostors of each other
5. how all of the above change across eras (regimes, breaks)
6. intraday and weekly shape of volume and volatility, as descriptive facts
7. what a trade or a bar in this data physically is (from DATA_CARD.md)
Then `OBSERVATIONS.md`: numbered, each with its number, plot, slice, and one line "what I expected vs what I saw". Facts already in
CLEANING_LOG.md are not observations (v2 rule kept).

### Phase 1 — hypothesis intake (scientific method, enforced as required fields)
From the session's mode, plus the Phase 0 observations, write up to 6 candidates in `BELIEFS.md`. An entry with an empty field is not accepted:
- **Observation / source** (file+section, URL, or observation number)
- **Question** it answers
- **Hypothesis** in the part-0 form, naming carded columns exactly: "a change in [column(s)] predicts [response over a stated horizon] because [reason]"
- **Prediction that FORBIDS something** — what we would see if it is false (lens rule 6: a story that forbids nothing does not count)
- **Rivals** — at least two other explanations for the same pattern (volatility, volume, time of day, a twin series, the impostor row of the floor)
- **Born on** — source, or EXPLORE/CONFIRM slice and observation number
- **Prior**, its **anchor**, and the trust arithmetic (RUNBOOK of x101: a tracker base rate carries ~30% weight; show the sum). No anchor = does not count.
A data-born idea with no mechanism is allowed to be tested but is marked NO-STORY and cannot be called anything but a lead.

### Phase 2 — the loop
Repeat until a stop rule fires:
1. **Pick the next test** = the available test with the largest expected belief shift among open hypotheses, cheapest first on ties. State the arithmetic.
2. **Write `cell_NN_rule.md` first**, containing the sub-claim, the 14c menu row and tool, the three branches, and the **evidence weight** below.
3. Run the cell (14c cell loop, plot, tables, ATTEMPTS row, guard for all loads).
4. **Update BELIEFS.md**: posterior odds = prior odds x weight of the branch that happened.
5. **Spawn**: what does this result suggest? New hypotheses enter `BELIEFS.md` as children (parent, born-on, prior, all Phase 1 fields).
6. **On refutation**: the hypothesis's probability drops, and a mandatory "where does the data point instead" cell runs (sign flipped? one era, one horizon, one subset?). What it finds is a NEW hypothesis with a new rule file, never a rewrite of the failed one.

**Evidence weight ("likelihood ratio") is fixed BEFORE the run** = how many times more likely this outcome is if the effect is real than if it is noise.
Computed from the rule itself: supported branch = power / alpha; refuted branch = (1 - power) / (1 - alpha); inconclusive = 1. `power` is from a simulation at
the smallest effect that would matter economically, stated in the rule file. Two guards: (a) several tests of the same sub-claim on the same sample
count as ONE piece of evidence (take the strongest, do not multiply); (b) no single test moves a hypothesis by more than 10x either way.

**Resolved states** (these describe where a probability sits, they are not kills; the user decides kills):
- LOW: posterior < 5%, closed for this session
- HIGH: posterior > 85% on EXPLORE -> queued for its one CONFIRM opening; passes CONFIRM -> queued for VAL
- OPEN: anything between

### Stop rules — the session may end ONLY when one of these fires, and STOP_REASON.md names which
- **S1** every hypothesis is LOW, or HIGH-and-tested through VAL
- **S2** diminishing returns: the best available test would move no open hypothesis by more than 3 percentage points, three picks in a row (the beliefs have settled)
- **S3** hard cap: 30 test cells (Phase 0 not counted) or 3 hours wall clock, whichever first
Not allowed: stopping on the first refutation, or with OPEN hypotheses and no S2/S3. Recommended starting caps are deliberately smaller than the
"40 cells" I floated in chat: an unattended run has to carry all state in files, and the first v3 run will show how much headroom there is.

### Phase 3 — close
`REPORT.md` (one page): mode and source; the belief table (each hypothesis: prior -> posterior, the evidence chain, the slice each test used); K = every look counted, with a note
that the deflated-Sharpe downstream deflates against it; one `1b finding` block per hypothesis that moved; still-open list; leads. Proposed inbox additions go in
the run's `INBOX_PROPOSALS.md` (the routine may not edit INBOX.md, same pattern as DATA_ADDED.md) for the user to merge.

## Enforcement — how "dig deeper" stops being a wish
1. **`gate.py`** (deterministic, follows `eda_guard.py`): run at every phase boundary and before `STATUS: DONE` may be written. It checks that required files
   and sections exist; that each rule file's timestamp precedes its result file and the file is unchanged since; that every BELIEFS prior has an anchor;
   that no CONFIRM or VAL opening lacks a pre-registered rule; that the open-hypothesis count matches BELIEFS.md; and that STOP_REASON.md names S1, S2 or S3 with the numbers behind it.
   If it fails, the routine may not write DONE.
2. **Post-run judge agent** (read-only, like the eda-judge-* agents): reads the run folder and answers one question, "was the stop legitimate and the process honest?". Returns PASS / FAIL with numbered issues.
3. Both are built AFTER this design is approved, as separate steps.

## Known risks and the guard for each
- More looks means more false positives -> funnel, K counted, CONFIRM once per hypothesis, VAL once.
- Evidence weights invented after the fact -> fixed in the rule file before the run, from power and alpha.
- Correlated tests treated as independent -> guard (a).
- Sessions too long for one context -> all state lives in files (PLAN.md, BELIEFS.md, ATTEMPTS.md); the routine reads them first each time it resumes.
- Confirmation-by-story -> Phase 1 "forbids something" and "rivals" fields are mandatory.
