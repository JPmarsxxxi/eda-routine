# Power simulations for the rule files. DGP mimics EXPLORE facts: common factor (pairwise corr ~0.62, OBS #10), t(3) tails
# (OBS #1), persistent common volatility (OBS #7), 10 coins. Each test's statistic is the SAME function the real cell runs.
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from tests import lag_ic, diff_ic, fm_interaction
rng = np.random.default_rng(20260930)
N = 10
def t3(size): return rng.standard_t(3, size) / np.sqrt(3.0)
def panel(T, phi, per_day=1, phi_high=None, high=None):
    h = np.zeros(T); eps = rng.normal(0, 1, T)
    for k in range(1, T): h[k] = 0.97 ** (1 / per_day) * h[k - 1] + np.sqrt(1 - 0.97 ** (2 / per_day)) * 0.5 * eps[k]
    sig = np.exp(h); f = t3(T); e = t3((T, N))
    u = sig[:, None] * (0.79 * f[:, None] + 0.62 * e)
    r = np.zeros_like(u); r[0] = u[0]
    ph = np.full(T, phi) if phi_high is None else np.where(high, phi_high, phi)
    for k in range(1, T): r[k] = ph[k - 1] * r[k - 1] + u[k]     # phi applies from the conditioning row to the next
    return pd.DataFrame(r), f, sig
def power_lag(T, phi, lag=1, per_day=1, sims=400, alpha_z=-1.645):
    hits = 0
    for _ in range(sims):
        X, _, _ = panel(T, 0.0, per_day) if lag != 1 else panel(T, phi, per_day)
        if lag != 1:   # impose corr at 'lag' (e.g. 24) directly: r_t += phi * r_{t-lag}
            V = X.values.copy()
            for k in range(lag, T): V[k] = V[k] + phi * V[k - lag]
            X = pd.DataFrame(V)
        cl = None if per_day == 1 else np.arange(T) // per_day
        ic, se, z, n = lag_ic(X, lag, cluster=cl)
        hits += z < alpha_z
    return hits / sims
def power_diff(T, phi0, dphi, sims=400):
    hits = 0
    for _ in range(sims):
        f_lat = np.abs(t3(T)); latent = 0.5 * f_lat / f_lat.std() + rng.normal(0, 1, T)
        high = latent > np.quantile(latent, 2 / 3)
        X, _, _ = panel(T, phi0, phi_high=phi0 + dphi, high=high)
        d, se, z, n = diff_ic(X, 1, high); hits += z < -1.645
    return hits / sims
def power_fm(T, b3, sd_rel=0.0349, sims=300):
    hits = 0
    for _ in range(sims):
        rel = pd.DataFrame(t3((T, N)) * sd_rel); rel = rel.sub(rel.mean(axis=1), axis=0)
        shock = pd.DataFrame(0.4 * np.abs(rel.values) / sd_rel + rng.normal(0, 1, (T, N)))
        za = rel.sub(rel.mean(axis=1), axis=0).div(rel.std(axis=1), axis=0); zb = shock.sub(shock.mean(axis=1), axis=0).div(shock.std(axis=1), axis=0)
        y = (b3 * za * zb).shift(1) + pd.DataFrame(t3((T, N)) * sd_rel)
        y = y.sub(y.mean(axis=1), axis=0)
        m, se, z, n = fm_interaction(y.shift(-1), rel, shock, min_n=min(8, N)); hits += z > 1.645
    return hits / sims
if __name__ == "__main__":
    which = sys.argv[1]
    if which == "H1":
        print("H1 size (phi=0):", power_lag(620, 0.0)); print("H1 power (phi=-0.045):", power_lag(620, -0.045))
    if which == "H5":
        print("H5 size:", power_lag(620 * 4, 0.0, per_day=4, sims=300)); print("H5 power (phi=-0.065):", power_lag(620 * 4, -0.065, per_day=4, sims=300))
    if which == "H3":
        print("H3 size:", power_lag(620 * 24, 0.0, lag=24, per_day=24, sims=150)); print("H3 power (rho=-0.05):", power_lag(620 * 24, -0.05, lag=24, per_day=24, sims=150))
    if which == "H2":
        print("H2 size:", power_diff(620, -0.03, 0.0)); print("H2 power (dphi=-0.045):", power_diff(620, -0.03, -0.045))
    if which == "H4":
        print("H4 size:", power_fm(620, 0.0)); print("H4 power (b3=28bp):", power_fm(620, 0.0028))

def power_h6(days=1400, dphi=-0.065, sims=200, n_coins=6):
    from tests import diff_ic_clustered
    global N
    N0 = N; N = n_coins; hits = 0; per = 4; T = days * per
    for _ in range(sims):
        X, f, sig = panel(T, 0.0, per_day=per)
        # trailing 7-day vol (28 blocks) of the EW series, top tercile -> high; applied to the NEXT block pair
        ew = X.mean(axis=1); tv = ew.pow(2).rolling(28).mean().shift(1)
        high = (tv > tv.quantile(2 / 3)).values
        V = X.values.copy()
        for k in range(1, T): V[k] = V[k] + (dphi if high[k - 1] else 0.0) * V[k - 1]
        X = pd.DataFrame(V); cl = np.arange(T) // per
        hm = pd.Series(high).groupby(cl).transform("first").values
        d, se, z, n = diff_ic_clustered(X, 1, hm, cl); hits += z < -1.645
    N = N0
    return hits / sims
if __name__ == "__main__" and sys.argv[1] == "H6":
    print("H6 size (dphi=0):", power_h6(dphi=0.0)); print("H6 power (dphi=-0.065):", power_h6())

if __name__ == "__main__" and sys.argv[1] == "R5":
    N = 7
    print("cell_05 FM on EXPLORE size:", power_fm(1100, 0.0, sims=200)); print("cell_05 FM on EXPLORE power (b3=28bp):", power_fm(1100, 0.0028, sims=200))

def power_big(days=1400, n_coins=6, phi_big=-0.2, sims=200):
    """Power of the IC on the top-10% |r| days (pooled products, clustered by day) when only those days reverse by phi_big."""
    from tests import nscore, nw_se
    global N
    N0 = N; N = n_coins; hits = 0
    for _ in range(sims):
        X, _, _ = panel(days, 0.0); V = X.values.copy(); A = np.abs(V); thr = np.nanquantile(A, .9, axis=0)
        for k in range(1, days): V[k] = V[k] + np.where(A[k - 1] >= thr, phi_big, 0.0) * V[k - 1]
        X = pd.DataFrame(V); Z = nscore(X); prod = Z * Z.shift(-1); big = X.abs().ge(X.abs().quantile(.9))
        c = prod.where(big).mean(axis=1).dropna(); se, n = nw_se(c.values); hits += c.mean() / se < -1.645
    N = N0; return hits / sims
if __name__ == "__main__" and sys.argv[1] == "R7":
    print("cell_07 big-day IC size:", power_big(phi_big=0.0)); print("cell_07 big-day IC power (phi_big=-0.2):", power_big())
if __name__ == "__main__" and sys.argv[1] == "R7min":
    print("cell_07 big-day IC power (phi_big=-0.024):", power_big(phi_big=-0.024))
if __name__ == "__main__" and sys.argv[1] == "VAL5":
    print("VAL H5 size:", power_lag(250 * 4, 0.0, per_day=4, sims=300)); print("VAL H5 power (phi=-0.065):", power_lag(250 * 4, -0.065, per_day=4, sims=300))
