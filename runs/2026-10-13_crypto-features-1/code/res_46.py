import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
tc = kit.tcrit_for(8)
pw = kit.power(0.0065, 0.02, tc)
w, cap = kit.capped(pw["w_no"], "search")
body = f"""# cell 46 result - H6 venue-gap residuals by home session (TRAIN, hourly, min_n 5; 16 variants; cells/cell_46_table.csv, cells/cell_46_output.txt, plots/cell_46_venue_sessions.png)
Pre-committed branch: NOT SUPPORTED (and not refuted: the best home-session IC is above 0.01). Best home-session variant: cb_gap_lvl (Coinbase gap, entry delay 1, residualised on rev1/rev3) in US-hour signals at h6: IC +0.0141 (NW t 1.63; C1 +0.019, C2 +0.005, C3 +0.026; 2,270 rows), bars IC >= 0.02, t >= Sidak {tc:.2f}, C2 and C3 positive.
Upbit in ASIA-hour signals: ub_retdiff_6 h6 +0.0107 (t 1.1; C3 +0.033, C1 -0.020), ub_gap_lvl h6 +0.0090 (t 0.9). Outside the home sessions the residuals are of the same size (cb_gap_lvl other h6 +0.0081 (1.7); ub_gap_lvl other h6 +0.0118 (1.8)), so a home-session concentration is not there.
weight_applied {w:.3f} (power {pw['power']:.2f} at se 0.0065, delta 0.02, tcrit {tc:.2f}).
Closing H6: three search cells (13, 14, 46), the Binance-bounce rival controlled (14, 46), a session conditional (46), posterior now below its prior: the venue gaps are the Binance bounce plus a residual of ~+0.01 that is C3-only. DROPPED (DECISIONS.md).
"""
kit.result(46, w, variants=16, suggests="none", body=body)
kit.attempt(46, "H6", "venue-gap residuals (delay1 + resid) in home sessions vs other", "best home-session +0.0141 t 1.6: not supported; H6 closed")
kit.set_state("H6", "DROPPED")
kit.write_beliefs(); print(kit.posterior("H6"), kit.load_state()["H6"]["prior"])
