import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
kit.add_h("H11", "Risk-shape features: trailing volatility, idiosyncratic volatility, MAX/skew and range rank the coins", "none",
  "OBSERVATIONS #3, #11 (vol clustering, fat tails); TARGET.md FAMILIES (volatility)",
  "Do recent-risk features (volatility, idiosyncratic volatility, maximum 1h return, skewness, 24h range) rank next-1h/6h/24h returns once the persistent coin level is removed?",
  "a change in a coin's trailing 168h volatility, idiosyncratic volatility, maximum hourly return, return skewness or 24h range predicts a LOWER cross-sectional rank of its next 1h/6h/24h primary return because lottery-like, high-risk coins attract speculative demand and are overpriced",
  "no one-sided risk feature shows a negative rank IC beyond min_useful after within-coin detrending; an IC that shrinks to zero when the coin's own 90-day mean is removed is a coin fixed effect, not a signal",
  "coin fixed effect (DOGE/SOL are persistently the most volatile; a 10-coin cross-section with 4 years of luck-dominated mean returns); the short-horizon reversal (high-vol coins have the extreme past returns); the vol clock",
  "EXPLORE #3 #11", 0.25,
  "no earlier run on this panel looked at risk-shape features; tracker base 0.30 for a standard anomaly x0.85 because a 10-coin cross-section has little room for a risk premium and cell 11 found a fixed-effect trap -> 0.25")
kit.write_beliefs()
print("ok")
