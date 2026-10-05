# BELIEFS — Bayesian ledger (RUNBOOK_v3 fixed format; `posterior` and `state` are the only fields updated in place)

Prior recipe used for every Phase-1 entry (stated once, applied identically):
prior = s x [0.3 x B + 0.7 x P(true | flagged)] x z, where
- B = 0.35, external base rate: share of published return anomalies that replicate at |t| > 1.96 (Hou, Xue & Zhang
  2020, ~35%), taken at the runbook's ~30% trust;
- P(true | flagged) = 0.55: Bayes for a flag from this run's K=29 EXPLORE screen with an assumed 10% share of true
  features, screen power 0.5 at a cost-sized effect, chance flag rate 0.046: 0.1x0.5 / (0.1x0.5 + 0.9x0.046) = 0.547;
- s = story factor: 1 = an economic mechanism that forbids something; 0.5 = weak story / a strong impostor rival;
- z = size factor: 1 if the EXPLORE point estimate already clears the cost-sized threshold the fold rules use;
  0.5 if it is at the threshold; 0.25 if it is below it (selection makes EXPLORE estimates biased upward).
Base value 0.3 x 0.35 + 0.7 x 0.547 = 0.105 + 0.383 = 0.488 -> 0.49.

## H1 — High perp premium coins underperform their peers over the next 72h
parent: none
source: OBSERVATIONS.md #1, #2, #3 (tables/00_4_explanatory_screen.csv, tables/00_4_impostor_premium.csv)
question: Does a coin's perp premium, relative to the other coins' premiums, predict its primary return relative to theirs over the next 72h?
hypothesis: a change in perp/perp_premium_<C> `close` (daily mean over day d, cross-sectional rank across coins) predicts the coin's primary `price` log return over the next 72h relative to the other coins (negatively) because a high premium means leveraged perp longs are crowding into that coin and paying up for exposure; as the crowding unwinds and the premium/funding mean-reverts, the crowded coin underperforms its peers
forbids: on a CONFIRM fold, a top-third-minus-bottom-third (by premium) 72h primary-return spread >= 0, or one that is not significantly negative (one-sided t > -1.645)
rivals: cross-sectional short-term reversal (premium proxies recent winners; OBS #2 says rank corr -0.01 on EXPLORE); funding twin (OBS #3, same signal, not separate evidence); coin volatility (high-vol alts carry higher premia and may simply have lower returns in down legs); 2021H1 alt-season regime (OBS #11)
born_on: EXPLORE #1
seen_on: none
prior: 0.49
anchor: recipe above with s=1 (crowded-leverage mechanism forbids a non-negative spread), z=1 (EXPLORE spread -170 bp vs cost threshold ~-120 bp/72h): 1 x 0.488 x 1 = 0.49
posterior: 0.321
state: OPEN
evidence:
- cell_01: C1 refuted weight=0.729 capped=no -> posterior 0.412
- cell_02: C1 redirect weight=1 capped=no -> posterior 0.412 (absent everywhere; no child)
- cell_03: C2 refuted weight=0.843 capped=no -> posterior 0.371
- cell_04: C2 redirect weight=1 capped=no -> posterior 0.371 (absent everywhere; no child)
- cell_05: C3 refuted weight=0.801 capped=no -> posterior 0.321
- cell_06: C3 redirect weight=1 capped=no -> posterior 0.321 (absent everywhere; no child)

## H2 — Fear & Greed level predicts the next-day panel return (sentiment momentum)
parent: none
source: OBSERVATIONS.md #5 (tables/00_4_explanatory_screen.csv row 22)
question: Does the Fear & Greed index known at 00:00 UTC predict the equal-weight primary panel return over the next 24h?
hypothesis: a change in attention/fear_greed `value` (level stamped <= day d) predicts the equal-weight mean of primary `price` 24h log returns over day d+1 (positively) because greedy retail sentiment keeps buying into strength for another day (herding / slow-moving retail flows), while fearful days see continued selling
forbids: on a CONFIRM fold, a non-positive Spearman IC, or a top-minus-bottom tercile (by fear_greed) next-day panel return spread that is not significantly positive (one-sided t < 1.645)
rivals: price momentum impostor (fear_greed is built partly from price momentum and volatility); bull-market regime (EXPLORE 2019-2021 is bull-heavy, high greed coincides with high drift, OBS #11); volatility level (fear = high vol days with larger negative skew)
born_on: EXPLORE #5
seen_on: none
prior: 0.12
anchor: recipe above with s=0.5 (weak story, strong price-momentum impostor), z=0.5 (EXPLORE half-spread 42 bp vs ~44.5 bp 24h panel cost: at the bar): 0.5 x 0.488 x 0.5 = 0.122 -> 0.12
posterior: 0.077
state: OPEN
evidence:
- cell_07: C1 refuted weight=0.759 capped=no -> posterior 0.094
- cell_08: C1 redirect weight=1 capped=no -> posterior 0.094 (absent everywhere; no child)
- cell_09: C2 refuted weight=0.804 capped=no -> posterior 0.077
- cell_10: C2 redirect weight=1 capped=no -> posterior 0.077 (absent everywhere; no child)

## H3 — Prior-session S&P 500 return predicts the next-day panel return (risk-on spillover)
parent: none
source: OBSERVATIONS.md #6 (tables/00_4_explanatory_screen.csv row 24)
question: Does the S&P 500 return of the session ending at least one session before day d+1 predict the panel's day d+1 return?
hypothesis: a change in macro/yahoo_GSPC `close` (log return of the session with local_date <= d-1) predicts the equal-weight mean of primary `price` 24h log returns over day d+1 (positively) because risk-on/risk-off information from equities diffuses slowly into crypto through cross-asset investors who rebalance with a lag
forbids: on a CONFIRM fold, a non-positive Spearman IC, or a top-minus-bottom tercile (by prior SPX return) next-day panel return spread that is not significantly positive (one-sided t < 1.645)
rivals: chance (t 2.18 in a 29-look screen; nothing at 72h); common macro shock days (both react to the same news, the lag is a timestamp artefact); volatility regime (2020 COVID months dominate both series)
born_on: EXPLORE #6
seen_on: none
prior: 0.06
anchor: recipe above with s=0.5 (weak story: a full extra session of lag should already be priced), z=0.25 (EXPLORE half-spread 18 bp vs ~44.5 bp cost: below the bar): 0.5 x 0.488 x 0.25 = 0.061 -> 0.06
posterior: 0.06
state: OPEN
evidence:
- (none yet)
