hypothesis: H1
slice: VAL
kind: val

# cell_28 rule — VAL pass for H1 (Alpha#101), the only HIGH-CONFIRM hypothesis

> **VAL_NOTE (TARGET.md, quoted beside every VAL number):** VAL is weak evidence. (1) BTC VAL was crossed twice by earlier work and overlaps a spent pooled row of an earlier BTC seasonality EDA. (2) VAL has since been opened ONCE more, on all 10 coins, for a pre-registered test of the crash-day rebound topic (see ALREADY TESTED): SOFT-clean for every coin for that topic. (3) VAL may be a DIFFERENT REGIME from TRAIN (2023 was calm; from 2023-04 BTC's 1-minute trade counts fell ~8x, cause not established).

Why VAL: H1 is HIGH-CONFIRM (posterior 0.863 > 0.85, supported on C1 and C2, refuted on none). RUNBOOK_v3 Phase 3: open VAL
ONCE, rule first, report even a failure; never described as out-of-sample proof. **Caveat written before the test:** the
0.863 rests on cell_01's overstated weight (DECISIONS D14); at the honest weight H1 would be ~0.67 (OPEN).

Sub-claim: on VAL (2023-03-25 .. 2023-12-01 excl.), the top half of coins by verbatim Alpha#101 (Binance UTC daily bar of day d)
out-earns the bottom half over end of d -> end of d+1 (primary `price`; FTMO mid for 7 coins in 2023) by >= 20 bp/day.
Tool: the same 2-bin quantile sort, mean spread, Newey-West(5) SE; IC descriptive.
Decision rule: **supported** if mean >= 20 bp/day AND t >= 1.645; **refuted** if mean + 1.645 SE < 20 AND t < 1.645;
**inconclusive** otherwise.
Power (normal sampling, 200,000 draws): N = 213 usable VAL signal days (coverage flags only), SE assumed 38.0 bp
(= C3's EXPLORE-pool simulated SE 8.21 x sqrt(310/213) x the largest measured fold null-noise ratio 3.83;
conservative). Result: power 0.131 at 20 bp/day, alpha 0.050 (P(ref|20) 0.050, P(ref|0) 0.131).
Weights: supported = power/alpha = 2.653 -> 2.653; refuted = (1-power)/(1-alpha) = 0.914; inconclusive 1.
Guard (a): first VAL look for H1. Guard (b): within 10x.
Cost line to report alongside (TARGET.md): round trip BTC 18.9, ETH 25.4, LTC 36.5, ADA/DOGE/DOT/BNB/SOL ~45-47, XRP 68.6 bp.
