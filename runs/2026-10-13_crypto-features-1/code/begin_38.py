import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
kit.add_h("H15", "Within-bar shape (last-hour microstructure): close location, wicks, bar gap and VWAP deviation of the last bar", "none",
  "TARGET.md FAMILIES (price-path shape: close location, gaps between sessions); OBSERVATIONS #1, #2; cells 5-6 (bounce)",
  "Do the shape of the last hourly bar (where it closed inside its range, wicks, the gap between its first trade and the previous close, the close vs the bar VWAP) rank the next-hour/6h/24h return once the print at the bar end can no longer be the entry (one-bar entry delay)?",
  "a change in the last bar's close location, body, wicks, open-versus-previous-close gap or close-versus-VWAP deviation predicts the cross-sectional rank of the following bars' returns because the bar's internal order flow (where the aggressive flow ended) is information about pressure that the close print does not fully carry",
  "no shape feature shows an IC beyond min_useful at the delayed-entry (bounce-free) scoring; an IC present only at the undelayed entry is the Binance last-print bounce (cells 5-6)",
  "bid-ask bounce of the last print (cells 5-6); the last-hour return itself (the shape variables are transforms of it); the trade-count and taker-imbalance bounce (cell 9: taker_1 contrarian = rev1)",
  "EXPLORE #1 #2", 0.25,
  "no earlier run looked at within-bar shape; tracker base 0.30 x0.85 because cells 6 and 9 show the last-print information is bounce at h1 and ~half of the 1-6h reversal dies with a one-bar delay -> 0.25")
tc = kit.tcrit_for(21)
rule = f"""# cell 38 rule - H15: within-bar shape of the last hourly bar (controls: bid-ask bounce via a one-bar entry delay; conditional: none)
Features (Binance spot hourly bar t, known at its end; O, H, L, C = open, high, low, close; vwap = quote_vol/vol): clv1 = (C-L)/(H-L); body = log(C/O); body_n = body/log(H/L); upper_wick = log(H/max(O,C))/log(H/L); lower_wick = log(min(O,C)/L)/log(H/L);
 gap = log(O_t/C_(t-1)); vwap_dev = log(C/vwap). 7 features. Horizons 1h, 6h, 24h. Entry timing: (a) as everywhere (response starts at the end of bar t); (b) one-bar delay (response starts at the end of bar t+1; the bounce-free scoring of cell 6).
Variants: 7 x 3 h x 2 timings = 42 (V = 42).
Pre-stated primary (two-sided, exploratory family): the 21 DELAYED-entry variants, V_primary = 21, tcrit {tc:.2f}: SUPPORTED if the best has |pooled-TRAIN IC| >= 0.02 and NW |t| >= {tc:.2f} (the sign is then taken as the finding, but it is a new hypothesis' birth, not the pre-stated claim).
Undelayed results are reported only (to show the bounce share). Power at the delayed h6 (se 0.0044) and h24 (se 0.0060): high; w_yes capped 3.0, w_no ~{kit.power(0.0044, 0.02, tc)['w_no']:.2f}-{kit.power(0.0060, 0.02, tc)['w_no']:.2f}.
"""
ann = """### Cell 38 - EDA: H15 does the shape of the last bar carry information beyond its bounce?
**Sub-claim:** (Q3 impostor) bar-shape variables are the last-print bounce; (Q6) the delayed scoring is the test. **Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(38, "H15", "TRAIN", "search", "bid-ask bounce (one-bar entry delay)", "none", rule, ann)
