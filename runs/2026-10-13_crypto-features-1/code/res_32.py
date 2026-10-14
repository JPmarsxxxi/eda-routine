import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 32 result - H14 hour-of-day seasonality persistence (TRAIN, hourly; 21 variants; cells/cell_32_table.csv, cells/cell_32_output.txt, plots/cell_32_season.png)
Pre-committed branch: SUPPORTED. Best demeaned form: season60_dm at h1: IC +0.0223 (NW t +9.2; EXPLORE +0.017, C1 +0.013, C2 +0.0125, C3 +0.0445), Sidak bar 3.04, size bar 0.02. weight_applied 3.0 (cap, hourly se 0.0026, power ~1).
Other: season60_raw h1 +0.0211 (8.8), season60_sign h1 +0.0204 (6.9), season20_dm h1 +0.0154; at h6 the demeaned form keeps +0.0086 (t 3.6) and sign60 +0.0094; at h24 ~0 (|IC| <= 0.003). Demeaning changes little (raw 0.0211 -> dm 0.0223): not a coin fixed effect. The lag-24 reference (same-hour-yesterday return) is slightly NEGATIVE at h1 (-0.0057, t -2.4), consistent with MEMORY.
Persistence works only with averaging: a 60-day mean of the same-hour returns, not the single yesterday.
SHAPE FLAG: the IC is concentrated in C3 (+0.0445, t 9.3) - the fold where the response for 7 of 9 coins is the FTMO hourly mid ('bid + bar spread/2' with the bar's MINIMUM spread, README) and where FTMO rows miss fixed Saturday hours. A mid built that way can carry a repeating hour-of-day offset that differs by coin (spread width), which a 60-day same-hour mean learns
and which is a property of the response series, not of the market. EXPLORE/C1 (response = Binance close) still show +0.017/+0.013 (t 4.4/2.3), so a smaller genuine piece may exist. The control is the same IC scored against the Binance-close response (next H14 cell).
"""
kit.result(32, 3.0, variants=21, suggests="none", body=body)
kit.attempt(32, "H14", "hour-of-day seasonality persistence N=20,60 x raw/demeaned/sign x h", "season60_dm h1 +0.0223 t 9.2 supported; C3-heavy (+0.0445): FTMO-mid artifact suspected")
kit.write_beliefs(); print(kit.posterior("H14"))
