### Cell 05 — EDA: H3 Alpha#2 predicts next-day cross-sectional returns on EXPLORE

**Sub-claim being tested:** H3: "the top half of coins by `(-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))` (day d) out-earns the bottom half over end of d -> end of
d+1 by >= 20 bp/day" (see cell_05_rule.md).

**Why it matters to the hypothesis:** it is the hypothesis's only sub-claim; if it is refuted, H3's probability drops and a
redirect cell follows (RUNBOOK_v3 step 8).

**Test(s) used:** 2-bin quantile sort of next-day primary returns by the alpha, mean spread with Newey-West(5) SE; Spearman IC
(descriptive).

**Decision rule before running:** "I will consider it **supported** if mean >= 20 bp/day and t >= 1.645; **refuted** if
mean + 1.645 SE < 20 bp/day and t < 1.645; **inconclusive** otherwise." Weights: supported 9.117, refuted
0.569, inconclusive 1 (cell_05_rule.md).

**Engine/library APIs used:** pandas rolling corr / rank (paper A.1 operators), numpy; code/run_lib.py (guarded loaders,
`build_panel`, `alpha`, `half_spread_series`, `nw_se`, `decide`); code/cell_test.py.

**Data loaded:** spot/binance_<COIN> (signal inputs, EXPLORE plus a 40-day lookback buffer) and primary/validated_<COIN>
(responses strictly inside EXPLORE); guard asserted at every load (ACCESS_LOG.md).

**Decisions I need from you:** none beyond DECISIONS.md D1-D13 (defaults taken, unattended).
