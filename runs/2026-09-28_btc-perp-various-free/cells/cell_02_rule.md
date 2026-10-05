# cell_02 RULE — mandatory REDIRECT cell after H1's refutation (written before any code for this cell exists)

**Trigger (Phase 2 step 8):** cell_01 refuted H1's core sub-claim on CONFIRM (mean D 0.163 bp < 0.25 bp, t 2.18). The
redirect question is "where does the data actually point?": opposite sign, one era only, one funding regime only, or
absent everywhere. Its finding is captured as a NEW child hypothesis (H6) with its own rule file later; H1 is not rewritten.

**Slice: EXPLORE only** (2020-09-01 .. 2021-12-31, where the metrics file exists). This is H1's birth slice, so nothing here
is evidence for anything; it is a description of where the EXPLORE effect lives, which is what a redirect needs. CONFIRM is
NOT re-opened by this cell (cell_01 was H1's one CONFIRM opening; guard a).

**Sub-claim (14c floor Q8/Q9, where does the effect live):** decompose the per-settlement statistic D of cell_01
(D_S = [b(S+30m)-b(S-30m)] - [b(S+4h30m)-b(S+3h30m)], same definition, same 30m spot/perp-metrics basis) over EXPLORE
settlements by (a) funding settled at S: LE = funding <= 0.0100%, HI = funding > 0.0100%; (b) sign: funding < 0.0100%
(NEG-side); (c) calendar quarter.

**14c menu row + tool:** "Distribution differs between groups" -> Welch difference of means on per-settlement D with
Newey-West(3) t on each group mean (OLS on group dummies is not needed: two groups, block structure is 8h cycles, so NW(3)
on the interleaved full-series regression `D ~ 1 + 1[HI]`).

**Decision rule, branches evaluated in this order; the first that holds names the redirect finding; all four are reported:**
- **B1 funding-conditional:** mean D(HI) - mean D(LE) >= 1.0 bp AND NW t on the HI coefficient > 3 AND mean D(LE) < 0.5 bp
  (the minimum economic effect fixed in cell_01). -> spawn H6: the settlement jump exists only when funding is above default.
- **B2 opposite sign at low funding:** mean D(funding < 0.0100%) <= -0.5 bp with NW t < -2. -> spawn H6: sign-flip.
- **B3 one era only:** the largest single calendar quarter carries > 60% of sum(D) (signed, over EXPLORE). -> spawn H6:
  era-specific.
- **B4 diffuse/absent:** none of the above. -> spawn nothing about the funding clock; H1's redirect closes as "no localised
  effect", state recorded, and the cell is the redirect record.

**Evidence weights:** none applied. The redirect describes the slice that produced H1 and H6; it is birth data, not evidence
(RUNBOOK_v3: a hypothesis born by looking at EXPLORE may be confirmed only on CONFIRM). weight = 1 for every branch. No
power simulation is needed for a weight that is not used; the spawned H6 gets its own power calculation in its own rule file.

**Testability caveat stated before running (from cell_01, sample facts only, no new look):** CONFIRM contains 9 of 1,328
settlements with funding above the default. Whatever B1/B2 finds, a CONFIRM opening of a funding-conditional H6 cannot
exercise the HI side; H6's rule file must say what power that leaves.
