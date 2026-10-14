import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
A = kit.add_h
A("H1", "Alpha#30 family: volume-scaled fade of the multi-day up/down streak", "none",
  "TARGET.md SEEDS (Kakushadze #30); MEMORY/FINDINGS 2026-10-06 b2 H1; OBSERVATIONS #1, #3",
  "Does a cross-sectional fade of the recent streak, scaled by short/long volume, predict next 1h/6h/24h returns across the 10 coins, and is the C3 fade only the response switch?",
  "a change in the 3-day sign-streak rank of Binance daily closes, scaled by sum(volume,5)/sum(volume,20), predicts the cross-sectional rank of the next 24h return of primary price (down-streak + volume surge = higher return) because forced sellers/volume-driven overreaction mean-revert",
  "no positive rank IC at any horizon on any fold when scored against the pre-2022 (Binance-print) response; if the effect is real it must not vanish when the response is held on the Binance close in C2/C3",
  "volume ratio alone (attention) ; trailing 1-day reversal ; the Binance-print/FTMO-mid response switch ; hour-of-day clock",
  "SOURCE Kakushadze #30 (seed) / MEMORY b2 H1", 0.35,
  "MEMORY b2 H1 posterior 0.85 on C1 +0.037, C2 +0.048 but EXPLORE -0.007 and C3 +0.001 (4 folds, 2 supported): base 0.30 x1.2 for a replicated-in-two-folds seed -> 0.35")
A("H2", "Alpha#54 family: closing strength (close location x open/close^5) continues", "none",
  "TARGET.md SEEDS (-Kakushadze #54); MEMORY/FINDINGS 2026-10-06 b2 H6; OBSERVATIONS #1, #6",
  "Does closing strength within the day (close near the high, weighted by (open/close)^5) continue into the next 1h/6h/24h, in rank across the coins?",
  "a change in the daily close-location value times (open/close)^5 of Binance prices predicts the cross-sectional rank of the next 24h return of primary price (higher = continues) because intraday buying pressure that closes near the high is not fully absorbed by the close",
  "no positive rank IC on any horizon across any anchor hour; an effect that flips sign between the first and second half of EXPLORE is a regime story, not a feature",
  "same-day return itself (CLV is a transform of the day move); intraday range/vol; response switch; hour-of-day clock",
  "SOURCE Kakushadze #54 (seed) / MEMORY b2 H6", 0.30,
  "MEMORY b2 H6 posterior 0.49 (C2 +0.057, C3 +0.023, but EXPLORE halves +0.096/-0.078): base 0.30, no trust uplift for an unstable sign -> 0.30")
A("H3", "Vol-scaled short-horizon reversal/momentum, market-residual", "none",
  "OBSERVATIONS #2, #3, #4, #11; MEMORY already-explored (daily TS reversal, same-hour-yesterday 1h reversal, 6h-block reversal)",
  "After removing the BTC/market beta component, is the trailing k-hour return scaled by trailing volatility a cross-sectional predictor, and at what lookback does reversal turn into momentum?",
  "a change in the trailing 1h/3h/6h/12h/24h/72h/168h return of a coin, net of beta x BTC return and divided by its trailing volatility, predicts the cross-sectional rank of its next 1h/6h/24h return (negative at short lookbacks, positive at long) because liquidity-driven overshoot reverts while slower information diffuses",
  "no lookback shows a rank IC beyond min_useful in either direction on the pooled TRAIN; no change with lookback (a flat IC profile) would say the cross-section is pure noise at these horizons",
  "bid-ask bounce in the Binance print vs the FTMO mid response (OBSERVATIONS #1); volatility level (high-vol coins are the extreme ranks); a BTC lead-lag; the hour-of-day vol clock",
  "EXPLORE #2 #3 #11", 0.40,
  "MEMORY: 1h and 6h reversal reached CONFIRM-IC -0.03..-0.06 on earlier runs (pre-v3.3, half its size threshold); tracker base 0.30 x1.3 for repeated sign across runs -> 0.40")
A("H4", "Volume, trade-count and taker-flow surprises (spot order flow)", "none",
  "OBSERVATIONS #3, #5, #13; MEMORY already-explored (reversal after panel volume-shock days; high-volume winners continue)",
  "Do surprises in a coin's own quote volume, trade count, average trade size or taker-buy share (vs its trailing norm) predict its next-hour/6h/24h cross-sectional rank?",
  "a change in a coin's quote volume, trade count, average trade size or taker-buy imbalance relative to its trailing 30-day norm predicts the cross-sectional rank of its next 1h/6h/24h return because informed or forced flow shows up in size and aggressor side before price fully adjusts",
  "no volume, trade-count, size or taker-imbalance surprise shows a rank IC beyond min_useful once its interaction with the same-period return is controlled",
  "the same-period return itself (signed volume is a transform of return); volatility (volume tracks |ret|, corr 0.26); the 5x C3 trade-count regime shift (OBSERVATIONS #5); hour-of-day volume clock",
  "EXPLORE #3 #5 #13", 0.30,
  "tracker base 0.30 at ~30% trust for a first look at order-flow features; MEMORY: high-volume winners continue opposite sign on CONFIRM (LOW) -> no uplift -> 0.30")
A("H5", "Perp positioning: funding, basis rank, open-interest and long/short changes", "none",
  "OBSERVATIONS #7, #8, #9; MEMORY already-explored (perp premium cross-section 72h underperformance: sign negative on C1/C2/C3, shrinking)",
  "Do cross-sectional ranks of funding, perp-spot basis (premium index), open-interest change and long/short ratio predict the next 1h/6h/24h return rank across coins?",
  "a change in a coin's rank of funding rate / perp premium / open-interest growth / account long-short ratio predicts the cross-sectional rank of its next 24h return (crowded long = lower return) because leveraged crowding is unwound and paid for through funding",
  "no positioning variable has the predicted (negative) sign with an IC beyond min_useful in C2 and C3 together; coverage is only C2+C3 for 9 coins (OBSERVATIONS #9), so a sign-flip between them refutes",
  "past return (basis and funding follow the trailing return, OBSERVATIONS #8); volatility; the response switch; the pinned funding floor (OBSERVATIONS #7)",
  "EXPLORE #7 #8 #9", 0.25,
  "MEMORY perp-premium XS: negative sign on all three folds but EXPLORE effect shrank 85% (OPEN 0.32); coverage limits power: base 0.30 x0.85 -> 0.25")
A("H6", "Cross-venue gap and lead-lag (Coinbase and Upbit vs Binance)", "none",
  "OBSERVATIONS #10",
  "Does a coin's Coinbase-minus-Binance return gap, or its Upbit (Asia-hours) return, lead the next Binance/primary return?",
  "a change in the 1h/6h return gap between a coin's Coinbase (or Upbit) close and its Binance close predicts the cross-sectional rank of its next 1h/6h/24h primary return because the venue that is slower to arbitrage reveals flow the other venue has not priced",
  "no venue-gap feature has an IC beyond min_useful; same-hour Coinbase/Binance correlation of 0.994 leaves little room, so a lead-lag larger than the bid-ask noise would be a surprise",
  "bid-ask bounce differences between venues; the Binance print vs FTMO mid response; stale prints in thin hours; own-coin reversal",
  "EXPLORE #10", 0.20,
  "no earlier run on this panel looked at venue gaps; low-prior speculative family: base 0.30 x0.67 for the near-identity of the venues (corr 0.994) -> 0.20")
kit.write_beliefs()
print(open(kit.RUN + r"\BELIEFS.md").read()[:1500])
