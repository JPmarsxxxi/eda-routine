# Cell 00 - data card. Structure + identity only. No forward returns, no VAL distribution statistics.
from common import *

out = {}
# ---- structure over the whole prepared file (max stamp <= VAL_END check), via raw read of the prepared copy
specs = dict(perp_hourly=PERP_HOURLY, perp_30m=PERP_30M, perp_1m=PERP_1M, dvol=DVOL, hspread=HSPREAD,
             funding=FUNDING, metrics=METRICS)
struct = {}
for k, s in specs.items():
    raw = G._read(s["path"])
    t = pd.to_datetime(raw[s["declare"]["time_col"]])
    if getattr(t.dtype, "tz", None) is not None:
        t = t.dt.tz_localize(None)
    dup_stamp = int(t.duplicated().sum())
    dup_rows = int(raw.duplicated().sum())
    tr = t[t <= TRAIN_HI]; va = t[(t >= VAL_LO) & (t <= VAL_HI)]; emb = t[(t > TRAIN_HI) & (t < VAL_LO)]
    step = tr.sort_values().diff().dropna()
    struct[k] = dict(rows=len(raw), first=str(t.min()), last=str(t.max()), max_le_val_end=bool(t.max() <= VAL_HI),
                     rows_train=len(tr), rows_embargo=len(emb), rows_val=len(va), dup_stamps=dup_stamp,
                     dup_rows=dup_rows, modal_step=str(step.mode().iloc[0]) if len(step) else None,
                     n_steps_gt_modal=int((step > step.mode().iloc[0]).sum()) if len(step) else None,
                     sorted=bool(t.is_monotonic_increasing),
                     minute_second_nonzero=int(((t.dt.second != 0) | (t.dt.microsecond != 0)).sum()),
                     symbol_values=sorted(raw["symbol"].unique().tolist()) if "symbol" in raw else None)
out["structure"] = struct
print(json.dumps(struct, indent=1))

# ---- TRAIN-only loads through the guard (these write ACCESS_LOG rows)
h = load(PERP_HOURLY, "cell_00", use=["close", "quote_volume"])
m30 = load(PERP_30M, "cell_00", use=["close", "quote_volume"])
m1 = load(PERP_1M, "cell_00", use=["close", "vol", "quote"])
mt = load(METRICS, "cell_00", use=["c", "o", "v", "sum_open_interest"])
fu = load(FUNDING, "cell_00", use=["funding"])

# identity 1: hourly vs 30m vs 1m at the same stamp (open-stamp hypothesis: close of bar T = 1m close at T+len-1min)
ident = {}
c1 = m1["close"]
for name, df, L in (("hourly", h, 60), ("30m", m30, 30)):
    x = df["close"]
    y_open = c1.reindex(x.index + pd.Timedelta(minutes=L - 1)).values   # open-stamped
    y_close = c1.reindex(x.index - pd.Timedelta(minutes=1)).values      # close-stamped
    ok = ~np.isnan(y_open)
    ident[f"{name}_close_eq_1m_close_at_T+{L-1}m_(open-stamp)"] = float(np.mean(np.isclose(x.values[ok], y_open[ok], rtol=0, atol=1e-8)))
    ok2 = ~np.isnan(y_close)
    ident[f"{name}_close_eq_1m_close_at_T-1m_(close-stamp)"] = float(np.mean(np.isclose(x.values[ok2], y_close[ok2], rtol=0, atol=1e-8)))
# 30m vs hourly directly
j = h["close"].to_frame("h").join(m30["close"].shift(freq="-30min").rename("m30_next"), how="inner")
ident["hourly_close_eq_30m_close_of_second_half"] = float(np.isclose(j["h"], j["m30_next"]).mean())

# identity 2: metrics embedded c (Binance USD-M futures endpoint) vs 1m close, several offsets.
res = []
for off in range(-10, 11):
    y = c1.reindex(mt.index + pd.Timedelta(minutes=off))
    ok = y.notna()
    exact = float(np.isclose(mt["c"].values[ok.values], y.values[ok.values], rtol=0, atol=1e-8).mean())
    bp = 1e4 * np.log(y.values[ok.values] / mt["c"].values[ok.values])
    res.append(dict(offset_min=off, n=int(ok.sum()), exact_match=exact, med_abs_bp=float(np.median(np.abs(bp))),
                    mean_bp=float(np.mean(bp))))
res = pd.DataFrame(res)
res.to_csv("tables/00_metrics_c_vs_1m_offsets.csv", index=False)
print(res.to_string())
ident["best_offset_metrics_vs_1m"] = res.loc[res.med_abs_bp.idxmin()].to_dict()

# identity 3: is the "1m perp" series spot?  Spot-perp basis should co-move with funding sign. Compute the 1m-vs-metrics
# log gap at the best offset per 8h funding window, and correlate with funding (TRAIN, 2020-09..2023-03).
best = int(ident["best_offset_metrics_vs_1m"]["offset_min"])
y = c1.reindex(mt.index + pd.Timedelta(minutes=best))
gap = pd.Series(1e4 * np.log(mt["c"].values / y.values), index=mt.index).dropna()   # futures(metrics) minus file, bp
g8 = gap.resample("8h").mean()
jj = pd.concat([g8.rename("gap_bp"), fu["funding"].rename("funding")], axis=1).dropna()
ident["corr_gap_vs_funding_8h"] = float(jj.corr().iloc[0, 1])
ident["gap_bp_by_year"] = gap.groupby(gap.index.year).agg(["mean", "median", "std", "count"]).round(3).to_dict("index")
print(json.dumps(ident, indent=1, default=str))

# identity 4: listing date - first date the metrics/funding files exist vs price files.
out["identity"] = ident

# ---- open-stamp check on the 1m file: every complete day 00:00..23:59?
days = c1.groupby(c1.index.floor("D"))
fl = pd.DataFrame({"first": days.apply(lambda s: s.index.min().strftime("%H:%M")),
                   "last": days.apply(lambda s: s.index.max().strftime("%H:%M")), "n": days.size()})
full = fl[fl.n == 1440]
out["1m_complete_days"] = int(len(full))
out["1m_complete_days_0000_2359"] = int(((full["first"] == "00:00") & (full["last"] == "23:59")).sum())
out["1m_days_total"] = int(len(fl))
# funding stamp hours
out["funding_hours"] = fu.index.hour.value_counts().sort_index().to_dict()
out["funding_minutes_nonzero"] = int((fu.index.minute != 0).sum())
# metrics sampling cadence
st = mt.index.to_series().diff().dropna()
out["metrics_step_counts"] = {str(k): int(v) for k, v in st.value_counts().head(6).items()}

# ---- plot: gap futures-minus-file (bp) daily median, with funding
fig, ax = plt.subplots(2, 1, figsize=(10, 5.5), sharex=True)
ax[0].plot(gap.resample("D").median(), color=PAL[0], lw=0.8)
ax[0].axhline(0, color=GRAY, lw=0.6); ax[0].set_ylabel("bp"); ax[0].set_title("metrics.c (USD-M futures) minus 1m-file close, daily median (TRAIN)")
ax[1].plot(fu["funding"].resample("D").mean() * 1e4, color=PAL[5], lw=0.8); ax[1].set_ylabel("funding, bp / 8h")
ax[1].axhline(0, color=GRAY, lw=0.6); ax[1].set_title("funding rate, daily mean (TRAIN)")
save(fig, "00_identity_gap")
json.dump(out, open("tables/00_datacard_checks.json", "w"), indent=1, default=str)
