hypothesis: H3
slice: C1
kind: test

# cell_23 rule — H3 (Alpha#2) on C1 (2020-06-04 .. 2021-05-06 excl.)

**Sub-claim (the one the hypothesis cannot survive without).** On C1, the verbatim Alpha#2 = `(-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))`, computed
from Binance UTC daily bars of day d, sorts coins so that the next-day primary `price` return (end of d -> end of d+1) of
the top half exceeds the bottom half by at least the economic bar of 20 bp/day (DECISIONS D7), with the hypothesis's stated sign.

**14c menu row + tool.** "X predicts forward Y" / "X is monotone in Y": quantile sort (2 bins, top vs bottom half by the
alpha, equal weight, ties = average rank, odd middle coin out, days with < 5 coins or an all-tied split skipped) of next-day
returns; statistic = mean daily spread (bp/day) with Newey-West(5) SE. Secondary, descriptive only: mean daily Spearman IC.

**Decision rule (pre-committed, three branches).**
- **supported** if mean spread >= 20 bp/day AND t >= 1.645 (size condition AND significance condition);
- **refuted** if mean + 1.645 x SE < 20 bp/day AND t < 1.645 (the economic effect is excluded at one-sided 95% and there is
  no significant positive effect);
- **inconclusive** otherwise (including a significant spread below 20 bp/day — never `supported`).

**Evidence weight (fixed now).** Power simulation (code/p2_power_v4.py, DECISIONS D14+D15+D17): the rule above applied to 200,000
draws of the mean spread ~ Normal(delta, SE) with SE = 31.01 bp = (EXPLORE-pool bootstrap SE at C1's own size,
N = 327 signal days) x noise scale 3.833
(the measured null-noise ratio of C1). Result: **power 0.158 at delta = 20 bp/day, false-
positive alpha 0.050** (P(refuted | delta=20) 0.051, P(refuted | null) 0.159).
alpha floored at 0.005 for simulation resolution -> alpha used 0.050.
- weight(supported) = power / alpha = 3.166 (within the 10x cap); applied 3.166
- weight(refuted) = (1 - power) / (1 - alpha) = 0.886
- weight(inconclusive) = 1

**Guard (a).** First test of this sub-claim for H3 on C1; no earlier cell in this session tested it here. Different folds are
separate samples, so their weights multiply.
**Guard (b).** Every weight above is within [0.1, 10] after the cap.

**Slice rules.** H3 is source-born (`born_on: SOURCE`, `seen_on: none`); C1 is not its birth slice, not in seen_on, not yet
opened by H3, and is the lowest CONFIRM fold it is still eligible for (no fold shopping).

**Why this test now (step 1 arithmetic, code/pick.py).**
| expected shift (pp) | hyp | slice | p now | P(sup) | P(ref) | p if sup | p if ref |
|---:|---|---|---:|---:|---:|---:|---:|
| 0.77 | H3 | C1 | 0.066 | 0.057 | 0.152 | 0.183 | 0.059 |
| 0.42 | H5 | C1 | 0.09 | 0.054 | 0.093 | 0.16 | 0.086 |
| 0.32 | H5 | EXPLORE | 0.09 | 0.053 | 0.083 | 0.144 | 0.087 |

