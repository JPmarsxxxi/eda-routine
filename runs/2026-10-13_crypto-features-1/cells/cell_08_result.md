weight_applied: 0.4454
variants: 39
suggests: H10

# cell 08 result - H4 volume / trade-count / size / taker surprises (TRAIN, hourly; 39 variants; cells/cell_08_table.csv, cells/cell_08_output.txt, plots/cell_08_flow_ic.png)
Pre-committed branch: NOT SUPPORTED. In the pre-stated directions (volume/trade-count/size surprise NEGATIVE, taker imbalance POSITIVE) the best pooled-TRAIN score is taker_6 at h24: +0.0095 (t 1.76), far below 0.02 and the Sidak bar 3.22. Every volume/count/size surprise
has the OPPOSITE sign to the pre-stated one at 6h and 24h: nsurp_1 h24 +0.0290 (t 4.3; EXPLORE +0.033, C1 +0.025, C2 -0.007, C3 +0.046), volsurp_1 h24 +0.0219 (t 3.3), nsurp_6 h24 +0.0209 (2.7), nsurp_6 h6 +0.0192 (t 4.3; +0.027/+0.021/-0.014/+0.021).
Wrong-signed significant results count as 'no' (rule). Weight: best variant's own se 0.0060, power 0.55 at delta 0.02 and tcrit 3.22 -> w_no 0.445 -> weight_applied 0.4454.
Other facts: taker_1 (last-hour taker-buy imbalance) at h1 is NEGATIVE: IC -0.0176 (t -8.1), same sign in all four folds (-0.021/-0.020/-0.003/-0.018) and gone by h6 (+0.001): buy-heavy last hour -> lower next hour. That is the order-flow face of the bounce found in cells 5-6 (the last bar's aggressor imbalance
is tied to the last bar's close location); it is a candidate rival of the reversal feature, not a separate predictor, and is checked as such in the next H4 cell. Trade-size surprise: no IC (|IC| <= 0.004 at TRAIN). Volume ratio at hourly anchors (Alpha#30 V5/V20): |IC| <= 0.003, confirming cell 3.
So (i) the predicted direction is refuted for volume/trades and for taker flow at 6h-24h; (ii) a sign-reversed continuation shows up for trade-count/volume surprise at 24h in 3 of 4 folds (C2 = bear market 2022H1 is the exception); (iii) the 1h taker imbalance is contrarian.
suggests: H10 (the volume/trade-count surprise continuation, 3/4 folds, born here, controlled against same-window return and |return| in the next H4/H10 cell); taker_1 contrarian goes into the same control cell as a residual-on-rev1 check (not a hypothesis of its own).
