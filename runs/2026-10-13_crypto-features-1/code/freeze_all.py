import sys, hashlib, os
sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
ROOT = r"C:\Users\User\eda-routine"; RUN = os.path.join(ROOT, "runs", "2026-10-13_crypto-features-1")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
FEAT = {i: sha(os.path.join(ROOT, "features", f"f00{i}.py")) for i in range(1, 8)}
SHA_W = sha(os.path.join(ROOT, "features", "_wide.py"))
C = {
 1: dict(h="H3", f="f001", H=6, mode="hourly", what="bounce-free 3-hour reversal -(log C[t-1] - log C[t-4]) on Binance spot closes, higher = past loser", cost="gross top-3 minus bottom-3 return -0.75 bp per 6h hold (TRAIN n 27,551) vs 87.6 bp round trip of 6 traded names; re-ranked hourly (a 6h hold re-formed up to 4x/day) -> COMBINE-ONLY",
         extra="Evidence behind it (TRAIN searches, cells 5-7, 17): pooled h6 IC +0.0301 (t 9.3); folds +0.027/+0.017/+0.045/+0.037; the unlagged version (IC +0.058) is bounce-contaminated and NOT frozen.", t="session note: strongest in signals formed 21-06 UTC (h6 +0.059), absent 13-16 UTC"),
 2: dict(h="H9", f="f002", H=6, mode="hourly", what="24-hour reversal, lag-1, only for signal hours 21-06 UTC: -(log C[t-1] - log C[t-25]), NaN at other hours", cost="gross top-3 minus bottom-3 return -4.59 bp per 6h hold (TRAIN n 11,516) vs 87.6 bp round trip -> COMBINE-ONLY (it is the session-gated 24h reversal; 0.88 correlated with the plain trailing-24h reversal baseline, 0.30 with the nearest candidate)",
         extra="Evidence behind it (cells 2, 4, 7, 17): h6 IC +0.0412 (t 6.2); folds +0.051/+0.043/+0.036/+0.019; hours 13-16 UTC show no reversal and are gated out.", t=""),
 3: dict(h="H10", f="f003", H=24, mode="hourly", what="1-hour trade-count surprise log(n[t]/mean n[t-720..t-1]) as a cross-sectional rank residualised on the ranks of the bar-t return and |return|, higher = busier than usual beyond the move", cost="gross top-3 minus bottom-3 return +23.5 bp per 24h hold (TRAIN n 25,759) vs 87.2 bp round trip -> COMBINE-ONLY",
         extra="Evidence behind it (cells 8, 9, 17): residual IC h24 +0.0324 (t 5.6); folds +0.031/+0.032/+0.011/+0.051; max |corr| 0.25 (168h momentum); incremental +0.0254.", t=""),
 4: dict(h="H5", f="f004", H=24, mode="hourly", what="perp premium-index crowding: premium_index_close minus its coin's trailing-720h mean, cross-sectional rank residualised on the ranks of r3s and r24, NEGATED (higher = less crowded long)", cost="gross top-3 minus bottom-3 return +5.98 bp per 24h hold (TRAIN n 24,029) vs 87.4 bp round trip -> COMBINE-ONLY",
         extra="Evidence behind it (cells 10-12, 17): h24 IC +0.0249 (t 5.0), h6 +0.0227, h1 +0.0239; folds at h24 +0.029/+0.019/+0.019/+0.025; max |corr| 0.05 with anything; incremental +0.0216.", t=""),
 5: dict(h="H2", f="f005", H=24, mode="hourly", what="Alpha#54 closing strength on rolling 24h blocks, ((C-L24)/(H24-L24))*(O24/C)^5 with O24 = open of bar t-23 (sign as 'minus #54': higher = strong close)", cost="gross top-3 minus bottom-3 return +20.8 bp per 24h hold (TRAIN n 25,941) vs 87.4 bp round trip -> COMBINE-ONLY",
         extra="Evidence behind it (cells 15-17): h24 IC +0.0291 (t 4.7); folds +0.016/+0.077/+0.026/+0.028 (C1-heavy); at h1/h6 the same feature has NEGATIVE IC (-0.035/-0.021): only the h24 continuation is frozen.", t=""),
 6: dict(h="H7", f="f006", H=6, mode="daily", what="3-day sign-streak fade at the UTC day boundary: 1 - pct rank of sum of sign(C[t-24i]-C[t-24(i+1)]), i=0..2, defined only at the 23:00 bar", cost="gross top-3 minus bottom-3 return +2.24 bp per 6h hold (TRAIN n 1,156 days) vs 87.2 bp round trip -> COMBINE-ONLY",
         extra="Evidence behind it (cells 1, 2, 17): h6 IC +0.0433 (t 3.6); folds +0.040/+0.059/+0.060/+0.029 (daily sampling: ~175 days per fold, se ~0.035 -> a fold rarely reaches t 1.96); incremental IC after f007/b_rev24 only +0.0098.", t=""),
 7: dict(h="H1", f="f007", H=24, mode="daily", what="Alpha#30 as written at the UTC day boundary: (1 - pct rank of the 3-day sign streak) * sum(vol,5d)/sum(vol,20d), 23:00 bar", cost="gross top-3 minus bottom-3 return +18.5 bp per 24h hold (TRAIN n 1,040 days) vs 87.2 bp round trip -> COMBINE-ONLY",
         extra="Evidence behind it (cells 1, 3, 17): h24 IC +0.0262 (t 2.3); folds +0.039/+0.037/-0.002/+0.002 (faded in C2/C3, the MEMORY pattern); corr 0.78 with f006 and incremental +0.0183 -> a duplicate of f006 expected; frozen because it is the TARGET.md seed.", t=""),
}
os.makedirs(os.path.join(RUN, "candidates"), exist_ok=True)
for n, c in C.items():
    lag = c["H"] + 5 if c["mode"] == "hourly" else 3
    txt = f"""hypothesis: {c['h']}
variant_of: none
feature: {c['f']}
spec: {c['f']} = features/{c['f']}.py (sha256 {FEAT[n]}; helpers features/_wide.py sha256 {SHA_W}): {c['what']}. Inputs: Binance spot hourly columns (and perp premium-index close for f004) as carded; point-in-time at the END of bar t. Primary horizon h = {c['H']}h: response = log of primary `price` from the END of bar t to the END of bar t+{c['H']} (h1 and the other horizons are reported, not judged); invalid where any bar in (t, t+h] has new_source=True. Statistic per fold = mean cross-sectional Spearman rank IC over signal timestamps with >= 6 coins ({'every hour' if c['mode']=='hourly' else 'the 23:00 bar only (daily sampling)'}), NW t with {lag} lags. Universe: the 10 coins as available. Slices built on: EXPLORE, C1, C2, C3 (TRAIN search only); VAL untouched.
{c['extra']}
construction: point-in-time inputs only (Binance spot/perp hourly bars knowable at open+1h; premium index likewise); trailing-only scaling (rolling windows end at t or t-1; no full-sample z-scores or ranks); cross-sectional ranks only; tails: ranks make 14-88x excess kurtosis harmless, inf/NaN dropped; RAW version = pooled panel Pearson corr of the feature rank-z with the next-h return (reported in the confirm cell) and MARKET-NEUTRAL version = the cross-sectional rank IC (neutral by construction); market correlation = corr of the cross-coin mean standardised feature with the equal-weight market forward return, reported in the confirm cell.
pass_rule: per fold (C1, C2, C3) and for VAL: supported if the primary-horizon mean rank IC >= +0.02 and NW t >= 1.96; refuted if IC < 0 and NW t <= -1.65; else inconclusive. CONFIRM-SHOWN needs >= 2 supported folds and none refuted. VAL judged with the same rule on 2023-03-25..2023-11-30.
min_useful: 0.02 (mean rank IC at the primary horizon)
cost_line: {c['cost']}
"""
    open(os.path.join(RUN, "candidates", f"F{n}.md"), "w", encoding="utf-8").write(txt)
print("frozen", list(C))
