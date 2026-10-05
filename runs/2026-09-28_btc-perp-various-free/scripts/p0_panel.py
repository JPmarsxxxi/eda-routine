# Phase 0 panel builder: EXPLORE slice only (hi = 2021-12-31 23:59). Hourly grid, open-stamped: a row stamped H describes
# the hour [H, H+1h) and is knowable at H+1h. Also a 1m-return frame for microstructure items.
import sys
from common import *

def build(slice_name, lo, hi, cell):
    # --- spot 1m (EXPLORE only; this file has no VAL at all)
    m1 = load(PERP_1M, cell, use=["close", "vol", "quote", "n", "buy_vol", "sell_vol"], lo=lo, hi=hi)
    m1 = m1[~m1.index.duplicated()]
    lc = np.log(m1["close"])
    step = m1.index.to_series().diff()
    r1 = lc.diff().where(step == pd.Timedelta("1min"))          # true 1-minute returns only
    H = m1.index.floor("h")
    g = pd.DataFrame({"r1": r1, "r1sq": r1 ** 2, "vol": m1["vol"], "quote": m1["quote"], "n": m1["n"],
                      "buy": m1["buy_vol"], "sell": m1["sell_vol"]}).groupby(H)
    spot_h = pd.DataFrame({"rv_1m": np.sqrt(g["r1sq"].sum(min_count=30)), "n_min": g["r1"].count(),
                           "quote_1m": g["quote"].sum(), "ntrades": g["n"].sum(),
                           "buy_share": g["buy"].sum() / (g["buy"].sum() + g["sell"].sum())})
    # --- spot hourly close from the 30m file (close of the second half-hour bar), return on consecutive hours only
    m30 = load(PERP_30M, cell, use=["close", "quote_volume"], lo=lo, hi=hi)
    c30 = m30["close"]
    hc = c30[c30.index.minute == 30]; hc.index = hc.index.floor("h")
    qv = m30["quote_volume"].groupby(m30.index.floor("h")).sum(min_count=2)
    grid = pd.date_range(max(lo, c30.index.min().floor("h")), min(hi, c30.index.max()).floor("h"), freq="h")
    P = pd.DataFrame(index=grid)
    P["close"] = hc.reindex(grid)
    P["r"] = np.log(P["close"]).diff()                           # NaN if either hour missing (gaps left missing)
    P["qvol"] = qv.reindex(grid)
    P = P.join(spot_h, how="left")
    # --- perp metrics: last snapshot in the hour + basis vs spot (perp c of 5m bar vs spot 1m close at +4m)
    mt = load(METRICS, cell, use=["c", "sum_open_interest", "sum_open_interest_value", "count_toptrader_long_short_ratio",
                                   "sum_toptrader_long_short_ratio", "count_long_short_ratio",
                                   "sum_taker_long_short_vol_ratio", "v", "n", "tbv"], lo=lo, hi=hi)
    spot_at = m1["close"].reindex(mt.index + pd.Timedelta(minutes=4)).values
    mt["basis_bp"] = 1e4 * np.log(mt["c"].values / spot_at)
    gm = mt.groupby(mt.index.floor("h"))
    M = pd.DataFrame({"oi": gm["sum_open_interest"].last(), "oi_val": gm["sum_open_interest_value"].last(),
                      "ls_top_cnt": gm["count_toptrader_long_short_ratio"].last(),
                      "ls_top_sum": gm["sum_toptrader_long_short_ratio"].last(),
                      "ls_all": gm["count_long_short_ratio"].last(),
                      "taker_ratio": gm["sum_taker_long_short_vol_ratio"].mean(),
                      "perp_vol": gm["v"].sum(), "perp_n": gm["n"].sum(),
                      "perp_taker_buy_share": gm["tbv"].sum() / gm["v"].sum(),
                      "basis_bp": gm["basis_bp"].mean(), "basis_n": gm["basis_bp"].count(),
                      "perp_c": gm["c"].last()})
    P = P.join(M, how="left")
    # --- DVOL hourly (open-stamped, close of hour)
    dv = load(DVOL, cell, use=["close"], lo=lo, hi=hi)["close"]
    P["dvol"] = dv.reindex(P.index)
    # --- half-spread
    hs = load(HSPREAD, cell, use=["half_bp"], lo=lo, hi=hi)["half_bp"]
    P["half_bp"] = hs.reindex(P.index)
    # --- funding (8h, hour-rounded). Kept only on settlement hours; never forward-filled in the panel.
    fu = load(FUNDING, cell, use=["funding"], lo=lo, hi=hi)["funding"]
    fu.index = fu.index.round("h")
    P["funding"] = fu.reindex(P.index)
    # derived changes (consecutive hours only by construction of the grid)
    for col in ["oi", "oi_val", "ls_top_cnt", "ls_top_sum", "ls_all", "dvol", "qvol", "half_bp"]:
        P[f"d_{col}"] = np.log(P[col]).diff()
    P["d_basis"] = P["basis_bp"].diff()
    P["log_taker"] = np.log(P["taker_ratio"])
    P.to_parquet(f"tables/p0_panel_{slice_name}.parquet")
    r1.to_frame("r1").to_parquet(f"tables/p0_r1_{slice_name}.parquet")
    fu.to_frame("funding").to_parquet(f"tables/p0_funding_{slice_name}.parquet")
    print(P.describe().T.to_string())
    return P

if __name__ == "__main__":
    build("EXPLORE", TRAIN_LO, EXPLORE_HI, "p0_panel")
