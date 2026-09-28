"""Hurst estimators copied verbatim from s2a_memory.py (importable without re-running the sweep)."""
import numpy as np

def hurst_aggvar(x, ms=(1, 2, 4, 8, 16, 32, 64, 128, 256)):
    x = x.dropna().values
    v = []
    for m in ms:
        k = len(x) // m
        v.append(np.var(x[: k * m].reshape(k, m).sum(1)) / m ** 0)
    sl = np.polyfit(np.log(ms), np.log(v), 1)[0]
    return sl / 2  # var(sum over m) ~ m^{2H}

def hurst_rs(x, ns=(16, 32, 64, 128, 256, 512, 1024, 2048)):
    x = x.dropna().values
    rs = []
    for n in ns:
        k = len(x) // n
        y = x[: k * n].reshape(k, n)
        z = np.cumsum(y - y.mean(1, keepdims=True), 1)
        R = z.max(1) - z.min(1); S = y.std(1)
        rs.append(np.mean(R[S > 0] / S[S > 0]))
    return np.polyfit(np.log(ns), np.log(rs), 1)[0]

