# JOB: data — find data with predictive power (v3.4)

Read RUNBOOK_v3.md first: every core rule there applies (TRAIN-only search, VAL only for frozen specs, never TEST, priors
updated after every cell, K counted, effort floors, gate.py). This file says only what is different for this job.

**The job.** Search the ocean of outside data for series that predict the target, beyond the data we already have. Guided
by the user's pointers in `INBOX.md` §S (always read) and by the picked source mode (A-E). **No cleaning duties.** Do the
minimum needed to test a dataset honestly — align timestamps, cut the holdout, note gaps — and hand the winners to the user,
who cleans them properly.

**The target** is the forward return of the main instrument(s) of the TARGET.md `DATA` bundle, at the horizons this run
declares in SPLITS.md (each horizon tried counts in K). TARGET.md may name a different one. The bundle is the yardstick:
its splits are the splits every fetched series is cut to.

## What a hypothesis is here

`hypothesis:` "a change in [outside series] predicts [target over horizon] beyond [the bundle's own features] because
[economic reason]". Rivals always include "it is a proxy for something the bundle already has" (market return, volatility,
volume, the time of day) — the `controls:` cells partial those out.

## Fetching — rules

1. **Sources:** public data reachable without a login, payment or a key the user has not supplied (official statistics,
   exchange and central-bank APIs, public datasets, academic data pages, sites in `INBOX.md` §S). Respect each site's terms
   and rate limits. No scraping behind logins, no paywalled data, no personal data.
2. **Log every source** in `SOURCES.md` before it is used, one row per dataset (gate.py parses it):
   ```
   | dataset | url | license | fetched | knowable_at |
   |---|---|---|---|---|
   | fred_t10y2y | https://fred.stlouisfed.org/series/T10Y2Y | public domain | 2026-10-13 | daily close + 1 day |
   ```
   `knowable_at` is when a value could really have been known: publication lag, release time, revisions. A series whose
   history is revised (most macro) uses first-release / vintage data where it exists, or says it cannot and lags by the
   publication delay. This is the single biggest way a data scout fools itself; the judge checks it.
3. **Cut before you look.** Save each fetched series under `fetched/<dataset>/data/` (gitignored) and write
   `fetched/<dataset>/CUT.json` with `"max_time"` before any relation to the target is measured. Nothing at or after the
   end of VAL is kept: TEST stays sealed for new data too. Anything sealed in HOLDOUT_RULES.md stays sealed.
4. **Light prep only:** timestamp alignment to `knowable_at`, resampling to the target's clock, a gap note. Anything more is
   the user's cleaning job; say what it would need in the proposal.

## Search and check

- **Screen wide, then narrow.** A first search cell may screen many series at once (count every series x horizon in
  `variants:`). Survivors get their own hypotheses and the usual search (rival controlled, conditional split, effort floor).
- **Incremental, not just predictive.** Every search cell reports the effect after partialling out the bundle's baseline
  features (market, momentum/reversal, volatility at least). `min_useful` applies to that incremental effect.
- **Freeze** with `dataset: <name>` (the SOURCES.md row) in `candidates\F<n>.md`; confirm and VAL as in the core.

## Product — `DATA_PROPOSALS.md`

One block per dataset with a VAL-PASS candidate (gate.py requires it), ranked best first:
```
## <dataset>
source: <who publishes it, series id>
access: <how to get it: URL/API, free or not, history length, update frequency>
knowable_at: <publication lag / revision handling>
target: <what it predicted, horizon>
incremental: <effect beyond the bundle's features, per fold>
val: <cell, number vs pass rule>
label: <STANDALONE | COMBINE-ONLY>
cleaning_needed: <what the user should check when cleaning it properly>
```
Also list, briefly, datasets that looked promising but were not reached, and datasets tried and dropped (one line each), so
the next data run does not repeat them.
