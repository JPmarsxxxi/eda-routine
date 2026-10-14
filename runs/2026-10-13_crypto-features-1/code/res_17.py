import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 17 result - H3: orthogonality, incremental IC and cost line of the seven feature modules (TRAIN; 28 variants; cells/cell_17_output.txt, cells/cell_17_corr.csv, work/cell17_stats.json, plots/cell_17_corr.png)
Code check: features/f001.py equals the search-cell rev3s (max abs diff 0.0) and features/f005.py equals the search-cell a54_roll (0.0). The registered code is the code that was searched.
PRE-STATED PRIMARY (f001 not a duplicate): max |corr| of f001 with the other six candidates and the five baselines = 0.24 (b_rev24; 0.23 with f002), far under 0.7; incremental IC after partialling out its two most correlated (b_rev24, f002) = +0.0364 (NW t +8.0) vs raw +0.0301 -> SUPPORTED. weight_applied 3.0 (cap).
Primary-horizon IC by fold (TRAIN): f001 h6 +0.027/+0.017/+0.045/+0.037 (pooled +0.0301, t 9.3); f002 h6 +0.051/+0.043/+0.036/+0.019 (+0.0412, t 6.2; C3 weakest); f003 h24 +0.031/+0.032/+0.011/+0.051 (+0.0324, t 5.6); f004 h24 +0.029/+0.019/+0.019/+0.025 (+0.0249, t 5.0);
f005 h24 +0.016/+0.077/+0.026/+0.028 (+0.0291, t 4.7); f006 h6 +0.040/+0.059/+0.060/+0.029 (+0.0433, t 3.6); f007 h24 +0.039/+0.037/-0.002/+0.002 (+0.0262, t 2.3: fades in C2 and C3, the MEMORY pattern).
Orthogonality (mean cross-sectional Spearman on shared timestamps): all candidate pairs |corr| <= 0.30 except f006-f007 = 0.78 (the seed is the streak times a volume scale) and f002-b_rev24 = 0.88 (f002 IS the 24h reversal, gated to 21-06 UTC and lag-1). f004 (premium crowding) is the most independent: max |corr| 0.05 with anything.
Incremental IC at the primary horizon after partialling out the two most correlated others: f001 +0.0364; f002 -0.0140 (b_rev24 explains it: duplicate of the baseline, though not of another candidate: its max corr with a CANDIDATE is 0.30); f003 +0.0254; f004 +0.0216; f005 +0.0290; f006 +0.0098 (t 0.8; f007 takes it); f007 +0.0183 (t 1.7; f006 takes it).
=> f006 and f007 are one family (corr 0.78); f007 does not clear the incremental bar over f006 (0.0183 < 0.02) and is the one to merge as a variant; both are still frozen and tested below because both are TARGET.md seeds (the registry row for f007 will say 'duplicate of f006').
Cost line (TRAIN, top-3 minus bottom-3 forward return in bp per signal at the primary horizon against 2 x the mean round trip of the six traded names ~87 bp): f001 -0.75 bp (h6), f002 -4.59 (h6), f003 +23.5 (h24), f004 +5.98 (h24), f005 +20.8 (h24), f006 +2.24 (h6), f007 +18.5 (h24): every feature is COMBINE-ONLY.
Note the mismatch between rank IC and extreme-quantile spread for f001/f002/f006: a +0.03-0.04 rank IC with ~0 bp top-3/bottom-3 return means the reversal is carried by the middle of the ranks (and by the lower-vol coins), not by the extreme high-vol coins (DOGE, SOL) that dominate the tails.
Library note: the IC table (all three horizons, per fold) is in the cell output; f003 is small at h1 (+0.006) and f001/f002/f004 are mostly 1-6h, f003/f004/f005 24h.
"""
kit.result(17, 3.0, variants=28, suggests="none", body=body)
kit.attempt(17, "H3", "7 feature modules: IC by horizon/fold, 12x12 correlation, incremental IC, cost line", "f001 max corr 0.24; f006~f007 0.78 duplicate; f002 = lagged b_rev24; all COMBINE-ONLY")
kit.write_beliefs(); print(kit.posterior("H3"))
