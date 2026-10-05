# INBOX_PROPOSALS — run 2026-09-28_btc-perp-various-free (not merged; the human merges by hand)

Ideas for a future session with a fresh slice. Each was a lead here, tested nowhere, and none goes into `INBOX.md` from this run.

- **Funding-clock basis jump decays by 2023**: the +0.74 bp post-settlement jump (EXPLORE) fell to +0.08 bp (CONFIRM), and CONFIRM had almost no
  positive-funding settlements. A future session on a longer or different-venue funding sample could ask whether the jump exists only when funding is above the 0.01% default.
- **Hourly rank reversal (H5) versus its size-weighted form**: the rank reversal is stable (-0.064 Spearman, all five CONFIRM quarters) while Pearson is +0.005,
  suggesting moderate moves reverse and extreme ones continue. Needs a fresh slice (2024+ spot data) since CONFIRM was H5's one opening.
- **Relative DVOL (dvol minus trailing 30-day median) vs next-24h return**: EXPLORE rho 0.109 (z 1.54, short history), CONFIRM raw-level quarters mostly positive. Needs DVOL beyond 2023-11 or a different index.
- **Half-spread coverage regime**: half_bp exists for only 32% of CONFIRM hours and 35-79% by year; whether missingness tracks a regime (venue change) is unexamined and affects every cost line.
- **TARGET.md correction** (no `INBOX.md` entry): the "perp" price files are Binance SPOT (DATA_CARD identity check); only `metrics` carries perp `c`, OI and ratios.
