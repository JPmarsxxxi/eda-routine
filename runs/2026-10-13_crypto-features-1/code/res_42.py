import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 42 result - H16 multi-day range position, drawdown, rally, MA distance (TRAIN, hourly; 96 variants; cells/cell_42_table.csv, cells/cell_42_output.txt, plots/cell_42_range.png)
Pre-committed branch: SUPPORTED by the letter: best detrended primary variant dd_72 (log of the close over the trailing 72-hour maximum close, minus the coin's own 2160h mean) at h6: score (-IC) +0.0317 (NW t +6.5; EXPLORE +0.033, C1 +0.034, C2 +0.034, C3 +0.025), bars score >= 0.02, t >= Sidak 3.16. weight_applied 3.0 (cap).
Also: madev_72 h6 +0.0261, dd_336 h6 +0.0252, dd_168 h6 +0.0250, madev_168 h6 +0.0211, pos_72 h6 +0.0209; at h24 only dd_336 +0.0262 (t 2.6, below Sidak). Everything is a 6h effect with a 3-14 day window and strongest at the short end (72h): the shorter the window the larger the IC.
Sign: the score is -IC, i.e. a coin that is farther below its recent high/mean (deeper drawdown, lower position) outperforms over the next 6 hours: it is the multi-day extension of the short-horizon reversal. Level forms show the fixed-effect trap again (dd_72 level h24 +0.041 t 4.8: collapses to ~0.016 detrended).
NOT CONTROLLED in this cell: the same-window return. A drawdown from a 72-hour high is mostly the last 72 hours' return (and the last hours' fall); the rule had the fixed-effect control but not the reversal rival, so the supported branch does not yet say the feature adds anything to f001/f002 (r3s 0.23 correlated, r24 baseline 0.24). Next H16 cell.
"""
kit.result(42, 3.0, variants=96, suggests="none", body=body)
kit.attempt(42, "H16", "range position/drawdown/rally/MA distance x 4 windows x level/detrended x 3 h", "dd_72 detrended h6 score +0.032 t 6.5: supported by rule; reversal rival uncontrolled")
kit.write_beliefs(); print(kit.posterior("H16"))
