# Cell 01 - C1 existence. TRAIN only.
from common import *
setup()
P = r"C:\Users\User\eda-routine\data\btcusdt_spot_1m_clean\btcusdt_spot_1m_clean.parquet"
df = pd.read_parquet(P, columns=["close", "vol", "buy_vol", "sell_vol", "gap_min", "flag_repeat_prev_bar", "flag_close_outlier", "flag_wick_gt3pct"])
df = df[df.index <= TRAIN_END]                      # TRAIN mask before anything else
lr = np.log(df["close"]).diff().where(df["gap_min"] == 1)
df["r2"] = lr ** 2
df["minute"] = df.index.minute
r = df.resample("30min", label="left", closed="left")
hh = pd.DataFrame({"p": r["close"].last(), "last_min": r["minute"].last(), "vol": r["vol"].sum(min_count=1),
                   "buy_vol": r["buy_vol"].sum(min_count=1), "sell_vol": r["sell_vol"].sum(min_count=1),
                   "nbars": r["close"].count(), "rv": r["r2"].sum(min_count=1),
                   "flags": (r["flag_repeat_prev_bar"].sum() + r["flag_close_outlier"].sum() + r["flag_wick_gt3pct"].sum())})
hh["exact"] = hh["last_min"].isin([29, 59])
hh.to_parquet("tables/halfhour_TRAIN.parquet")

d, M = daily("TRAIN")
d = d[(d.index >= "2017-08-18") & (d.index <= "2023-03-19")]   # first full day with a previous-day anchor
ex = hh["exact"].reindex(pd.date_range(hh.index.min(), hh.index.max(), freq="30min", tz="UTC")).fillna(False)
exk = pd.DataFrame({"e": ex.values, "d": ex.index.floor("D"), "k": ex.index.hour * 2 + ex.index.minute // 30}).pivot(index="d", columns="k", values="e")
d["exact_all"] = (exk[0] & exk[46] & exk[47] & exk[47].shift(1).fillna(False)).reindex(d.index).astype(bool)
use = d.dropna(subset=["r_first", "r_last"])
d.to_parquet("tables/01_daily_legs_TRAIN.parquet")

n_days = len(d); n_use = len(use)
yr = pd.DataFrame({"days": d.groupby(d.index.year).size(), "usable": use.groupby(use.index.year).size(),
                   "exact_anchor_days": use[use.exact_all].groupby(use[use.exact_all].index.year).size(),
                   "r_last_zero_pct": use.groupby(use.index.year)["r_last"].apply(lambda s: 100 * (s == 0).mean()),
                   "r_first_zero_pct": use.groupby(use.index.year)["r_first"].apply(lambda s: 100 * (s == 0).mean())})
yr["dropped"] = yr["days"] - yr["usable"]
era_std = {n: float(use.loc[a:b, "r_first"].std()) for n, a, b in ERAS}
flags_on_used = int(hh.loc[hh.index.floor("D").isin(use.index), "flags"].sum())
print(yr.round(2)); print("usable", n_use, "of", n_days); print("era std r_first", era_std); print("flags on used days (all half-hours)", flags_on_used)
yr.to_csv("tables/01_existence_by_year.csv")
pd.Series(era_std, name="std_r_first").to_csv("tables/01_std_r_first_by_era.csv")

zero_bad = yr.loc[yr.index >= 2018, "r_last_zero_pct"].max()
if n_use < 1500 or zero_bad > 5 or min(era_std.values()) == 0: verdict = "REFUTED"
elif yr.loc[2017, "r_last_zero_pct"] > 5: verdict = "INCONCLUSIVE (2017 only)"
else: verdict = "SUPPORTED"
print("C1 verdict:", verdict, "| max 2018+ r_last zero %:", round(zero_bad, 2))

fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(yr.index, yr["usable"], color=PAL[0], label="usable days")
ax.bar(yr.index, yr["dropped"], bottom=yr["usable"], color=GRAY, label="dropped (missing anchor)")
ax.axhline(0, color=GRAY, lw=0.8)
ax.set_ylabel("UTC days (TRAIN)"); ax.legend(frameon=False)
ax.set_title(f"C1 {verdict}: {n_use:,} of {n_days:,} TRAIN days usable; max exact-zero r_last 2018+ = {zero_bad:.2f}%")
save(fig, "01_existence")
