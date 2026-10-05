"""D14 support: the SE the power simulation assumed vs the SE a cell realised. Simulated SE of the mean spread at a slice's
size, noise x1.0 (EXPLORE residuals), 500 sims. No new data opened (EXPLORE noise pool + coverage flags only)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
src = open(os.path.join(os.path.dirname(__file__), "p1_power.py")).read().split("res = {}")[0]
exec(src.replace('"Phase 1 power-sim', '"D14 noise check'))
out = {}
for name in ["EXPLORE", "C1", "C2", "C3"]:
    a, b = S[name]
    nd = n_resp[(n_resp.index >= a) & (n_resp.index + pd.Timedelta(days=2) <= b)]
    nd = nd[nd >= L.MIN_COINS].astype(int).values
    ses, sds = [], []
    for _ in range(300):
        idx = rng.integers(0, len(days), len(nd)); s = np.empty(len(nd))
        for k, (i, n) in enumerate(zip(idx, nd)):
            e = rng.choice(days[i], size=n, replace=True); perm = rng.permutation(n); h = n // 2
            s[k] = (e[perm[:h]].mean() - e[perm[n - h:]].mean()) * 1e4
        ses.append(L.nw_se(s)); sds.append(s.std())
    out[name] = {"sim_se_x1": float(np.median(ses)), "sim_sd_x1": float(np.median(sds))}
    print(name, out[name])
json.dump(out, open(os.path.join(L.RUN, "code", "sim_se.json"), "w"), indent=1)
