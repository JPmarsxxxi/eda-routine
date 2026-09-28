"""Step 6: the ONE opening of VAL, top-3 leads, rules in VAL_RULES.md (written before this ran)."""
import warnings; warnings.filterwarnings("ignore")
from lib import *

df = pd.read_parquet(DATA, columns=["open", "high", "low", "close", "vol", "buy_vol", "n", "gap_min"],
                     filters=[("t", ">=", VAL_START), ("t", "<=", VAL_END)])
assert df.index.min() >= VAL_START and df.index.max() <= VAL_END
g = grid(df); r = g["r"]
res = {"rows": len(df), "first": str(df.index.min()), "last": str(df.index.max())}

def verdict(est, lo, hi, sign):
    if sign > 0:
        return "SUPPORTED" if lo > 0 else ("REFUTED" if est <= 0 else "INCONCLUSIVE")
    return "SUPPORTED" if hi < 0 else ("REFUTED" if est >= 0 else "INCONCLUSIVE")

# ---- L1 = OBS5
hr = r.resample("60min").sum(min_count=1)
ah = hr.abs().to_frame("a"); ah["h"] = ah.index.hour; ah["day"] = ah.index.floor("D")
ah["rel"] = ah.a / ah.groupby("day").a.transform("mean")
x = ah.pivot_table(index="day", columns="h", values="rel"); dd = (x[0] - x[5]).dropna()
m, se, t, p = nw_mean(dd, 5)
res["L1"] = dict(est=m, lo=m - 1.96 * se, hi=m + 1.96 * se, t=t, n=len(dd), verdict=verdict(m, m - 1.96 * se, m + 1.96 * se, +1))
prof = ah.groupby("h").rel.mean()

# ---- L2 = OBS6
dr = r.resample("1D").sum(min_count=1).dropna()
DD = pd.DataFrame({"a": dr.abs()}); DD["we"] = (DD.index.dayofweek >= 5).astype(float)
DD["tv"] = DD.a.shift(1).rolling(28, min_periods=14).mean(); DD["rel"] = DD.a / DD.tv; DD = DD.dropna()
b, se, t, p, n = nw_slope(DD.rel, DD.we, 7)
res["L2"] = dict(est=b, lo=b - 1.96 * se, hi=b + 1.96 * se, t=t, n=n, n_weekend_days=int(DD.we.sum()), verdict=verdict(b, b - 1.96 * se, b + 1.96 * se, -1))
raw = nw_slope(DD.a * 1e4, DD.we, 7); res["L2"]["raw_bp"] = raw[0]

# ---- L3 = OBS1
g["tr5"] = trail(r, 5); g["f5"] = fwd(r, 5); g["absr60"] = r.abs().rolling(60, min_periods=60).sum(); g["tr5z"] = g.tr5 / g.absr60
def tb(d, xc):
    d = d[[xc, "f5"]].dropna().copy(); d["q"] = pd.qcut(d[xc].rank(method="first"), 10, labels=False); d = d[d.q.isin([0, 9])]
    b, se, t, p, n = nw_slope(d.f5 * 1e4, (d.q == 9).astype(float), 10); return b, b - 1.96 * se, b + 1.96 * se, t, n
b, lo, hi, t, n = tb(g, "tr5")
res["L3"] = dict(est=b, lo=lo, hi=hi, t=t, n=n, verdict=verdict(b, lo, hi, -1))
res["L3"]["vol_scaled"] = tb(g, "tr5z")
res["L3"]["by_month"] = {str(k): tb(x_, "tr5")[:2] for k, x_ in g.groupby(g.index.to_period("M"))}
res["L3"]["zero_return_share"] = float((r == 0).mean())
json.dump(res, open(os.path.join(RUN, "tables", "24_val_results.json"), "w"), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))

train = {"L1": (0.407, 0.347, 0.467), "L2": (-0.400, -0.497, -0.302), "L3": (-2.061, -2.416, -1.706)}
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
for i, (k, lab) in enumerate([("L1", "h00 - h05 |r| (day-means)"), ("L2", "weekend - weekday |r| (rel.)"), ("L3", "fwd5 top-bottom tr5 (bp)")]):
    tv = train[k]; vv = res[k]
    ax[i].errorbar([0], [tv[0]], yerr=[[tv[0] - tv[1]], [tv[2] - tv[0]]], fmt="o", color=GRAY, capsize=4)
    ax[i].errorbar([1], [vv["est"]], yerr=[[vv["est"] - vv["lo"]], [vv["hi"] - vv["est"]]], fmt="o", color=PAL[i], capsize=4)
    ax[i].axhline(0, color="k", lw=0.6); ax[i].set_xticks([0, 1]); ax[i].set_xticklabels(["TRAIN", "VAL"]); ax[i].set_xlim(-0.5, 1.5)
    ax[i].set_title(f"{k}: {lab}\nVAL {vv['est']:+.2f} [{vv['lo']:+.2f},{vv['hi']:+.2f}] {vv['verdict']}", fontsize=9)
fig.suptitle("24: VAL (opened once; SOFT-clean, different regime per VAL_NOTE)", fontweight="bold")
save(fig, 24, "val_results")
