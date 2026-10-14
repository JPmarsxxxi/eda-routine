import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 03 result - H1 attribution + response-switch control (TRAIN; 24 variants; cells/cell_03_output.txt)
PRIMARY (volume scale adds?): IC(seed) - IC(streak-only), paired per day, primary response: h6 -0.0105 (NW t -1.31), h24 +0.0076 (t +1.03). Neither reaches +0.01 with t >= 2.24; the difference is not significantly negative either
(refuted needs t <= -1.65) -> NOT SUPPORTED (inconclusive). weight_applied 0.89 (the no-branch weight stated in the rule file; power 0.13 at delta 0.01).
Reading: in every slice and horizon the volume-scaled seed is no better than the bare streak; the V5/V20 scale is not a feature of this alpha on these coins.
V5/V20 ALONE (rival): the IC changes sign by fold: EXPLORE +0.024 (h1), then C1 -0.053 (t -2.1), C2 -0.066 (-2.3), C3 -0.045 (-2.0) at h1; h6 C2 -0.050, C3 -0.053 (t -2.6). I.e. from 2021-H2 on, a coin whose
5-day volume is high relative to its 20-day volume UNDER-performs over the next 1-6h (volratio_neg IC +0.05 in C1-C3), and not before. A fold-dependent volume-surge reversal, not tied to the streak -> lead for H4.
RESPONSE SWITCH (secondary, no belief weight): scoring against the Binance close instead of the primary price in C2+C3 does NOT recover the seed's C3 IC (seed h6 C3: primary -0.008, Binance -0.015; h24 +0.010 vs +0.002):
paired difference IC(Binance) - IC(primary) over C2+C3: streak h6 -0.004 (t -0.6), h24 +0.013 (t 1.8), h1 -0.020 (t -2.5); r24 h1 -0.014 (t -1.7), h6 -0.011 (t -1.8); seed h24 +0.009 (1.2). The primary (FTMO mid) response is, if anything,
the BETTER response for the short horizons. Cross-sectional rank agreement between the two responses is 0.986-0.995 in C2/C3 (1.000 before). The C3 fade of the seed is therefore NOT the response switch (MEMORY lead answered).
Side finding: r24 (trailing-24h return fade) at anchor 23 is the dominant piece: h6 IC +0.074 (t 6.3) primary / +0.054 (t 5.1) Binance; this is H8.
"""
kit.result(3, 0.89, variants=24, suggests="H4, H8", body=body)
kit.attempt(3, "H1", "volume scale attribution + response-switch control, 4 features x 3 h x 2 responses", "seed - streak -0.0105 (t -1.3) at h6: volume scale adds nothing; C3 fade is not the response switch; volratio flips sign by fold -> H4")
kit.write_beliefs(); print(kit.posterior("H1"))
