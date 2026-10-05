### Cell 08 — EDA: H1 Alpha#101 predicts next-day cross-sectional returns on C2

**Sub-claim being tested:** H1: "the top half of coins by `((close - open) / ((high - low) + .001))` (day d) out-earns the bottom half over end of d -> end of
d+1 by >= 20 bp/day" (see cell_08_rule.md).

**Why it matters to the hypothesis:** it is the hypothesis's only sub-claim; if it is refuted, H1's probability drops and a
redirect cell follows (RUNBOOK_v3 step 8).

**Test(s) used:** 2-bin quantile sort of next-day primary returns by the alpha, mean spread with Newey-West(5) SE; Spearman IC
(descriptive).

**Decision rule before running:** "I will consider it **supported** if mean >= 20 bp/day and t >= 1.645; **refuted** if
mean + 1.645 SE < 20 bp/day and t < 1.645; **inconclusive** otherwise." Weights: supported 3.311, refuted
0.881, inconclusive 1 (cell_08_rule.md).

**Engine/library APIs used:** pandas rolling corr / rank (paper A.1 operators), numpy; code/run_lib.py (guarded loaders,
`build_panel`, `alpha`, `half_spread_series`, `nw_se`, `decide`); code/cell_test.py.

**Data loaded:** spot/binance_<COIN> (signal inputs, C2 plus a 40-day lookback buffer) and primary/validated_<COIN>
(responses strictly inside C2); guard asserted at every load (ACCESS_LOG.md).

**Decisions I need from you:** none beyond DECISIONS.md D1-D13 (defaults taken, unattended).
