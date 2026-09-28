"""Step 0: data card checks (TRAIN only). Open- vs close-time stamping; zero-gap rate; Roll / Corwin-Schultz."""
from lib import *

df = load_train()
df = add_returns(df)
out = {}
out["rows_train"] = len(df)
out["first"], out["last"] = str(df.index.min()), str(df.index.max())

# (1) day boundaries: first/last stamp of each full UTC day
d = df.index.floor("D")
g = pd.Series(df.index, index=d).groupby(level=0)
first_min = (g.min() - g.min().index).dt.total_seconds() / 60
last_min = (g.max() - g.max().index).dt.total_seconds() / 60
out["days"] = int(len(first_min))
out["days_first_bar_0000"] = int((first_min == 0).sum())
out["days_last_bar_2359"] = int((last_min == 1439).sum())
out["days_with_bar_2400_equiv"] = 0  # a close-stamp scheme would put a bar at next-day 00:00 belonging to prior day: not testable directly

# (2) activity by minute-of-hour: scheduled events fire at HH:00:00. Open-stamped -> spike in bar stamped :00;
#     close-stamped -> spike in bar stamped :01.
x = df[df.index.year >= 2018]
lab = np.log(x["n"])
mh = x.index.minute
by_min = pd.DataFrame({"mean_log_trades": lab.groupby(mh).mean(),
                       "mean_abs_r_bp": (x["r"].abs() * 1e4).groupby(mh).mean()})
by_min.index.name = "minute_of_hour"
table(by_min, 0, "activity_by_minute_of_hour")
base = by_min.loc[[m for m in range(60) if m not in (59, 0, 1, 2)]]
out["log_trades_excess_min00"] = float(by_min.loc[0, "mean_log_trades"] - base["mean_log_trades"].mean())
out["log_trades_excess_min01"] = float(by_min.loc[1, "mean_log_trades"] - base["mean_log_trades"].mean())
out["absr_ratio_min00"] = float(by_min.loc[0, "mean_abs_r_bp"] / base["mean_abs_r_bp"].mean())
out["absr_ratio_min01"] = float(by_min.loc[1, "mean_abs_r_bp"] / base["mean_abs_r_bp"].mean())

# (3) zero-gap rate by year: open == previous close (consecutive minutes only)
prev_close = df["close"].shift(1)
cons = df["gap_min"] == 1
zg = ((df["open"] == prev_close) & cons).groupby(df.index.year).sum() / cons.groupby(df.index.year).sum()
# open-vs-prev-close gap size in bp
gap_bp = (np.log(df["open"] / prev_close) * 1e4)[cons]
zgt = pd.DataFrame({"zero_gap_rate": zg, "median_abs_open_gap_bp": gap_bp.abs().groupby(gap_bp.index.year).median()})
table(zgt, 0, "zero_gap_rate_by_year")

# (4) Roll effective spread and Corwin-Schultz by year (trade prints, no quotes)
def roll(r):
    r = r.dropna().values
    c = np.cov(r[1:], r[:-1])[0, 1]
    return 2 * np.sqrt(-c) * 1e4 if c < 0 else np.nan, c

def corwin_schultz(h, l):
    b = (np.log(h / l) ** 2).rolling(2).sum()
    g = np.log(h.rolling(2).max() / l.rolling(2).min()) ** 2
    k = 3 - 2 * np.sqrt(2)
    a = (np.sqrt(2 * b) - np.sqrt(b)) / k - np.sqrt(g / k)
    s = 2 * (np.exp(a) - 1) / (1 + np.exp(a))
    return s.clip(lower=0)

rows = []
for y, x in df.groupby(df.index.year):
    rs, c = roll(x["r"])
    cs = corwin_schultz(x["high"], x["low"])
    rows.append(dict(year=y, roll_spread_bp=rs, lag1_autocov=c, lag1_autocorr=x["r"].autocorr(1),
                     corwin_schultz_median_bp=cs.median() * 1e4))
rt = pd.DataFrame(rows).set_index("year")
table(rt, 0, "roll_corwin_schultz_by_year")

json.dump(out, open(os.path.join(RUN, "tables", "00_datacard_checks.json"), "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str)); print(zgt); print(rt)

fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
ax[0].bar(by_min.index, by_min["mean_log_trades"] - base["mean_log_trades"].mean(), color=[PAL[0] if m == 0 else GRAY for m in by_min.index])
ax[0].axhline(0, color="k", lw=0.6)
ax[0].set_xlabel("minute of hour (bar stamp)"); ax[0].set_ylabel("mean log(trades) minus baseline")
ax[0].set_title(f"Trades jump in the bar stamped :00 (+{out['log_trades_excess_min00']:.2f} log) not :01 (+{out['log_trades_excess_min01']:.2f})", fontsize=10)
ax[1].plot(zgt.index, zgt["zero_gap_rate"] * 100, marker="o", color=PAL[0])
ax[1].set_ylabel("% bars with open == previous close"); ax[1].set_xlabel("year")
ax[1].set_title("Zero-gap rate by year (TRAIN)", fontsize=10)
fig.suptitle("Step 0: activity spikes in the bar STAMPED at the hour -> stamps are bar OPEN times", fontweight="bold")
save(fig, 0, "timestamp_open_check")
