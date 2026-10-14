"""supplementary (NOT a cell): incremental IC of f008 at h1 after partialling out dense partners (f001, b_rev24), to correct the registry number
(cell 34's two most-correlated partners f006/f007 exist only at 23:00, so its residual used 969 rows)."""
import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code"); sys.path.insert(0, r"C:\Users\User\eda-routine")
from fx import *
import importlib, json
B = Base("supp_f008"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
PR = perp_hourly("supp_f008", "premium"); L = make_long(B, PR["close"])
f008 = unstack_feature(importlib.import_module("features.f008").compute(L), ix); f001 = unstack_feature(importlib.import_module("features.f001").compute(L), ix)
b24 = -(lr - lr.shift(24)); b1 = -(lr - lr.shift(1))
out = {}
for nm, parts in (("f001+b_rev24", [f001[tr], b24[tr]]), ("b_rev1+f001", [b1[tr], f001[tr]])):
    r = residual_rank(f008[tr], parts); ic = xs_ic(r, B.R[1][tr]); m = nw(ic, 6); out[nm] = (m["mean"], m["t"]); print(nm, round(m["mean"], 4), round(m["t"], 2), fmt_rep(slice_report(ic, 6)))
json.dump(out, open("work/supp_f008_inc.json", "w"))
