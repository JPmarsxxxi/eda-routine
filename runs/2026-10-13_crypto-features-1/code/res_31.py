import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
tc = kit.tcrit_for(2)
pw = kit.power(0.0062, 0.015, tc)
w, cap = kit.capped(pw["w_no"], "search")
body = f"""# cell 31 result - H13 fixed effect or reversal (TRAIN, hourly; 30 variants; cells/cell_31_table.csv, cells/cell_31_output.txt, plots/cell_31_updown.png)
Pre-committed branch: REFUTED (the fixed-effect reading). Both pre-stated pairs have opposite signs in the two market states: (k=6, h=6) UP -0.0628 (t -9.8) vs DOWN +0.0135 (t +2.0); (k=24, h=24) UP -0.0931 (t -7.6) vs DOWN +0.0379 (t +2.7).
All 4 k at h24: UP -0.0785..-0.0931 (4/4 folds negative), DOWN +0.038..+0.056 (3/4 folds positive, EXPLORE ~0): the ranking by beta flips with the sign of the market move and so does the IC, i.e. the IC is 'high-beta coins underperformed' (a coin attribute), not a conditional reversal.
weight_applied {w:.3f} (no-branch at power {pw['power']:.2f}, se 0.0062, delta 0.015, tcrit {tc:.2f}).
What survives: (1) the detrended product (lead minus the coin's own trailing mean) is still -0.0325 at h1 (k=1; t -13.2; folds -0.038/-0.036/-0.032/-0.019) and -0.027 at h6 (k=6; t -6.6) - a time-varying piece is there. (2) At h1 the asymmetry is the finding: after market-UP hours high-beta coins fall in the next hour (IC -0.052, t -16.3; 4/4 folds) but after market-DOWN hours there is no matching rebound (IC -0.009, t -2.5).
That h1 up-state pattern is most plausibly the same Binance last-print bounce as cells 5-6 (market-wide up hours close on the ask side, more so for high-beta coins); the delayed-entry control was not run here.
Not pursued: the h1 UP-state beta reversal (probable bounce; below the value of chasing it: the library already holds the bounce-free reversal f001, which it would need to beat with an entry delay), and the detrended-product form (no mechanism beyond the market reversal).
Library consequence: no feature from H12/H13; the beta x market products are fixed effects in sign-agnostic ICs and must be state-split before being believed.
"""
kit.result(31, w, variants=30, suggests="not pursued: h1 UP-state beta reversal (probable Binance last-print bounce, no delay control run; f001 already covers the bounce-free reversal); detrended-product form (no mechanism beyond the market reversal)", body=body)
kit.attempt(31, "H13", "beta x market move by UP/DOWN state + detrended form", "opposite signs in UP/DOWN at h6, h24: fixed effect, refuted")
kit.write_beliefs(); print(kit.posterior("H13"))
