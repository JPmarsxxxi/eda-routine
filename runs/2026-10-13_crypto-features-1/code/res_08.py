import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 08 result - H4 volume / trade-count / size / taker surprises (TRAIN, hourly; 39 variants; cells/cell_08_table.csv, cells/cell_08_output.txt, plots/cell_08_flow_ic.png)
Pre-committed branch: NOT SUPPORTED. In the pre-stated directions (volume/trade-count/size surprise NEGATIVE, taker imbalance POSITIVE) the best pooled-TRAIN score is taker_6 at h24: +0.0095 (t 1.76), far below 0.02 and the Sidak bar 3.22. Every volume/count/size surprise
has the OPPOSITE sign to the pre-stated one at 6h and 24h: nsurp_1 h24 +0.0290 (t 4.3; EXPLORE +0.033, C1 +0.025, C2 -0.007, C3 +0.046), volsurp_1 h24 +0.0219 (t 3.3), nsurp_6 h24 +0.0209 (2.7), nsurp_6 h6 +0.0192 (t 4.3; +0.027/+0.021/-0.014/+0.021).
Wrong-signed significant results count as 'no' (rule). Weight: best variant's own se 0.0060, power 0.55 at delta 0.02 and tcrit 3.22 -> w_no 0.445 -> weight_applied 0.4454.
Other facts: taker_1 (last-hour taker-buy imbalance) at h1 is NEGATIVE: IC -0.0176 (t -8.1), same sign in all four folds (-0.021/-0.020/-0.003/-0.018) and gone by h6 (+0.001): buy-heavy last hour -> lower next hour. That is the order-flow face of the bounce found in cells 5-6 (the last bar's aggressor imbalance
is tied to the last bar's close location); it is a candidate rival of the reversal feature, not a separate predictor, and is checked as such in the next H4 cell. Trade-size surprise: no IC (|IC| <= 0.004 at TRAIN). Volume ratio at hourly anchors (Alpha#30 V5/V20): |IC| <= 0.003, confirming cell 3.
So (i) the predicted direction is refuted for volume/trades and for taker flow at 6h-24h; (ii) a sign-reversed continuation shows up for trade-count/volume surprise at 24h in 3 of 4 folds (C2 = bear market 2022H1 is the exception); (iii) the 1h taker imbalance is contrarian.
suggests: H10 (the volume/trade-count surprise continuation, 3/4 folds, born here, controlled against same-window return and |return| in the next H4/H10 cell); taker_1 contrarian goes into the same control cell as a residual-on-rev1 check (not a hypothesis of its own).
"""
kit.result(8, 0.4454, variants=39, suggests="H10", body=body)
kit.add_h("H10", "Trade-count / volume surprise continuation: coins whose recent trade count runs above its 30-day norm outperform over 6-24h", "H4",
  "cells/cell_08_result.md (nsurp_1 h24 +0.029 t 4.3; 3 of 4 folds positive); OBSERVATIONS #3, #5",
  "Does a coin's 1-24h trade-count (or quote-volume) surprise vs its trailing 30-day norm predict a HIGHER 6-24h cross-sectional return rank, beyond what the same-window return and absolute return explain?",
  "a change in a coin's trade count (volume) over the last 1-24 hours relative to its trailing 720h norm predicts a higher cross-sectional rank of its next 6h/24h primary return because rising participation marks information arrival or attention that continues (an attention-driven momentum), unlike the H4 sign (overheating) we pre-stated",
  "an IC that vanishes after partialling out the same-window signed return and |return| (volume as a transform of the move); a negative sign in 2 or more folds; an effect present only in the C3 trade-count regime",
  "same-window return and |return| (high-volume winners continue: MEMORY LOW on CONFIRM, opposite sign); volatility; the C3 5x trade-count regime shift (OBSERVATIONS #5); market-wide volume days",
  "EXPLORE cell_08", 0.35,
  "cell_08: nsurp_1 h24 IC +0.033/+0.025/-0.007/+0.046 (3/4 folds positive), pooled t 4.3, volsurp_1 h24 +0.022 (t 3.3), but opposite to the story pre-stated in H4 and C2 negative; MEMORY says an earlier volume-winner continuation had the opposite sign on CONFIRM: base 0.30 x1.5 for 3/4 folds, x0.8 for the post-hoc sign -> 0.35")
kit.attempt(8, "H4", "volume/trade count/size/taker surprises x w(1,6,24) x h(3)", "pre-stated directions refuted; opposite-signed nsurp continuation at 24h (3/4 folds); taker_1 contrarian at h1")
kit.write_beliefs(); print(kit.posterior("H4"), kit.posterior("H10"))
