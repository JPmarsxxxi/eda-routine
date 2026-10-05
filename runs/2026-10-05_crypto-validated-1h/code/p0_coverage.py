"""Coverage counts only (no prices, no returns) -> used to declare SPLITS.md before any forward return."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
from guard import load
COINS = ["BTCUSD","ETHUSD","BNBUSD","SOLUSD","XRPUSD","DOGEUSD","ADAUSD","LTCUSD","BCHUSD","DOTUSD"]
rows = {}
ns = {}
for c in COINS:
    d = load(f"primary/validated_{c}.parquet", "p0_coverage")
    d = d[d._t < pd.Timestamp("2023-03-20", tz="UTC")]  # TRAIN only for counting
    rows[c] = d.groupby(d._t.dt.to_period("Q").astype(str)).size()
    ns[c] = int(d.new_source.sum())
cov = pd.DataFrame(rows).fillna(0).astype(int)
cov.to_csv("tables/00_coverage_primary_by_quarter.csv")
print(cov.to_string())
print("new_source=True rows in TRAIN:", ns)
fam = {}
for f in ["perp/funding_BTCUSD.parquet","perp/funding_SOLUSD.parquet","perp/perp_premium_BTCUSD.parquet","perp/perp_premium_DOTUSD.parquet",
          "perp/metrics_ETHUSD.parquet","deriv/deribit_dvol_BTC.parquet","spot/coinbase_BTCUSD.parquet","spot/upbit_BTCKRW.parquet",
          "spot/coinbase_USDTUSD.parquet","attention/fear_greed.parquet","macro/yahoo_GSPC.parquet","deriv/deribit_funding_BTC.parquet"]:
    d = load(f, "p0_coverage"); d = d[d._t < pd.Timestamp("2023-03-20", tz="UTC")]
    fam[f] = d.groupby(d._t.dt.year).size()
print(pd.DataFrame(fam).fillna(0).astype(int).T.to_string())
