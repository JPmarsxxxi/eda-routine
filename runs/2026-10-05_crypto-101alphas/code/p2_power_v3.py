"""D14+D15: power/alpha of the pre-registered rule with the fold noise re-calibrated. Mean spread ~ Normal(delta, SE),
SE = sim_se_x1(slice, N) * scale; rule = run_lib.decide (supported: m >= 20 and m/SE >= 1.645; refuted: m + 1.645 SE < 20
and m/SE < 1.645). Monte Carlo with 200,000 draws per cell of the table. H5 uses its non-degenerate N (SE x sqrt(N/N_nd))."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import run_lib as L
rng = np.random.default_rng(141)
se1 = json.load(open(os.path.join(L.RUN, "code", "sim_se.json")))
P1 = json.load(open(os.path.join(L.RUN, "code", "power.json")))
SC = {"C1": json.load(open(os.path.join(L.RUN, "code", "noise_c1.json")))["ratio"], "C2": json.load(open(os.path.join(L.RUN, "code", "noise_c2.json")))["ratio"]}; SC["C3"] = max(SC.values())
NONDEG = {"EXPLORE": 16, "C1": 94, "C2": 86, "C3": 52}
def probs(se, delta):
    m = rng.normal(delta, se, 200000); t = m / se
    sup = (m >= L.ECON_BP) & (t >= 1.645); ref = (m + 1.645 * se < L.ECON_BP) & (t < 1.645)
    return sup.mean(), ref.mean()
out = {}
for h in ["all", "H5"]:
    out[h] = {}
    for s in ["EXPLORE", "C1", "C2", "C3"]:
        scale = 1.5 if s == "EXPLORE" else SC[s]
        se = se1[s]["sim_se_x1"] * scale
        if h == "H5":
            se *= np.sqrt(P1[s]["N"] / NONDEG[s])
        a, r0 = probs(se, 0.0); pw, r1 = probs(se, L.ECON_BP)
        al = max(a, 0.005)
        out[h][s] = {"N": P1[s]["N"] if h == "all" else NONDEG[s], "scale": round(scale, 3), "se_bp": round(se, 2),
                     "x1.5": {"alpha": a, "ref_null": r0, "power": pw, "ref_alt": r1},
                     "weights": {"alpha_used": al, "power_used": pw, "supported": round(L.capped(pw / al), 3),
                                 "supported_raw": round(pw / al, 3), "refuted": round((1 - pw) / (1 - al), 3)}}
        print(h, s, out[h][s]["se_bp"], {k: round(v, 3) for k, v in out[h][s]["x1.5"].items()}, out[h][s]["weights"])
json.dump(out, open(os.path.join(L.RUN, "code", "power_v3.json"), "w"), indent=1)
