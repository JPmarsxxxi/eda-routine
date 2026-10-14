import sys, hashlib, os
ROOT = r"C:\Users\User\eda-routine"; RUN = os.path.join(ROOT, "runs", "2026-10-13_crypto-features-1")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
SHA_W = sha(os.path.join(ROOT, "features", "_wide.py"))
C = {
 8: dict(h="H5", f="f004", variant="F4", H=1, what="perp premium-index crowding (exactly the code of F4/f004): premium_index_close minus its coin's trailing-720h mean, cross-sectional rank residualised on the ranks of r3s and r24, NEGATED",
         cost="gross top-3 minus bottom-3 return +2.12 bp per 1h hold (TRAIN n 25,971) vs 87.3 bp round trip -> COMBINE-ONLY",
         extra="WHAT CHANGED AND WHY (variant_of F4): F4 froze the h24 horizon and failed CONFIRM (C1 +0.0186 t 1.61, C2 +0.0190 t 1.87, C3 +0.0253 t 2.39: all positive, two just under the 0.02 bar). This candidate is the SAME feature code at the declared h1 horizon, chosen from TRAIN looks made BEFORE F4 was run (cell 12 table: h1 +0.0236/+0.0212/+0.0343/+0.0200 per fold, recomputed from features/f004.py in cell 34: residual IC +0.0248, t 11.4) - not from VAL, which was never opened for this feature. It counts as a new spec in K.", mode="hourly"),
 9: dict(h="H14", f="f008", variant="none", H=1, what="hour-of-day seasonality persistence, demeaned: mean 1h log return of the coin at the upcoming hour of day over the previous 60 days (>= 48 observations) minus the coin's trailing 1440h mean 1h return", cost="gross top-3 minus bottom-3 return +2.13 bp per 1h hold (TRAIN n 20,510) vs 88.7 bp round trip -> COMBINE-ONLY",
         extra="Evidence behind it (cells 32-34): TRAIN h1 IC +0.0222 (t 8.3; folds +0.017/+0.017/+0.009/+0.045), Binance-response h1 +0.0203 (t 9.4), max |corr| 0.024 with any candidate/baseline, incremental IC against dense partners +0.018-0.020 (t 7-8). Folds C1 and C2 are below 0.02: a CONFIRM-FAIL is the expected outcome under the unchanged rule.", mode="hourly"),
}
for n, c in C.items():
    lag = c["H"] + 5
    txt = f"""hypothesis: {c['h']}
variant_of: {c['variant']}
feature: {c['f']}
spec: {c['f']} = features/{c['f']}.py (sha256 {sha(os.path.join(ROOT, 'features', c['f'] + '.py'))}; helpers features/_wide.py sha256 {SHA_W}): {c['what']}. Inputs: Binance spot hourly columns (and perp premium-index close for f004) as carded; point-in-time at the END of bar t. Primary horizon h = {c['H']}h: response = log of primary `price` from the END of bar t to the END of bar t+{c['H']} (the other horizons are reported, not judged); invalid where any bar in (t, t+h] has new_source=True. Statistic per fold = mean cross-sectional Spearman rank IC over signal timestamps with >= 6 coins (every hour), NW t with {lag} lags. Universe: the 10 coins as available. Slices built on: EXPLORE, C1, C2, C3 (TRAIN search only); VAL untouched.
{c['extra']}
construction: point-in-time inputs only (Binance spot/perp hourly bars knowable at open+1h; premium index likewise); trailing-only scaling (rolling windows end at t or t-1; no full-sample z-scores or ranks); cross-sectional ranks only; tails: ranks make 14-88x excess kurtosis harmless, inf/NaN dropped; RAW version = pooled panel Pearson corr of the feature rank-z with the next-h return (reported in the confirm cell) and MARKET-NEUTRAL version = the cross-sectional rank IC (neutral by construction); market correlation = corr of the cross-coin mean standardised feature with the equal-weight market forward return, reported in the confirm cell.
pass_rule: per fold (C1, C2, C3) and for VAL: supported if the primary-horizon mean rank IC >= +0.02 and NW t >= 1.96; refuted if IC < 0 and NW t <= -1.65; else inconclusive. CONFIRM-SHOWN needs >= 2 supported folds and none refuted. VAL judged with the same rule on 2023-03-25..2023-11-30.
min_useful: 0.02 (mean rank IC at the primary horizon)
cost_line: {c['cost']}
"""
    open(os.path.join(RUN, "candidates", f"F{n}.md"), "w", encoding="utf-8").write(txt)
print("frozen", list(C))
