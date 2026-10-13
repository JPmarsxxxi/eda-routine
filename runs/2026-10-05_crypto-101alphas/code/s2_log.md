# S2 counter (consecutive picks whose best expected shift is <= 3 pp)
| before cell | best pick | expected shift | count |
|---|---|---|---|
| 08 | H1 C2 | 2.82 pp (power v2) | 1 — RESET: D15 re-calibrated power after cell_08, so counting restarts under v3 |
| 09 | H6 C1 | 1.50 pp (power v3) | 1 |
| 10 | H6 C2 (the best; cell_10 instead ran H4 C1 at 1.22 pp — operator error, DECISIONS D16) | 7.92 pp | 0 — RESET (> 3 pp) |
| 14 | H4 C2 | 5.26 pp | 0 (> 3 pp) |
| 15 | H4 C3 | 0.99 pp | 1 |
| 17 | H6 C3 | 4.45 pp (power v4, C3 measured) | 0 — RESET (> 3 pp) |
| 19 | H2 C1 (tie with H3 C1; H2 taken first by id) | 0.77 pp | 1 |
| 20 | H2 C2 | 4.02 pp | 0 — RESET (> 3 pp) |
| 21 | H2 C3 | 3.70 pp | 0 (> 3 pp) |
| 23 | H3 C1 | 0.77 pp | 1 |
| 24 | H3 C2 | 4.02 pp | 0 — RESET (> 3 pp) |
| 26 | H5 C1 | 0.42 pp | 1 |
| 27 | H5 C2 | 1.96 pp | 2 |
| (28) | H5 C3 | 1.69 pp | 3 -> S2 fires: three consecutive picks (before cells 26, 27 and the would-be 28) with best expected shift <= 3 pp; the third pick is not run |
