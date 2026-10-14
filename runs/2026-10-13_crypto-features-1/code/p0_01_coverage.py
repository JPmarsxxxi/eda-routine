import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from panel import *
P, NS, QV, SRC = prim("phase0_01")
cnt = {}
for nm in SLICES:
    m = in_slice(P.index, nm)
    cnt[nm] = P[m].notna().sum()
print("hourly primary rows by coin x slice (TRAIN only)"); print(pd.DataFrame(cnt).T.to_string())
print("\nmedian coins available per hour:", {nm: int(P[in_slice(P.index,nm)].notna().sum(axis=1).median()) for nm in SLICES})
print("\nhours with >=6 coins:", {nm: int((P[in_slice(P.index,nm)].notna().sum(axis=1)>=6).sum()) for nm in SLICES})
print("\nnew_source True rows by coin (TRAIN):"); print(NS.sum().to_string())
