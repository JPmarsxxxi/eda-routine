# BELIEFS — Bayesian ledger (mode E: every hypothesis traces to an OBSERVATIONS.md number)

Prior anchor convention (x101 rule: a tracker/base rate carries ~30% trust): prior = 0.3 x base + 0.7 x mechanism-specific
estimate. Base = 0.35, the replication rate of published return anomalies (Hou, Xue & Zhang 2020, "Replicating
Anomalies": ~35% of 452 survive at |t| > 1.96). It is used for every data-born claim, because the internal tracker
(alpha_log.md) is off-limits to this routine. The mechanism-specific estimate is argued per entry.
Observations NOT taken to Phase 1, with the reason: #5 (basis/funding vs direction) and #9 (taker ratio) are ALREADY-TESTED
positioning/flow families; #7 (lag-24 reversal) is the ALREADY-TESTED hour-of-day family; #10 (d_basis vs next-hour spot) is
most likely the #6 impostor; #3 (half_bp) is mostly an RV impostor on a 32%-covered CONFIRM, so it is a lead; #11 and #12 are
descriptive. All of these are listed as leads in REPORT.md.

## H1 — Funding-clock basis sawtooth
parent: none
source: OBSERVATIONS.md #1
question: Does the perp-minus-spot basis systematically jump up right after each 00/08/16 UTC funding settlement (relative to a non-settlement point in the same cycle)?
hypothesis: a funding settlement (00/08/16 UTC, `funding` in btcusdt_funding_8h) predicts a rise in the basis (1e4*log(metrics `c` / spot `close`)) from 30 min before to 30 min after settlement, larger than the same-width change at the mid-cycle point (S+4h), because leveraged perp longs (who pay funding when it is positive) reduce perp exposure into the settlement to avoid the payment and rebuild it afterwards, so perp demand, and with it the premium, dips before the timestamp and recovers after
forbids: a CONFIRM mean of D = [b(S+30m)-b(S-30m)] - [b(S+4h30m)-b(S+3h30m)] at or below 0 (no settlement-specific jump); and (side bet, reported) no increase of the jump with the funding just settled
rivals: session-open flows at 00 UTC (Asia/daily candle) and 08 UTC (Europe open) move the perp more than spot regardless of funding; a stamping/alignment artefact at 8h boundaries in the metrics klines; mean-reversion of the basis level coinciding with the clock
born_on: EXPLORE #1
prior: 0.60
anchor: 0.3 x 0.35 (anomaly replication base) + 0.7 x 0.71 (documented funding mechanics + 14-SE EXPLORE jump vs placebo, discounted because the clock rival is not yet separated) = 0.105 + 0.497 = 0.60
posterior: 0.13
state: OPEN
evidence:
- cell_01: REFUTED (CONFIRM, mean D 0.163bp, t 2.18) weight=0.1 capped=yes (raw 0.0303) -> posterior 0.13

## H2 — DVOL adds next-day realized-vol information beyond trailing RV
parent: none
source: OBSERVATIONS.md #2
question: Does the implied-vol index forecast the next 24h of realized spot volatility beyond what trailing 24h / 7d / 30d realized vol already say?
hypothesis: a change in `dvol` (Deribit DVOL close) predicts next-24h realized spot volatility (log RV from 30m spot returns over (t+1h, t+25h]) beyond trailing 24h/7d/30d RV, because option prices aggregate forward-looking information (scheduled events, hedging demand, positioning of informed option traders) that past realized volatility does not contain
forbids: a CONFIRM partial Spearman (dvol vs next-24h log RV | trailing 24h, 7d, 30d log RV) at or below 0
rivals: DVOL is a 30-day smoother of past RV, so any partial effect is longer-memory RV that the 30d control misses (HAR impostor); the leverage effect (price falls raise both DVOL and future RV); an era/level effect in a 9-month EXPLORE
born_on: EXPLORE #2
prior: 0.60
anchor: 0.3 x 0.35 + 0.7 x 0.71 (implied vol subsuming information beyond historical vol replicates widely in equities/FX, e.g. Christensen & Prabhala 1998; discounted for a young crypto index and a 9-month EXPLORE) = 0.105 + 0.497 = 0.60
posterior: 0.992
state: HIGH-VAL
evidence:
- cell_05: SUPPORTED (CONFIRM, partial rho 0.174, crit 0.0869) weight=12.2 capped=yes (to 10) -> posterior 0.9375 (recorded 0.938)
- cell_10: PASS (VAL, partial rho 0.2985, crit 0.1213; VAL_NOTE: soft-clean VAL, different liquidity regime post-2023-04) weight=8.28 capped=no -> posterior 0.992

## H3 — Perp basis level forecasts next-day realized vol beyond trailing RV
parent: none
source: OBSERVATIONS.md #4
question: Does a high perp premium over spot forecast higher realized volatility over the next 24h, beyond trailing RV?
hypothesis: a change in the basis (1e4*log(metrics `c` / spot `close`), hourly mean of 30m-mark snapshots) predicts next-24h realized spot volatility (log RV of 30m returns over (t+1h, t+25h]) beyond trailing 24h/7d/30d RV, because a high premium means leveraged long demand exceeds arbitrage capacity, and that leverage unwinds through liquidation cascades that raise future volatility. This differs from the ALREADY-TESTED positioning family: the response is the MAGNITUDE of moves, not direction, and the predictor is a traded price spread, not an account ratio
forbids: a CONFIRM partial Spearman (basis vs next-24h log RV | trailing 24h, 7d, 30d log RV) at or below 0
rivals: basis is a proxy for the implied-vol/risk regime (twin of DVOL, H2); bull-market trend regimes carry both high basis and high vol (2021H1); volume/activity (busy markets have both)
born_on: EXPLORE #4
prior: 0.35
anchor: 0.3 x 0.35 + 0.7 x 0.35 (plausible leverage-cascade mechanism, 8-SE EXPLORE partial, but a single 16-month EXPLORE dominated by one bull regime and an obvious regime rival) = 0.105 + 0.245 = 0.35
posterior: 0.114
state: OPEN
evidence:
- cell_03: REFUTED (CONFIRM, partial rho 0.0099, crit 0.0689) weight=0.240 capped=no -> posterior 0.114

## H4 — High implied vol precedes positive next-day spot returns
parent: none
source: OBSERVATIONS.md #8
question: Does a high DVOL level predict a higher next-24h spot return (a volatility/fear premium)?
hypothesis: a change in `dvol` (level) predicts a higher next-24h spot log return (spot close, (t+1h, t+25h]) because holders of BTC exposure are paid a premium for bearing risk when implied variance is high (fear premium, as with VIX in equities)
forbids: a CONFIRM Spearman (dvol, next-24h spot return) at or below 0
rivals: era trend (EXPLORE is 9 months of mostly-bull 2021, where high DVOL coincided with rallies); short-term reversal after crashes (high DVOL follows falls, falls partly revert: the reversal impostor #6); overlapping 24h windows inflate the EXPLORE number
born_on: EXPLORE #8
prior: 0.25
anchor: 0.3 x 0.35 + 0.7 x 0.21 (weak: 9-month EXPLORE, sign of the vol-return relation in crypto is mixed in the literature, 2.6-band effect) = 0.105 + 0.147 = 0.25
posterior: 0.183
state: OPEN
evidence:
- cell_08: REFUTED (CONFIRM, Spearman +0.0194, refute bar +0.025) weight=0.671 capped=no -> posterior 0.183

## H5 — Hourly spot return reversal (liquidity provision)
parent: none
source: OBSERVATIONS.md #6
question: Do hourly spot returns reverse the next hour?
hypothesis: a change in spot `close` over hour t (r_t) predicts a return of opposite sign in hour t+1 because liquidity providers who absorb one-sided flow demand compensation (inventory risk), so prices overshoot and partially revert. This differs from the ALREADY-TESTED "reversal after taker imbalance": it conditions on the price move, not on taker flow
forbids: a CONFIRM Spearman(r_t, r_{t+1}) at or above 0
rivals: bid-ask bounce in trade prints (sized at ≈ -0.001 hourly ACF from the Roll estimate, too small); a handful of crash hours (fat tails, 2020 exkurt 125); era noise (EXPLORE eras alternate sign -0.084/+0.005/-0.076/+0.004)
born_on: EXPLORE #6
prior: 0.20
anchor: 0.3 x 0.35 + 0.7 x 0.14 (short-term reversal is a documented liquidity effect, but EXPLORE's era-by-era sign alternation is the floor-Q8 noise signature) = 0.105 + 0.098 = 0.20
posterior: 0.714
state: OPEN
evidence:
- cell_06: SUPPORTED (CONFIRM, Spearman -0.0640, crit -0.01526) weight=18.9 capped=yes (to 10) -> posterior 0.714

## H6 — Hourly basis change leans against next-hour spot return, beyond the spot's own reversal
parent: H5
source: OBSERVATIONS.md #10
question: Is the EXPLORE lean of the hourly basis change against next-hour spot return (-0.041) a separate effect, or just H5's spot reversal seen through a series that contains the spot price?
hypothesis: a change in the basis (hourly mean of 30m-mark snapshots of 1e4*log(metrics `c` / spot `close`), diff over one hour) predicts a spot return of opposite sign in the next hour, beyond the spot's own last-hour return, because a basis rise reflects perp-side buying pressure that spot liquidity providers absorb with a lag and lean against, so spot drifts down as the basis mean-reverts through the spot leg
forbids: a CONFIRM partial Spearman (d_basis_t vs r_{t+1} | r_t) at or above -0.015 (the H5 rival reading: d_basis carries nothing once r_t is removed)
rivals: H5's spot reversal (d_basis contains -r_t mechanically because the spot close sits in the denominator of the basis); basis mean-reversion (ACF1 -0.23) working through the perp leg only, leaving spot untouched; a handful of large-move hours
born_on: EXPLORE #10
prior: 0.15
anchor: 0.3 x 0.35 (anomaly replication base) + 0.7 x 0.06 (mechanism is a guess, and the EXPLORE lean is likely the H5 impostor; a second-order effect on a two-series construct) = 0.105 + 0.042 = 0.15
posterior: 0.638
state: OPEN
evidence:
- cell_07: SUPPORTED (CONFIRM, partial Spearman -0.0188, crit -0.0168) weight=18.1 capped=yes (to 10) -> posterior 0.638
