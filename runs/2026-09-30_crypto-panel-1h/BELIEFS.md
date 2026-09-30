# BELIEFS — Bayesian ledger (RUNBOOK_v3 fixed format; `state` and `posterior` updated in place, all else written once)

Mode E: every entry traces to an OBSERVATIONS.md number (EXPLORE). Data-born -> the first and only CONFIRM look is its first
test. Prior anchor used throughout (trust arithmetic, RUNBOOK "tracker base rate at ~30% trust"): no tracker is readable in
this run (alpha_log.md is off-limits), so the base-rate slot uses a published replication rate — Hou, Xue & Zhang (2020,
"Replicating Anomalies") report roughly 35% of anomalies surviving |t| >= 1.96 — at 30% weight; the remaining 70% is this
run's own assessment of the EXPLORE evidence + mechanism, stated per entry. prior = 0.30 x 0.35 + 0.70 x own.
States: OPEN (5-85%), LOW (<5%), HIGH-EXPLORE / HIGH-CONFIRM / HIGH-VAL (>85%, by the slice that got it there).

## H1 — Daily time-series reversal of coin returns
parent: none
source: OBSERVATIONS.md #9 (daily raw ACF(1) -0.089, 6/10 coins significant) and #6 (VR(24) < 1)
question: Does a coin's return over one UTC day predict the opposite-sign return over the next UTC day?
hypothesis: a change in [close] over UTC day d (daily log return of spot/binance_<COIN> close, per coin) predicts [the opposite-sign log return over UTC day d+1] because large daily moves in this retail- and leverage-heavy market overshoot (forced liquidations, stop cascades, attention-driven buying) and liquidity providers are paid to absorb that temporary price pressure, which then unwinds.
forbids: on CONFIRM, a pooled day-clustered normal-score IC between day-d and day-(d+1) returns that is >= 0 or only weakly negative (z >= -1.645); and a reversal confined to bid-ask-bounce size (a few bp) rather than tens of bp per 1-sd day
rivals: outlier impostor — one or two crash-rebound pairs (2020-03-12/13 type) produce the negative ACF while the typical day shows nothing (OBS #1, #14); volatility — reversal is a property of high-vol regimes only (it is volatility, not return); weekday composition — Sunday->Monday / Friday->Saturday effects masquerading as a general 1-day reversal (OBS #16)
born_on: EXPLORE #9
prior: 0.39
anchor: 0.30 x 0.35 (HXZ 2020 replication rate) + 0.70 x 0.40 (own: 6/10 coins significant, stable sign, a mechanism, but kurtosis 10-104 means few days drive it) = 0.385 -> 0.39
posterior: 0.39
state: OPEN
evidence:

## H2 — Daily reversal is stronger after panel-wide volume-shock days
parent: none
source: OBSERVATIONS.md #13 (EW day-to-day corr -0.136 on top-tercile volume-shock days vs -0.066 otherwise) and #11
question: Is the next-day reversal larger when the day's move came on abnormally high market volume?
hypothesis: a change in [vol] (panel mean of log(daily vol / median daily vol of the prior 30 days), spot/binance_<COIN>) predicts [a more negative day-d to day-(d+1) return IC in close] because high-volume days are the forced-flow days (liquidations, capitulation) whose price pressure is temporary, while low-volume moves are more often information that persists.
forbids: on CONFIRM, the normal-score day-to-day IC on top-tercile volume-shock days being equal to or higher (less negative) than on the other days (difference z >= -1.645)
rivals: volatility impostor — high-volume days are high-|r| days, and a larger IC magnitude on them is just bigger moves (OBS #11 says volume is not a pure vol proxy, but the overlap is 0.4-0.5); outlier impostor — a few crash days sit in the top tercile and carry the whole difference (OBS #1); regime — volume-shock days cluster in 2018 / 2020-03 (OBS #14)
born_on: EXPLORE #13
prior: 0.35
anchor: 0.30 x 0.35 (HXZ 2020) + 0.70 x 0.35 (own: a descriptive split, never tested on EXPLORE, n 448/895 days, same mechanism as H1) = 0.35
posterior: 0.35
state: OPEN
evidence:

## H3 — Same-hour-yesterday reversal of 1h returns (lag-24 ACF)
parent: none
source: OBSERVATIONS.md #5 (lag-24 ACF of 1h returns -0.051, negative in 10/10 coins and in every EXPLORE era; lags 12, 48 not)
question: Does a coin's 1h return predict the opposite-sign 1h return at the same clock hour the next day?
hypothesis: a change in [close] over hour h of day d (1h log return, spot/binance_<COIN>) predicts [the opposite-sign 1h log return over hour h of day d+1] because (NO-STORY: no economic mechanism is claimed; the pattern is a data-nature lead)
forbids: on CONFIRM, a pooled day-clustered normal-score IC between r(t) and r(t+24h) that is >= 0 or not significantly negative (z >= -1.645); and lag-24 being no more negative than the neighbouring lags 23 and 25 (a lag-24-specific effect is what the lead claims)
rivals: time-of-day seasonality of volatility crossed with outliers (OBS #16) producing a spurious lag-24 value; outlier impostor — a few paired crash/rebound hours 24 h apart (OBS #1); daily-candle anchoring artefact of the 00:00 UTC bar (the |r| profile peaks at 00 UTC, OBS #16)
born_on: EXPLORE #5
prior: 0.28
anchor: 0.30 x 0.35 (HXZ 2020) + 0.70 x 0.25 (own: 10/10 and every era, but no mechanism, correlated coins, and even at full EXPLORE size ~5 bp per 1-sd hour it cannot clear the cheapest 6.6 bp round trip) = 0.28
posterior: 0.795
state: OPEN
no_story: yes
evidence:
- cell_03: supported (CONFIRM, lag-24 IC -0.035, z -4.38; lag-24 < lags 23/25) weight=10 capped=yes (raw 12.5) -> posterior 0.795 [CONFIRM spent; below economic size]

## H4 — High-volume relative winners keep winning the next day
parent: none
source: OBSERVATIONS.md #12 (high-minus-low volume-shock winners-minus-losers +42 bp, t 1.5) and #11
question: Does abnormal volume on a coin's relative up (down) day predict relative continuation the next day?
hypothesis: a change in [vol] (coin's daily volume shock, log(vol / 30-day median)) interacted with [the coin's daily return relative to the 10-coin mean] predicts [the next-day relative log return with the same sign] because a volume shock is an attention/visibility shock (Gervais-Kaniel-Mingelgrin high-volume return premium) that draws further buyers into coins that already rose on it, while low-volume relative moves are liquidity noise that fades.
forbids: on CONFIRM, a daily Fama-MacBeth interaction coefficient (next-day relative return on z(rel) x z(volume shock)) that is <= 0 or not significantly positive (z <= 1.645)
rivals: size/liquidity — volume shocks are concentrated in small, illiquid coins (DOGE, DOT, SOL) whose relative returns are noisier (OBS #1, #10); outlier impostor — a few meme days (DOGE 2021) carry the interaction (OBS #1, #6: DOGE trends); momentum at the daily grain without any volume role (the 2017-18 +50 bp Q5-Q1 era, OBS #8)
born_on: EXPLORE #12
prior: 0.21
anchor: 0.30 x 0.35 (HXZ 2020) + 0.70 x 0.15 (own: t 1.5 only, 402 days, mechanism from equities that may not transfer) = 0.21
posterior: 0.026
state: LOW
evidence:
- cell_04: refuted (CONFIRM, FM b3 -14.5 bp, z -2.32, opposite sign) weight=0.1 capped=yes (raw 0.063) -> posterior 0.026
- cell_05: redirect (EXPLORE, absent everywhere: b3 +3.6 bp, z 0.40) weight=1 capped=no -> posterior 0.026 (no spawn)

## H5 — Intraday 6-hour reversal
parent: none
source: OBSERVATIONS.md #6 (VR(6) = 0.86, below 1 in 10/10) and #4
question: Does a coin's return over a 6-hour block predict the opposite-sign return over the next 6-hour block?
hypothesis: a change in [close] over a 6h block (00-06, 06-12, 12-18, 18-24 UTC; spot/binance_<COIN>) predicts [the opposite-sign log return over the next 6h block] because intraday order-flow imbalances (retail bursts, liquidation clusters) move prices beyond their information content and are absorbed by market makers within hours.
forbids: on CONFIRM, a pooled day-clustered normal-score IC between consecutive 6h block returns that is >= 0 or not significantly negative (z >= -1.645)
rivals: bid-ask bounce at block edges (OBS #4: Roll 23-36 bp is too large to be bounce, but a 1-bar edge effect remains); outlier impostor (OBS #1); volatility regime — only in the 2018 bear high-vol era (OBS #14: ACF(1) -0.067 in 2017-18 vs -0.02 later)
born_on: EXPLORE #6
prior: 0.39
anchor: 0.30 x 0.35 (HXZ 2020) + 0.70 x 0.40 (own: VR(6) < 1 in 10/10 but Lo-MacKinlay SE is optimistic under the vol clustering of OBS #7; a mechanism) = 0.385 -> 0.39
posterior: 0.865
state: HIGH-CONFIRM
evidence:
- cell_01: supported (CONFIRM, IC -0.032, z -1.89) weight=10 capped=yes (raw 15.6) -> posterior 0.865 [effect is half the economic threshold; lives in 2022-05..2023-03 only]

## H6 — 6h reversal is stronger when trailing volatility is high
parent: H5
source: cells/cell_01_result.md (CONFIRM: 6h IC +0.004 in 2021-07..2022-05 vs -0.074 in 2022-05..2023-03)
question: Is the 6h-block reversal concentrated in high-volatility (stressed) periods?
hypothesis: a change in [close] over a 6h block (spot/binance_<COIN>) predicts [the opposite-sign next-6h return] more strongly when [trailing 7-day realized volatility of the equal-weight panel, from close, known at the block start] is in its top tercile, because market makers' risk-bearing capacity shrinks in stress, so the premium for absorbing order-flow imbalances (and hence the subsequent reversal) grows (Nagel 2012, "Evaporating Liquidity").
forbids: on EXPLORE, the 6h-block normal-score IC on high-trailing-vol days being equal to or less negative than on the other days (difference z >= -1.645)
rivals: outlier impostor — high-vol terciles contain the crash days (2018-11, 2020-03) whose paired blocks carry the difference (OBS #1, #14); era, not volatility — the difference is 2018-bear vs the rest (OBS #14 ACF(1) by era) and trailing vol just labels the era; bid-ask/tick effects are larger in stressed markets (spreads widen) so the reversal is microstructure, not a premium (OBS #4)
born_on: CONFIRM cell_01
prior: 0.40
anchor: 0.30 x 0.35 (HXZ 2020) + 0.70 x 0.42 (own: published mechanism with equity evidence (Nagel 2012), one CONFIRM half-split that fits it, but a half-split is two points and the 1h-ACF-by-era table on EXPLORE (OBS #14) was already seen) = 0.399 -> 0.40
posterior: 0.870
state: HIGH-EXPLORE
evidence:
- cell_02: supported (EXPLORE, diff IC -0.081, z -2.48) weight=10 capped=yes (raw 19.7) -> posterior 0.870 [no CONFIRM/VAL per DECISIONS D10]
