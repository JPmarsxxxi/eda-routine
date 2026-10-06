"""Build and cache the daily panels used by every cell: Binance daily fields (signal inputs) and primary responses."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
import common as C

F = C.daily_fields("p0_build")
for k, v in F.items():
    v.index = pd.to_datetime(v.index); v.to_parquet(os.path.join(C.RUN, "tables", f"_daily_{k}.parquet"))
R = C.panel(C.daily_response, "p0_build")
R.index = pd.to_datetime(R.index); R.to_parquet(os.path.join(C.RUN, "tables", "_response.parquet"))
print({k: v.shape for k, v in F.items()}, R.shape, R.index.min(), R.index.max())
