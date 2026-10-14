hypothesis: H14
slice: TRAIN
kind: search
controls: response series: FTMO-mid artifact (Binance-close response)
conditional: fold (C2/C3 mid vs EXPLORE/C1 prints)

# cell 33 rule - H14 rival control: is the seasonality a property of the FTMO-mid response? (controls: response series - Binance close vs primary price; conditional: fold)
Features: season60_dm and season20_sign (cell 32), at h = 1 and 6. Each scored against (a) the PRIMARY forward return and (b) the BINANCE-close forward return for the same bars (RB; no source switch, a pure print series throughout).
Variants: 2 features x 2 responses x 2 horizons = 8; plus an hour-of-day decomposition (IC by signal hour u = hour of the NEXT bar, for season60_dm at h1, both responses, C2+C3) = 24 x 2 = 48 descriptive cells, not counted as test variants. V = 8.
Pre-stated primary (one test): season60_dm at h1 scored on the BINANCE-close response: SUPPORTED if the pooled-TRAIN IC >= +0.02 with NW t >= 1.96 AND the C2+C3 IC on the Binance response is >= +0.015 (the seasonal persistence is not carried by the FTMO mid).
REFUTED (response artifact) if the pooled-TRAIN Binance-response IC is <= 0.01. Else INCONCLUSIVE.
Power: hourly h1, se 0.0026, delta 0.02: power ~1.0; w_yes capped 3.0; w_no capped 0.33.
