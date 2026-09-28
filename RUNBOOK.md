# EDA RUNBOOK v2: follow skill 14c-eda.md TO THE LETTER, unattended

THE METHOD IS C:\Users\User\backtest_engine\backtest_engine2\skills\14c-eda.md. This runbook does NOT replace or reinterpret it.
It adds only: (1) the unattended substitutions, (2) the holdout rules, (3) the two additions that Step 1b of
finding-alphas\part-0-daily-workflow.md puts on top of 14c (cheap cost sanity; the decay-first gate), (4) where files go.
Where this runbook and 14c seem to differ, 14c wins, EXCEPT the HOLDOUTS section, which always wins.
(The previous sweep-every-row runbook is kept as RUNBOOK_v1_sweep.md. Do not follow it.)

READ IN FULL FIRST, in this order (14c itself says to read the first three before any cell):
  TARGET.md; C:\Users\User\backtest_engine\backtest_engine2\PROTOCOL.md; ...\skills\00-overview.md;
  ...\skills\12-alpha-overview.md; ...\skills\14c-eda.md; C:\Users\User\finding-alphas\data-hygiene.md;
  and, for crypto, C:\Users\User\eda-routine\HOLDOUT_RULES.md.

UNATTENDED SUBSTITUTIONS. 14c and PROTOCOL assume a human who confirms every cell. Nobody is here, so:
  - "Announce the cell and wait for confirmation" -> write the FULL announcement (the 14c Step-3 template) to
    cells\cell_NN_announce.md BEFORE any code for that cell exists, then proceed.
  - "Decisions I need from you" / "stop and ask" -> write the question and the CONSERVATIVE default in DECISIONS.md and take the
    default. This covers heavy dependencies (PyMC, ruptures, deepgraph, ...): 14c says stop and ask, so DO NOT INSTALL them;
    skip that tool, log it, and use a listed alternative. Only if TARGET.md has a PRE-APPROVED INSTALLS line is the question
    already answered: install just those packages, just into C:\Users\User\eda-routine\.venv, and log versions.
  - "Confirm the net status before signal_construction" -> there is no signal_construction here. Write the net status; a
    human confirms it later.
  - If you cannot proceed safely: write STOPPED.md with the reason, set TARGET.md STATUS to STOPPED <run folder>, and end.

SCOPE (14c "What does NOT belong here"): EDA only. No backtest, no signal, no PnL, no validation of signal output, no plot with no
claim attached. Write only inside the run folder. Never touch alpha_log.md, live strategies, MT5 or the raw data.

HOLDOUTS (strict). You have been given TRAIN and VAL only. There is NO TEST set in what you were given; do not look for one.
  - Your data lives ONLY under C:\Users\User\eda-routine\data\<name>\ and has a CUT.json (made by prep_target.py). If TARGET.md
    points anywhere else, write STOPPED.md.
  - NEVER open, list or read anything under C:\Users\User\backtest_engine\backtest_engine2\data\. That folder holds TEST and
    sealed data you are not to see. Do not load a "fuller" version of a file you were given.
  - If you ever see a row later than VAL_END, write STOPPED.md and report it: the preparation failed.
  - If a sub-claim would need data you were not given, it is UNTESTED. Never ask for more data.
  - Crypto: read C:\Users\User\eda-routine\HOLDOUT_RULES.md before opening any file. Do NOT read
    C:\Users\User\backtest_engine\backtest_engine2\_SEALED_HOLDOUT.md: it contains RESULTS of earlier hunts and records of
    breaches. If TARGET.md or any file you were told to read names an earlier hunt's hypothesis or result, say so in DECISIONS.md
    and do not let it steer which tests you run.
  - TRAIN is for every cell. VAL is opened ONCE, at step 7, as the "Replication" row of the 14c floor.

BROWSER (allowed, narrow). You MAY use the user's Chrome through the Claude-in-Chrome tools, ONLY on ssrn.com (papers.ssrn.com) and
*.substack.com, for exactly these purposes: (1) in step 1, to SEARCH those sites and go through papers or posts to find ONE
hypothesis when TARGET.md's HYPOTHESIS is "SEARCH" or blank; (2) to read the exact claim, definitions, horizon or method of a source
named in TARGET.md or picked by you; (3) the definition of a method 14c does not spell out. No other browsing.
  - Read-only. Open your OWN new tab (call tabs_context first), never touch the user's other tabs, close your tab when done. Do not
    log in, enter credentials, download paid content, post, comment, subscribe or click anything that changes state. If a page needs
    a login, a paywall or a captcha, stop using it and log that in DECISIONS.md. Do not trigger browser dialogs.
  - Any other website: not allowed. If you feel you need one, log the question in DECISIONS.md and go on without it.
  - Time-box it: at most 12 page loads per run (searches and result pages count). Log every page in DECISIONS.md: URL, why, and the
    sample period the source reports.
  - HOLDOUT RULE FOR SOURCES: a source is for the CLAIM and the METHOD. Its reported RESULTS are not evidence in this run, and above
    all NOT for any period after TRAIN_END. Do not copy its numbers into a cell, a decision rule or a prior. If its sample period
    overlaps VAL, VAL is soft-clean for that claim: say so in DECISIONS.md and next to the VAL result. If you notice results for
    periods after VAL_END, write down that you saw them and do not let them steer any test.
  - The source's story is the hypothesis's story: it feeds the floor rows "assumption" and "side bets"; it does not license a new one.

THE RUN. Each item names the 14c step it comes from.

0. DATA CARD (not in 14c; data-hygiene requires it). DATA_CARD.md: files, rows, date range, timezone, what each column IS
   (trade/bid/ask/mid), venue, knowable-when, whether a timestamp is a bar's OPEN or CLOSE (check it; do not assume). Cannot fill
   it in -> STOPPED.md. Returns from MID where quotes exist, never one side of the book; returns not levels; never pool feeds; no
   silent fills. Record TRAIN_END / VAL_START / VAL_END from TARGET.md in ATTEMPTS.md. No splits -> STOPPED.md.

1. GET THE HYPOTHESIS (part-0-daily-workflow.md Step 1: pick a SOURCE, get one claim, state it in one sentence).
   14c is hypothesis-driven, so nothing after this step starts without one.
   a. If TARGET.md gives a HYPOTHESIS, use it verbatim and skip to step 2 (you may open its named source, see BROWSER).
   b. If it says SEARCH or is blank, FIND one on SSRN or Substack, AFTER the data card, so a claim can be tied to the carded columns:
      - BEFORE opening the first page, write a DECISIONS.md entry: which site, the search terms, and why (the part-0 rule: "a source
        picked silently is a source picked badly").
      - Search, and go through papers or posts. Pick EXACTLY ONE claim. Consider at most 3 candidates; log the ones you reject and why.
      - The claim must be testable with ONLY the carded columns, the time window and the resolution you have. If it needs data you
        do not have (order book, options, on-chain, another asset), reject it.
      - It must not be a claim listed under TARGET.md's ALREADY TESTED line.
      - It must have an economic reason (part-0: "no economic reason -> drop it"). A pattern with no reason is not a hypothesis.
      - Write it in the part-0 form, naming carded columns EXACTLY:  "a change in [column(s)] predicts [price response over a stated
        horizon] because [the source's economic reason]".  Record source, URL and the source's sample period.
      - A claim you could not turn into that sentence is not found: write STOPPED.md.
   The result of step 1 is ONE sentence. Treat it exactly like a human-supplied hypothesis from here on.

2. 14c STEP 1: DECOMPOSE. Write DECOMPOSITION.md:
   - the hypothesis copied VERBATIM from TARGET.md;
   - the table  # | Sub-claim | Falsifiable by  with atomic, falsifiable sub-claims C1..Cn; every "Falsifiable by" carries a number;
   - THE DECOMPOSITION FLOOR: all ten questions (existence, assumption, impostor, attribution, the effect, the mechanism's side
     bets, shape, stability, economics, replication). Each is a row, or is dropped IN WRITING WITH A REASON. Then add the rows
     specific to THIS claim: "a decomposition containing only these ten has probably not thought hard enough";
   - the story is TESTED, not extended: the "assumption" and "side bets" rows test the reason TARGET.md gave. Do not invent a
     different mechanism;
   - declared BEFORE any test: which sub-claim is the Replication row and opens VAL, with its rule.

3. 14c STEP 2: PICK TOOLS. For each sub-claim name its claim type from the 14c menu and list that row's tools. EXHAUSTIVE WITHIN THE
   HYPOTHESIS: run EVERY tool in the matching row(s), one after another, until the tests give a consistent picture. A tool is
   skipped only as N/A with a reason tied to this data, or under the dependency rule above. A tool outside the menu is allowed only
   if its cell says which claim it tests. Standing cautions: returns not levels; never diagnose one side of the book. Do NOT test
   claims outside the hypothesis (calendar effects, regimes, PCA...) "for interest": list such patterns under "Observations not in
   the original hypothesis" and never chase them.

4. 14c STEP 3: ONE CELL PER SUB-CLAIM, in dependency order. For each cell:
   a. cells\cell_NN_announce.md FIRST, in the 14c template, including "Decision rule before running": supported if ... / refuted if
      ... / inconclusive if ... WITH NUMBERS;
   b. then the code;
   c. every cell ends with a saved plot, plots\NN_slug.png, titled with the takeaway and the number (part-0 Step 1b, PROTOCOL 5.1),
      plus tables\NN_*.csv for every table you quote;
   d. state the result against the pre-committed rule; do not soften the verdict;
   e. refuted, for a sub-claim the hypothesis cannot survive without -> STOP THE HUNT and go to step 6. Supported -> next.
      Inconclusive -> ONE tighter test, or accept and flag;
   f. log every look in ATTEMPTS.md (recorded, never capped). Disagreement between tools is itself an observation: investigate, do
      not average it away.

5. STEP 1b ADDITIONS (part-0-daily-workflow.md):
   a. CHEAP COST SANITY: compare the effect with the round-trip cost. If TARGET.md gives no cost, write "cost UNKNOWN" and mark the
      economics row UNTESTED. If it gives one and the effect is not the same order of magnitude, stop the hunt.
   b. DECAY-FIRST GATE: split TRAIN into eras and read the effect era by era, NEVER pooled first. Classify: monotone decay /
      flat or strongest-recent / alternating. Monotone decay and alternating are kills.

6. 14c STEP 4: HYPOTHESIS-UPDATE CELL (non-code), in exactly the 14c template: Original hypothesis; Sub-claims tested
   (supported / refuted / inconclusive + one-line evidence); Net status (a) stands, (b) partially holds and narrows to <subset>,
   (c) refuted in this data; Observations not in the original hypothesis (candidate future hunts, do not chase); and "Decisions I
   need from you: confirm the net status".

7. REPLICATION ON VAL (14c floor #10). Open VAL ONCE, for the sub-claim(s) declared in step 2, with rules written first. Report it
   even if it fails. Quote TARGET.md's VAL_NOTE beside every VAL result. A VAL result is never described as "out-of-sample proof".

8. REPORT.md, one page: the hypothesis; the net status; the sub-claim table (verdict, deciding number, plot); the decay-first shape;
   the cost line; what died, with the number; what is still untested; and Part-0's "1b finding" block:
       1b finding - <claim>   [source: <TARGET.md>]   [ledger: ALPHA|METHOD]
         C1 <sub-claim> - supported | REFUTED (<number>)
         decay-first: <decaying | flat | strongest-recent | ALTERNATING>  <era numbers>
         cost: edge/cost = <x> or UNKNOWN     K so far: <n>     notebook: <run folder>
         still untested: <what a later pass would have to do to overturn this>
   Every factual line cites a plot or table plus a number, or is stamped UNTESTED.

NEVER (14c "What NOT to do"): run EDA as a "show what you can do" exercise; present a finding without a pre-committed decision rule;
silently ignore a refuted sub-claim; chase observations outside the hypothesis; build a generic eda.py.
