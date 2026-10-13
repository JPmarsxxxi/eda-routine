hypothesis: H1
slice: C1
kind: test

# cell_01 rule — H1 (Alpha#101) on C1 (2020-06-04 .. 2021-05-06 excl.)

**Sub-claim (the one the hypothesis cannot survive without).** On C1, the verbatim Alpha#101 = `((close - open) / ((high - low) + .001))`, computed
from Binance UTC daily bars of day d, sorts coins so that the next-day primary `price` return (end of d -> end of d+1) of
the top half exceeds the bottom half by at least the economic bar of 20 bp/day (DECISIONS D7), with the paper's sign.

**14c menu row + tool.** "X predicts forward Y" / "X is monotone in Y": quantile sort (2 bins, top vs bottom half by the
alpha, equal weight, ties = average rank, odd middle coin out, days with < 5 coins or an all-tied split skipped) of next-day
returns; statistic = mean daily spread (bp/day) with Newey-West(5) SE. Secondary, descriptive only: mean daily Spearman IC.

**Decision rule (pre-committed, three branches).**
- **supported** if mean spread >= 20 bp/day AND t >= 1.645 (size condition AND significance condition);
- **refuted** if mean + 1.645 x SE < 20 bp/day AND t < 1.645 (the economic effect is excluded at one-sided 95% and there is
  no significant positive effect);
- **inconclusive** otherwise (including a significant spread below 20 bp/day — never `supported`).

**Evidence weight (fixed now).** Power simulation (code/p1_power.py): EXPLORE's empirical daily
cross-sectional residuals, resampled at C1's own size (N = 327 signal days, mean 8.5 coins/day),
random half split + delta, the rule above applied. Result at noise x1.5 (used): **power 0.480 at delta = 20 bp/day, false-
positive alpha 0.038** (P(refuted | delta=20) 0.050, P(refuted | null) 0.522). At noise x1.0: power 0.495, alpha 0.008 (not used: the lower-power x1.5 numbers are the conservative choice for both weights).
alpha floored at 0.005 for simulation resolution -> alpha used 0.038.
- weight(supported) = power / alpha = 12.735 -> CAPPED at 10 (guard b); applied 10.0
- weight(refuted) = (1 - power) / (1 - alpha) = 0.541
- weight(inconclusive) = 1

**Guard (a).** First test of this sub-claim for H1 on C1; no earlier cell in this session tested it here. Different folds are
separate samples, so their weights multiply.
**Guard (b).** Every weight above is within [0.1, 10] after the cap.

**Slice rules.** H1 is source-born (`born_on: SOURCE`, `seen_on: none`); C1 is not its birth slice, not in seen_on, not yet
opened by H1, and is the lowest CONFIRM fold it is still eligible for (no fold shopping).

**Why this test now (step 1 arithmetic, code/pick.py).**
| expected shift (pp) | hyp | slice | p now | P(sup) | P(ref) | p if sup | p if ref |
|---:|---|---|---:|---:|---:|---:|---:|
| 8.34 | H1 | C1 | 0.16 | 0.108 | 0.446 | 0.656 | 0.093 |
| 7.7 | H1 | EXPLORE | 0.16 | 0.111 | 0.394 | 0.64 | 0.1 |
| 6.04 | H2 | C1 | 0.11 | 0.086 | 0.47 | 0.553 | 0.063 |
| 6.04 | H3 | C1 | 0.11 | 0.086 | 0.47 | 0.553 | 0.063 |
| 6.04 | H4 | C1 | 0.11 | 0.086 | 0.47 | 0.553 | 0.063 |
| 5.66 | H2 | EXPLORE | 0.11 | 0.091 | 0.414 | 0.536 | 0.067 |
| 5.66 | H3 | EXPLORE | 0.11 | 0.091 | 0.414 | 0.536 | 0.067 |
| 5.66 | H4 | EXPLORE | 0.11 | 0.091 | 0.414 | 0.536 | 0.067 |
| 1.69 | H5 | C1 | 0.09 | 0.078 | 0.221 | 0.264 | 0.075 |
| 0.58 | H5 | EXPLORE | 0.09 | 0.129 | 0.179 | 0.127 | 0.084 |

