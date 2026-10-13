# EDA RUNBOOK v3.4: a signal engine with three jobs (data, features, methods) — search TRAIN freely, check on VAL,
# hand TEST to the user — unattended

THE METHOD FOR EVERY INDIVIDUAL CLAIM IS STILL C:\Users\User\backtest_engine\backtest_engine2\skills\14c-eda.md. This runbook does
NOT replace it. v3 wraps 14c in a session that chases many hypotheses from a chosen source mode, searches for signals on
TRAIN as hard as it likes, updates a prior -> posterior for every hypothesis after every cell, and checks only
frozen candidates on VAL. The full reasoning is
C:\Users\User\eda-routine\DESIGN_v3.md — read it if anything below is unclear; this file is the operational version of it.

Where this runbook, 14c and RUNBOOK.md (v2) seem to differ: 14c wins on method for a single claim; the HOLDOUTS section below
always wins; v3's rules win over v2. RUNBOOK.md (v2) and RUNBOOK_v1_sweep.md are kept for reference. Do not follow either.

**v3.3 (2026-10-13) overrides 14c wherever 14c limits how often data may be looked at:** TRAIN may be searched without
limit (HOLDOUTS below). **v3.2 overrides 14c in two places**, both stated where they apply: (1) 14c's "heavy dependency ->
stop and ask" is replaced by INSTALLS AND METHODS below; (2) in modes B/C the source's own method is followed as written
(METHOD_SPEC.md), even where 14c's menu would pick a different tool. Everything else in 14c still wins on method.

**The one line that matters (v3.3).** SEARCHING happens only on TRAIN (EXPLORE and the CONFIRM folds): any number of looks,
variants, re-slicings and conditionings. VAL and TEST are only for CHECKING: a candidate's spec is frozen in a file first,
then run unchanged. VAL may check as many frozen candidates as the run produces. TEST is never opened by the routine — VAL
passes are handed to the user. Rigor beyond this line (multiple-testing haircuts, stress tests) is the user's later step;
this engine's job is to find candidates and count honestly how many looks it took (K).

## JOBS (v3.4) — one routine, three jobs; this file is the core every job follows

Alpha comes from three places: the data you can get, what you do with it, and the tools you process it with. The routine
has one job for each. `TARGET.md`'s `JOB:` line picks it; read the matching file right after this one and follow both:

| `JOB:` | file | what it does | its product |
|---|---|---|---|
| `data` | `JOB_DATA.md` | finds outside data with predictive power for the target; no cleaning | `DATA_PROPOSALS.md` (ranked), `SOURCES.md` |
| `features` | `JOB_FEATURES.md` | engineers as many predictive, non-redundant features as possible from data we have | the `features\` library |
| `methods` | `JOB_METHODS.md` | applies toolbox methods to our data, or finds new algorithms and tries them | the `toolbox\` registry |

Everything in this file applies to every job: holdouts, Phase 0, hypotheses with priors updated after every cell, the
search / freeze / confirm / VAL line, effort floors, stop rules, TEST_REQUESTS.md, memory, gate.py and the judge. A job
file only adds what is particular to it. Where they differ, the job file wins on its own ground (what a hypothesis is,
what a cell must report, its product); this file wins on everything else, and HOLDOUTS always wins.

- **The target** for every job is the forward return of the TARGET.md `DATA` bundle's main instrument(s), at horizons the
  run declares in SPLITS.md (every horizon tried counts in K), unless TARGET.md names another. Priors are beliefs about
  hypotheses; they never change the target.
- **Source modes A-E** (MODE SELECTION below) still say where ideas come from, inside any job: a papers-mode methods run
  takes its algorithm from a paper; a data-only features run builds from Phase 0 observations. `INBOX.md` §S (data
  pointers) is always read by the data job, whatever the mode.
- `DECISIONS.md` carries one machine-readable line `job: <data|features|methods>` next to `mode:` (gate.py reads both).
- Every job reads `features\REGISTRY.md` and `toolbox\REGISTRY.md` at the start: the library is the baseline a new result
  must add to, and the toolbox lists methods already validated.

READ IN FULL FIRST, in this order:
  MEMORY\LEDGER.md, MEMORY\FINDINGS.md, MEMORY\DATA_FACTS.md (see MEMORY below); TARGET.md; DESIGN_v3.md; C:\Users\User\backtest_engine\backtest_engine2\PROTOCOL.md; ...\skills\00-overview.md;
  ...\skills\12-alpha-overview.md; ...\skills\14c-eda.md; C:\Users\User\finding-alphas\data-hygiene.md;
  C:\Users\User\eda-routine\HOLDOUT_RULES.md; INBOX.md; MODES.md (create if absent, see MODE SELECTION below);
  the JOB_<job>.md file that TARGET.md's `JOB:` line names; features\REGISTRY.md; toolbox\REGISTRY.md.

UNATTENDED SUBSTITUTIONS (unchanged from v2). Nobody confirms a cell live. Instead:
  - "Announce the cell and wait for confirmation" -> write the full 14c Step-3 announcement to cells\cell_NN_announce.md BEFORE
    any code for that cell exists, then proceed.
  - "Decisions I need from you" / "stop and ask" -> write the question and the CONSERVATIVE default in DECISIONS.md and take the
    default. **Except installs:** 14c's "stop and ask before a heavy dependency" does not apply when TARGET.md's
    PRE-APPROVED INSTALLS line reads `any` (the default from v3.2) — follow INSTALLS AND METHODS below instead. If the line
    names packages, only those; if it reads `none`, nothing.
  - "Confirm net status / confirm the stop" -> write it; a human confirms later.
  - Cannot proceed safely -> write STOPPED.md with the reason, set TARGET.md STATUS to STOPPED <run folder>, end.

SCOPE (14c "What does NOT belong here"): no backtest, no PnL. The output is frozen candidate specs for the user's stress tests. Write only inside the run folder,
plus `MEMORY\` (PHASE 3 step 4 only), plus `.venv\` (installs). Never touch alpha_log.md, live strategies, MT5, or the raw data. Never edit INBOX.md or
MODES.md's counts except as this runbook specifies.

---

## INSTALLS AND METHODS (v3.2)

**The aim:** the best tool for the claim, not the tool that happens to be installed. A weak proxy chosen because the right
library was missing is a defect the judge scores down. A well-chosen, validated tool that sharpens a test is what the
judge scores up.

**Installs.** With `PRE-APPROVED INSTALLS: any` (the default), install what the claim needs:
- Only into `C:\Users\User\eda-routine\.venv`. If it does not exist, create it once with
  `python -m venv --system-site-packages C:\Users\User\eda-routine\.venv` (so the base stack stays importable), log that in
  DECISIONS.md, and run every cell that uses an install with `.venv\Scripts\python.exe`. Only from **PyPI or conda-forge**, only packages with a public release
  history, version **pinned** (`pkg==x.y.z`). No git URLs, no unpublished code, no install scripts from a paper's repo
  (port the method instead and say so in METHOD_SPEC.md).
- Before first use, a **validation cell** `cells\install_<pkg>.md` (+ its script): the package must recover a known answer
  on synthetic data built for the claim (a planted break at a known row, a simulated AR(1) with known phi, a known HMM
  state path). A tool that fails its validation is not used; say so and fall back.
- One `INSTALLS.md` row per package, in this table (gate.py parses it):

  ```
  | import | package | version | source | claim | replaces | adds | validation | result |
  |---|---|---|---|---|---|---|---|---|
  | ruptures | ruptures | 1.1.9 | pypi | H2-C8 break date | rolling-mean eyeballing | penalised change-point search with a stated cost | cells/install_ruptures.md | PASS |
  ```
- An install no cell uses is decoration and the judge marks it down. "Adds" must name what the base stack
  (numpy/pandas/scipy/statsmodels) cannot do or does worse for THIS claim.

**Method fidelity (modes B and C — the source is a paper).** Before any data is opened for a source claim, write
`METHOD_SPEC.md`, one `## M<n>` block per method the source uses:

```
## M1 — <short name>
source: <paper, section/equation/table>
estimator: <exactly what is estimated and how inference is done, e.g. Fama-MacBeth, NW(6) t>
library: <the library/function the paper used or the closest published implementation>
parameters: <every parameter the paper states: windows, lags, thresholds, rebalancing>
sample: <the paper's sample construction: frequency, universe filters, skip periods>
match: <exact | deviation>
deviation_reason: <none | why this data forces a difference, and what the difference is>
```

The first cell of every SOURCE-born hypothesis replicates M<n> **as specified** and carries `method: M<n>` in its
rule header. If the paper used a specific library, install and use it (INSTALLS above). Where it cannot be matched (a
proprietary package, data the bundle lacks), the deviation is written down BEFORE the cell runs. Additional variants may
follow as separate cells, but the replication comes first and is reported first. An exact, validated replication is the
highest-scoring outcome a mode B/C run can produce, whatever its result.

**The reward — `METHODS_SCORE` (0-3), given by the judge, logged in `MEMORY\LEDGER.md` so runs are compared over time:**
- **0** — a weaker proxy used where a standard better tool existed, with no stated reason; or an unlisted deviation from a
  source method; or an install that is decoration.
- **1** — sound base-stack tools, no gaps, nothing beyond.
- **2** — at least one validated non-base tool that fits its claim better than the base stack would (and is used in a
  cell); OR (B/C) every source method replicated with all deviations justified.
- **3** — both of the above, AND the better tool demonstrably mattered: it changed a branch, raised a test's power, or
  tested a structure (regimes, breaks, non-linearity, conditional effects) the base stack could not.

---

## MEMORY (v3.2, K split in v3.3) — what the routine remembers across runs, and nothing more

Three files in `C:\Users\User\eda-routine\MEMORY\`, read at the start of every run, appended at Phase 3 step 4 only. Each
line must earn its place: if a future run would not do something differently because of it, it does not go in.

| file | one entry | budget | used for |
|---|---|---|---|
| `LEDGER.md` | one table row per run: `date, run, job, target, mode, stop, cells, K_train, K_val, dataset, K_cum_train, K_cum_val, methods_score` | 250 lines | step log; cumulative looks per dataset, for the user's multiple-testing haircut; methods score over time |
| `FINDINGS.md` | `### <run> F<n> — <title>` + at most 3 lines: the frozen spec in one line; CONFIRM folds + VAL result; what it needs next | 300 lines | leads to pick up, the already-tried list |
| `DATA_FACTS.md` | `- <dataset>: <fact> (<run>)`, one line | 150 lines | what a dataset IS, so no run re-discovers it |

Rules:
- **K, counted, never capped.** `K_train` = every spec evaluated on TRAIN: the sum of `variants:` over search cells (a grid
  of 40 parameter sets is 40) plus one per confirm cell. `K_val` = every VAL check. Each has a running total per `dataset`
  (`K_cum_train`, `K_cum_val`). Report all four in REPORT.md beside every VAL result. K exists for the user's stress tests:
  a candidate that passed VAL on the 6th variant of its family is weaker than one that passed on the 1st.
- **FINDINGS** gets an entry for every candidate that reached CONFIRM-SHOWN, VAL-PASS or VAL-FAIL. Frozen candidates that
  failed CONFIRM go on one line `- <run> CONFIRM-FAIL: F2, F4`; dropped hypotheses on one line `- <run> DROPPED: H3, H5`.
- **DATA_FACTS** holds facts about the data only (identity, stamping, coverage holes, twins), never results.
- **How memory may be used.** FINDINGS informs which hypotheses to pick and which variants were already tried. A later run
  may search the same TRAIN again and may re-check an earlier candidate on VAL — its earlier VAL check is already in
  `K_cum_val`, and FINDINGS says what it showed, so a repeat check of an unchanged spec is pointless and a changed spec is a
  new candidate with `variant_of` pointing back.
- **Consolidate, don't grow.** If an append would push a file over budget, first merge entries that say the same thing,
  drop superseded ones, and fold old one-line lists together. Log the consolidation in DECISIONS.md.

---

## HOLDOUTS (strict) — search on TRAIN, check on VAL, never open TEST

TRAIN and VAL only are supplied; there is no TEST here. Data lives only under C:\Users\User\eda-routine\data\<name>\ with a
CUT.json. Never open C:\Users\User\backtest_engine\backtest_engine2\data\. A row later than VAL_END -> STOPPED.md. Read
HOLDOUT_RULES.md before opening any file; never read backtest_engine2\_SEALED_HOLDOUT.md.

**Slices.** TRAIN is cut into EXPLORE and n CONFIRM folds (n = 3 by default; 2 only if three would leave a fold under the
minimum length SPLITS.md states from coverage counts), chronological, with an embargo between neighbours at least as long as
the longest horizon the run intends to use. Declare it in `SPLITS.md` from coverage counts only, BEFORE any forward return is
measured, and never revise it after one is. `SPLITS.md` carries the machine-readable block `gate.py` parses:

```
slices:
- EXPLORE 2017-08-17 2021-07-01
- C1 2021-07-08 2022-01-01
- C2 2022-01-08 2022-07-01
- C3 2022-07-08 2023-03-20
- VAL 2023-03-25 2023-12-01
```
(from inclusive, to exclusive, UTC dates; slices in this order, non-overlapping.)

**What each slice is for:**

| slice | used for | limit |
|---|---|---|
| EXPLORE, C1..Cn (TRAIN) | **searching**: look, tweak, re-slice, condition on regimes, try variants, follow leads | none — every spec evaluated counts in `K_train` |
| CONFIRM (all folds) | also the **stability check** of a frozen spec: run unchanged, per fold | one confirm cell per frozen spec |
| VAL | **checking** a frozen spec that held on CONFIRM. Nothing is tuned on what it shows | any number of candidates, one VAL check each |
| TEST | never opened by the routine. VAL passes go to the user in `TEST_REQUESTS.md` | the user's call |

Why the folds survive even though TRAIN is open: a spec that only works in one fold is a regime story. The confirm cell
shows the user that shape, and only a spec that holds on at least 2 folds and is refuted on none goes on to VAL.

**The line between searching and checking.** Before a confirm or VAL cell, the candidate's spec is written to
`candidates\F<n>.md` and not edited again. The VAL cell records the file's sha256; `gate.py` refuses a spec that changed
after its check. If VAL fails, the run may go back to TRAIN and search again — and if that produces a different spec, it is
a new candidate with `variant_of: F<n>`, its own confirm cell and its own VAL check. That chain is legitimate and it is
logged: the user discounts a family of variants, the routine does not hide one.

Every data load goes through the guard and is a row in `ACCESS_LOG.md`. A search cell's code never loads a VAL row.

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
Whatever the route, `DECISIONS.md` carries one machine-readable line `mode: <A|B|C|D|E>` (gate.py reads it).

For A/B/C: mark the picked inbox item `used <run folder>` in `INBOX.md` at the end of Phase 3 (only after REPORT.md exists).
Do not consume more than one item (B) or one group (C) per session.

Source material (any mode) is for the CLAIM and MECHANISM only. Its reported RESULTS are never evidence in this run — same
HOLDOUT RULE FOR SOURCES as v2, including the ⚑ flag for any source whose sample overlaps VAL or later.

BROWSER (mode B, C, or D pointing outside the local lens files): same as v2 — ssrn.com and *.substack.com only, read-only, own
new tab, 12 page loads max, log every page in DECISIONS.md. Mode D reading local lens files needs no browser.

---

## PHASE 0 — know the data before any claim (TRAIN only; never VAL)

Not optional for any mode, including B/C/D where a claim is already in hand — the data-nature facts here feed the Phase 1
"assumption" and "impostor" checks for EVERY hypothesis regardless of where it came from.

**Supplied-clean data (v3.2).** The user cleans data before supplying it. When the data folder has a `CLEANING_LOG.md`, do
not re-clean and do not re-report its facts; item 2 shrinks to "anything the log does not cover". What is never skipped is
the **identity check** in DATA_CARD.md: is each file the instrument, venue and stamping it claims to be (first timestamp
against the instrument's listing date; a cross-match against a second series of the same instrument where the bundle has
one; open- vs close-stamp from day boundaries). Check `MEMORY\DATA_FACTS.md` first — a fact already recorded there for this
dataset is cited, not re-derived.

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

Close Phase 0 with `OBSERVATIONS.md`: numbered entries, each with its plot/table reference, the slice it was seen on,
and one line "expected vs saw". This is the raw material Phase 1 mode E draws from, and every mode's Phase 1 "assumption" /
"impostor" checks cite it.

---

---

## PHASE 1 — hypothesis intake

Write up to 6 starting hypotheses into `BELIEFS.md`, sourced per the picked mode (A: the inbox one-liner(s); B: the one
paper; C: the paper group; D: the lens corpus; E: Phase 0 observations only). More are added during Phase 2 as children,
without a cap. An entry missing any field below is not accepted — fix it or drop it:

- **Observation / source** — file + section, URL, or `OBSERVATIONS.md` number.
- **Question** it answers.
- **Hypothesis**, part-0 form, naming carded columns exactly: *"a change in [column(s)] predicts [response over a stated
  horizon] because [economic reason]."*
- **Prediction that forbids something** — what we would NOT see if it's false.
- **Rivals** — at least two other explanations for the same pattern (volatility, volume, time-of-day, a twin series, or a
  floor-Q3 impostor). Search cells are where the rivals get controlled for.
- **Born on** — `SOURCE` + source name, or EXPLORE / a fold + the observation or cell it came from. Never VAL.
- **Prior + anchor + trust arithmetic** — a stated source (tracker base rate at ~30% trust, a published replication rate,
  `MEMORY\FINDINGS.md`, an uninformative default, a mechanism argument) and the arithmetic that turned it into a number. No
  anchor -> does not count. A child's prior is anchored too — usually on what the parent's cell showed.

A hypothesis with no economic mechanism may still be searched and frozen, marked **NO-STORY** (`forbids: none - NO-STORY`,
`no_story: yes`). It is reported as a lead, and its TEST request says it has no story.

### `BELIEFS.md` format — fixed, so `gate.py` can check it

```
## H<n> — <short title>
parent: <H<m> | none>
source: <file+section | URL | OBSERVATIONS.md #k>
question: <...>
hypothesis: <a change in [...] predicts [...] because [...]>
forbids: <what we would NOT see if false | none - NO-STORY>
rivals: <rival 1>; <rival 2>[; ...]
born_on: <SOURCE <name> | EXPLORE #k | EXPLORE cell_NN | C<j> cell_NN>
prior: <0.xx>
anchor: <source + trust arithmetic, one line>
posterior: <0.xx>
state: <OPEN | DROPPED | CHECKED>
candidates: <none | F1, F3>
evidence:
- cell_NN: <kind> <slice> weight=<w> capped=<yes/no> -> posterior <p>
```

`prior` and `anchor` are written once at intake. `posterior`, `state`, `candidates` and `evidence` are updated after
every cell. **OPEN** = still being searched; **DROPPED** = the effort floor below is met, the posterior has fallen below the
prior, and DECISIONS.md has a `drop H<n>: <reason>` line; **CHECKED** = at least one of its candidates has a VAL result and
the run is done with it.

---

## PHASE 2 — the loop (repeat until a stop rule fires)

### Belief updating — after EVERY cell, no exceptions

Every cell (search, confirm, VAL) moves the posterior of the hypothesis it names:
- The rule file states, before the cell runs, the evidence weight of each outcome: `weight = power / alpha` if the effect
  is there at the stated size, `(1 - power) / (1 - alpha)` if it is not, `1` if the cell cannot tell. `power` comes from a
  stated simulation at `min_useful`, at this cell's own sample size — its one-line result in the rule file, not just the
  number. **The simulation's noise is measured on data already seen** (e.g. a day-permutation null on EXPLORE), never
  assumed: a v3.1 run's assumed noise was off by 3-4x, so its weights over- and under-stated the evidence.
- **Caps.** A search cell moves the odds at most **3x** either way (it looked at data the run may already have searched, so
  its evidence is weaker); a confirm or VAL check of a frozen spec at most **10x**. Cap the weight before applying it and
  say so.
- The result file states `weight_applied: <w>`. Posterior odds = prior odds x every `weight_applied` on that hypothesis, in
  cell order. Write the new posterior and an `evidence:` line in `BELIEFS.md`. `gate.py` recomputes the chain and refuses a
  posterior that does not match.
- **Pick by belief.** The next cell is the one with the largest expected shift in any OPEN hypothesis's posterior (ties:
  cheapest), arithmetic in the rule file. The posterior is what drives where the run spends its effort.

### Effort — the run is not allowed to be lazy

- **No hypothesis is DROPPED** until it has had at least **3 search cells**, at least one with `controls: <a named rival>`
  in its header and at least one with `conditional: <a regime or conditional split>` (high/low vol, trend/range, a session,
  a sign condition — whatever the mechanism says should matter), its posterior is below its prior, and DECISIONS.md says
  `drop H<n>: <reason>`. `gate.py` enforces all of it.
- **Every lead gets an answer.** Every search result has a `suggests:` line: each lead it names becomes a child hypothesis
  (`H<n>`) or gets `not pursued: <reason>`; `none` only if it truly suggests nothing. The judge reads the result text for
  leads the line skipped.
- **No early "nothing left".** S1 cannot fire before 20 cells or 90 minutes. If every hypothesis is resolved before that,
  go back to OBSERVATIONS.md and the `suggests:` lines and open new hypotheses.

**A. Search cells** — as many as the run wants, on any TRAIN slice, for any OPEN hypothesis.
1. **Pick** by the largest expected belief shift (above).
2. **`cells\cell_NN_rule.md` first**, with the header `gate.py` parses:
   ```
   hypothesis: H<n>
   slice: <EXPLORE | C<j> | C1, C2 | CONFIRM | TRAIN>      # TRAIN = EXPLORE + every fold; never VAL
   kind: search
   controls: <the rival this look controls for | none>
   conditional: <the regime / conditional split this look uses | none>
   method: <M<n>>        # optional; required on the first cell of every SOURCE-born hypothesis in modes B/C
   ```
   then what is looked at and why, the 14c menu row and tool, and the evidence weight of each outcome (above).
3. **`cells\cell_NN_announce.md`** in the 14c template; **run the cell** (guard for every load, plot + tables, `ATTEMPTS.md`
   row).
4. **`cells\cell_NN_result.md`**, starting with:
   ```
   weight_applied: <w after the cap>
   variants: <n>        # distinct specs this cell evaluated (every grid point, subset, horizon) - the K the user deflates by
   suggests: <H<n>[, H<m>] | not pursued: <reason> | none>
   ```
   then what it showed against the rule.
5. **Update `BELIEFS.md`** (posterior, evidence line, state) and **spawn** any child the cell suggests (parent named,
   `born_on` = this cell's slice + cell, its own anchored prior).

**B. Freeze** — when a search has found a spec worth checking, write `candidates\F<n>.md` and do not edit it again:
```
hypothesis: H<n>
variant_of: <none | F<k>>
spec: <exactly what is computed: columns, statistic, every parameter, universe, horizon, conditioning, the slices it was
       built on — enough for the user to re-run it on TEST without asking>
construction: <point-in-time inputs only; trailing-only scaling (no full-sample z-scores or ranks); tail handling
       stated; raw AND market-neutral versions; the signal's correlation with the market reported>
pass_rule: <three branches with numbers: supported if ..., refuted if ..., else inconclusive>
min_useful: <the smallest effect worth keeping, e.g. |rank IC| 0.02 — `supported` requires significance AND this size>
cost_line: <turnover x round-trip cost vs the gross effect -> STANDALONE (clears cost alone) | COMBINE-ONLY (real but
       too small or too costly alone)>
```
**Supported = significant AND at least `min_useful`.** An effect that is significant but smaller is `inconclusive`, never
`supported`. (A v3.0 run reached "supported" on an effect half its own threshold.) **Cost never decides a branch:** a
real-but-small signal is exactly what a later combination stage needs, so cost only sets the STANDALONE / COMBINE-ONLY
label. (A v3.1 run's cost-based rule threw such signals away; carried over from the cloud v3.2 of 2026-10-06.)

**C. Confirm cell** — the frozen spec run unchanged on each CONFIRM fold, judged per fold by its `pass_rule`. Header
`hypothesis: H<n>`, `slice: CONFIRM`, `kind: confirm`, `candidate: F<n>`. The result starts with `weight_applied: <w>` and
`folds: C1=<branch>, C2=<branch>, C3=<branch>`. The candidate is **CONFIRM-SHOWN** with at least 2 folds supported and none
refuted; otherwise **CONFIRM-FAIL** (back to search, or drop). One confirm cell per frozen spec — the folds were already
open to search, so this cell's job is the per-fold shape and one capped belief update.

**D. VAL cell** — for every CONFIRM-SHOWN candidate, before the session ends. Header `hypothesis: H<n>`, `slice: VAL`,
`kind: val`, `candidate: F<n>`, `spec_sha256: <sha256 of candidates\F<n>.md>`. The rule file copies the `pass_rule`
verbatim, states the weights, and quotes VAL_NOTE from TARGET.md. The result starts with `weight_applied: <w>` and
`branch: <supported | refuted | inconclusive>`. One VAL check per frozen spec; no change to the spec, the threshold or the
universe because of what VAL showed.
- **VAL-PASS** -> a `## F<n>` block in `TEST_REQUESTS.md` (Phase 3). Never described as out-of-sample proof.
- **VAL-FAIL** (refuted or inconclusive) -> the run may return to search on TRAIN. A new spec found there is a new candidate
  with `variant_of: F<n>`; say in its first search cell what changed and why.

---

## STOP RULES — a session ends ONLY when one of these fires; write `STOP_REASON.md` naming which, with the numbers

- **S1 — nothing left open.** Every hypothesis in `BELIEFS.md` is DROPPED or CHECKED, and the run has used at least 20 cells
  or 90 minutes.
- **S2 — dry.** The last 8 cells were search cells and none of them led to a frozen candidate.
- **S3 — hard cap.** 60 cells (Phase 0 cells don't count) OR 3 wall-clock hours, whichever comes first.

Before any stop, every frozen candidate has had its confirm cell and every CONFIRM-SHOWN candidate its VAL cell — those
are owed, and `gate.py` refuses a session that leaves one behind. Not allowed: stopping on a single bad result; stopping
because a hypothesis "felt" exhausted without a stated S1-S3.

### `STOP_REASON.md` format — fixed, so `gate.py` can check the claim

```
rule: S1 | S2 | S3
open_count: <n>          # BELIEFS.md entries with state: OPEN, at the moment of stopping
dropped_count: <n>
frozen_count: <n>        # candidates\F*.md files
val_pass_count: <n>
minutes: <wall-clock minutes since the run started>
detail: <one line — S2: the 8 cells; S3: cells used / minutes elapsed>
```

---

## PHASE 3 — close

1. **`TEST_REQUESTS.md`** — one block per VAL-PASS candidate, for the user. The routine never opens TEST.
   ```
   ## F<n> — <title>
   spec_sha256: <same as its VAL cell>
   hypothesis: H<n> (NO-STORY: yes|no)
   variant_of: <none | F<k> — and how many variants its family had>
   confirm: C1=..., C2=..., C3=...
   val: <cell_NN, the deciding number vs the pass rule, VAL_NOTE>
   k: K_train <n>, K_val <n>, K_cum_train <n>, K_cum_val <n>
   label: <STANDALONE | COMBINE-ONLY>      # from the cost line
   turnover: <per day> ; cost_line: <gross vs cost>
   correlations: <with the market, with simple baselines (momentum, reversal, volatility), and with every other
                  VAL-PASS candidate — so a later combination stage knows what is new>
   test_check: <the pass_rule, to run unchanged on TEST>
   ```
   The routine never combines signals or fits weights; it hands them on with what a combiner needs.
2. **`REPORT.md`**, one page: source mode and item used; the belief table (hypothesis, prior -> posterior, the evidence chain with kind and slice per cell, state, children,
   candidates); the candidate
   table (F, hypothesis, variant_of, per-fold CONFIRM branches and effects — the decay shape — VAL branch and number); the cost
   line for everything that reached VAL; K_train, K_val, K_cum_train, K_cum_val; one part-0 `1b finding` block per candidate
   that reached VAL; leads (NO-STORY entries, observations not chased).
3. **The job's product** (JOB_<job>.md): `DATA_PROPOSALS.md` + `SOURCES.md` (data); rows in `features\REGISTRY.md` +
   code (features); rows in `toolbox\REGISTRY.md` + validation files (methods). gate.py checks that every frozen candidate
   is tied to its row or block.
3b. **`INBOX_PROPOSALS.md`** — any new idea/paper/group worth a future session goes here, never written into `INBOX.md`
   directly (the human merges it).
4. **Memory** (MEMORY section above): append this run's one `LEDGER.md` row (`methods_score: pending`), its `FINDINGS.md`
   entries and one-line lists, and any new `DATA_FACTS.md` lines; consolidate first if a file would pass its budget.
5. Run `gate.py`; it must print PASS. Then the judge. Copy the judge's `METHODS_SCORE` into this run's LEDGER row
   (replacing `pending`) and its verdict block into REPORT.md verbatim.
6. Mark the consumed inbox item(s) `used <run folder>` in `INBOX.md`. Increment this mode's count in `MODES.md`.
7. Set `TARGET.md` STATUS to `DONE <run folder>` — but only if `gate.py` passed. If it fails, fix what it names and re-run
   the check; do not write DONE around a failing gate.

---

## ENFORCEMENT

- **`C:\Users\User\eda-routine\gate.py`** — deterministic. Run it (`python gate.py <run_dir>`) before `STATUS: DONE` may be
  written; it must print `PASS`. Checks: every required file/section from Phases 0-3 exists; `SPLITS.md` declares EXPLORE, at
  least 2 ordered non-overlapping CONFIRM folds and VAL; every rule file predates its result and carries its header; every
  `BELIEFS.md` entry has its fields (prior, anchor, posterior included) and nothing is born on VAL; every posterior equals
  its prior times the `weight_applied` chain, each weight within its cap (3x search, 10x confirm/VAL); no DROPPED hypothesis
  without 3 search cells, a rival controlled, a conditional split, a fallen posterior and a `drop` line; every search
  result has a `suggests:` line naming only real hypotheses; S1 not before 20 cells or 90 minutes, S3 not under its cap; no search cell names VAL; every search result counts its
  `variants`; every confirm and VAL cell names a `candidates\F<n>.md` that existed before the cell, with all its fields; a
  confirm result covers every fold; VAL only for a CONFIRM-SHOWN candidate, once per spec, with a `spec_sha256` matching the
  file as it is now; no confirm or VAL check owed at the end; CHECKED hypotheses really have a VAL result; every VAL-PASS in
  `TEST_REQUESTS.md` with the matching sha; `STOP_REASON.md`'s counts and S1-S3 claim match the run; a `mode:` line in
  DECISIONS.md, and a `job:` line with the job's product in place (JOB files); every non-base import has a pinned, validated INSTALLS.md row from PyPI/conda-forge; in modes B/C a complete
  METHOD_SPEC.md and a cell citing it for every SOURCE-born hypothesis; exactly one LEDGER row with K_train and K_val at
  least what the cells show and both K_cum carried per dataset; FINDINGS entries and one-line lists; every MEMORY file inside
  its budget. If it prints `FAIL`, fix what it names — do not edit a result or candidate file to make an mtime or sha check
  pass; fix the process defect it's pointing at.
- **`eda-v3-judge` agent** (`C:\Users\User\eda-routine\.claude\agents\eda-v3-judge.md`) — read-only, run AFTER `gate.py`
  passes. Checks what `gate.py` cannot: that no search cell's code read VAL rows; that each evidence weight's power/alpha was real and
  correctly applied; that `suggests:` answers every lead the result text names; that `variants` honestly counts what each
  search evaluated; that VAL cells ran the frozen spec exactly as written; that variants after a VAL failure were found on
  TRAIN and logged as variants; that pass rules carry a real size condition; the stop; tool fitness, method fidelity and
  memory discipline, with a `METHODS_SCORE` 0-3. Returns PASS/FAIL with numbered issues; a FAIL is read by the human review
  that follows every `DONE`.

Run both at the end of Phase 3, in that order.

---

## NEVER
Search on VAL, or load a VAL row in a search cell; change a frozen spec after its confirm or VAL cell (write a new candidate
instead); check a spec on VAL that has not held on CONFIRM; open TEST, or ask for TEST data; under-count `variants`; call a
significant-but-too-small effect "supported"; skip a belief update; let a cell move odds past its cap; drop a hypothesis
before the effort floor; leave a lead without an answer; describe a VAL pass as out-of-sample proof; use a package with no validated
INSTALLS.md row; deviate from a source's method without saying so in METHOD_SPEC.md; install a package that no cell uses;
write results into DATA_FACTS.md or more than 3 lines per finding into FINDINGS.md; stop with a check owed; build a generic
`eda.py`.
