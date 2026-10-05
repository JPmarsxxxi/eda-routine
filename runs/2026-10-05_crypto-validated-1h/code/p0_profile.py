"""PHASE 0 on EXPLORE only (2019-01-01 -> 2021-07-01). Rules are pre-stated in DATA_PROFILE.md section headers."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from panel import *
from guard import load
setup()
CELL = "phase0"
A, B = ts(SLICES["EXPLORE"][0]), ts(SLICES["EXPLORE"][1])
OUT = {}
H = hourly(CELL)
H = H[(H.t >= A) & (H.t < B)]          # EXPLORE only; first hour's return needs t-1 which is pre-2019 -> NaN anyway
D = daily(H)
r24 = D["r24"]; r24 = r24[(r24.index >= A) & (r24.index + pd.Timedelta(days=1) <= B)]

# ---------------- 1. distributions
rows = []
for c in COINS:
    x = H[H.coin == c].r1.dropna()
    if len(x) == 0: continue
    y = r24[c].dropna() if c in r24 else pd.Series(dtype=float)
    q = np.log(H[H.coin == c].qvol.replace(0, np.nan).dropna())
    xs = np.sort(np.abs(x.values))[::-1]; k = int(0.01 * len(xs))
    hill = 1 / np.mean(np.log(xs[:k] / xs[k]))
    rows.append(dict(coin=c, n_h=len(x), sd_h_bp=x.std() * 1e4, skew_h=stats.skew(x), exkurt_h=stats.kurtosis(x),
                     zero_h_pct=(x == 0).mean() * 100, hill_top1pct=hill, n_d=len(y), sd_d_pct=y.std() * 100,
                     skew_d=stats.skew(y), exkurt_d=stats.kurtosis(y), logqvol_skew=stats.skew(q), qvol_zero_pct=(H[H.coin == c].qvol == 0).mean() * 100))
T1 = pd.DataFrame(rows).set_index("coin").round(3); T1.to_csv("tables/00_1_distributions.csv"); print(T1.to_string())
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
for i, c in enumerate(["BTCUSD", "ETHUSD", "DOGEUSD"]):
    x = H[H.coin == c].r1.dropna() / H[H.coin == c].r1.std()
    (osm, osr), _ = stats.probplot(x, dist="norm"); ax[0].plot(osm, osr, ".", ms=2, color=PAL[i], label=c)
ax[0].plot([-5, 5], [-5, 5], color=GRAY, lw=1); ax[0].set_title("Hourly returns: tails far beyond normal (Q-Q, standardised)")
ax[0].set_xlabel("normal quantile"); ax[0].set_ylabel("sample quantile (sd units)"); ax[0].legend()
ax[1].bar(T1.index.str[:-3], T1.exkurt_h, color=PAL[0]); ax[1].axhline(3, color=GRAY, ls="--", lw=1)
ax[1].set_title("Excess kurtosis of hourly returns, EXPLORE (rule line = 3)"); save(fig, "00_distributions.png")

# ---------------- 2. missingness
H_all = hourly(CELL); H_all = H_all[(H_all.t >= A) & (H_all.t < B)]
miss = H_all.assign(y=H_all.t.dt.year, miss=H_all.price.isna()).groupby(["coin", "y"]).agg(hours=("miss", "size"), missing=("miss", "sum"), new_source=("ns", "sum"))
# hours = span from first row; add coins/years absent entirely
miss["missing_pct"] = (miss.missing / miss.hours * 100).round(3)
miss.to_csv("tables/00_2_missing.csv"); print(miss.to_string())
fam = {}
for f, col in [("perp/funding_{}.parquet", None), ("perp/perp_premium_{}.parquet", None), ("spot/coinbase_{}.parquet", None)]:
    pass
cov = {}
for c in COINS:
    for lab, f in [("funding", f"perp/funding_{c}.parquet"), ("premium", f"perp/perp_premium_{c}.parquet"),
                   ("coinbase", f"spot/coinbase_{c}.parquet"), ("binance_spot", f"spot/binance_{c}.parquet")]:
        try:
            d = load(f, CELL)
        except Exception:
            continue
        d = d[(d._t >= A) & (d._t < B)]
        cov[(lab, c)] = (d._t.min().date() if len(d) else None, len(d))
covdf = pd.Series({k: f"{v[0]} ({v[1]:,})" for k, v in cov.items()}).unstack(0); covdf.to_csv("tables/00_2_family_coverage_explore.csv"); print(covdf.to_string())
fig, ax = plt.subplots(figsize=(11, 3.4))
pv = H_all.assign(m=H_all.t.dt.to_period("M").dt.to_timestamp(), miss=H_all.price.isna()).groupby(["m", "coin"]).miss.sum().unstack()
for i, c in enumerate(pv.columns[:8]): ax.plot(pv.index, pv[c], color=PAL[i % 8], label=c[:-3])
ax.set_title("Missing primary hours per month, EXPLORE: rare, clustered in a few outage months"); ax.legend(ncol=8, fontsize=7); save(fig, "00_missingness.png")

# ---------------- 3. autocorrelation
def acf(x, lags):
    x = pd.Series(x); return {l: x.autocorr(l) for l in lags}
rows = []
for c in COINS:
    h = H[H.coin == c].set_index("t")
    if h.r1.count() < 1000: continue
    a = acf(h.r1, range(1, 25)); b = acf(h.r1.abs(), [1, 24, 168]); v = acf(np.log(h.qvol.replace(0, np.nan)), [1, 24, 168])
    dd = acf(r24[c].dropna().reindex(r24.index), range(1, 6)) if c in r24 else {}
    n = h.r1.count(); nd = r24[c].count()
    rows.append(dict(coin=c, n_h=n, band_h=2 / np.sqrt(n), **{f"r_l{k}": a[k] for k in [1, 2, 3, 6, 12, 24]},
                     n_sig_r_l1_24=sum(abs(a[k]) > 2 / np.sqrt(n) for k in a),
                     **{f"absr_l{k}": b[k] for k in b}, **{f"lqv_l{k}": v[k] for k in v},
                     n_d=nd, band_d=2 / np.sqrt(nd), **{f"rd_l{k}": dd.get(k, np.nan) for k in range(1, 6)}))
T3 = pd.DataFrame(rows).set_index("coin").round(3); T3.to_csv("tables/00_3_acf.csv"); print(T3.to_string())
fig, ax = plt.subplots(figsize=(11, 3.6))
bt = H[H.coin == "BTCUSD"].set_index("t")
for i, (lab, s) in enumerate([("BTC return", bt.r1), ("BTC |return|", bt.r1.abs()), ("BTC log quote vol", np.log(bt.qvol.replace(0, np.nan)))]):
    ax.plot(range(1, 169), [s.autocorr(l) for l in range(1, 169)], color=PAL[i], label=lab)
ax.axhline(2 / np.sqrt(bt.r1.count()), color=GRAY, ls="--", lw=1); ax.axhline(-2 / np.sqrt(bt.r1.count()), color=GRAY, ls="--", lw=1)
ax.set_xlabel("lag (hours)"); ax.set_title("Returns are ~uncorrelated; |returns| and volume persist for a week with a 24h cycle"); ax.legend(); save(fig, "00_acf.png")

# ---------------- 4. cross-column relationships
C = r24.corr(min_periods=100).round(2); C.to_csv("tables/00_4_corr_daily.csv"); print(C.to_string())
off = C.where(~np.eye(len(C), dtype=bool)).stack()
OUT["max_pair_corr"] = (off.idxmax(), float(off.max())); OUT["mean_pair_corr"] = float(off.mean())
# twin check: primary price vs spot/binance close in EXPLORE
tw = {}
SP = binance_spot_hourly(CELL, cols=("close", "quote_vol"))
for c in COINS:
    h = H[H.coin == c].set_index("t")
    if h.price.count() == 0: continue
    b = SP[("close", c)].reindex(h.index)
    dlog = np.abs(np.log(h.price / b)).dropna() * 1e4
    qv = (h.qvol / SP[("quote_vol", c)].reindex(h.index) - 1).abs().dropna()
    tw[c] = dict(n=len(dlog), median_abs_gap_bp=dlog.median(), share_identical=(dlog < 1e-6).mean(), qvol_identical=(qv < 1e-9).mean())
TW = pd.DataFrame(tw).T.round(4); TW.to_csv("tables/00_4_twin_primary_vs_binance_spot.csv"); print(TW.to_string())

# explanatory screen (knowable-lagged, daily, decision at d+1 00:00)
close_h = SP["close"]
F = {}
F["funding"] = feat_funding(CELL)
F["perp_premium"] = feat_premium(CELL)
F["coinbase_premium"] = feat_coinbase_premium(CELL, close_h)
# kimchi: upbit KRW close at d 23:00 / (binance close at d 23:00 * USDKRW of the last Yahoo session with local_date <= d-1)
krw = load("macro/yahoo_KRW_X.parquet", CELL); krw = krw.set_index(pd.to_datetime(krw.local_date).dt.tz_localize("UTC")).close.sort_index()
kim = {}
for c, u in [("BTCUSD", "BTCKRW"), ("ETHUSD", "ETHKRW"), ("XRPUSD", "XRPKRW"), ("ADAUSD", "ADAKRW"), ("DOGEUSD", "DOGEKRW"), ("SOLUSD", "SOLKRW")]:
    up = load(f"spot/upbit_{u}.parquet", CELL).set_index("_t").close.sort_index()
    up = up[up.index.hour == 23]; up.index = up.index.floor("D")
    bn = close_h[c]; bn = bn[bn.index.hour == 23]; bn.index = bn.index.floor("D")
    fx = krw.reindex(pd.date_range(krw.index.min(), ts("2023-12-01"), freq="D")).ffill().shift(1)  # session <= d-1
    kim[c] = np.log(up / (bn * fx.reindex(up.index)))
F["kimchi_premium"] = pd.DataFrame(kim)
# on-chain active addresses: day d value knowable ~00:00-02:00 d+1 -> use d-1; feature = log(7d mean / 28d mean)
aa = {}
for c in COINS:
    try:
        d = load(f"onchain/cm_{c[:-3]}.parquet", CELL)
    except Exception:
        continue
    if "AdrActCnt" not in d: continue
    s = d.set_index(d._t.dt.floor("D")).AdrActCnt.astype(float).sort_index()
    aa[c] = np.log(s.rolling(7).mean() / s.rolling(28).mean()).shift(1)
F["active_addr_growth"] = pd.DataFrame(aa)
# market-wide
db = load("deriv/deribit_funding_BTC.parquet", CELL).set_index("_t").interest_8h.sort_index()
mk = {}
mk["deribit_btc_funding"] = db.groupby(db.index.floor("D")).mean()
fg = load("attention/fear_greed.parquet", CELL).set_index("_t").value.astype(float).sort_index()
mk["fear_greed"] = fg.reindex(pd.date_range(fg.index.min(), fg.index.max(), freq="D")).ffill()  # stamped d, published d 00:00 -> knowable for decision at d+1
def yahoo_ret(f):
    y = load(f, CELL); y = y.set_index(pd.to_datetime(y.local_date).dt.tz_localize("UTC")).close.sort_index()
    r = np.log(y).diff()
    idx = pd.date_range(ts("2015-01-01"), ts("2023-12-01"), freq="D")
    return r.reindex(idx).shift(1)  # session local_date <= d-1 only (lag one session); non-session days NaN
mk["spx_prev_session_ret"] = yahoo_ret("macro/yahoo_GSPC.parquet")
v = load("macro/yahoo_VIX.parquet", CELL); v = v.set_index(pd.to_datetime(v.local_date).dt.tz_localize("UTC")).close.sort_index()
mk["vix_5d_change"] = np.log(v / v.shift(5)).reindex(pd.date_range(ts("2015-01-01"), ts("2023-12-01"), freq="D")).ffill().shift(1)
g = load("attention/gdelt_timelinevolraw_bitcoin.parquet", CELL); g = g[g.Series == "Article Count"].set_index("_t").Value.astype(float).sort_index()
mk["gdelt_btc_attention"] = np.log(g.rolling(3).mean() / g.rolling(30).mean()).shift(1)  # day d knowable d+1 00:15 -> use d-1
MK = pd.DataFrame(mk)

days = r24.index
R = {h: fwd(D["r24"], h) for h in (1, 3)}
def screen_ts(f, h):  # f: Series (market) or DataFrame (per coin)
    m = in_slice(R[h].index, "EXPLORE", h)
    Rp = R[h][m]
    if isinstance(f, pd.DataFrame):
        cols = [c for c in f.columns if c in Rp]
        fr = f[cols].reindex(Rp.index)
        fr = fr.rank(pct=True) - 0.5
        valid = fr.notna() & Rp[cols].notna()
        Fd = fr.where(valid).mean(1); Rd = Rp[cols].where(valid).mean(1)
    else:
        Fd = f.reindex(Rp.index); Rd = Rp.mean(1)
    z = pd.concat([Fd, Rd], axis=1).dropna().iloc[::h]
    if len(z) < 30: return dict(n=len(z))
    rho = stats.spearmanr(z.iloc[:, 0], z.iloc[:, 1])[0]
    q = z.iloc[:, 0].rank(pct=True)
    eff = (z.iloc[:, 1][q > 2 / 3].mean() - z.iloc[:, 1][q <= 1 / 3].mean()) * 1e4
    return dict(n=len(z), ic=rho, t=rho * np.sqrt(len(z) - 2), top_minus_bottom_bp=eff, start=str(z.index.min().date()))
def screen_xs(f, h):
    m = in_slice(R[h].index, "EXPLORE", h)
    Rp = R[h][m]; cols = [c for c in f.columns if c in Rp]
    fr = f[cols].reindex(Rp.index)
    ics, sp = [], []
    for d in Rp.index[::h]:
        a = pd.concat([fr.loc[d], Rp.loc[d, cols]], axis=1).dropna()
        if len(a) < 5 or a.iloc[:, 0].nunique() < 3: continue
        ics.append(stats.spearmanr(a.iloc[:, 0], a.iloc[:, 1])[0])
        q = a.iloc[:, 0].rank(pct=True); sp.append(a.iloc[:, 1][q > 2 / 3].mean() - a.iloc[:, 1][q <= 1 / 3].mean())
    ics = np.array(ics)
    if len(ics) < 30: return dict(n=len(ics))
    return dict(n=len(ics), ic=ics.mean(), t=ics.mean() / ics.std() * np.sqrt(len(ics)), top_minus_bottom_bp=np.nanmean(sp) * 1e4)
rows = []
for name, f in F.items():
    for h in (1, 3):
        rows.append(dict(feature=name, design="TS", h_days=h, **screen_ts(f, h)))
        rows.append(dict(feature=name, design="XS", h_days=h, **screen_xs(f, h)))
for name in MK:
    for h in (1, 3):
        rows.append(dict(feature=name, design="TS", h_days=h, **screen_ts(MK[name], h)))
S = pd.DataFrame(rows); S["flag_|t|>2"] = S.t.abs() > 2
S.round(4).to_csv("tables/00_4_explanatory_screen.csv"); print(S.round(3).to_string())
OUT["screen_K"] = int(S.t.notna().sum()); OUT["screen_flags"] = int(S["flag_|t|>2"].sum())
# impostor check (floor Q3) for the strongest flag: is XS perp premium a twin of funding or of past-3d return (XS reversal)?
P = F["perp_premium"]; FU = F["funding"]; past3 = sum(D["r24"].shift(k) for k in range(0, 3))  # return over days d-2..d (knowable at d+1 00:00)
m = in_slice(R[3].index, "EXPLORE", 3); Rp = R[3][m]
rows_i = []
for d in Rp.index[::3]:
    cols = list(Rp.columns)
    a = pd.DataFrame({"prem": P.reindex(index=[d], columns=cols).iloc[0], "fund": FU.reindex(index=[d], columns=cols).iloc[0],
                      "past3": past3.reindex(index=[d], columns=cols).iloc[0], "fwd": Rp.loc[d, cols]}).dropna()
    if len(a) < 5: continue
    rk = a.rank()
    # residual premium rank after removing past3 rank (cross-sectional OLS on ranks)
    b = np.polyfit(rk.past3, rk.prem, 1); res = rk.prem - np.polyval(b, rk.past3)
    rows_i.append(dict(d=d, c_prem_fund=stats.spearmanr(a.prem, a.fund)[0] if a.fund.nunique() > 2 else np.nan,
                       c_prem_past3=stats.spearmanr(a.prem, a.past3)[0], ic_past3=stats.spearmanr(a.past3, a.fwd)[0],
                       ic_prem=stats.spearmanr(a.prem, a.fwd)[0], ic_prem_resid=stats.spearmanr(res, a.fwd)[0]))
I = pd.DataFrame(rows_i).set_index("d")
Isum = pd.DataFrame({"mean": I.mean(), "t": I.mean() / I.std() * np.sqrt(I.count()), "n": I.count()}).round(3)
Isum.to_csv("tables/00_4_impostor_premium.csv"); print(Isum.to_string())
OUT["impostor_premium"] = Isum.to_dict()
fig, ax = plt.subplots(figsize=(11, 4.2))
lab = S.feature + " " + S.design + " " + S.h_days.astype(str) + "d"
ax.barh(lab, S.t, color=[PAL[7] if abs(t) > 2 else PAL[0] for t in S.t.fillna(0)])
for x in (-2, 2): ax.axvline(x, color=GRAY, ls="--", lw=1)
ax.set_xlabel("t-stat of IC vs forward primary return (EXPLORE)"); ax.set_title(f"Explanatory screen: {OUT['screen_flags']} of {OUT['screen_K']} cross |t|>2 (expect ~{0.046*OUT['screen_K']:.1f} by chance)")
ax.tick_params(axis="y", labelsize=7); save(fig, "00_explanatory_screen.png")
fig, ax = plt.subplots(figsize=(6.5, 5.2))
im = ax.imshow(C.values, cmap=matplotlib.colors.LinearSegmentedColormap.from_list("d", DIV), vmin=-1, vmax=1)
ax.set_xticks(range(len(C))); ax.set_xticklabels(C.columns.str[:-3], rotation=90); ax.set_yticks(range(len(C))); ax.set_yticklabels(C.index.str[:-3])
for i in range(len(C)):
    for j in range(len(C)): ax.text(j, i, f"{C.values[i, j]:.2f}", ha="center", va="center", fontsize=6)
ax.set_title("Daily returns move together (EXPLORE); no pair > 0.95"); ax.grid(False); save(fig, "00_corr.png")

# ---------------- 5. regimes (half-years)
rows = []
Hh = H.assign(hy=H.t.dt.year.astype(str) + "H" + ((H.t.dt.month > 6) + 1).astype(str))
r24h = r24.assign(hy=r24.index.year.astype(str) + "H" + ((r24.index.month > 6) + 1).astype(str))
for hy, g in r24h.groupby("hy"):
    g = g.drop(columns="hy")
    cc = g.corr(min_periods=60); offc = cc.where(~np.eye(len(cc), dtype=bool)).stack()
    hb = Hh[(Hh.hy == hy) & (Hh.coin == "BTCUSD")].r1
    rows.append(dict(half=hy, coins=int(g.notna().any().sum()), daily_vol_pct_median=g.std().median() * 100, mean_pair_corr=offc.mean(),
                     btc_h_acf1=hb.autocorr(1), panel_d_acf1=g.mean(1).autocorr(1), btc_mean_daily_bp=g["BTCUSD"].mean() * 1e4))
T5 = pd.DataFrame(rows).set_index("half").round(3); T5.to_csv("tables/00_5_regimes.csv"); print(T5.to_string())
fig, ax = plt.subplots(figsize=(11, 3.6))
rv = r24.rolling(30, min_periods=20).std().median(1) * np.sqrt(365) * 100
rc = r24["BTCUSD"].rolling(60, min_periods=40).corr(r24["ETHUSD"])
ax.plot(rv.index, rv, color=PAL[0], label="median coin 30d vol (ann. %)")
ax2 = ax.twinx(); ax2.plot(rc.index, rc * 100, color=PAL[3], label="BTC-ETH 60d corr x100"); ax2.grid(False)
ax.set_title("Vol spikes at 2020-03 and 2021-05; correlation stays high throughout"); ax.legend(loc="upper left"); ax2.legend(loc="upper right"); save(fig, "00_regimes.png")

# ---------------- 6. intraday / weekly
H6 = H.assign(hr=H.t.dt.hour, wd=H.t.dt.dayofweek, ar=H.r1.abs())
iv = H6.groupby("hr").ar.mean() * 1e4; ivol = H6.assign(sh=H6.qvol / H6.groupby(["coin", H6.t.dt.floor("D")]).qvol.transform("sum")).groupby("hr").sh.mean() * 100
wv = H6.groupby("wd").ar.mean() * 1e4; wq = H6.groupby("wd").qvol.median()
T6 = pd.DataFrame({"mean_abs_r_bp": iv, "qvol_share_pct": ivol}).round(3); T6.to_csv("tables/00_6_intraday.csv"); print(T6.to_string())
T6w = pd.DataFrame({"mean_abs_r_bp": wv, "median_qvol": wq}).round(2); T6w.to_csv("tables/00_6_weekly.csv"); print(T6w.to_string())
OUT["intraday_absr_max_min"] = float(iv.max() / iv.min()); OUT["intraday_qvol_max_min"] = float(ivol.max() / ivol.min()); OUT["weekly_absr_max_min"] = float(wv.max() / wv.min())
fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
ax[0].plot(iv.index, iv / iv.mean(), color=PAL[0], label="mean |r1|"); ax[0].plot(ivol.index, ivol / ivol.mean(), color=PAL[1], label="volume share")
ax[0].set_xlabel("UTC hour (bar open)"); ax[0].set_title("Activity peaks at the US open (13-15 UTC)"); ax[0].legend()
ax[1].bar(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], wv / wv.mean(), color=PAL[0]); ax[1].set_title("Weekend hours are quieter")
save(fig, "00_intraday_weekly.png")

# ---------------- 7. what a row is: Roll check
rows = []
for c in COINS:
    h = H[H.coin == c].set_index("t")
    if h.price.count() < 1000: continue
    lr = h.r1.dropna(); cov1 = lr.autocorr(1) * lr.var()
    roll_half_bp = np.sqrt(-cov1) * 1e4 if cov1 < 0 else np.nan
    rows.append(dict(coin=c, src=h.src.dropna().unique().tolist(), roll_half_spread_bp=roll_half_bp, hourly_acf1=lr.autocorr(1), rt_cost_24h_bp=RT24[c]))
T7 = pd.DataFrame(rows).set_index("coin").round(3); T7.to_csv("tables/00_7_roll.csv"); print(T7.to_string())
fig, ax = plt.subplots(figsize=(8, 3.4))
ax.bar(T7.index.str[:-3], T7.roll_half_spread_bp.fillna(0), color=PAL[0], label="Roll half-spread (bp) from hourly prints")
ax.plot(T7.index.str[:-3], T7.rt_cost_24h_bp / 2, "o", color=PAL[7], label="half of FTMO RT cost (bp)")
ax.set_title("Hourly prints: Roll's bounce estimate (0 = no negative lag-1 cov)"); ax.legend(); save(fig, "00_roll.png")
json.dump({k: (v if not isinstance(v, tuple) else list(map(str, v))) for k, v in OUT.items()}, open("tables/00_summary.json", "w"), indent=1)
print(OUT)
