weight_applied: 3.0000
variants: 54
suggests: none

# cell 06 result - H3 rival control: bid-ask bounce (TRAIN, hourly; 54 variants; cells/cell_06_table.csv, cells/cell_06_output.txt, plots/cell_06_bounce.png)
Pre-stated primary (delay-1 / skip-1 reversal, h6): k=3: pooled TRAIN IC +0.0301 (NW t +9.3); C1 +0.017 (t 2.2), C2 +0.045 (5.0), C3 +0.037 (5.5); C2+C3 +0.040. k=2: +0.0284 (t 10.1); C2+C3 +0.036. Bars (IC >= 0.02, t >= 2.24, C2+C3 >= 0.02): MET -> SUPPORTED. Power ~1.0 -> weight_applied 3.0 (cap).
Bounce share (1 - IC(delay1)/IC(base), TRAIN): h1 60-69% for k1-k3, 52% for k6; h6 49% (k2, k3), 58% (k1), 41% (k6); h24 61-66%. So roughly half of the base 1-6h IC is gone once the print at t cannot be the start of the response.
Identity found: skip-1 (feature lagged one bar) and entry-delay-1 give the SAME IC series (shift invariance) - the bounce-free feature is simply the reversal lagged one bar. The IC after delay 2 is still positive at 3 hours (k3 h6: +0.0222, t 6.8; k6 h6 +0.0217), and ~0 at h24 (delay2 k3 h24 +0.003).
Fold shape of the surviving reversal (delay1 k3 h6): EXPLORE +0.027, C1 +0.017, C2 +0.045, C3 +0.037 - NOT decaying; EXPLORE/C1 (pure Binance print response) are the LOWEST, C2/C3 (FTMO mid response for 7 coins) the highest. The base IC drops from EXPLORE 0.068 to C2/C3 0.06/0.052 but the delayed IC rises
0.027 -> 0.045/0.037. In C2/C3 the base-vs-delay gap shrinks (0.061 -> 0.045 in C2) as expected if the print's own bounce no longer sits in the response; the Binance-response comparison (k2: base_binResp C3 h1 +0.074 vs primary +0.065) agrees.
Not separable here: how much of the 41-69% lost is pure bounce versus a fast genuine 1-hour reversal that decays by the next hour. Whichever, the tradeable-after-delay IC is 0.03 at h6 (t 9) and passes min_useful with room; the base IC (0.058) must not be quoted as the signal.
Consequences for the library: the feature to freeze is the skip-1 version (k=3 or k=2), horizons h1/h6; the unlagged version is flagged bounce-contaminated. Costs: see the cost line at freeze (turnover is hourly).
