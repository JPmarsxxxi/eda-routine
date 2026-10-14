import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
kit.add_h("H12", "BTC / market lead-lag through beta: high-beta coins follow the market's last k-hour move with a delay", "none",
  "TARGET.md FAMILIES (cross-coin lead-lag; market-wide return conditioning); OBSERVATIONS #4",
  "After a BTC (or equal-weight market) move over the last 1-24 hours, do high-beta coins outperform (market up) or underperform (market down) over the next 1-24 hours?",
  "a change in beta_i x (BTC or EW-market return over the last k hours) predicts the cross-sectional rank of coin i's next 1h/6h/24h primary return with a positive sign because information in BTC reaches high-beta alts with a delay",
  "no lead_k feature shows a positive IC beyond min_useful at any horizon; a negative IC (market reversal times beta) would refute the diffusion story",
  "market-wide hourly reversal times beta (raw vs market-residual reversal differed by 0.010 at h1, cell 5); the volatility of the market move (large moves make beta dispersion matter more); the response switch",
  "EXPLORE #4", 0.20,
  "no earlier run looked at beta-weighted market moves; tracker base 0.30 x0.67 because cross-sectional dispersion from beta alone is small (pairwise corr 0.4-0.84) and market reversal argues the opposite sign -> 0.20")
kit.write_beliefs(); print("ok")
