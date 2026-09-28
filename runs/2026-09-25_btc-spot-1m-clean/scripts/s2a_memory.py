"""Sweep rows 1-2: 01 ADF/KPSS/PP, 02 variance ratio, 03 AR(1)/OU, 04 Hurst, 05 ACF/PACF. TRAIN only."""
import warnings; warnings.filterwarnings("ignore")
from lib import *
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from arch.unitroot import PhillipsPerron
import statsmodels.api as sm

g = grid(load_train(["open", "high", "low", "close", "vol", "buy_vol", "n", "gap_min"]))
r = g["r"]
E = pd.Series(era(g.index), index=g.index)

# ---------- 01 unit root tests
daily_close = g["close"].resample("1D").last().dropna()
ld = np.log(daily_close)
rd = ld.diff().dropna()
res = []
for name, s in [("daily log close (level)", ld), ("daily log return", rd)]:
    a = adfuller(s, autolag="AIC"); k = kpss(s, regression="c", nlags="auto"); pp = PhillipsPerron(s)
    res.append(dict(series=name, adf_stat=a[0], adf_p=a[1], kpss_stat=k[0], kpss_p=k[1], pp_stat=pp.stat, pp_p=pp.pvalue, n=len(s)))
# 1-min returns: sample one month per era (full 2.9M ADF is slow and trivially rejects)
for e in ERAS:
    s = r[E == e].dropna().iloc[:40000]
    a = adfuller(s, maxlag=30, autolag=None); k = kpss(s, regression="c", nlags="auto")
    res.append(dict(series=f"1-min r, first 40k bars of {e}", adf_stat=a[0], adf_p=a[1], kpss_stat=k[0], kpss_p=k[1], pp_stat=np.nan, pp_p=np.nan, n=len(s)))
t01 = pd.DataFrame(res); table(t01, 1, "unit_root_tests"); print(t01)
reg_p("01_adf_level", "ADF", "daily log close", "adf", t01.adf_p[0], "null=unit root")
reg_p("01_pp_level", "PP", "daily log close", "pp", t01.pp_p[0], "null=unit root")
reg_p("01_kpss_ret", "KPSS", "daily log return", "kpss", t01.kpss_p[1], "null=stationary; p floored at 0.01/capped 0.1")
fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
ax[0].plot(ld.index, ld.values, color=PAL[0]); ax[0].set_title(f"log close: ADF p={t01.adf_p[0]:.2f}, PP p={t01.pp_p[0]:.2f} (unit root kept)", fontsize=10)
ax[1].plot(rd.index, rd.values * 1e4, color=GRAY, lw=0.6); ax[1].set_ylabel("bp"); ax[1].set_title(f"daily return: ADF p={t01.adf_p[1]:.1e}, KPSS p={t01.kpss_p[1]:.2f} (stationary)", fontsize=10)
fig.suptitle("01: price level is I(1), returns are I(0): the null picture, no observation", fontweight="bold")
save(fig, 1, "unit_root")

# ---------- 02 variance ratio (Lo-MacKinlay, heteroskedasticity-robust z*), non-overlapping-safe on the grid
def vr_test(x, q):
    x = x.values
    ok = ~np.isnan(x)
    x0 = np.where(ok, x, 0.0)
    mu = np.nanmean(x)
    n = ok.sum()
    var1 = np.nansum((x - mu) ** 2) / (n - 1)
    cs = np.concatenate([[0], np.cumsum(x0)]); cn = np.concatenate([[0], np.cumsum(ok)])
    sq = cs[q:] - cs[:-q]; full = (cn[q:] - cn[:-q]) == q
    sq = sq[full]
    varq = np.sum((sq - q * mu) ** 2) / (len(sq) * q)
    vr = varq / var1
    # heteroskedasticity-robust asymptotic variance (Lo-MacKinlay 1988, eq. for z*)
    d = np.where(ok, (x - mu) ** 2, 0.0)
    den = np.sum(d) ** 2
    theta = 0.0
    for j in range(1, q):
        dj = np.sum(d[j:] * d[:-j])
        theta += (2 * (q - j) / q) ** 2 * dj / den
    theta *= n
    z = (vr - 1) / np.sqrt(theta / n)
    return vr, z

from scipy.stats import norm
rows = []
for q in [2, 5, 15, 60, 240]:
    vr, z = vr_test(r, q); rows.append(dict(era="pooled", q=q, vr=vr, z=z, p=2 * norm.sf(abs(z))))
    reg_p(f"02_vr_q{q}", "variance ratio", "1-min r pooled", "z*", 2 * norm.sf(abs(z)))
    for e in ERAS:
        vr, z = vr_test(r[E == e], q); rows.append(dict(era=e, q=q, vr=vr, z=z, p=2 * norm.sf(abs(z))))
t02 = pd.DataFrame(rows); table(t02, 2, "variance_ratio"); print(t02.pivot(index="era", columns="q", values="vr").round(3))
fig, ax = plt.subplots(figsize=(9, 4))
pv = t02.pivot(index="q", columns="era", values="vr")
for i, e in enumerate(ERAS):
    ax.plot(pv.index, pv[e], marker="o", label=e, color=(PAL + [GRAY])[i])
ax.axhline(1, color="k", lw=0.8); ax.set_xscale("log"); ax.set_xlabel("q (minutes)"); ax.set_ylabel("VR(q)")
ax.legend(ncol=4, fontsize=8)
v60 = pv.loc[60]
zp = t02[(t02.era == "pooled") & (t02.q == 60)].z.iloc[0]
ax.set_title(f"02: VR(60) < 1 in {(v60 < 1).sum()} of 7 eras ({v60.min():.2f}..{v60.max():.2f}); pooled z* = {zp:.1f}", fontsize=11)
save(fig, 2, "variance_ratio")

# ---------- 03 AR(1) on 1-min and 60-min r, by era, HAC t
rows = []
r60 = r.resample("60min").sum(min_count=60)
E60 = pd.Series(era(r60.index), index=r60.index)
for lab, s, EE, L in [("1-min", r, E, 10), ("60-min", r60, E60, 5)]:
    for e in ["pooled"] + ERAS:
        x = s if e == "pooled" else s[EE == e]
        b, se, t, p, n = nw_slope(x, x.shift(1), L)
        hl = -np.log(2) / np.log(b) if 0 < b < 1 else np.nan
        rows.append(dict(series=lab, era=e, phi=b, t_hac=t, p=p, n=n, half_life_bars=hl))
        if e == "pooled": reg_p(f"03_ar1_{lab}", "AR(1)", f"{lab} r pooled", "t_HAC", p)
t03 = pd.DataFrame(rows); table(t03, 3, "ar1_by_era"); print(t03.round(4))
fig, ax = plt.subplots(figsize=(9, 3.8))
for i, lab in enumerate(["1-min", "60-min"]):
    x = t03[(t03.series == lab) & (t03.era != "pooled")]
    ax.plot(x.era, x.phi, marker="o", label=lab, color=PAL[i])
ax.axhline(0, color="k", lw=0.8); ax.set_ylabel("AR(1) coefficient"); ax.legend()
a1 = t03[(t03.series == "1-min") & (t03.era != "pooled")].set_index("era").phi
ax.set_title(f"03: 1-min AR(1) goes from {a1['2017']:.3f} (2017) to {a1['2021']:+.3f} (2021): sign flips mid-TRAIN", fontsize=11)
save(fig, 3, "ar1_by_era")

# ---------- 04 Hurst: aggregated-variance on r; R/S on |r|; by era
def hurst_aggvar(x, ms=(1, 2, 4, 8, 16, 32, 64, 128, 256)):
    x = x.dropna().values
    v = []
    for m in ms:
        k = len(x) // m
        v.append(np.var(x[: k * m].reshape(k, m).sum(1)) / m ** 0)
    sl = np.polyfit(np.log(ms), np.log(v), 1)[0]
    return sl / 2  # var(sum over m) ~ m^{2H}

def hurst_rs(x, ns=(16, 32, 64, 128, 256, 512, 1024, 2048)):
    x = x.dropna().values
    rs = []
    for n in ns:
        k = len(x) // n
        y = x[: k * n].reshape(k, n)
        z = np.cumsum(y - y.mean(1, keepdims=True), 1)
        R = z.max(1) - z.min(1); S = y.std(1)
        rs.append(np.mean(R[S > 0] / S[S > 0]))
    return np.polyfit(np.log(ns), np.log(rs), 1)[0]

rows = []
for e in ["pooled"] + ERAS:
    x = r if e == "pooled" else r[E == e]
    rows.append(dict(era=e, H_aggvar_r=hurst_aggvar(x), H_rs_r=hurst_rs(x), H_rs_absr=hurst_rs(x.abs())))
t04 = pd.DataFrame(rows).set_index("era"); table(t04, 4, "hurst"); print(t04.round(3))
fig, ax = plt.subplots(figsize=(9, 3.8))
x = t04.drop("pooled")
ax.plot(x.index, x.H_aggvar_r, marker="o", label="H of r (aggregated variance)", color=PAL[0])
ax.plot(x.index, x.H_rs_r, marker="s", label="H of r (R/S)", color=PAL[1])
ax.plot(x.index, x.H_rs_absr, marker="^", label="H of |r| (R/S)", color=PAL[3])
ax.axhspan(0.45, 0.55, color=GRAY, alpha=0.2); ax.axhline(0.5, color="k", lw=0.8); ax.legend(fontsize=8)
ax.set_title(f"04: H of r stays near 0.5 (pooled {t04.loc['pooled','H_aggvar_r']:.2f}); H of |r| = {t04.loc['pooled','H_rs_absr']:.2f} (size persists)", fontsize=11)
save(fig, 4, "hurst")

# ---------- 05 ACF / PACF lags 1..60 by era
rows = {}
for e in ERAS:
    x = r[E == e]
    x0 = (x - x.mean()).fillna(0)  # missing minutes contribute 0 to the cross-products (not filled into returns)
    rows[e] = acf(x0, nlags=60, fft=True)[1:]
A = pd.DataFrame(rows, index=range(1, 61)); A.index.name = "lag"
P = pd.DataFrame({e: pacf((r[E == e] - r[E == e].mean()).fillna(0).values[:300000], nlags=10)[1:] for e in ERAS}, index=range(1, 11))
table(A, 5, "acf_by_era"); table(P, 5, "pacf_by_era_lags1_10")
nbar = {e: r[E == e].notna().sum() for e in ERAS}
band = pd.Series({e: 5 / np.sqrt(nbar[e]) for e in ERAS})
hits = (A.abs() > band).astype(int)
sgn = np.sign(A)
cand = [lag for lag in A.index if lag > 1 and hits.loc[lag].sum() >= 5 and abs(sgn.loc[lag][hits.loc[lag] == 1].sum()) >= 5]
print("ACF lag1:", A.loc[1].round(3).to_dict()); print("candidate lags >1:", cand)
fig, ax = plt.subplots(figsize=(10, 4))
for i, e in enumerate(ERAS):
    ax.plot(A.index, A[e], label=e, color=(PAL + [GRAY])[i], lw=1)
ax.axhline(0, color="k", lw=0.6); ax.set_xlabel("lag (min)"); ax.set_ylabel("ACF of 1-min r"); ax.legend(ncol=4, fontsize=8)
ax.set_ylim(-0.06, 0.06)
ax.set_title(f"05: ACF beyond lag 1 is inside noise; lags >1 passing the 5-of-7 rule: {cand if cand else 'none'} (2017 lag1={A.loc[1,'2017']:.2f}, clipped)", fontsize=10)
save(fig, 5, "acf_by_era")
json.dump({"acf_candidates": [int(c) for c in cand]}, open(os.path.join(RUN, "tables", "05_acf_candidates.json"), "w"))
