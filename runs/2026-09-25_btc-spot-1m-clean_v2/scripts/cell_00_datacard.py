# Cell 00 - data card checks (structure only; no distributional stats on VAL)
import pandas as pd, numpy as np, json
P = r"C:\Users\User\eda-routine\data\btcusdt_spot_1m_clean\btcusdt_spot_1m_clean.parquet"
df = pd.read_parquet(P)
TRAIN_END = pd.Timestamp("2023-03-19 23:59", tz="UTC"); VAL_START = pd.Timestamp("2023-03-25", tz="UTC"); VAL_END = pd.Timestamp("2023-11-30 23:59", tz="UTC")
out = {}
out["rows"] = len(df); out["min"] = str(df.index.min()); out["max"] = str(df.index.max())
out["max_le_VAL_END"] = bool(df.index.max() <= VAL_END)
out["tz"] = str(df.index.tz)
out["train_rows"] = int((df.index <= TRAIN_END).sum())
out["embargo_rows"] = int(((df.index > TRAIN_END) & (df.index < VAL_START)).sum())
out["val_rows"] = int(((df.index >= VAL_START) & (df.index <= VAL_END)).sum())
# open/close stamping: first/last minute of each full calendar month and day
m = df.groupby(df.index.to_period("M").astype(str)).apply(lambda g: (g.index.min().strftime("%d %H:%M"), g.index.max().strftime("%d %H:%M"), len(g)))
out["months_first_is_01_0000"] = int(sum(v[0] == "01 00:00" for v in m.values))
out["months_last_is_2359"] = int(sum(v[1].endswith("23:59") for v in m.values))
out["n_months"] = len(m)
d = df.index.floor("D"); first_min = pd.Series(df.index.hour * 60 + df.index.minute, index=df.index).groupby(d).agg(["min", "max", "size"])
full = first_min[first_min["size"] == 1440]
out["full_days"] = len(full); out["full_days_start_0000_end_2359"] = int(((full["min"] == 0) & (full["max"] == 1439)).sum())
# continuity: open[t] vs close[t-1] on gap_min==1 (holds under either stamping; reported as structural sanity)
g1 = df["gap_min"] == 1
diff_bp = ((df["open"] / df["close"].shift(1) - 1) * 1e4)[g1 & (df.index <= TRAIN_END)]
out["train_open_eq_prevclose_share"] = float((diff_bp.abs() < 1e-9).mean())
out["train_abs_open_prevclose_bp_p99"] = float(diff_bp.abs().quantile(0.99))
out["columns"] = list(df.columns)
out["buy_plus_sell_eq_vol"] = bool(np.allclose(df.buy_vol + df.sell_vol, df.vol))
print(json.dumps(out, indent=1))
json.dump(out, open("tables/00_datacard_checks.json", "w"), indent=1)
