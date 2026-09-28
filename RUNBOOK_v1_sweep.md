# EDA RUNBOOK: an unattended run of the repo's EDA step (skill 14c)

Unattended. Where the normal loop says "ask and wait", write the decision and reason in DECISIONS.md and take the
conservative option. If you cannot proceed safely, write STOPPED.md with the reason and end.

READ IN FULL FIRST: TARGET.md; C:\Users\User\backtest_engine\backtest_engine2\skills\14c-eda.md;
C:\Users\User\finding-alphas\data-hygiene.md; the plot convention in
C:\Users\User\backtest_engine\backtest_engine2\PROTOCOL.md §5.1.

SCOPE: EDA only. No backtest, no signal, no cost-model run. Write only inside the run folder. Never touch
alpha_log.md, live strategies, MT5 or the raw data. DO NOT write mechanisms or stories: your job is to find leads
and check them. A result you cannot explain is reported as "unexplained".

HOLDOUTS (strict). You have been given TRAIN and VAL only. There is NO TEST set in what you were given, and you must
not look for one.
  - Your data lives ONLY under C:\Users\User\eda-routine\data\<name>\ and has a CUT.json (made by prep_target.py).
    If TARGET.md points anywhere else, write STOPPED.md.
  - NEVER open, list or read anything under C:\Users\User\backtest_engine\backtest_engine2\data\. That folder holds
    TEST and sealed data you are not to see. Do not load a "fuller" version of a file you were given.
  - If you ever see a row later than VAL_END, write STOPPED.md and report it: something in the preparation failed.
  - If a lead would need data you were not given, report it as UNTESTED. Never ask for more data.
  - Crypto: read C:\Users\User\eda-routine\HOLDOUT_RULES.md before opening any file. Do NOT read
    C:\Users\User\backtest_engine\backtest_engine2\_SEALED_HOLDOUT.md: it contains RESULTS of earlier hunts and records of
    breaches, and reading them would contaminate your exploration. If TARGET.md or any file you were told to read names an
    earlier hunt's hypothesis or result, say so in DECISIONS.md and do not let it steer which tests you run.

STEP 0  DATA CARD. Write DATA_CARD.md: files, rows, date range, timezone, what each column IS (trade/bid/ask/mid),
        venue, knowable-when, and whether the timestamp is a bar's OPEN or CLOSE time (check it; do not assume).
        Cannot fill it in -> STOPPED.md. Returns from MID where quotes exist, never one side of the book; returns not
        levels; never pool feeds; no silent fills.
STEP 1  SPLIT. TARGET.md gives TRAIN_END, VAL_START, VAL_END. Explore on TRAIN only (<= TRAIN_END). VAL is opened
        ONCE, at Step 6. Rows between TRAIN_END and VAL_START are an embargo: ignore them. No splits in TARGET.md ->
        STOPPED.md. Record the dates in ATTEMPTS.md.
STEP 2  TOOL SWEEP. Go through EVERY row of the 14c Step-2 table, in order, one after another. TOOL_LOG.md gets an
        entry per row: RUN (tool, series, plot file, one-line result) or N/A (a reason that refers to THIS data).
        A row with no entry = incomplete run. Extra tools are allowed if the entry names the observation they serve.
        Before each run write one line: "counts as an observation if ...". TRAIN only.
        Every tool run ends with a saved plot plots/NN_slug.png titled with the takeaway and the number, plus
        tables/NN_*.csv. No plot = it does not count. Log every look in ATTEMPTS.md. The sweep GENERATES leads, it
        proves nothing: count K = number of tests run.
STEP 3  OBSERVATIONS. List what looks non-random (OBS1..n), including disagreements between tools; report those,
        do not average them away.
STEP 4  CHECK each observation against the boring explanations. Eliminate, do not explain:
        (a) twin: does it survive after conditioning on volatility and on trailing return?
        (b) artifact: spread clock, stale prices / zero-return runs, session / DST / rollover hour, one outlier day
            carrying it (drop the top 1% of moves and re-measure).
        (c) luck: adjust for the K tests (Benjamini-Hochberg across the sweep's p-values).
        (d) stability: era by era WITHIN TRAIN, NEVER pooled first. Classify: decaying / flat / strongest-recent /
            alternating.
        (e) size: the effect in bp; compare with a round-trip cost only if TARGET.md gives one, otherwise "cost unknown".
        Use an autocorrelation-robust interval for every effect. Plot each check.
STEP 5  RANK (Bayes). For each observation that survives Step 4: PRIOR = base rate for that KIND of claim.
        Direction/mean-return claims start LOW: this programme measured negative out-of-sample R2 for direction and
        mean across 445 series; only the SIZE of moves (|return|, volatility) has been forecastable. Then prior odds
        x likelihood ratio = posterior odds, arithmetic shown, the ratio taken from your measurement and discounted for
        K. This ranks what the human should check first; it does not decide anything.
STEP 6  CONFIRM ON VAL. Open VAL ONCE, for the top 3 leads, rules written first (supported if / refuted if /
        inconclusive if, each with a number). Report it even if it fails. If TARGET.md has a VAL_NOTE, quote it beside
        every VAL result. A VAL result is never described as "out-of-sample proof".
STEP 7  REPORT.md, one page: table [lead | as a testable claim | effect (bp) + interval | K-adjusted p | eras (TRAIN) |
        posterior | VAL result | plot]; then what died, with the number; then the full tool-log summary.
        Phrase each lead as "a change in X predicts Y" or "distribution of Z differs by W", ready for the engine.
        Every factual line cites a plot or table plus a number, or is stamped UNTESTED. Observations for future
        hunts go in a separate list: do not chase them now.

A null result is valid and useful. If nothing survives Step 4, say so plainly. Do not stretch the analysis to find something.
