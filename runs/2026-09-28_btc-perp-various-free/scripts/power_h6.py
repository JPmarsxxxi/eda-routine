# H6 power simulation (EXPLORE only), same recipe as power_all.corr_power. Written BEFORE cell_07_rule.md.
from kit import *
N_C = 10632
E_LO = pd.Timestamp("2020-09-01")
F, b30, c30 = hourly("power_h6", E_LO, EXPLORE_HI - pd.Timedelta("3h"), warm_days=1)
F = F.loc[E_LO:].replace([np.inf, -np.inf], np.nan)
F["d_basis"] = F["basis"].diff(); F["r_next1"] = F["r"].shift(-1)
ex, ey = resid_ranks(F, "d_basis", "r_next1", ["r"]); ex, ey = ex.values, ey.values
print("EXPLORE partial rho(d_basis, r_next | r) =", float(np.corrcoef(ex, ey)[0, 1]), "n", len(ex))
rho0, alpha = -0.03, 0.05
ey_null = np.roll(ey, len(ey) // 2); ey_null = (ey_null - ey_null.mean()) / ey_null.std()
null = block_boot_corr(ex, ey_null, 240, 1000, 1, N_C); null = null - null.mean(); se = null.std()
alt = rho0 + block_boot_corr(ex, ey_null, 240, 1000, 2, N_C); alt = alt - (alt.mean() - rho0)
crit = -1.6449 * se
out = dict(x="d_basis", y="r_next1", ctrl=["r"], rho0=rho0, alpha=alpha, n_explore=len(ex), n_sim=N_C, block=240, reps=1000,
           se_null=float(se), crit=float(crit), power=float(np.mean(alt < crit)), empirical_size=float(np.mean(null < crit)),
           explore_partial_rho=float(np.corrcoef(ex, ey)[0, 1]))
json.dump(out, open("tables/power_h6.json", "w"), indent=1); print(out)
