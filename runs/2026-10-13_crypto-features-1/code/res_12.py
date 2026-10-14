import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 12 result - H5 conditional split of the detrended, return-residualised premium signal (TRAIN, hourly; 33 variants; cells/cell_12_table.csv, cells/cell_12_output.txt, plots/cell_12_prem_conditions.png)
Pre-stated primary (h6, robustness across the market-premium regime): above-median market premium score +0.0237 (NW t 5.4), below-median +0.0219 (t 5.3); both >= 0.015 and >= tcrit 2.24 -> SUPPORTED: the crowding signal is not a bull/bear impostor (same size in both regimes). weight_applied 3.0 (cap).
Exploratory conditionals (score = -IC, no belief weight): session at h6: US(13-16) +0.0405 (t 6.1; EXPLORE +0.040, C1 +0.042, C2 +0.054, C3 +0.031), ASIA +0.0255, EU +0.0227, other +0.0142; at h24 ASIA +0.0349, US +0.0312, other +0.0208, EU +0.0186.
Funding clock: hours 0-2 after settlement are the strongest at h1/h6 (+0.0274/+0.0281); 3-5 the weakest (+0.0206/+0.0157). Funding floor: when more than half of the coins sit on the 0.0001 floor (neutral-to-bullish funding) the signal is much stronger at h6/h24 (+0.0342/+0.0403 vs +0.0156/+0.0152).
Market premium above its median is stronger at h24 (+0.0349 vs +0.0160; C2 +0.039 vs +0.004). Fold stability of the unconditional form: h6 +0.0255/+0.0146/+0.0316/+0.0168 (EXPLORE/C1/C2/C3), h24 +0.0288/+0.0184/+0.0196/+0.0251, h1 +0.0236/+0.0212/+0.0343/+0.0200: 12/12 positive.
Reading: conditioning helps by up to 2x (floor_hi, US session, above-median market premium) but the unconditional form already passes in every cell and fold; the library keeps the unconditional form (the conditions are for a combiner).
Cross-cell note on hypotheses: the US-session premium strength (premium score +0.040 at h6) is the mirror image of the reversal (no reversal in US hours, cells 4 and 7): the two features are complementary by session. Orthogonality to the reversal features is measured at the freeze stage.
"""
kit.result(12, 3.0, variants=33, suggests="none", body=body)
kit.attempt(12, "H5", "prem_dtr_resid x conditions (market premium regime, funding clock, session, funding floor)", "robust to market premium regime (+0.024/+0.022 at h6); stronger in US hours and when funding is on the floor")
kit.write_beliefs(); print(kit.posterior("H5"))
