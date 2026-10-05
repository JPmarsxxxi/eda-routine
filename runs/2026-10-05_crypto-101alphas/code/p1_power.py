"""Phase 1 support: simulated power / alpha of the pre-registered rule (run_lib.decide) at each slice's OWN size.
Noise model: EXPLORE's daily cross-sectional residuals (r_i,d - mean_d r) of primary responses — a null property
(no alpha enters). For a slice, days and coins-per-day come from SPLITS coverage counts (code/p0_splits.py logic, flags
only). Each simulated day draws n_d residuals (with replacement) from a random EXPLORE day, splits them at random into
halves, and adds delta to the top-minus-bottom spread. Run at noise x1.0 and x1.5; the weight uses the x1.5 result
(lower power -> both weights conservative)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import run_lib as L
rng = np.random.default_rng(20261005)
S = L.slices()
# EXPLORE residual pool
pool = {}
for c in L.COINS:
    p = L.load_primary(c, "Phase 1 power-sim noise pool (EXPLORE responses, no alpha)", S["EXPLORE"])
    if len(p):
        pool[c] = L.daily_response(p)
R = pd.DataFrame(pool)
R = R[R.notna().sum(axis=1) >= L.MIN_COINS]
days = [(r.dropna() - r.dropna().mean()).values for _, r in R.iterrows()]
# coverage (flags only) per slice
win = (pd.Timestamp("2018-12-01", tz="UTC"), pd.Timestamp("2023-03-21", tz="UTC"))
cov = {}
for c in L.COINS:
    p = L.load_primary(c, "Phase 1 power-sim coverage counts only (t, new_source)", win)[["t", "new_source"]]
    day = p.t.dt.floor("D"); g = pd.DataFrame({"n": p.groupby(day).size(), "ns": p.new_source.groupby(day).sum()})
    cov[c] = ((g.n == 24) & (g.ns == 0))
C = pd.DataFrame(cov).asfreq("D").fillna(False).astype(bool)
n_resp = C.sum(axis=1).shift(-1)      # signal day d uses response day d+1

def sim(ncoins, delta, scale, nsim=3000):
    out = {"supported": 0, "refuted": 0, "inconclusive": 0}
    N = len(ncoins)
    for _ in range(nsim):
        idx = rng.integers(0, len(days), N)
        s = np.empty(N)
        for k, (i, n) in enumerate(zip(idx, ncoins)):
            e = rng.choice(days[i], size=n, replace=True) * scale
            perm = rng.permutation(n); h = n // 2
            s[k] = (e[perm[:h]].mean() - e[perm[n - h:]].mean()) * 1e4 + delta
        out[L.decide(s.mean(), L.nw_se(s))] += 1
    return {k: v / nsim for k, v in out.items()}

res = {}
for name in ["EXPLORE", "C1", "C2", "C3"]:
    a, b = S[name]
    nd = n_resp[(n_resp.index >= a) & (n_resp.index + pd.Timedelta(days=2) <= b)]
    nd = nd[nd >= L.MIN_COINS].astype(int).values
    r = {"N": int(len(nd)), "mean_coins": float(nd.mean())}
    for sc in (1.0, 1.5):
        h0, h1 = sim(nd, 0.0, sc), sim(nd, L.ECON_BP, sc)
        r[f"x{sc}"] = {"alpha": h0["supported"], "ref_null": h0["refuted"], "power": h1["supported"], "ref_alt": h1["refuted"]}
    w = r["x1.5"]; alpha = max(w["alpha"], 0.005)     # floor alpha at 0.005 (simulation resolution; conservative)
    r["weights"] = {"alpha_used": alpha, "power_used": w["power"],
                    "supported": round(L.capped(w["power"] / alpha), 3), "supported_raw": round(w["power"] / alpha, 3),
                    "refuted": round((1 - w["power"]) / (1 - alpha), 3)}
    res[name] = r
    print(name, json.dumps(r))
json.dump(res, open(os.path.join(L.RUN, "code", "power.json"), "w"), indent=1)
