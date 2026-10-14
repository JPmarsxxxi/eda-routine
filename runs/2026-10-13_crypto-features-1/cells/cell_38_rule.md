hypothesis: H15
slice: TRAIN
kind: search
controls: bid-ask bounce (one-bar entry delay)
conditional: none

# cell 38 rule - H15: within-bar shape of the last hourly bar (controls: bid-ask bounce via a one-bar entry delay; conditional: none)
Features (Binance spot hourly bar t, known at its end; O, H, L, C = open, high, low, close; vwap = quote_vol/vol): clv1 = (C-L)/(H-L); body = log(C/O); body_n = body/log(H/L); upper_wick = log(H/max(O,C))/log(H/L); lower_wick = log(min(O,C)/L)/log(H/L);
 gap = log(O_t/C_(t-1)); vwap_dev = log(C/vwap). 7 features. Horizons 1h, 6h, 24h. Entry timing: (a) as everywhere (response starts at the end of bar t); (b) one-bar delay (response starts at the end of bar t+1; the bounce-free scoring of cell 6).
Variants: 7 x 3 h x 2 timings = 42 (V = 42).
Pre-stated primary (two-sided, exploratory family): the 21 DELAYED-entry variants, V_primary = 21, tcrit 3.04: SUPPORTED if the best has |pooled-TRAIN IC| >= 0.02 and NW |t| >= 3.04 (the sign is then taken as the finding, but it is a new hypothesis' birth, not the pre-stated claim).
Undelayed results are reported only (to show the bounce share). Power at the delayed h6 (se 0.0044) and h24 (se 0.0060): high; w_yes capped 3.0, w_no ~0.07-0.38.
