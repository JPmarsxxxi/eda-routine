hypothesis: H8
slice: TRAIN
kind: search
controls: none
conditional: anchor session (Asia-night vs US) - time-of-day conditional

# cell 04 rule - H8: session-conditional 24h reversal (controls: none this cell; conditional: anchor session)
Looked at: feature r24 = -(log C_t - log C_{t-24}) (reversal direction: past loser ranks high), a rolling 24h trailing return evaluated at EVERY hour (anchor a = 0..23), scored on h = 1, 6, 24 (24 x 3 = 72 variants).
Session groups, collapsed to one daily series by averaging the anchor ICs of the group within each UTC day: ASIA-NIGHT anchors {21,22,23,0,1} and US anchors {13,14,15,16} (6 group variants). V = 78.
Tool: xs_ic per timestamp, NW t on the daily series (lags h//24+3).
Pre-stated primary test (h6 only, two sides -> tcrit 2.24): SUPPORTED if IC(ASIA-NIGHT, h6) >= +0.02 with NW t >= 2.24 AND IC(US, h6) <= -0.02 with t <= -2.24 (reversal overnight, continuation in US hours).
REFUTED if IC(ASIA-NIGHT) <= 0 with t <= -1.65. Else INCONCLUSIVE. (Both sides were glimpsed in cell 2 for the streak, not for r24 at the US anchors.)
Power: daily-sampled h6, N ~ 1170 days, se 0.0133; delta 0.02, tcrit 2.24: power 0.23, alpha 0.0125, w_yes 18.3 -> 3.00, w_no 0.78.
