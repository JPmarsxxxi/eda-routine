import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 45 result - H10 conditional split of f003 (TRAIN, hourly; 16 variants; cells/cell_45_table.csv, cells/cell_45_output.txt, plots/cell_45_f003_cond.png)
Pre-stated primary (session contrast at h24): ASIA minus other = +0.0065 (paired by day, NW t +1.08, 1,093 days); US minus other = +0.0008 (t +0.12). Neither is <= -0.02; both are within +-0.01 -> the sign does NOT depend on the session (REFUTED as a dependence claim).
f003 at h24 by session: ASIA +0.0359 (t 5.3), EU +0.0360 (4.3), US +0.0306 (4.0), other +0.0296 (4.4) - all four positive and equal within noise; by market state: up-trend +0.0321, down-trend +0.0328, high market vol +0.0334, low +0.0312. At h6: ASIA +0.0088, EU +0.0269, US +0.0219, other +0.0174.
So the negative nsurp_6/volsurp_6 leads of cell 44 (ASIA and US signals) are properties of those 6-hour-window surprises, not of f003's 1-hour surprise, and they do not carry over; f003's participation continuation is session- and trend-independent at h24.
The one dimension where f003 is weak is the FOLD: C2 (2022H1, a bear/high-correlation period) gives +0.0113 pooled and ~0 in most conditions (ASIA -0.0046, trend_down -0.0022, high market vol +0.0046); C1 and C3 are +0.032 / +0.051. That is the fold-level reason f003's VAL (calm 2023) came in at +0.0201 with t 1.4 rather than failing outright.
weight_applied 1.0: the cell tests a sub-claim (session dependence) whose outcome neither supports nor refutes H10's pooled claim beyond cell 9; applying the rule file's yes/no weights (3.0 / 0.73) to H10 would move it the wrong way for a refuted dependence, so the 'cannot tell' weight 1 is used and the deviation is stated.
"""
kit.result(45, 1.0, variants=16, suggests="none", body=body)
kit.attempt(45, "H10", "f003 IC by session / trend / market-vol conditions at h6, h24", "no session dependence (ASIA-other +0.0065 t 1.1); C2 is the weak fold")
kit.write_beliefs(); print(kit.posterior("H10"))
