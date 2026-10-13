# BELIEFS — Bayesian ledger (RUNBOOK_v3 v3.2 fixed format)

Mode B, one item: Kakushadze (2015) "101 Formulaic Alphas", Appendix A.1, second batch (TARGET.md). Five candidates, one per
alpha, all SOURCE-born (the paper), so EXPLORE is an ordinary slice for each. Common prior anchor (written before any test):
published equity anomalies replicate at a t > 1.96 bar about 35% of the time in their own market (Hou, Xue & Zhang 2020,
"Replicating Anomalies", RFS: 65% of 452 fail), and these are short-horizon formula alphas built for US equities 2010-13 being
moved to a 10-coin 24/7 crypto panel and a daily UTC bar, which this run discounts by half for the transfer: 0.35 x 0.5 =
0.175, rounded to 0.17. No tracker base rate from earlier runs in this repo is used (DECISIONS D1). The claim in every
entry is the `neutral` version: the daily cross-sectional rank IC with next-day primary returns is >= MIN_USEFUL_IC (0.02) in
the paper's direction.

## H1 — Alpha#30: volume-scaled 3-day streak fade
parent: none
source: 1601.00991v3.pdf Appendix A.1, Alpha#30 (TARGET.md HYPOTHESIS)
question: does a coin's recent up/down streak, faded and scaled by its 5-day/20-day volume ratio, rank next-day returns across coins?
hypothesis: a change in `close` over the last 3 days (sum of daily signs, cross-sectionally ranked and faded) times sum(`volume`, 5)/sum(`volume`, 20) predicts the next-day (00:00-24:00 UTC) relative return because losing streaks on rising volume are forced selling that liquidity providers absorb at a discount and are paid back next day
forbids: a mean daily cross-sectional rank IC between Alpha#30 and the next-day primary return that is negative, or excluded from 0.02 by its upper 95% bound, on the CONFIRM folds
rivals: plain 1-day reversal (b_rev1) carried by the sign terms; a volume-trend effect alone (b_volu) with the streak irrelevant; liquidity/size (small coins have both volume spikes and reversals)
born_on: SOURCE 1601.00991v3.pdf
seen_on: none
prior: 0.17
anchor: Hou-Xue-Zhang 2020 own-market replication ~0.35 x 0.5 equity-to-crypto transfer discount = 0.175 -> 0.17
posterior: 0.8497
state: OPEN
evidence:
- cell_12: C1 supported weight=5.103 capped=no -> posterior 0.5110
- cell_13: C2 supported weight=5.411 capped=no -> posterior 0.8497
- cell_14: C3 inconclusive weight=1 capped=no -> posterior 0.8497
- cell_20: EXPLORE inconclusive weight=1 capped=no -> posterior 0.8497

## H2 — Alpha#35: high own-volume, low own-price, low own-return
parent: none
source: 1601.00991v3.pdf Appendix A.1, Alpha#35 (TARGET.md HYPOTHESIS)
question: do coins whose volume is high, and whose price level and return are low, against their own recent history, outperform the next day?
hypothesis: a change in `volume` (Ts_Rank over 32 days) together with low ((close + high) - low) (Ts_Rank over 16 days) and low returns (Ts_Rank over 32 days) predicts the next-day relative return because heavy volume at a local price low marks capitulation that reverses
forbids: a mean daily cross-sectional rank IC between Alpha#35 and the next-day primary return that is negative, or excluded from 0.02 by its upper 95% bound, on the CONFIRM folds
rivals: 1-day reversal (Phase 0 rho 0.43 with b_rev1, OBSERVATIONS #3); a volume-shock effect alone (b_volu); high-volatility coins earning a risk premium (b_vol20)
born_on: SOURCE 1601.00991v3.pdf
seen_on: none
prior: 0.17
anchor: Hou-Xue-Zhang 2020 own-market replication ~0.35 x 0.5 equity-to-crypto transfer discount = 0.175 -> 0.17
posterior: 0.1700
state: OPEN
evidence:
- cell_01: C1 inconclusive weight=1 capped=no -> posterior 0.1700
- cell_02: C2 inconclusive weight=1 capped=no -> posterior 0.1700
- cell_03: C3 inconclusive weight=1 capped=no -> posterior 0.1700
- cell_19: EXPLORE inconclusive weight=1 capped=no -> posterior 0.1700

## H3 — Alpha#38: short coins at the top of their 10-day range that rose today
parent: none
source: 1601.00991v3.pdf Appendix A.1, Alpha#38 (TARGET.md HYPOTHESIS)
question: does ranking coins by -(rank of Ts_Rank(close, 10)) x rank(close / open) predict next-day relative returns?
hypothesis: a change in `close` relative to its 10-day range, combined with the day's close/open move, predicts the next-day relative return with the paper's (negative) sign because coins that both sit at a 10-day high and rose on the day are overextended and give some of it back
forbids: a mean daily cross-sectional rank IC between Alpha#38 and the next-day primary return that is negative, or excluded from 0.02 by its upper 95% bound, on the CONFIRM folds
rivals: plain 1-day cross-sectional reversal — Phase 0 IMPOSTOR, rho 0.863 with b_rev1 (OBSERVATIONS #1), so a pass may be reversal alone; 10-day momentum with the opposite sign; volatility (big movers rank extreme)
born_on: SOURCE 1601.00991v3.pdf
seen_on: none
prior: 0.17
anchor: Hou-Xue-Zhang 2020 own-market replication ~0.35 x 0.5 equity-to-crypto transfer discount = 0.175 -> 0.17 (the impostor makes a pass less informative about #38 itself, not less likely; handled as a descriptive net of b_rev1 in every cell)
posterior: 0.0378
state: LOW
evidence:
- cell_04: C1 inconclusive weight=1 capped=no -> posterior 0.1700
- cell_05: C2 refuted weight=0.192 capped=no -> posterior 0.0378
- cell_06: C2 inconclusive (redirect) weight=1 capped=no -> posterior 0.0378

## H4 — Alpha#53: fade the 9-day change in close location
parent: none
source: 1601.00991v3.pdf Appendix A.1, Alpha#53 (paper: delay-0) (TARGET.md HYPOTHESIS)
question: does the 9-day change in ((close - low) - (high - close)) / (close - low), faded, rank next-day returns across coins?
hypothesis: a change in where `close` sits between `low` and `high` over 9 days predicts the next-day relative return (faded) because closes drifting toward the day's high reflect buying pressure that overshoots and reverts
forbids: a mean daily cross-sectional rank IC between Alpha#53 and the next-day primary return that is negative, or excluded from 0.02 by its upper 95% bound, on the CONFIRM folds
rivals: 1-day reversal (rho 0.34 with b_rev1); Alpha#54 (rho 0.50, OBSERVATIONS #2: the same close-location information); the ratio's explosions near the low (OBSERVATIONS #6) ranking coins by noise
born_on: SOURCE 1601.00991v3.pdf
seen_on: none
prior: 0.15
anchor: Hou-Xue-Zhang 2020 own-market replication ~0.35 x 0.5 transfer discount = 0.175, less 0.025 for a Phase-0 assumption failure (division problem, OBSERVATIONS #6) = 0.15
posterior: 0.0323
state: LOW
evidence:
- cell_15: C1 inconclusive weight=1 capped=no -> posterior 0.1500
- cell_16: C2 inconclusive weight=1 capped=no -> posterior 0.1500
- cell_17: C3 refuted weight=0.189 capped=no -> posterior 0.0323
- cell_18: C3 inconclusive (redirect) weight=1 capped=no -> posterior 0.0323

## H5 — Alpha#54: close location times (open/close)^5
parent: none
source: 1601.00991v3.pdf Appendix A.1, Alpha#54 (paper: delay-0) (TARGET.md HYPOTHESIS)
question: does -((close - low) / (high - low)) x (open / close)^5 rank next-day returns across coins?
hypothesis: a change in `close` toward the day's `high` (and above the `open`) predicts a lower next-day relative return because closing strength at the 00:00 UTC boundary is short-lived intraday pressure that reverses
forbids: a mean daily cross-sectional rank IC between Alpha#54 and the next-day primary return that is negative, or excluded from 0.02 by its upper 95% bound, on the CONFIRM folds
rivals: 1-day reversal (rho 0.19 with b_rev1); Alpha#53 (rho 0.50); trade-print bounce at the daily boundary (Roll) — from 2022 the response is a mid, which removes bounce for 7 coins
born_on: SOURCE 1601.00991v3.pdf
seen_on: none
prior: 0.17
anchor: Hou-Xue-Zhang 2020 own-market replication ~0.35 x 0.5 equity-to-crypto transfer discount = 0.175 -> 0.17
posterior: 0.0437
state: LOW
evidence:
- cell_07: C1 refuted weight=0.223 capped=no -> posterior 0.0437
- cell_08: C1 supported (redirect) weight=1 capped=no -> posterior 0.0437

## H6 — closing strength continues: -1 x Alpha#54 (child of H5, from redirect cell_08)
parent: H5
source: redirect cells/cell_08_result.md (H5 refuted on C1 with the opposite sign significant)
question: do coins that close near the top of the day's range, and above the open, outperform the other coins the next day?
hypothesis: a change in `close` toward the day's `high` (and above `open`), measured as +((close - low)/(high - low)) x (open/close)^5, predicts a HIGHER next-day relative return because closing strength at the 00:00 UTC boundary reflects buying that continues into the next day (the opposite of the paper's delay-0 reversal)
forbids: a mean daily cross-sectional rank IC between -1 x Alpha#54 and the next-day primary return that is negative, or excluded from 0.02 by its upper 95% bound, on EXPLORE, C2 or C3
rivals: plain 1-day cross-sectional momentum of the day's return (b_rev1 with the opposite sign); a C1-only regime (2020-21 alt-season trends); trade-print bounce at the daily boundary (removed from 2022 for 7 coins, whose response is a mid)
born_on: C1 cell_08
seen_on: none
alpha_code: A54
sign: -1
prior: 0.15
anchor: same base rate as its parent (Hou-Xue-Zhang ~0.35 x 0.5 transfer = 0.175), less 0.025 because this sign has no published source (it is a redirect finding) = 0.15; C1, where it was born, is not evidence
posterior: 0.4899
state: OPEN
evidence:
- cell_09: C2 supported weight=5.443 capped=no -> posterior 0.4899
- cell_10: C3 inconclusive weight=1 capped=no -> posterior 0.4899
- cell_11: EXPLORE inconclusive weight=1 capped=no -> posterior 0.4899

