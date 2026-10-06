"""Power simulation inputs, MEASURED (RUNBOOK v3.2 / DECISIONS D10): for each alpha, the sd and lag-1 autocorrelation of its
daily cross-sectional rank IC under a day-permutation null on EXPLORE (response days shuffled against signal days: the alpha's
own noise, any real effect destroyed). Scaled to each slice by sqrt((coins_EXPLORE - 1) / (coins_slice - 1)) — the sd of a
Spearman correlation across n coins goes as 1/sqrt(n - 1). Day counts per slice are coverage counts (days with >= 5 coins
having both a signal and a valid response); no return is related to a signal here."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import common as C

F, R = C.cached()
A = {k: f(F) for k, f in C.ALPHAS.items()}
rng = np.random.default_rng(11)
rows = []
for k, S in A.items():
    SE = S.loc[C.in_slice(S.index, "EXPLORE")]
    RE = C.response_in_slice(R, "EXPLORE")
    sds, ars = [], []
    for rep in range(40):
        perm = RE.copy()
        perm.index = rng.permutation(RE.index)
        perm = perm.sort_index()
        ic = C.daily_rank_ic(SE, perm)
        sds.append(ic.std()); ars.append(ic.autocorr(1))
    sd_e, ar_e = float(np.mean(sds)), float(np.mean(ars))
    def cover(name):
        Ss = S.loc[C.in_slice(S.index, name)]
        Rs = C.response_in_slice(R, name)
        Ss, Rs = Ss.align(Rs, join="inner")
        both = (Ss.notna() & Rs.notna()).sum(axis=1)
        return int((both >= C.MIN_COINS).sum()), float(both[both >= C.MIN_COINS].median())
    nE, cE = cover("EXPLORE")
    for sl in ["EXPLORE", "C1", "C2", "C3", "VAL"]:
        n, c = cover(sl)
        sd = sd_e * np.sqrt((cE - 1) / (c - 1))
        sim = C.simulate_branch_probs(sd, n, ar1=max(ar_e, 0.0), sims=3000)
        rows.append({"alpha": k, "slice": sl, "n_days": n, "coins_median": c, "sd_ic_explore_null": sd_e,
                     "ar1_explore_null": ar_e, "sd_ic_slice": sd, "power": sim["P_H1"]["supported"],
                     "alpha_size": sim["P_H0"]["supported"], "P_ref_H1": sim["P_H1"]["refuted"],
                     "P_ref_H0": sim["P_H0"]["refuted"], "w_sup_raw": sim["w_sup_raw"], "w_ref_raw": sim["w_ref_raw"],
                     "w_sup": sim["w_sup"], "w_ref": sim["w_ref"]})
        print(rows[-1])
pd.DataFrame(rows).to_csv(os.path.join(C.RUN, "tables", "power.csv"), index=False)
