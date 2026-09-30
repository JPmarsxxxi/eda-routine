import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from guarded_load import spot, load, COINS
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
rows = []
for c in COINS:
    d = spot(c, "p0_07", "EXPLORE", columns=["open", "high", "low", "close"]).set_index("t")
    on_hour = bool((d.index == d.index.floor("h")).all()); uniq = d.index.is_unique
    prev = d.close.shift(1); consec = (d.index.to_series().diff() == pd.Timedelta("1h")).values
    zg = (d.open[consec] == prev[consec]).mean()
    zg_y = (d.open[consec] == prev[consec]).groupby(d.index[consec].year).mean().round(2).to_dict()
    hl_ok = ((d.high >= d[["open", "close"]].max(axis=1) - 1e-12) & (d.low <= d[["open", "close"]].min(axis=1) + 1e-12)).mean()
    rows.append(dict(coin=c, on_hour=on_hour, unique=uniq, zero_gap_rate=round(zg, 3), zero_gap_by_year=zg_y, hl_consistent=hl_ok))
T = pd.DataFrame(rows).set_index("coin"); print(T.to_string())
b = spot("BTCUSD", "p0_07", "EXPLORE", columns=["close"]).set_index("t")["close"]
cb = load("spot/coinbase_BTCUSD.parquet", "p0_07", "EXPLORE", columns=["close"]).set_index("t")["close"]
idx = pd.date_range(b.index.min(), b.index.max(), freq="1h", tz="UTC")
rb = np.log(b.reindex(idx)).diff(); rc = np.log(cb.reindex(idx)).diff()
lag = {k: rb.corr(rc.shift(k)) for k in [-2, -1, 0, 1, 2]}
print("corr(binance r_t, coinbase r_{t-k})", {k: round(v, 3) for k, v in lag.items()})
T["btc_venue_lag0"] = lag[0]; T["btc_venue_lag+1"] = lag[1]; T["btc_venue_lag-1"] = lag[-1]
T.to_csv(os.path.join(TB, "p0_07_row.csv"))
ok = T.on_hour.all() and T.unique.all() and T.zero_gap_rate.between(.3, .6).all() and max(abs(lag[1]), abs(lag[-1])) < lag[0] / 3 and (T.hl_consistent == 1).all()
print("ROW CONFIRMED:", ok, "| zero-gap range", T.zero_gap_rate.min(), T.zero_gap_rate.max(), "| hl min", T.hl_consistent.min())
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.bar([str(k) for k in lag], list(lag.values()), color=[PAL[0] if k == 0 else GRAY for k in lag])
ax.set_xlabel("k: Coinbase bar shifted by k hours"); ax.set_ylabel("corr with Binance BTC r_t")
ax.set_title("Binance and Coinbase BTC bars align at lag 0 (corr %.2f): both OPEN-stamped (EXPLORE)" % lag[0])
save(fig, "00_row_alignment")
