import sys, os, json, re, hashlib, glob
sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code"); sys.path.insert(0, r"C:\Users\User\eda-routine")
import kit, gate

ROOT = r"C:\Users\User\eda-routine"; RUN = os.path.join(ROOT, "runs", "2026-10-13_crypto-features-1"); RN = os.path.basename(RUN)
W = lambda p, t, mode="w": open(p, mode, encoding="utf-8").write(t)

# ---- 1. hypothesis states
for h in ("H2", "H3", "H5", "H9", "H10"):
    kit.set_state(h, "CHECKED")
kit.write_beliefs()

# ---- 2. feature registry rows (no pipes inside cells)
rows = [
 ("f001", "reversal (bounce-free)", "-(log C[t-1] - log C[t-4]) on Binance spot closes; higher = past loser; primary h6 (h1 also)", "close", "features/f001.py", "C1= C2+ C3+", "+0.0141 (t 1.99, inconclusive)", "0.24 (b_rev24; 0.23 f002)", "+0.0364 (h6, after b_rev24 and f002)", "VAL-FAIL"),
 ("f002", "reversal (24h, session-gated)", "-(log C[t-1] - log C[t-25]) only for signal hours 21-06 UTC; primary h6", "close", "features/f002.py", "C1+ C2+ C3=", "+0.0284 (t 1.93, inconclusive)", "0.30 (f006); 0.88 (b_rev24 baseline: it is the gated 24h reversal)", "-0.0140 (h6, after b_rev24 and f006: no gain over the plain 24h reversal)", "VAL-FAIL"),
 ("f003", "participation surprise", "log(trades[t] / mean trades[t-720..t-1]) as XS rank residualised on the bar return and abs return; primary h24", "n, close", "features/f003.py", "C1+ C2= C3+", "+0.0201 (t 1.38, inconclusive)", "0.25 (b_mom168)", "+0.0254 (h24, after b_mom168 and b_liq)", "VAL-FAIL"),
 ("f004", "perp premium crowding", "premium_index_close minus own trailing-720h mean, XS rank residualised on r3s and r24, negated; F4 h24 frozen (CONFIRM-FAIL C1= C2= C3+), F8 h1 variant (C1+ C2+ C3=)", "prem_close, close", "features/f004.py", "F8 h1: C1+ C2+ C3=", "F8 h1 +0.0210 (t 4.73, supported)", "0.05 (b_rev1)", "+0.0248 (h1, after b_rev1 and f005); +0.0216 (h24)", "VAL-PASS"),
 ("f005", "closing strength (Alpha#54)", "((C-L24)/(H24-L24)) * (O24/C)^5 on rolling 24h blocks; primary h24 (h1/h6 have the opposite sign)", "open, high, low, close", "features/f005.py", "C1+ C2= C3+", "+0.0164 (t 1.14, inconclusive)", "0.22 (f001, b_rev1)", "+0.0290 (h24, after b_rev1 and f001)", "VAL-FAIL"),
 ("f006", "streak fade (Alpha#30 leg)", "1 - pct rank of the 3-day sign streak at the 23:00 bar; primary h6", "close", "features/f006.py", "C1+ C2= C3=", "not run (CONFIRM-FAIL)", "0.78 (f007)", "+0.0098 (h6, after f007 and b_rev24)", "CONFIRM-FAIL"),
 ("f007", "volume-scaled streak fade (Alpha#30 seed)", "(1 - pct rank of the 3-day sign streak) * sum(vol,5d)/sum(vol,20d) at the 23:00 bar; primary h24; duplicate of f006", "close, vol", "features/f007.py", "C1= C2= C3=", "not run (CONFIRM-FAIL)", "0.78 (f006)", "+0.0183 (h24, after f006 and b_rev24: duplicate)", "CONFIRM-FAIL"),
 ("f008", "hour-of-day seasonality", "mean 1h return of the coin at the upcoming hour over the last 60 days minus its 1440h mean return; primary h1", "close", "features/f008.py", "C1= C2= C3+", "not run (CONFIRM-FAIL)", "0.02 (f006)", "+0.018 to +0.020 (h1, after dense partners f001, b_rev24 / b_rev1, f001)", "CONFIRM-FAIL"),
 ("f009", "funding crowding beyond premium", "last settled funding minus own trailing-720h mean, XS rank residualised on r3s, r24 and f004, negated; primary h24", "funding, prem_close, close", "features/f009.py", "C1= C2= C3+", "not run (CONFIRM-FAIL)", "0.02 (f005)", "+0.0172 (h24, after r3s, r24 and f004)", "CONFIRM-FAIL"),
]
reg = os.path.join(ROOT, "features", "REGISTRY.md")
txt = open(reg, encoding="utf-8").read()
if "f001" not in txt:
    for r in rows:
        assert not any("|" in c for c in r)
        txt += f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | crypto_panel_validated_2026-10-05 | {r[4]} | {r[5]} | {r[6]} | {r[7]} | {r[8]} | {r[9]} | {RN} |\n"
    W(reg, txt)

# ---- 3. TEST_REQUESTS for VAL-PASS (F8)
F8 = os.path.join(RUN, "candidates", "F8.md")
sha8 = hashlib.sha256(open(F8, "rb").read()).hexdigest()
W(os.path.join(RUN, "TEST_REQUESTS.md"), f"""# TEST_REQUESTS - VAL-PASS candidates handed to the user (the routine never opens TEST)

## F8 - perp premium crowding (feature f004), horizon h1
spec_sha256: {sha8}
hypothesis: H5 (NO-STORY: no)
variant_of: F4 (same feature code at the declared h1 horizon after F4 at h24 failed CONFIRM with C1 +0.0186 and C2 +0.0190 just under 0.02; the family has 2 candidates: F4 h24 and F8 h1; plus F10 funding beyond premium, CONFIRM-FAIL)
confirm: C1=supported (+0.0213, t 4.1), C2=supported (+0.0336, t 6.0), C3=inconclusive (+0.0195, t 4.3)
val: cell_37: IC +0.0210 (NW t +4.73, n 5,803 signal hours, 2023-03-25..2023-11-30) against the pass rule (supported if IC >= +0.02 and t >= 1.96); monthly IC -0.025 (Mar), +0.014, +0.031, +0.031, +0.012, +0.016, +0.042, +0.037, -0.004 (Nov). VAL_NOTE: VAL is weak evidence (crossed on this panel by earlier runs, calm 2023 regime, trade counts fell after 2023-04); not out-of-sample proof.
k: K_train 1245, K_val 5, K_cum_train 1369, K_cum_val 6 (this run's counts over all 17 hypotheses and 10 frozen specs, dataset crypto_panel_validated_2026-10-05; the premium family's own looks are cells 10, 11, 12, 34, 40 (search variants 39+30+33+6+18 = 126) and the confirm cells 21, 35, 41, with VAL cell 37)
label: COMBINE-ONLY
turnover: signal re-ranked every hour (a 1h hold re-forms 24x per day; a 24h hold once per day); no PnL or turnover simulation was run (SCOPE: no backtest)
cost_line: TRAIN gross top-3 minus bottom-3 return +2.12 bp per 1h hold (n 25,971) against 2 x 43.7 = 87.3 bp round trip of the six traded names (TARGET.md measured FTMO costs) -> COMBINE-ONLY; the rank IC is real but the extreme-quantile spread is a few bp.
correlations: market: cross-coin mean standardised feature vs EW market forward return +0.002 (CONFIRM folds), +0.007 (VAL). Baselines/candidates (mean XS Spearman, TRAIN): b_rev1 -0.05, b_rev24 0.00, b_mom168 -0.01, b_lowvol 0.00, b_liq +0.01, f001 0.00, f002 +0.01, f003 +0.01, f005 +0.03, f006 0.00, f007 +0.02, f008 0.00; f009 +0.01. No other VAL-PASS exists in this run.
test_check: run features/f004.py unchanged on TEST; response = log of primary `price` from the END of bar t to the END of bar t+1 (invalid across new_source); per signal hour the cross-sectional Spearman rank IC over the coins with a value; SUPPORTED if the mean IC >= +0.02 with NW t (lags 6) >= 1.96, REFUTED if IC < 0 with t <= -1.65, else inconclusive.
""")
print("sha8", sha8)
