weight_applied: 3.0000
variants: 8
suggests: none

# cell 33 result - H14 response-series artifact control (TRAIN, hourly; 8 variants; cells/cell_33_table.csv, cells/cell_33_output.txt, plots/cell_33_hours.png)
Pre-committed branch: SUPPORTED. Scored on the BINANCE-close response (a pure print series with no source switch), season60_dm at h1 has pooled-TRAIN IC +0.0203 (NW t +9.4) and C2+C3 IC +0.0307 (bars: >= 0.02, t >= 1.96, C2+C3 >= 0.015). weight_applied 3.0 (cap).
The primary-price IC (0.0223) and the Binance-response IC (0.0203) are within 0.002 of each other; by fold on the Binance response: EXPLORE +0.0159 (t 5.1), C1 +0.0128 (2.3), C2 +0.0160 (3.0), C3 +0.0408 (9.1). season20_sign h1 on Binance: +0.0175 (t 7.1). At h6 season60_dm is +0.0076 (t 3.7).
So the persistence is not carried by the FTMO mid: it is there in the pure print series too, and in EXPLORE (pre-2021-07, before any source switch) at +0.016.
Hour-of-day decomposition (C2+C3, season60_dm h1, IC by the upcoming hour u): positive at 21 of 24 hours on either response; largest at u = 0, 1 (0.056-0.071), 12 (0.060-0.077), 19, 20 (0.059-0.063), 6; negative only at 10 and 13 UTC (-0.008, -0.009). No single hour or rollover clock carries it.
Open: why C3 is double the other folds (+0.041 on the Binance response): C3 is the fold with the 5x trade-count regime (OBSERVATIONS #5); a smaller C1/C2 value (+0.013/+0.016) is the honest TRAIN size. The seasonal feature is small (IC ~0.013-0.017 in three of four folds) and will be judged by the same 0.02-per-fold pass rule at the freeze stage.
