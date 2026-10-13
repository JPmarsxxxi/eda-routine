hypothesis: H1
slice: C2
kind: test

# cell_08 rule — H1 (Alpha#101) on C2 (2021-05-13 .. 2022-03-08 excl.)

**Sub-claim (the one the hypothesis cannot survive without).** On C2, the verbatim Alpha#101 = `((close - open) / ((high - low) + .001))`, computed
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

**Evidence weight (fixed now).** Power simulation (code/p2_power_v2.py, DECISIONS D14): the rule above applied to 200,000
draws of the mean spread ~ Normal(delta, SE) with SE = 30.37 bp = (EXPLORE-pool bootstrap SE at C2's own size,
N = 282 signal days) x noise scale 3.833
(the measured C1 null-noise ratio, applied to every CONFIRM fold). Result: **power 0.163 at delta = 20 bp/day, false-
positive alpha 0.049** (P(refuted | delta=20) 0.050, P(refuted | null) 0.161).
alpha floored at 0.005 for simulation resolution -> alpha used 0.049.
- weight(supported) = power / alpha = 3.311 (within the 10x cap); applied 3.311
- weight(refuted) = (1 - power) / (1 - alpha) = 0.881
- weight(inconclusive) = 1

**Guard (a).** First test of this sub-claim for H1 on C2; no earlier cell in this session tested it here. Different folds are
separate samples, so their weights multiply.
**Guard (b).** Every weight above is within [0.1, 10] after the cap.

**Slice rules.** H1 is source-born (`born_on: SOURCE`, `seen_on: none`); C2 is not its birth slice, not in seen_on, not yet
opened by H1, and is the lowest CONFIRM fold it is still eligible for (no fold shopping).

**Why this test now (step 1 arithmetic, code/pick.py).**
| expected shift (pp) | hyp | slice | p now | P(sup) | P(ref) | p if sup | p if ref |
|---:|---|---|---:|---:|---:|---:|---:|
| 2.82 | H1 | C2 | 0.656 | 0.124 | 0.088 | 0.863 | 0.627 |
| 1.5 | H6 | C1 | 0.14 | 0.065 | 0.144 | 0.34 | 0.126 |
| 1.22 | H4 | C1 | 0.11 | 0.062 | 0.147 | 0.281 | 0.099 |
| 0.77 | H2 | C1 | 0.066 | 0.057 | 0.152 | 0.183 | 0.059 |
| 0.77 | H3 | C1 | 0.066 | 0.057 | 0.152 | 0.183 | 0.059 |
| 0.42 | H5 | C1 | 0.09 | 0.054 | 0.093 | 0.16 | 0.086 |
| 0.32 | H5 | EXPLORE | 0.09 | 0.053 | 0.083 | 0.144 | 0.087 |

