### Cell 28 — VAL: does H1 (Alpha#101) hold on VAL?

**Sub-claim being tested:** H1 top-minus-bottom next-day spread >= 20 bp/day on VAL (cell_28_rule.md).
**Why it matters:** the last look RUNBOOK_v3 allows this session; HIGH-CONFIRM -> HIGH-VAL only if supported.
**Test(s) used:** 2-bin quantile sort, NW(5) SE.
**Decision rule before running:** supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645; else
inconclusive. Weights 2.653 / 0.914 / 1.
**VAL_NOTE:** quoted in the rule file and the result file.
**Data loaded:** VAL only (signal inputs + 40-day lookback buffer that lies in the embargo/C3 tail; responses inside VAL).
**Decisions I need from you:** none (unattended; RUNBOOK Phase 3 authorises one VAL opening for HIGH-CONFIRM).
