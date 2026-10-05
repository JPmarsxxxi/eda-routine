"""Phase 0 profile, EXPLORE only. Rules are in DATA_PROFILE.md (written before this ran)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from scipy import stats
import run_lib as L
plt = L.setup_mpl()
S = L.slices(); W = S["EXPLORE"]
out = []
def P(s=""): out.append(s); print(s)

prim, bin_ = {}, {}
for c in L.COINS:
    p = L.load_primary(c, "Phase 0 profile (EXPLORE)", W)
    if len(p): prim[c] = p.set_index("t")
    b = L.load_binance(c, "Phase 0 profile (EXPLORE)", W)
    if len(b): bin_[c] = b.set_index("t")
coins = list(prim)
# hourly log returns, never across new_source or a gap
H = {}
for c in coins:
    p = prim[c]
    r = np.log(p.price).diff()
    gap = p.index.to_series().diff() != pd.Timedelta(hours=1)
    r[gap.values | p.new_source.values] = np.nan
    H[c] = r
H = pd.DataFrame(H)
# daily log returns (end-of-day to end-of-day, valid response days only) -- descriptive, not conditioned on anything
D = {}
for c in coins:
    D[c] = np.log1p(L.daily_response(prim[c].reset_index()))
D = pd.DataFrame(D)

# ---------------- 1
P("### 1. Distributions"); P()
rows = []
for c in coins:
    h, d = H[c].dropna(), D[c].dropna()
    lv = np.log(bin_[c].vol[bin_[c].vol > 0])
    rows.append([c, len(h), round(h.std() * 1e4, 1), round(stats.skew(h), 2), round(stats.kurtosis(h), 1),
                 round((h == 0).mean() * 100, 2), round(h.quantile(.01) * 1e4, 1), round(h.quantile(.99) * 1e4, 1),
                 len(d), round(d.std() * 1e4, 0), round(stats.kurtosis(d), 1), round(lv.std(), 2)])
t1 = pd.DataFrame(rows, columns=["coin", "n_h", "sd_h_bp", "skew_h", "exkurt_h", "zero_%", "p1_bp", "p99_bp",
                                 "n_d", "sd_d_bp", "exkurt_d", "sd_logvol_h"])
P(L.md(t1)); P()
P(f"Verdict: excess kurtosis of hourly returns {t1.exkurt_h.min()}..{t1.exkurt_h.max()} (> 3 for every coin -> FAT-TAILED); "
  f"daily {t1.exkurt_d.min()}..{t1.exkurt_d.max()}; zero-mass {t1['zero_%'].min()}..{t1['zero_%'].max()}% "
  f"({'none suspicious' if t1['zero_%'].max() <= 2 else 'SUSPICIOUS > 2%'}).")
fig, ax = plt.subplots(figsize=(8, 3.6))
for i, c in enumerate(coins):
    h = H[c].dropna(); z = (h - h.mean()) / h.std()
    ax.hist(z.clip(-10, 10), bins=200, histtype="step", density=True, color=L.PAL[i % 8], label=c, log=True)
x = np.linspace(-10, 10, 400); ax.plot(x, stats.norm.pdf(x), color=L.GRAY, ls="--", label="normal")
ax.set_title("Hourly returns are fat-tailed for every coin (EXPLORE, standardised, log density)")
ax.set_xlabel("standardised hourly log return (clipped at +-10)"); ax.legend(ncol=4, fontsize=7)
L.save(fig, "00_distributions"); P("Plot: plots/00_distributions.png"); P()

# ---------------- 2
P("### 2. Missingness and gaps"); P()
rows = []
for c in coins:
    p = prim[c]; idx = pd.date_range(p.index.min(), p.index.max(), freq="h")
    days = pd.date_range(p.index.min().floor("D"), p.index.max().floor("D"), freq="D")
    valid = L.daily_response(p.reset_index()).shift(1).reindex(days)  # validity of day d as a response day
    n_valid = valid.notna().sum()
    b = bin_[c]; bidx = pd.date_range(max(b.index.min(), W[0]), b.index.max(), freq="h")
    rows.append([c, str(p.index.min().date()), len(idx), len(idx) - len(p), round((len(idx) - len(p)) / len(idx) * 100, 2),
                 int(p.new_source.sum()), len(days), round((1 - n_valid / len(days)) * 100, 1),
                 len(bidx) - len(b.loc[b.index >= bidx[0]])])
t2 = pd.DataFrame(rows, columns=["coin", "first", "exp_hours", "missing_h", "missing_%", "new_source", "days",
                                 "invalid_resp_day_%", "binance_missing_h"])
P(L.md(t2)); P()
fl = t2[(t2["missing_%"] > 1) | (t2["invalid_resp_day_%"] > 5)].coin.tolist()
P(f"Verdict: flagged coins (> 1% hours missing or > 5% invalid response days): {fl if fl else 'none'}. "
  "Invalid response days include the first day of each coin's coverage and days after a new_source/gap row.")
miss = pd.DataFrame({c: prim[c].price.resample("D").count().reindex(pd.date_range(W[0], W[1], freq="D", inclusive="left"))
                     for c in coins})
fig, ax = plt.subplots(figsize=(8, 3.2))
im = ax.imshow((miss.fillna(0).T.values < 24), aspect="auto", cmap="Greys", interpolation="nearest")
ax.set_yticks(range(len(coins))); ax.set_yticklabels(coins); ax.grid(False)
ticks = np.arange(0, len(miss), 90); ax.set_xticks(ticks); ax.set_xticklabels([str(miss.index[i].date()) for i in ticks], fontsize=7)
ax.set_title("Incomplete days (black) are coverage starts (ADA, BCH) and scattered outages (EXPLORE)")
L.save(fig, "00_missingness"); P("Plot: plots/00_missingness.png"); P()

# ---------------- 3
P("### 3. Autocorrelation (hourly time-series lags only)"); P()
lags = [1, 2, 3, 6, 12, 24]
rows = []
for c in coins:
    h = H[c]; a = h.abs()
    lv = np.log(bin_[c].vol.where(bin_[c].vol > 0)).asfreq("h")
    n = h.notna().sum(); thr = 2 / np.sqrt(n)
    rows.append([c, n, round(thr, 3)] + [round(h.autocorr(k), 3) for k in lags] + [round(a.autocorr(1), 3), round(a.autocorr(24), 3),
                 round(lv.autocorr(1), 3), round(lv.autocorr(24), 3)])
t3 = pd.DataFrame(rows, columns=["coin", "n", "2/sqrt(n)"] + [f"r_l{k}" for k in lags] + ["|r|_l1", "|r|_l24", "logvol_l1", "logvol_l24"])
P(L.md(t3)); P()
sig = {k: int((t3[f"r_l{k}"].abs() > t3["2/sqrt(n)"]).sum()) for k in lags}
P(f"Verdict: coins with |ACF| of signed hourly returns > 2/sqrt(n), by lag: {sig}. |r| and log volume are strongly "
  f"persistent (|r| lag1 {t3['|r|_l1'].min()}..{t3['|r|_l1'].max()}, log-volume lag1 {t3['logvol_l1'].min()}..{t3['logvol_l1'].max()}): "
  "volatility and activity cluster.")
fig, ax = plt.subplots(figsize=(8, 3.4))
for i, c in enumerate(coins):
    ax.plot(range(1, 25), [H[c].autocorr(k) for k in range(1, 25)], marker="o", ms=2, color=L.PAL[i % 8], label=c)
thr = 2 / np.sqrt(H.notna().sum().min()); ax.axhline(thr, color=L.GRAY, ls="--"); ax.axhline(-thr, color=L.GRAY, ls="--", label="+-2/sqrt(n)")
ax.set_title("Signed hourly returns: ACF small; only a few lags clear the noise band (EXPLORE)"); ax.set_xlabel("lag (hours)")
ax.legend(ncol=4, fontsize=7); L.save(fig, "00_acf"); P("Plot: plots/00_acf.png"); P()

# ---------------- 4
P("### 4. Cross-column relationships and impostors"); P()
cm = H.corr()
P("Pairwise correlation of hourly returns (EXPLORE):"); P(); P(L.md(cm.round(2), index=True)); P()
off = cm.values[np.triu_indices(len(coins), 1)]
P(f"Mean pairwise hourly-return correlation {off.mean():.2f} (min {off.min():.2f}, max {off.max():.2f}): one common factor dominates.")
rows = []
for c in coins:
    p, b = prim[c], bin_[c]
    j = p.join(b[["open", "close", "high", "low"]], how="inner")
    rp = np.log(j.price).diff(); rb = np.log(j.close).diff()
    # binance daily bars
    db = L.daily_bars(b.reset_index()); db = db[(db.index >= W[0]) & (db.index < W[1])]
    gap = (db.open / db.close.shift(1) - 1).abs() * 1e4
    co = np.log(db.close / db.open); cc = np.log(db.close / db.close.shift(1))
    rows.append([c, round(rp.corr(rb), 4), round((gap < 5).mean() * 100, 1), round(gap.median(), 2), round(co.corr(cc), 4)])
t4 = pd.DataFrame(rows, columns=["coin", "corr(primary r, binance close r) 1h", "days |open-prevclose|<5bp %",
                                 "median gap bp", "corr(log c/o, log c/prev c) daily"])
P(L.md(t4)); P()
# rank(low) crossings
lows = {}
for c in coins:
    db = L.daily_bars(bin_[c].reset_index()); lows[c] = db.low
lows = pd.DataFrame(lows); lows = lows[(lows.index >= W[0]) & (lows.index < W[1])]
rk = lows.rank(axis=1)
both = rk.notna() & rk.shift(1).notna()
chg = ((rk != rk.shift(1)) & both).sum().sum() / both.sum().sum()
P(f"Cross-sectional rank of daily `low` changes on {chg*100:.1f}% of coin-days (rule: near-static if < 10%). "
  f"Order of the median rank: {rk.median().sort_values(ascending=False).round(1).to_dict()}.")
P(f"Verdict: primary price vs Binance close is a twin in EXPLORE (corr >= {t4.iloc[:,1].min():.4f}) — expected, primary IS "
  "the Binance trade close in validated years (an impostor pair by construction; the response and the signal share a "
  "source until 2022). Binance daily open == previous close (24/7 continuous) on "
  f"{t4.iloc[:,2].min()}..{t4.iloc[:,2].max()}% of days; (close-open) is a twin of the close-to-close return "
  f"(corr {t4.iloc[:,4].min():.3f}..{t4.iloc[:,4].max():.3f}). rank(low) is {'NEAR-STATIC' if chg < .10 else 'not static'}.")
fig, ax = plt.subplots(figsize=(6.2, 5))
im = ax.imshow(cm.values, cmap="Blues", vmin=0, vmax=1); ax.grid(False)
ax.set_xticks(range(len(coins))); ax.set_xticklabels(coins); ax.set_yticks(range(len(coins))); ax.set_yticklabels(coins)
for i in range(len(coins)):
    for j in range(len(coins)):
        ax.text(j, i, f"{cm.values[i,j]:.2f}", ha="center", va="center", fontsize=7, color="white" if cm.values[i,j] > .6 else L.TEXT)
ax.set_title("Hourly returns share one strong common factor (EXPLORE)"); fig.colorbar(im, ax=ax, shrink=.7)
L.save(fig, "00_crosscorr"); P("Plot: plots/00_crosscorr.png"); P()

# ---------------- 5
P("### 5. Regime structure (EXPLORE half-years)"); P()
eras = [("2019H1", "2019-01-01", "2019-07-01"), ("2019H2", "2019-07-01", "2020-01-01"), ("2020H1", "2020-01-01", "2020-05-28")]
rows = []
for name, a, b in eras:
    sub = H[(H.index >= pd.Timestamp(a, tz="UTC")) & (H.index < pd.Timestamp(b, tz="UTC"))]
    sd = sub.std() * 1e4; k = sub.apply(lambda s: stats.kurtosis(s.dropna()))
    c2 = sub.corr().values; o = c2[np.triu_indices(len(coins), 1)]
    ac = sub.apply(lambda s: s.autocorr(1))
    rows.append([name, sub.notna().any(axis=0).sum(), round(sd.median(), 1), round(k.median(), 1), round(np.nanmean(o), 2), round(ac.median(), 3)])
t5 = pd.DataFrame(rows, columns=["era", "coins", "median sd_h bp", "median exkurt_h", "mean pair corr", "median ACF1"])
P(L.md(t5)); P()
vr = t5["median sd_h bp"].max() / t5["median sd_h bp"].min(); dc = t5["mean pair corr"].max() - t5["mean pair corr"].min()
P(f"Verdict: vol ratio max/min {vr:.2f} ({'BREAK' if vr > 2 else 'no break by the 2x rule'}); correlation range {dc:.2f} "
  f"({'BREAK' if dc > .2 else 'no break by the 0.2 rule'}). 2020H1 contains the March-2020 crash.")
fig, ax = plt.subplots(figsize=(8, 3.2))
roll = (H.rolling(24 * 30, min_periods=24 * 20).std() * 1e4)
for i, c in enumerate(coins):
    ax.plot(roll.index, roll[c], color=L.PAL[i % 8], label=c, lw=1)
ax.set_title("30-day rolling hourly vol: calm 2019H2, March-2020 spike (EXPLORE)"); ax.set_ylabel("bp per hour")
ax.legend(ncol=4, fontsize=7); L.save(fig, "00_regimes"); P("Plot: plots/00_regimes.png"); P()

# ---------------- 6
P("### 6. Intraday / weekly shape (descriptive)"); P()
vs = pd.DataFrame({c: bin_[c].quote_vol for c in coins})
share = vs.div(vs.sum(axis=1), axis=0)
byh_v = (vs / vs.rolling(24 * 7, min_periods=24).mean()).groupby(vs.index.hour).median().median(axis=1)
byh_a = H.abs().groupby(H.index.hour).mean().median(axis=1) * 1e4
byd_v = (vs / vs.rolling(24 * 7, min_periods=24).mean()).groupby(vs.index.dayofweek).median().median(axis=1)
byd_a = H.abs().groupby(H.index.dayofweek).mean().median(axis=1) * 1e4
t6 = pd.DataFrame({"rel_quote_vol": byh_v.round(2), "mean_|r|_bp": byh_a.round(1)})
P("By UTC hour (median across coins):"); P(); P(L.md(t6.T, index=True)); P()
P("By weekday (0=Mon):"); P(); P(L.md(pd.DataFrame({"rel_quote_vol": byd_v.round(2), "mean_|r|_bp": byd_a.round(1)}).T, index=True)); P()
P(f"Descriptive: relative volume max/min hour ratio {byh_v.max()/byh_v.min():.2f} (peak {byh_v.idxmax()}h, trough {byh_v.idxmin()}h UTC); "
  f"|r| ratio {byh_a.max()/byh_a.min():.2f}; weekend volume {byd_v.loc[[5,6]].mean():.2f} vs weekday {byd_v.loc[:4].mean():.2f}.")
fig, ax = plt.subplots(figsize=(8, 3.2))
ax.plot(byh_v.index, byh_v / byh_v.mean(), marker="o", color=L.PAL[0], label="relative quote volume (scaled)")
ax.plot(byh_a.index, byh_a / byh_a.mean(), marker="o", color=L.PAL[3], label="mean |hourly return| (scaled)")
ax.axhline(1, color=L.GRAY, ls="--"); ax.set_xlabel("UTC hour (bar open)")
ax.set_title("Volume and |return| peak in US hours (13-16 UTC), trough ~03-06 UTC (EXPLORE)"); ax.legend(fontsize=7)
L.save(fig, "00_intraday"); P("Plot: plots/00_intraday.png"); P()

# ---------------- 7
P("### 7. What a row physically is"); P()
rows = []
for c in coins:
    j = prim[c].join(bin_[c][["open", "close"]], how="inner")
    j = j[j.source == "binance_trade"]
    e_c = (np.log(j.price / j.close)).abs() * 1e4; e_o = (np.log(j.price / j.open)).abs() * 1e4
    e_n = (np.log(j.price / bin_[c].open.shift(-1).reindex(j.index))).abs() * 1e4
    rows.append([c, len(j), round(e_c.median(), 3), round(e_o.median(), 2), round(e_n.median(), 2)])
t7 = pd.DataFrame(rows, columns=["coin", "n", "med |price - binance close_t| bp", "med |price - binance open_t| bp", "med |price - binance open_t+1| bp"])
P(L.md(t7)); P()
ok = (t7.iloc[:, 2] < 1).all() and (t7.iloc[:, 3] > 5 * t7.iloc[:, 2].clip(lower=0.01)).all()
P(f"Verdict: {'CONFIRMED' if ok else 'NOT confirmed'} — primary `price` stamped t equals the Binance close of bar t (the value at "
  "t+1h), i.e. OPEN-stamped, value at bar END, knowable at t+1h. One row = one hour's closing trade print (Binance years) or "
  "closing FTMO mid (2022+, 7 coins). Hence the daily response uses the bar stamped 23:00 as 'end of day'.")
fig, ax = plt.subplots(figsize=(7, 3))
ax.bar(np.arange(len(coins)) - .2, t7.iloc[:, 2], width=.4, color=L.PAL[0], label="vs Binance close of same stamp")
ax.bar(np.arange(len(coins)) + .2, t7.iloc[:, 3], width=.4, color=L.GRAY, label="vs Binance open of same stamp")
ax.set_xticks(range(len(coins))); ax.set_xticklabels(coins); ax.set_ylabel("median |gap| bp")
ax.set_title("Primary price = Binance close of the same stamp (0 bp), not its open (EXPLORE)"); ax.legend(fontsize=7)
L.save(fig, "00_row_meaning"); P("Plot: plots/00_row_meaning.png"); P()

open(os.path.join(L.RUN, "code", "p0_results.md"), "w").write("\n".join(out) + "\n")
