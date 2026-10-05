"""D14 calibration: NULL noise on C1 (already opened by cell_01). Random half splits of C1's daily cross-sections of
next-day primary returns (no alpha enters), 400 permutations: median NW SE of the mean spread, vs the EXPLORE-pool sim."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import run_lib as L
rng = np.random.default_rng(14)
S = L.slices(); R = {}
for c in L.COINS:
    p = L.load_primary(c, "D14 null-noise calibration on C1 (already opened by cell_01; random splits, no alpha)", S["C1"])
    if len(p): R[c] = L.daily_response(p)
R = pd.DataFrame(R); a, b = S["C1"]
R = R[(R.index >= a) & (R.index + pd.Timedelta(days=2) <= b)]
R = R[R.notna().sum(axis=1) >= L.MIN_COINS]
rows = [r.dropna().values for _, r in R.iterrows()]
ses = []
for _ in range(400):
    s = []
    for v in rows:
        n = len(v); perm = rng.permutation(n); h = n // 2
        s.append((v[perm[:h]].mean() - v[perm[n - h:]].mean()) * 1e4)
    ses.append(L.nw_se(np.array(s)))
sim = json.load(open(os.path.join(L.RUN, "code", "sim_se.json")))["C1"]["sim_se_x1"]
out = {"C1_random_split_se": float(np.median(ses)), "sim_se_x1": sim, "ratio": float(np.median(ses) / sim),
       "cell01_realised_se": 32.71, "cell01_ratio": 32.71 / sim}
print(out); json.dump(out, open(os.path.join(L.RUN, "code", "noise_c1.json"), "w"), indent=1)
