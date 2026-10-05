# Cell 00b - declare EXPLORE/CONFIRM from coverage counts only (no returns, no values beyond non-null counts).
from common import *

frames = {
    "spot_hourly": (load(PERP_HOURLY, "cell_00b", use=["close"]), ["close"]),
    "spot_30m": (load(PERP_30M, "cell_00b", use=["close"]), ["close"]),
    "dvol": (load(DVOL, "cell_00b", use=["close"]), ["close"]),
    "hspread": (load(HSPREAD, "cell_00b", use=["half_bp"]), ["half_bp"]),
    "funding": (load(FUNDING, "cell_00b", use=["funding"]), ["funding"]),
    "metrics": (load(METRICS, "cell_00b", use=["c", "sum_open_interest", "count_long_short_ratio",
                                                 "sum_taker_long_short_vol_ratio"]),
                ["c", "sum_open_interest"]),
}
# candidate boundaries, compared on usable-row counts only
cands = ["2021-06-30 23:59:59", "2021-12-31 23:59:59", "2022-06-30 23:59:59"]
rows = []
for b in cands:
    b = pd.Timestamp(b)
    for k, (df, cols) in frames.items():
        use = df[cols].notna().all(axis=1)
        e = (df.index <= b); c = (df.index > b)
        rows.append(dict(boundary=str(b.date()), file=k, explore_usable=int((use & e).sum()),
                         confirm_usable=int((use & c).sum())))
cen = pd.DataFrame(rows)
cen["confirm_share"] = (cen.confirm_usable / (cen.explore_usable + cen.confirm_usable)).round(3)
cen.to_csv("tables/00b_split_census.csv", index=False)
print(cen.to_string())

# declared split (chosen in SPLITS.md from the census above): EXPLORE <= 2021-12-31, CONFIRM 2022-01-01..2023-03-19
for k, (df, cols) in frames.items():
    d = df.reset_index().rename(columns={df.index.name: "_ts"})
    tab = G.declare_split(RUN, {"EXPLORE": (d["_ts"] <= EXPLORE_HI), "CONFIRM": (d["_ts"] >= CONFIRM_LO)},
                          d, cols, time_col="_ts")
    tab.insert(0, "file", k)
    print(tab.to_string(index=False))
