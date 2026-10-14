import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 09 result - H10 control: same-window return and |return| partialled out (TRAIN, hourly; 13 variants; cells/cell_09_table.csv, cells/cell_09_output.txt, plots/cell_09_resid.png)
Pre-committed branch: SUPPORTED. Best residual variant nsurp_1 at h24: IC +0.0323 (NW t +5.5; EXPLORE +0.031, C1 +0.032, C2 +0.011, C3 +0.051 - 4/4 folds positive, C2 weak), bars: IC >= 0.02, t >= Sidak 2.89. Power (se 0.0060, delta 0.02) high -> w_yes capped 3.0, weight_applied 3.0.
Partialling out the move made it STRONGER, not weaker: raw +0.0290 (C2 -0.007) -> residual +0.0323 (C2 +0.011): the C2 negative sign of cell 8 was the signed return of the surprise window. Other residual ICs at h24: volsurp_1 +0.0268 (t 4.6), volsurp_6 +0.0214, nsurp_6 +0.0242 (t 3.6), nsurp_24 +0.006 and volsurp_24 +0.005 (no).
At h6: nsurp_6 +0.0212 (t 5.3), nsurp_1 +0.0183 (t 5.1), volsurp_1 +0.0151, volsurp_6 +0.0179. So the 1-6 hour surprise is what matters (24h-window surprises are zero) and it carries to a 6-24h horizon: a participation/attention shock that persists.
Trade count beats quote volume at the same window (nsurp_1 h24 residual +0.0323 vs volsurp_1 +0.0268), consistent with many-small-trades (retail/attention) rather than big prints. Sizes (sizesurp) had no IC in cell 8.
Taker_1 contrarian check: residualised on the 1h-return rank rev1, the taker imbalance IC at h1 is -0.0020 (t -0.9; raw -0.0176): the whole contrarian taker signal was the last bar's return (the bounce) - answered, no hypothesis (rival of H3).
Fold shape (nsurp_1 h24 residual): +0.031, +0.032, +0.011, +0.051 - the C3 value is the highest and C3 is the 5x trade-count regime; normalising by the trailing 720h norm removes the level shift but a regime-dependence of the effect remains possible. Not yet decided: whether the IC lives in particular sessions (conditional split next).
"""
kit.result(9, 3.0, variants=13, suggests="none", body=body)
kit.attempt(9, "H10", "nsurp/volsurp (w=1,6,24) residualised on same-window return and |return|; taker_1 on rev1", "nsurp_1 h24 residual IC +0.032 t 5.5, 4/4 folds positive: supported; taker_1 contrarian = rev1")
kit.write_beliefs(); print(kit.posterior("H10"))
