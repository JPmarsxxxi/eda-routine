# JOB: methods — new tools, algorithms and techniques (v3.4)

Read RUNBOOK_v3.md first: every core rule there applies (TRAIN-only search, VAL only for frozen specs, never TEST, priors
updated after every cell, K counted, effort floors, gate.py). INSTALLS AND METHODS there applies in full. This file says
only what is different for this job.

**The job.** Get more out of data we already have by processing it better. Two routes, either or both in one run:
1. **Apply** a method already in `toolbox\REGISTRY.md` to data or features it has not been used on.
2. **Find and try** recent advancements — new estimators, models, transforms, algorithms (papers via `INBOX.md` §B/§C or
   the browser rules of the core; established libraries on PyPI/conda-forge).

Typical ground: regime models (HMM, Markov switching), change-point detection, nonlinear and conditional estimators
(quantile/threshold regression, gradient boosting with honest folds), signal processing (wavelets, filters), volatility
models (HAR, GARCH families), cross-sectional methods (Fama-MacBeth, shrinkage), representation learning on returns.

## Validate before it touches market data

Every method gets a validation cell first: it must recover a planted answer on synthetic data built for the use (a known
regime path, a planted break, a known nonlinear response). Fail -> it is not used, and the failure is logged in the
toolbox row with `result: FAIL` so no run tries it the same way again.

## What a hypothesis is here

`hypothesis:` "[method] on [data / features] extracts [effect] that [the baseline] misses, because [why the structure is
there]". The **baseline** is the plain tool a run would otherwise use (linear IC, trailing-vol split, OLS). Every search
cell reports method vs baseline on the same data, and `min_useful` applies to the **lift** over the baseline, not to the
raw effect. A method that only matches the baseline is not a finding.

## Freeze, confirm, VAL

Freeze with `method_id: <toolbox id>` and `baseline: <what it is compared with>` in `candidates\F<n>.md`; every fitted
parameter is fitted on TRAIN only and written into the spec (a model refitted on VAL is a VAL search, which is forbidden).
Confirm and VAL as in the core, reporting method and baseline side by side.

## Product — `toolbox\`

- `toolbox\REGISTRY.md` — one row per method (gate.py parses it):
  ```
  | id | what | package | version | source | validation | result | beats | runs |
  |---|---|---|---|---|---|---|---|---|
  | hmm2 | 2-state Gaussian HMM on daily returns | hmmlearn | 0.3.2 | pypi | toolbox/hmm2_validation.md | PASS | trailing-vol median split (+0.015 IC, C1-C3) | <run> |
  ```
  `beats`: the baseline it beat and by how much, or `-`. `runs`: every run that used it.
- `toolbox\<id>_validation.md` — the planted-answer test and its result, so later runs reuse the method without
  re-validating the same version.
- Methods that need an install still get their INSTALLS.md row in the run folder (core rule).
