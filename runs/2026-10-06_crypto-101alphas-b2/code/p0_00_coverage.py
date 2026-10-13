"""p0_00: coverage counts per quarter (NO returns computed) -> declare EXPLORE / C1..C3 / VAL."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd, numpy as np
import common as C

rows = []
for coin in C.COINS:
    p = C.load(f"primary/validated_{coin}.parquet", "p0_00")
    p["day"] = p["t"].dt.floor("D")
    n = p.groupby("day")["t"].count()
    full = n[n == 24]
    s = pd.Series(1, index=full.index.tz_convert("UTC").date)
    rows.append(s.rename(coin))
cov = pd.concat(rows, axis=1).fillna(0)
cov.index = pd.to_datetime(cov.index)
train = cov[cov.index <= "2023-03-19"]
q = train.resample("QE").sum()
q["coin_days"] = q.sum(axis=1); q["coins_live"] = (q[C.COINS] > 0).sum(axis=1)
q.to_csv(os.path.join(C.RUN, "tables", "p0_00_coin_days_by_quarter.csv"))
daily = train.sum(axis=1)
cum = daily.cumsum() / daily.sum()
print(q[["coin_days", "coins_live"]].to_string())
for f in (0.25, 0.5, 0.75):
    print(f, cum[cum >= f].index[0].date())
print("total coin-days TRAIN", int(daily.sum()), "first", daily[daily > 0].index[0].date())
