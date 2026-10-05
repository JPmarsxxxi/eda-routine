# H2 VAL power simulation (EXPLORE only), same recipe as power_all.corr_power, at VAL length. Written BEFORE cell_10_rule.md.
from kit import *
N_V = 5990
E_LO = pd.Timestamp("2020-09-01")
F, b30, c30 = hourly("power_val_h2", E_LO, EXPLORE_HI - pd.Timedelta("25h"), warm_days=31)
F = F.loc[E_LO:]
ex, ey = resid_ranks(F, "dvol", "rv24f", ["rv24b", "rv7d", "rv30d"]); ex, ey = ex.values, ey.values
ey_null = np.roll(ey, len(ey) // 2); ey_null = (ey_null - ey_null.mean()) / ey_null.std()
null = block_boot_corr(ex, ey_null, 240, 1000, 1, N_V); null = null - null.mean(); se = null.std()
alt = 0.10 + block_boot_corr(ex, ey_null, 240, 1000, 2, N_V); alt = alt - (alt.mean() - 0.10)
crit = 1.6449 * se
out = dict(x="dvol", y="rv24f", ctrl=["rv24b", "rv7d", "rv30d"], rho0=0.10, alpha=0.05, n_explore=len(ex), n_sim=N_V, block=240, reps=1000,
           se_null=float(se), crit=float(crit), power=float(np.mean(alt > crit)), empirical_size=float(np.mean(null > crit)))
json.dump(out, open("tables/power_val_h2.json", "w"), indent=1); print(out)
