weight_applied: 3.0000
variants: 12
suggests: none

# cell 48 result - H13 orthogonality of the UP-state -beta feature (TRAIN, hourly; 12 variants; cells/cell_48_table.csv, cells/cell_48_output.txt, plots/cell_48_bup.png)
Pre-committed branch: SUPPORTED. Residualised on f001 and the market-residual 3h reversal, the UP-state -beta feature at h6 has pooled UP-state score +0.0307 / +0.0331 / +0.0354 (k = 1 / 3 / 6; NW t +6.7 / +7.0 / +7.1); best k=6: folds +0.0271 / +0.0535 / +0.0515 / +0.0321 (EXPLORE/C1/C2/C3), bars score >= 0.015, t >= Sidak 2.64, C2 and C3 positive. weight_applied 3.0 (cap).
Orthogonality (mean XS correlation inside the UP state): with f001 +0.07 (k=1), +0.16 (k=3), +0.08 (k=6); with f002 -0.04 / -0.01 / +0.02; with the market-residual reversal -0.05 / -0.07 / -0.06. At h1 the residual scores are +0.0282 / +0.0242 / +0.0253 (t 8-9).
So the UP-state beta effect is NOT the market component of own-return reversal: it keeps 55-72% of its raw IC after removing it and is essentially uncorrelated with the library reversal features.
OPEN RISK, decomposed from cells 31 and 47: -beta ranking has a positive IC in BOTH market states (UP about +0.063 at h6, DOWN about +0.0135), i.e. a static 'low-beta coins outperform' component a ~ +0.038 plus a market-reversal component c ~ +0.025 (IC(-beta | UP) = a + c, IC(-beta | DOWN) = a - c).
A static beta ranking is a persistent coin attribute (BTC/ETH low, DOGE/SOL high) - the fixed-effect trap of cells 11 and 29 - and 10 coins do not make it a premium. The reversal-only part (the sign flips with the market move) is the claim worth freezing; the next H13 cell separates a, c and the time-varying beta.
