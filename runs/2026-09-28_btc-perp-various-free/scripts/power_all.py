# Power simulations for the five CONFIRM tests, calibrated on EXPLORE ONLY (the slice every hypothesis was born on),
# resampled to CONFIRM's usable length. Written BEFORE any rule file; each rule file quotes its line from here.
from kit import *

N_C_HOURS = 10632          # CONFIRM hourly rows (SPLITS.md census)
N_C_SETTLE = 1329          # CONFIRM funding settlements
E_LO = pd.Timestamp("2020-09-01")
F, b30, c30 = hourly("power_sim", E_LO, EXPLORE_HI - pd.Timedelta("25h"), warm_days=31)
F = F.loc[E_LO:]
out = {}

def corr_power(x, y, ctrl, rho0, alpha, name, block=240, reps=1000):
    ex, ey = resid_ranks(F, x, y, ctrl)
    ex, ey = ex.values, ey.values
    shift = len(ey) // 2
    ey_null = np.roll(ey, shift)                                  # keeps autocorrelation, kills the real link
    ey_null = (ey_null - ey_null.mean()) / ey_null.std()
    ey_alt = rho0 * ex + np.sqrt(1 - rho0 ** 2) * ey_null
    null = block_boot_corr(ex, ey_null, block, reps, 1, N_C_HOURS)
    null = null - null.mean()                                    # centered: sampling noise of rho-hat at CONFIRM length
    se = null.std()
    alt = rho0 + block_boot_corr(ex, ey_null, block, reps, 2, N_C_HOURS)
    alt = alt - (alt.mean() - rho0)                               # centered at the smallest meaningful effect
    crit = (1.6449 if alpha == 0.05 else 2.3263) * se * np.sign(rho0)
    pw = float(np.mean(alt > crit)) if rho0 > 0 else float(np.mean(alt < crit))
    size = float(np.mean(null > crit)) if rho0 > 0 else float(np.mean(null < crit))
    out[name] = dict(x=x, y=y, ctrl=ctrl, rho0=rho0, alpha=alpha, n_explore=len(ex), n_sim=N_C_HOURS, block=block,
                     reps=reps, se_null=float(se), crit=float(crit), power=pw, empirical_size=size)
    print(name, out[name])

corr_power("dvol", "rv24f", ["rv24b", "rv7d", "rv30d"], 0.10, 0.05, "H2")
corr_power("basis", "rv24f", ["rv24b", "rv7d", "rv30d"], 0.10, 0.05, "H3")
corr_power("dvol", "r24f", [], 0.05, 0.05, "H4")
F["r_next1"] = F["r"].shift(-1)
corr_power("r", "r_next1", [], -0.03, 0.05, "H5", block=240)

# H1: per-settlement D = [b(S+30m) - b(S-30m)] - [b(S+4h30m) - b(S+3h30m)]; test mean(D) > 0, NW(3) t, alpha 0.01.
S = pd.date_range(E_LO.ceil("8h"), EXPLORE_HI - pd.Timedelta("8h"), freq="8h")
jump = b30.reindex(S + pd.Timedelta("30min")).values - b30.reindex(S - pd.Timedelta("30min")).values
plac = b30.reindex(S + pd.Timedelta("4h30min")).values - b30.reindex(S + pd.Timedelta("3h30min")).values
D = pd.Series(jump - plac, index=S).dropna()
out["H1_explore_descr"] = dict(n=len(D), mean=float(D.mean()), sd=float(D.std()))
Dz = (D - D.mean()).values
rng = np.random.default_rng(3); reps = 2000; blk = 21; eff0 = 0.5
import statsmodels.api as sm
def nw_t(v):
    m = sm.OLS(v, np.ones(len(v))).fit(cov_type="HAC", cov_kwds={"maxlags": 3}); return m.tvalues[0]
hits = 0; hits0 = 0
for i in range(reps):
    st = rng.integers(0, len(Dz) - blk, int(np.ceil(N_C_SETTLE / blk)))
    idx = (st[:, None] + np.arange(blk)[None, :]).ravel()[:N_C_SETTLE]
    v = Dz[idx]
    hits += nw_t(v + eff0) > 2.3263; hits0 += nw_t(v) > 2.3263
out["H1"] = dict(stat="mean D, NW(3) t, one-sided", eff0_bp=eff0, alpha=0.01, n_sim=N_C_SETTLE, block=blk, reps=reps,
                 power=hits / reps, empirical_size=hits0 / reps)
print("H1", out["H1"], out["H1_explore_descr"])
json.dump(out, open("tables/power_all.json", "w"), indent=1)
