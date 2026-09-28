"""Step 4: check each observation against the boring explanations. TRAIN only. HAC (Newey-West) intervals throughout."""
import warnings; warnings.filterwarnings("ignore")
from lib import *
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

g = grid(load_train(["open", "high", "low", "close", "vol", "buy_vol", "n", "gap_min"]))
r = g["r"]; g["E"] = era(g.index)
g["tr5"] = trail(r, 5); g["tr60"] = trail(r, 60); g["f5"] = fwd(r, 5); g["f5s2"] = fwd(r, 5, skip=2)
g["absr60"] = r.abs().rolling(60, min_periods=60).sum()
g["imb5"] = g["imb"].rolling(5, min_periods=5).mean()
out = {}

# ---------------- (c) Benjamini-Hochberg across the sweep
P = pd.read_csv(PVALS)
P["p_bh"] = multipletests(P.p.clip(lower=1e-300), method="fdr_bh")[1]
P["survives_bh_5pct"] = P.p_bh < 0.05
table(P.set_index("test_id"), 15, "bh_adjusted_pvals")
K = len(P); print("K =", K, "survive BH:", P.survives_bh_5pct.sum())

def classify(v):
    """v: per-era effect signed so that + = the claimed direction, in era order."""
    v = pd.Series(v).dropna()
    s = np.sign(v); flips = int((s.diff().fillna(0) != 0).sum())
    rho = stats.spearmanr(np.arange(len(v)), v.values)[0]
    if flips >= 2: return "alternating"
    if rho <= -0.6 and v.iloc[-1] < 0.5 * v.iloc[0]: return "decaying"
    if rho >= 0.6: return "strongest-recent"
    return "flat"

def tb_bp(d, xc, yc, lags, per_era_deciles=True):
    """top-minus-bottom decile of xc, mean yc difference in bp with HAC 95% CI."""
    d = d[[xc, yc, "E"]].dropna().copy()
    if per_era_deciles:
        d["q"] = d.groupby("E")[xc].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    else:
        d["q"] = pd.qcut(d[xc].rank(method="first"), 10, labels=False)
    d = d[d.q.isin([0, 9])]
    b, se, t, p, n = nw_slope(d[yc] * 1e4, (d.q == 9).astype(float), lags)
    return b, b - 1.96 * se, b + 1.96 * se, t, n

# ================= OBS1: trailing 5-min return -> forward 5-min return (reversal)
o = {}
base = tb_bp(g, "tr5", "f5", 10)
o["base"] = base
# (a) twin: vol-scaled X; controls for trailing vol and trailing 60-min return
g["tr5z"] = g["tr5"] / g["absr60"]
o["vol_scaled_X"] = tb_bp(g, "tr5z", "f5", 10)
d = g[["f5", "tr5", "tr60", "absr60", "E"]].dropna()
Z = (d[["tr5", "tr60", "absr60"]] - d[["tr5", "tr60", "absr60"]].mean()) / d[["tr5", "tr60", "absr60"]].std()
m = sm.OLS(d.f5.values * 1e4, sm.add_constant(np.column_stack([Z.tr5, Z.tr60, Z.absr60, Z.tr5 * Z.absr60]))).fit(cov_type="HAC", cov_kwds={"maxlags": 10})
o["partial_slope_bp_per_sd"] = (m.params[1], m.params[1] - 1.96 * m.bse[1], m.params[1] + 1.96 * m.bse[1], m.tvalues[1], len(d))
o["interaction_tr5_x_vol_t"] = m.tvalues[4]
# within trailing-vol terciles (per era)
g["volq"] = g.groupby("E")["absr60"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
o["vol_terciles"] = {int(k): tb_bp(g[g.volq == k], "tr5", "f5", 10) for k in range(3)}
# (b) artifacts: skip 2 bars (bounce), drop 2017, drop top 1% |tr5| and |f5|, by UTC session
o["skip2"] = tb_bp(g, "tr5", "f5s2", 10)
o["ex2017"] = tb_bp(g[g.E != "2017"], "tr5", "f5", 10)
cut = g[["tr5", "f5"]].abs().quantile(0.99)
o["drop_top1pct"] = tb_bp(g[(g.tr5.abs() < cut.tr5) & (g.f5.abs() < cut.f5)], "tr5", "f5", 10)
o["exclude_zero_return_windows"] = tb_bp(g[g.tr5 != 0], "tr5", "f5", 10)
sess = {"00-08": (0, 8), "08-16": (8, 16), "16-24": (16, 24)}
o["sessions"] = {}
hours = np.asarray(g.index.hour)
for k, (h0, h1) in sess.items():
    sub = g.loc[(hours >= h0) & (hours < h1)]
    print("session", k, len(sub), sub[["tr5", "f5"]].dropna().shape)
    o["sessions"][k] = tb_bp(sub, "tr5", "f5", 10)
# (d) eras
o["eras"] = {e: tb_bp(g[g.E == e], "tr5", "f5", 10) for e in ERAS}
o["era_class"] = classify({e: -o["eras"][e][0] for e in ERAS})
o["era_class_ex2017"] = classify({e: -o["eras"][e][0] for e in ERAS if e != "2017"})
out["OBS1"] = o
def row(lbl, v): return dict(check=lbl, effect_bp=v[0], lo=v[1], hi=v[2], t=v[3], n=v[4])
t1 = pd.DataFrame([row("base: top-bottom decile tr5 -> fwd5", o["base"]), row("(a) X scaled by trailing 60-min |r|", o["vol_scaled_X"]),
                   row("(a) partial slope bp per 1 sd tr5 | tr60, vol", o["partial_slope_bp_per_sd"])] +
                  [row(f"(a) trailing-vol tercile {k}", v) for k, v in o["vol_terciles"].items()] +
                  [row("(b) skip 2 bars", o["skip2"]), row("(b) ex 2017", o["ex2017"]), row("(b) drop top 1% |moves|", o["drop_top1pct"]),
                   row("(b) tr5 != 0 only", o["exclude_zero_return_windows"])] +
                  [row(f"(b) session {k} UTC", v) for k, v in o["sessions"].items()] +
                  [row(f"(d) era {e}", v) for e, v in o["eras"].items()])
table(t1.set_index("check"), 16, "obs1_checks"); print(t1.round(3).to_string())
fig, ax = plt.subplots(figsize=(10, 6))
yy = np.arange(len(t1))[::-1]
ax.errorbar(t1.effect_bp, yy, xerr=[t1.effect_bp - t1.lo, t1.hi - t1.effect_bp], fmt="o", color=PAL[0], ecolor=GRAY)
ax.set_yticks(yy); ax.set_yticklabels(t1.check, fontsize=8); ax.axvline(0, color="k", lw=0.6)
ax.set_xlabel("fwd 5-min return, top minus bottom decile (bp), HAC 95% CI (row 3: bp per sd)")
ax.set_title(f"16 OBS1: base {o['base'][0]:+.2f} bp; vol-scaled X {o['vol_scaled_X'][0]:+.2f}; skip-2 ({o['skip2'][0]:+.2f}), top-1% drop ({o['drop_top1pct'][0]:+.2f}); eras: {o['era_class']}", fontsize=10)
save(fig, 16, "obs1_checks")

# ================= OBS2: taker imbalance -> forward return (negative)
o = {}
d = g[["f5", "imb", "imb5", "r", "tr5", "absr60", "E"]].dropna()
def partial(dd, cols, lags=10):
    Z = (dd[cols] - dd[cols].mean()) / dd[cols].std()
    m = sm.OLS(dd.f5.values * 1e4, sm.add_constant(Z.values)).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return m.params[1], m.params[1] - 1.96 * m.bse[1], m.params[1] + 1.96 * m.bse[1], m.tvalues[1], len(dd)
o["imb_alone"] = partial(d, ["imb"])
o["imb_given_r_tr5_vol"] = partial(d, ["imb", "r", "tr5", "absr60"])
o["imb5_alone"] = partial(d, ["imb5"])
o["imb5_given_tr5_vol"] = partial(d, ["imb5", "r", "tr5", "absr60"])
o["tb_decile"] = tb_bp(g, "imb", "f5", 10)
o["eras_imb_given"] = {e: partial(d[d.E == e], ["imb", "r", "tr5", "absr60"]) for e in ERAS}
o["era_class"] = classify({e: -o["eras_imb_given"][e][0] for e in ERAS})
o["corr_imb_r_same_bar"] = d.imb.corr(d.r)
out["OBS2"] = o
t2 = pd.DataFrame([row("imb alone (bp per sd)", o["imb_alone"]), row("imb | r, tr5, vol", o["imb_given_r_tr5_vol"]), row("imb5 alone", o["imb5_alone"]),
                   row("imb5 | r, tr5, vol", o["imb5_given_tr5_vol"]), row("top-bottom imb decile (bp)", o["tb_decile"])] +
                  [row(f"(d) era {e}: imb | r, tr5, vol", v) for e, v in o["eras_imb_given"].items()])
table(t2.set_index("check"), 17, "obs2_checks"); print(t2.round(3).to_string(), "corr(imb, r same bar)", o["corr_imb_r_same_bar"])
fig, ax = plt.subplots(figsize=(10, 5))
yy = np.arange(len(t2))[::-1]
ax.errorbar(t2.effect_bp, yy, xerr=[t2.effect_bp - t2.lo, t2.hi - t2.effect_bp], fmt="o", color=PAL[1], ecolor=GRAY)
ax.set_yticks(yy); ax.set_yticklabels(t2.check, fontsize=8); ax.axvline(0, color="k", lw=0.6); ax.set_xlabel("fwd 5-min return, bp per sd of X (HAC 95% CI)")
ax.set_title(f"17 OBS2: imbalance {o['imb_alone'][0]:+.3f} bp/sd alone -> {o['imb_given_r_tr5_vol'][0]:+.3f} given same-bar r, tr5, vol (corr imb,r = {o['corr_imb_r_same_bar']:.2f})", fontsize=10)
save(fig, 17, "obs2_checks")

# ================= OBS3: AR(1) of 1-min r drifts from negative to positive
o = {}
mo = g.index.to_period("M")
mon = pd.DataFrame({"ar1": pd.read_csv(os.path.join(RUN, "tables", "09_monthly_coefficients.csv"), index_col=0)["ar1"]})
mon.index = pd.PeriodIndex(mon.index, freq="M")
mon["log_trades_med"] = np.log(g["n"].groupby(mo).median())
hl = np.log(g["high"] / g["low"])
mon["cs_proxy_bp"] = (hl.groupby(mo).median() * 1e4)
mon["zero_ret_share"] = (r == 0).groupby(mo).mean()
mon["vol_bp"] = r.groupby(mo).std() * 1e4
mon = mon.dropna()
o["corr_ar1_logtrades"] = stats.spearmanr(mon.ar1, mon.log_trades_med)[0]
o["corr_ar1_zero_share"] = stats.spearmanr(mon.ar1, mon.zero_ret_share)[0]
o["corr_ar1_vol"] = stats.spearmanr(mon.ar1, mon.vol_bp)[0]
o["corr_ar1_hl"] = stats.spearmanr(mon.ar1, mon.cs_proxy_bp)[0]
X = sm.add_constant(((mon[["log_trades_med", "vol_bp", "zero_ret_share"]] - mon[["log_trades_med", "vol_bp", "zero_ret_share"]].mean()) / mon[["log_trades_med", "vol_bp", "zero_ret_share"]].std()).values)
X = np.column_stack([X, (mon.index.to_timestamp() >= "2020-01-01").astype(float)])
mm = sm.OLS(mon.ar1.values, X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
o["post2020_dummy_given_liquidity"] = (mm.params[4], mm.params[4] - 1.96 * mm.bse[4], mm.params[4] + 1.96 * mm.bse[4], mm.tvalues[4], len(mon))
# drop top 1% |r|
c1 = r.abs().quantile(0.99)
rr = r.where(r.abs() < c1)
o["ar1_drop_top1_pre"] = nw_slope(rr[g.index < "2020-01-01"], rr.shift(1)[g.index < "2020-01-01"], 10)[:2]
o["ar1_drop_top1_post"] = nw_slope(rr[g.index >= "2020-01-01"], rr.shift(1)[g.index >= "2020-01-01"], 10)[:2]
o["ar1_by_vol_tercile"] = {}
for k in range(3):
    s = g.volq == k
    o["ar1_by_vol_tercile"][k] = (nw_slope(r[s & (g.index < "2020-01-01")], r.shift(1)[s & (g.index < "2020-01-01")], 10)[0],
                                  nw_slope(r[s & (g.index >= "2020-01-01")], r.shift(1)[s & (g.index >= "2020-01-01")], 10)[0])
out["OBS3"] = o
table(mon, 18, "obs3_monthly_ar1_vs_liquidity"); print({k: v for k, v in o.items()})
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].scatter(mon.log_trades_med, mon.ar1, c=[PAL[0] if p.year < 2020 else PAL[2] for p in mon.index], s=18)
ax[0].axhline(0, color="k", lw=0.6); ax[0].set_xlabel("log median trades per minute (month)"); ax[0].set_ylabel("monthly AR(1) of 1-min r")
ax[0].set_title(f"AR(1) vs liquidity: Spearman {o['corr_ar1_logtrades']:.2f} (blue <2020, pink >=2020)", fontsize=9)
ax[1].scatter(mon.zero_ret_share * 100, mon.ar1, color=PAL[1], s=18); ax[1].axhline(0, color="k", lw=0.6); ax[1].set_xscale("log")
ax[1].set_xlabel("% zero-return bars (month)"); ax[1].set_title(f"AR(1) vs zero-return share: Spearman {o['corr_ar1_zero_share']:.2f}", fontsize=9)
pdm = o["post2020_dummy_given_liquidity"]
fig.suptitle(f"18 OBS3: AR(1) tracks liquidity; post-2020 shift given liquidity+vol = {pdm[0]:+.3f} [{pdm[1]:+.3f},{pdm[2]:+.3f}]", fontweight="bold", fontsize=10)
save(fig, 18, "obs3_checks")

# ================= OBS4: 21:00-23:00 UTC mean return (hour 21 + 22), KNOWN PRIOR (21-23 UTC seasonality EDA)
o = {}
hr = r.resample("60min").sum(min_count=1)
day = hr.index.floor("D")
w = hr[(hr.index.hour == 21) | (hr.index.hour == 22)].groupby(day[(hr.index.hour == 21) | (hr.index.hour == 22)]).sum()
alld = hr.groupby(day).sum()
other = (alld - w.reindex(alld.index).fillna(0)) / 22 * 2  # mean 2-hour chunk outside the window, same day
D = pd.DataFrame({"w": w, "other2h": other}).dropna(); D["ex"] = D.w - D.other2h
D["E"] = era(D.index)
tv = r.abs().rolling(1440, min_periods=720).sum()        # trailing 24h sum |r| at each minute
D["tv"] = tv.reindex(D.index + pd.Timedelta(hours=20, minutes=59)).values
D["tr24"] = trail(r, 1440).reindex(D.index + pd.Timedelta(hours=20, minutes=59)).values
def mean_ci(x, lags=5):
    m_, se, t, p = nw_mean(x, lags); return m_ * 1e4, (m_ - 1.96 * se) * 1e4, (m_ + 1.96 * se) * 1e4, t, len(pd.Series(x).dropna())
o["base_window_bp"] = mean_ci(D.w)
o["base_excess_bp"] = mean_ci(D.ex)
o["vol_scaled_t"] = nw_mean((D.w / D.tv).dropna(), 5)[2]
res = sm.OLS(D.w.values, sm.add_constant(D[["tr24"]].fillna(0).values)).fit()
o["resid_on_trailing24h_bp"] = mean_ci(D.w - res.params[1] * D.tr24.fillna(0))
o["after_up_day_bp"] = mean_ci(D.w[D.tr24 > 0]); o["after_down_day_bp"] = mean_ci(D.w[D.tr24 <= 0])
c1 = D.w.abs().quantile(0.99); o["drop_top1pct_bp"] = mean_ci(D.w[D.w.abs() < c1])
o["ex2017_bp"] = mean_ci(D.w[D.E != "2017"])
ny = pd.Series(D.index.tz_convert("America/New_York").map(lambda x: x.utcoffset().total_seconds() / 3600), index=D.index)
o["us_dst_on_bp"] = mean_ci(D.w[ny == -4]); o["us_dst_off_bp"] = mean_ci(D.w[ny == -5])
o["weekday_bp"] = mean_ci(D.w[D.index.dayofweek < 5]); o["weekend_bp"] = mean_ci(D.w[D.index.dayofweek >= 5])
o["eras"] = {e: mean_ci(D.w[D.E == e]) for e in ERAS}
o["era_class"] = classify({e: o["eras"][e][0] for e in ERAS})
out["OBS4"] = o
t4 = pd.DataFrame([row("21-23 UTC window r (bp/day)", o["base_window_bp"]), row("window minus mean 2h chunk", o["base_excess_bp"]),
                   row("(a) residual on trailing 24h r", o["resid_on_trailing24h_bp"]), row("(a) after trailing-24h up", o["after_up_day_bp"]),
                   row("(a) after trailing-24h down", o["after_down_day_bp"]), row("(b) drop top 1% days", o["drop_top1pct_bp"]), row("(b) ex 2017", o["ex2017_bp"]),
                   row("(b) US DST on (window = 17-19 NY)", o["us_dst_on_bp"]), row("(b) US DST off (window = 16-18 NY)", o["us_dst_off_bp"]),
                   row("(b) weekdays", o["weekday_bp"]), row("(b) weekends", o["weekend_bp"])] + [row(f"(d) era {e}", v) for e, v in o["eras"].items()])
table(t4.set_index("check"), 19, "obs4_checks"); print(t4.round(2).to_string(), "vol-scaled t", o["vol_scaled_t"])
fig, ax = plt.subplots(figsize=(10, 6))
yy = np.arange(len(t4))[::-1]
ax.errorbar(t4.effect_bp, yy, xerr=[t4.effect_bp - t4.lo, t4.hi - t4.effect_bp], fmt="o", color=PAL[3], ecolor=GRAY)
ax.set_yticks(yy); ax.set_yticklabels(t4.check, fontsize=8); ax.axvline(0, color="k", lw=0.6); ax.set_xlabel("bp per day, HAC 95% CI")
ax.set_title(f"19 OBS4 (known prior): 21-23 UTC mean {o['base_window_bp'][0]:+.1f} bp/day; top-1% drop {o['drop_top1pct_bp'][0]:+.1f}; eras: {o['era_class']}", fontsize=10)
save(fig, 19, "obs4_checks")

# ================= OBS5: |r| by UTC hour (peak h0 vs trough h5), size claim
o = {}
ah = hr.abs().to_frame("a"); ah["h"] = ah.index.hour; ah["day"] = ah.index.floor("D"); ah["E"] = era(ah.index)
ah["rel"] = ah.a / ah.groupby("day").a.transform("mean")     # vol twin: hour |r| relative to the same day's mean hour
prof = ah.groupby("h").rel.mean()
def ratio_ci(sub):
    x = sub.pivot_table(index="day", columns="h", values="rel")
    dd = (x[0] - x[5]).dropna()
    m_, se, t, p = nw_mean(dd, 5); return m_, m_ - 1.96 * se, m_ + 1.96 * se, t, len(dd)
o["h0_minus_h5_rel"] = ratio_ci(ah)
c1 = ah.a.quantile(0.99); o["drop_top1pct"] = ratio_ci(ah[ah.a < c1].copy())
nyh = pd.Series(ah.index.tz_convert("America/New_York").map(lambda x: x.utcoffset().total_seconds() / 3600), index=ah.index)
o["dst_on"] = ratio_ci(ah[nyh == -4]); o["dst_off"] = ratio_ci(ah[nyh == -5])
o["peak_hour_dst_on"] = int(ah[nyh == -4].groupby("h").rel.mean().idxmax()); o["peak_hour_dst_off"] = int(ah[nyh == -5].groupby("h").rel.mean().idxmax())
o["us_open_hour_dst_on_rel"] = float(ah[nyh == -4].groupby("h").rel.mean()[13]); o["us_open_hour_dst_off_rel"] = float(ah[nyh == -5].groupby("h").rel.mean()[14])
o["eras"] = {e: ratio_ci(ah[ah.E == e]) for e in ERAS}
o["era_class"] = classify({e: o["eras"][e][0] for e in ERAS})
out["OBS5"] = o
prof_on = ah[nyh == -4].groupby("h").rel.mean(); prof_off = ah[nyh == -5].groupby("h").rel.mean()
t5 = pd.DataFrame([row("h0 minus h5, |r| relative to same-day mean hour", o["h0_minus_h5_rel"]), row("(b) drop top 1% hours", o["drop_top1pct"]),
                   row("(b) US DST on", o["dst_on"]), row("(b) US DST off", o["dst_off"])] + [row(f"(d) era {e}", v) for e, v in o["eras"].items()])
table(t5.set_index("check"), 20, "obs5_checks"); table(pd.DataFrame({"all": prof, "dst_on": prof_on, "dst_off": prof_off}), 20, "obs5_rel_profile")
print(t5.round(3).to_string()); print({k: o[k] for k in ["peak_hour_dst_on", "peak_hour_dst_off", "us_open_hour_dst_on_rel", "us_open_hour_dst_off_rel"]})
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(prof_on.index, prof_on, marker="o", color=PAL[0], label="US DST on (EDT)"); ax.plot(prof_off.index, prof_off, marker="s", color=PAL[2], label="US DST off (EST)")
ax.axhline(1, color="k", lw=0.6); ax.set_xlabel("UTC hour"); ax.set_ylabel("|hourly r| / same-day mean"); ax.legend()
ax.set_title(f"20 OBS5: h0 is {o['h0_minus_h5_rel'][0]:+.2f} day-means above h5 after removing the day's vol level; eras: {o['era_class']}", fontsize=10)
save(fig, 20, "obs5_checks")

# ================= OBS6: weekend |daily r| lower
o = {}
dr = r.resample("1D").sum(min_count=1).dropna()
DD = pd.DataFrame({"a": dr.abs()}); DD["E"] = era(DD.index); DD["we"] = (DD.index.dayofweek >= 5).astype(float)
DD["tv"] = DD.a.shift(1).rolling(28, min_periods=14).mean()   # trailing 4-week mean |daily r| (knowable before the day)
DD["rel"] = DD.a / DD.tv
def we_ci(sub, col="rel"):
    b, se, t, p, n = nw_slope(sub[col], sub.we, 7); return b, b - 1.96 * se, b + 1.96 * se, t, n
o["raw_bp"] = tuple(v * (1e4 if i < 3 else 1) for i, v in enumerate(we_ci(DD, "a")))
o["vol_scaled"] = we_ci(DD.dropna())
c1 = DD.a.quantile(0.99); o["drop_top1pct"] = we_ci(DD[DD.a < c1].dropna())
o["ex2017"] = we_ci(DD[DD.E != "2017"].dropna())
o["eras"] = {e: we_ci(DD[DD.E == e].dropna()) for e in ERAS}
o["era_class"] = classify({e: -o["eras"][e][0] for e in ERAS})
out["OBS6"] = o
t6 = pd.DataFrame([row("weekend minus weekday |daily r| (bp)", o["raw_bp"]), row("(a) relative to trailing 4-week vol", o["vol_scaled"]),
                   row("(b) drop top 1% days", o["drop_top1pct"]), row("(b) ex 2017", o["ex2017"])] + [row(f"(d) era {e}", v) for e, v in o["eras"].items()])
table(t6.set_index("check"), 21, "obs6_checks"); print(t6.round(3).to_string())
fig, ax = plt.subplots(figsize=(10, 4.5))
tt = t6.iloc[1:]; yy = np.arange(len(tt))[::-1]
ax.errorbar(tt.effect_bp, yy, xerr=[tt.effect_bp - tt.lo, tt.hi - tt.effect_bp], fmt="o", color=PAL[4], ecolor=GRAY)
ax.set_yticks(yy); ax.set_yticklabels(tt.check, fontsize=8); ax.axvline(0, color="k", lw=0.6); ax.set_xlabel("weekend minus weekday, |daily r| / trailing 4-week mean |daily r| (HAC 95% CI)")
ax.set_title(f"21 OBS6: weekend days {o['vol_scaled'][0]:+.2f} of a normal day's size after vol scaling; raw {o['raw_bp'][0]:+.0f} bp; eras: {o['era_class']}", fontsize=10)
save(fig, 21, "obs6_checks")

# ================= OBS7: Hurst estimators disagree (0.47 vs 0.53): is it estimator bias? shuffle test on 2021
from s2a_memory_hurst import hurst_aggvar, hurst_rs
x = r[g.E == "2021"].dropna()
rng = np.random.default_rng(1)
sh = [(hurst_aggvar(pd.Series(rng.permutation(x.values))), hurst_rs(pd.Series(rng.permutation(x.values)))) for _ in range(5)]
o = {"real_2021": (hurst_aggvar(x), hurst_rs(x)), "shuffled_mean": tuple(np.mean(sh, 0)), "shuffled_sd": tuple(np.std(sh, 0))}
out["OBS7"] = o; print(o)
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.bar(["aggvar real", "aggvar shuffled", "R/S real", "R/S shuffled"], [o["real_2021"][0], o["shuffled_mean"][0], o["real_2021"][1], o["shuffled_mean"][1]],
       color=[PAL[0], GRAY, PAL[1], GRAY]); ax.axhline(0.5, color="k", lw=0.6); ax.set_ylim(0.4, 0.6); ax.set_ylabel("H (2021 1-min r)")
ax.set_title(f"22 OBS7: R/S real {o['real_2021'][1]:.3f} vs shuffled {o['shuffled_mean'][1]:.3f}; aggvar real {o['real_2021'][0]:.3f} vs shuffled {o['shuffled_mean'][0]:.3f}", fontsize=10)
save(fig, 22, "obs7_hurst_shuffle")

json.dump(out, open(os.path.join(RUN, "tables", "step4_all_checks.json"), "w"), indent=1, default=lambda z: float(z) if np.isscalar(z) else str(z))
