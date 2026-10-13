# Session notes, 2026-10-13: v3.3 done, next = split into three jobs

Hand-off for continuing on cloud. What was decided, what was built, what's open.

## 1. Built and committed this session: v3.3 "signal engine"

The user wants a signal engine, not a referee. Overfitting rigor (stress tests, deflation) is the user's later step.

- **Search only on TRAIN** (EXPLORE + CONFIRM folds), unlimited looks: re-look, tweak, grids, regime splits.
- **VAL and TEST are only for checking** frozen specs, never for searching. Any number of checks, each spec once.
- **Freeze before checking:** `candidates/F<n>.md` (spec, pass_rule with a size condition, size + cost line). Confirm cell
  runs it unchanged per fold (>= 2 supported, 0 refuted = CONFIRM-SHOWN), then VAL cell with the spec's sha256.
- After a VAL fail the run may re-search TRAIN; a new spec is a new candidate with `variant_of`.
- **TEST is never opened by the routine.** VAL passes go to `TEST_REQUESTS.md` for the user (user chose option b).
- **K always counted, never capped:** K_train (search `variants:` + confirm runs) and K_val, with K_cum per dataset in
  MEMORY/LEDGER.md.
- **Prior -> posterior updating after EVERY cell is essential and must never be removed** (user was explicit). Search cells
  cap at 3x odds, confirm/VAL at 10x. Picks go by largest expected belief shift. gate.py recomputes the chain.
- **Not lazy (gate-enforced):** no DROP before 3 search cells incl. a `controls:` rival and a `conditional:` split, a fallen
  posterior and a `drop H<n>: reason` line; every search result has `suggests:` (lead -> H<n> or `not pursued: reason`);
  S1 not before 20 cells / 90 min; S3 cap 60 cells / 3 h; S2 = 8 dry search cells.
- Files: RUNBOOK_v3.md, gate.py (+ 63 tests passing), .claude/agents/eda-v3-judge.md, DESIGN_v3.md (v3.3 amendment),
  HOLDOUT_RULES.md rule 2, MEMORY/LEDGER.md (K split), MEMORY/FINDINGS.md header.
- Old runs (4) are in the pre-v3.3 format and do not pass the new gate. Expected.

## 2. Next: one routine, three jobs (the user's design — build this)

From a podcast: alpha today comes from (1) the data you can get, (2) what you do with it (features/transforms),
(3) the tech/methods used to process it. The user wants the routine organised around exactly these three.

**One routine, easy to maintain:** `TARGET.md` gets a `JOB:` line that picks the runbook. Each job has its own runbook.
The v3.3 core (TRAIN-only search, VAL checks, never TEST, priors updated every cell, K counted, effort rules, gate.py)
is shared by all three.

1. **Data job** (`JOB: data`) — find data with predictive power "in the vast ocean of data out there". The user will add
   source material to guide it. **NO cleaning duties** — only light prep needed to test predictiveness. Output: ranked
   dataset proposals (source, how to get it, what it predicted, how strongly, incremental over data we already have).
   The user cleans the winners.
2. **Features job** (`JOB: features`) — on data we already have, engineer as many predictive features as possible; test
   predictive power AND orthogonality to each other / the existing library. Output: a feature library (code, definition,
   predictive power, correlation/overlap, where tried, K).
3. **Methods job** (`JOB: methods`) — either apply methods already in the library/toolbox to our data, or look for recent
   advancements / new algos and try them. Each tool validated on synthetic data with a planted answer first.

## 2b. Decided later the same day

- **Target:** the goal is always alpha/beta, so the user doesn't pick a target per run. Default: the forward return of the
  dataset's main instrument(s), at horizons the run declares (each horizon tried counts in K). TARGET.md may override.
  (Priors are beliefs about hypotheses; they don't change the target.)
- **Modes A-E stay**, as "where ideas come from", inside every job (e.g. a papers-mode methods run = an algo from a paper).
- **Merged in** the cloud runs from branch claude/friendly-volta-rq2l22: 2026-10-05_crypto-validated-1h (E),
  2026-10-05_crypto-101alphas (B), 2026-10-06_crypto-101alphas-b2 (B) + LEDGER/FINDINGS/DATA_FACTS/MODES/INBOX. Their
  data bundle (249 MB) is NOT merged into git; it lives in that branch and locally under data/.
- **Folded into v3.3 from that branch's own v3.2:** supported = significant AND >= min_useful (cost only labels
  STANDALONE / COMBINE-ONLY); power-sim noise measured on seen data; signal construction floor; TEST_REQUESTS carry
  label, turnover, correlations. 65 gate tests pass.
- Those runs are more evidence for v3.3: all stopped on "slices exhausted" after 14-28 cells / ~25-30 minutes.

## 3. Open questions (original wording; see 2b for answers)

1. **Predictive of what?** Data and features jobs need a target (e.g. US500 next-day return). Proposed: TARGET.md names it
   per run.
2. **What happens to the 5 source modes** (A ideas, B papers, C paper groups, D lens, E data-only)? Proposed: drop them as
   divisions; INBOX.md gets one section per job for the user's source material (data pointers -> data job, papers on
   algos -> methods job, etc.).
- Also to check: data job downloading from the internet — which sources are allowed, and the holdout rule for new data
  (screen on TRAIN dates only).

## 4. Other things noticed

- `ROUTINE_PROMPT.md` still tells the routine to follow `RUNBOOK.md` (v2), not `RUNBOOK_v3.md`. Check the app's saved
  prompt at `~/.claude/scheduled-tasks/eda-routine/SKILL.md` — runs may not be using v3.
- FTMO US500 prep work (clean_ftmo_us500_*.py, prep_ftmo_us500.py, rules/, tools/) is still uncommitted on the local
  machine, not on GitHub. HOLDOUT_RULES.md's US500 split/seal lines were committed with v3.3.
- TARGET.md still shows `DONE` for the BTC perp run; no US500 target written yet.
