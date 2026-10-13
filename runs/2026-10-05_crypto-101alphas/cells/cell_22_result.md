branch: inconclusive
weight_applied: 1

# cell_22 result — redirect for H2 (Alpha#42) on C3

Pointers (mean bp/day, NW(5) t). Bar: |mean| >= 20 and |t| >= 2.5, positive mean in the stated direction.

| pointer | days | mean_bp_day | t | clears_bar |
|---|---|---|---|---|
| P0 paper sign, h=1 (the refuted test, for reference) | 292 | -28.8 | -2.25 | False |
| P1 sign flipped, h=1 | 292 | 28.8 | 2.25 | False |
| P2 paper sign, h=2 | 237 | -35.6 | -2.99 | False |
| P2 flipped, h=2 | 237 | 35.6 | 2.99 | True |
| P2 paper sign, h=3 | 183 | -31.2 | -2.9 | False |
| P2 flipped, h=3 | 183 | 31.2 | 2.9 | True |
| P2 paper sign, h=5 | 88 | -30.8 | -2.68 | False |
| P2 flipped, h=5 | 88 | 30.8 | 2.68 | True |
| P3 paper sign, 2022 only | 227 | -24.0 | -1.72 | False |
| P3 flipped, 2022 only | 227 | 24.0 | 1.72 | False |
| P3 paper sign, 2023 only | 65 | -45.3 | -1.51 | False |
| P3 flipped, 2023 only | 65 | 45.3 | 1.51 | False |
| P4 variant, paper sign | 310 | -15.4 | -1.32 | False |
| P4 variant, flipped | 310 | 15.4 | 1.32 | False |
| P5 rival, high-minus-low | 310 | 14.1 | 1.49 | False |
| P5 rival, low-minus-high | 310 | -14.1 | -1.49 | False |

**Finding:** points to: P2 flipped, h=2 (mean 35.6 bp/day, t 2.99) -> ONE child spawned in BELIEFS.md
Redirect: weight 1, no posterior moves. `branch: inconclusive` is the gate.py-required placeholder for a redirect.

Plot: plots/cell_22_H2_redirect_C3.png

Child: **H7** (BELIEFS.md) — born_on C3 cell_22, seen_on EXPLORE, C1, C2 (DECISIONS D18) -> no admissible TRAIN slice.
