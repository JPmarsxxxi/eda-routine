import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from panel import *
os.chdir(RUN)
P, NS, QV, SRC = prim("phase0_04_noise")
rng = np.random.default_rng(20261013)
m_ex = in_slice(P.index, "EXPLORE")
idx = P.index[m_ex]
F0 = back(P, NS, 6)[m_ex]; R0 = {h: fwd(P, NS, h)[m_ex] for h in HORIZONS}
day = idx.floor("D"); days = day.unique(); ndays = len(days)
hours = idx.hour.values
# map (day number, hour) -> row position
pos = {(d, h): i for i, (d, h) in enumerate(zip(day, hours))}
rows_by_day = {d: np.where(day == d)[0] for d in days}
out = {}
def perm_feature(F, mode):
    order = rng.permutation(ndays)
    new = np.full(F.shape, np.nan)
    Fv = F.values
    for k, d in enumerate(days):
        src = rows_by_day[days[order[k]]]; dst = rows_by_day[d]
        # align by hour of day
        sh = {hours[i]: i for i in src}
        for j in dst:
            i = sh.get(hours[j])
            if i is not None: new[j] = Fv[i]
    return pd.DataFrame(new, index=F.index, columns=F.columns)
NP = 80
for mode in ("h", "d"):
    Fm = sample(F0, mode); 
    for h in HORIZONS:
        Rm = sample(R0[h], mode)
        means, ts = [], []
        for _ in range(NP):
            Fp = perm_feature(F0, mode); Fp = sample(Fp, mode)
            ic = xs_ic(Fp, Rm)
            L = (h + 5) if mode == "h" else (h // 24 + 3)
            r = nw(ic, L); means.append(r["mean"]); ts.append(r["t"])
        n = int(xs_ic(Fm, Rm).notna().sum())
        sd = float(np.std(means)); c = sd * np.sqrt(n)
        out[f"{mode}_{h}"] = dict(n=n, sd_mean_ic=sd, c=c, t_sd=float(np.std(ts)), t_mean=float(np.mean(ts)))
        print(mode, h, out[f"{mode}_{h}"])
json.dump(out, open("work/noise.json", "w"), indent=1)
# sd of a single-period IC (the dispersion that goes into a daily-sampled mean)
ic1 = xs_ic(sample(perm_feature(F0, "h"), "h"), R0[1]); print("single-hour null IC sd:", round(float(ic1.std()),4))
