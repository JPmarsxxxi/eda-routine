import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 16 result - H2 conditional split of f54_roll (TRAIN; 24 variants; cells/cell_16_table.csv, cells/cell_16_output.txt, plots/cell_16_f54_conditions.png)
Pre-stated primary (h24, trend state): down-trend state IC +0.0263 (NW t +2.95, 11,920 hours; slices +0.006/+0.059/+0.024/+0.039), up-trend +0.0308 (t 3.7). The continuation is NOT a bull-only impostor: the down-state IC clears 0.02 with t >= 1.96 -> SUPPORTED. weight_applied 3.0 (cap).
Caveat on the up/down shares: the up state covers 64% of EXPLORE hours, 54% C1, 22% C2, 41% C3 (2022H1 was a bear market): C2's IC at h24 (+0.026 pooled) comes mostly from the down state. After residualising on the 24h return rank the down-state IC is smaller (+0.0184, t 2.3) and the up-state larger (+0.0385, t 5.0).
Session of the anchor (h24): US(13-16) +0.0450 (t 5.1; +0.040/+0.100/+0.020/+0.029), EU +0.0304, other +0.0254, ASIA +0.0208. h1 and h6 stay negative in every state (h1: up -0.0295, down -0.0413; ASIA -0.0491; US -0.0113), i.e. the 1-6h reversal of strong closes sits mainly in the ASIA anchors (the H9 amplitude clock again) and the 24h continuation is strongest in US anchors.
Reading: f54's h24 continuation survives the trend split, is positive in all four folds and largest in the US-anchor window; its candidate (freeze) has a fold profile 1 strongly supported (C1), others weak: freeze as is and let CONFIRM decide.
"""
kit.result(16, 3.0, variants=24, suggests="none", body=body)
kit.attempt(16, "H2", "f54_roll h24 by trend state (up/down) and session; residual on r24", "down-state IC +0.026 t 2.95: not a bull impostor; US-anchor strongest")
kit.write_beliefs(); print(kit.posterior("H2"))
