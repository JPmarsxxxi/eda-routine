"""Phase 0 / SPLITS: declare EXPLORE + C1..C3 + VAL from COVERAGE COUNTS ONLY (row existence and new_source
flags; no price, no return is read into any statistic). Run before any forward return is measured."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import run_lib as L

win = (pd.Timestamp("2017-01-01", tz="UTC"), L.TRAIN_END + pd.Timedelta(days=1))   # TRAIN only
cov = {}
for c in L.COINS:
    p = L.load_primary(c, "SPLITS coverage counts only (t, new_source; price not used)", win)[["t", "new_source"]]
    day = p.t.dt.floor("D")
    g = pd.DataFrame({"n": p.groupby(day).size(), "ns": p.new_source.groupby(day).sum()})
    cov[c] = ((g.n == 24) & (g.ns == 0))          # day is a valid RESPONSE day (all 24 bars, no new_source)
C = pd.DataFrame(cov).asfreq("D").fillna(False).astype(bool)
C = C[C.index <= pd.Timestamp("2023-03-19", tz="UTC")]
n = C.sum(axis=1)
usable = n[n >= L.MIN_COINS]
print("usable days (>=5 coins with a valid response day):", len(usable), "coin-days:", int(usable.sum()))
cum = usable.cumsum() / usable.sum()
# equal coin-day quarters, 7-day embargo between slices
q = [cum[cum >= k / 4].index[0] for k in (1, 2, 3)]
cuts = [pd.Timestamp(x.date(), tz="UTC") for x in q]
emb = pd.Timedelta(days=7)
start = usable.index[0]
bounds = [("EXPLORE", start, cuts[0]), ("C1", cuts[0] + emb, cuts[1]), ("C2", cuts[1] + emb, cuts[2]),
          ("C3", cuts[2] + emb, pd.Timestamp("2023-03-20", tz="UTC"))]
rows = []
for name, a, b in bounds:
    u = usable[(usable.index >= a) & (usable.index < b)]
    rows.append((name, a.date(), b.date(), len(u), int(u.sum()), round(u.mean(), 2),
                 ",".join(sorted([c for c in C.columns if C.loc[(C.index >= a) & (C.index < b), c].any()]))))
tab = pd.DataFrame(rows, columns=["slice", "from", "to(excl)", "usable_days", "coin_days", "mean_coins", "coins_present"])
print(tab.to_string(index=False))
tab.to_csv(os.path.join(L.RUN, "code", "splits_table.csv"), index=False)
