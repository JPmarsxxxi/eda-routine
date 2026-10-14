"""fx.py - base panels, seed/feature builders and the sweep evaluator used by the cells."""
import sys
sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from panel import *
import kit
from scipy.stats import norm

NOISE = json.load(open(os.path.join(RUN, "work", "noise.json")))


class Base:
    def __init__(self, cell, need=("P", "S")):
        os.chdir(RUN)
        self.P, self.NS, self.QV, self.SRC = prim(cell)
        self.S = spot(cell)
        self.R = {h: fwd(self.P, self.NS, h) for h in HORIZONS}
        # same horizons scored against the BINANCE close (response-switch control); ignores new_source (Binance is one series)
        zero = self.NS * False
        self.RB = {h: fwd(self.S["close"].reindex(self.P.index), zero, h) for h in HORIZONS}
        self.D = daily(self.S)
        self.ret1 = back(self.P, self.NS, 1)
        self.mkt = {h: self.R[h].mean(axis=1) for h in HORIZONS}


def sgn(x):
    return np.sign(x)


# ----------------------------------------------------------------- H1 : Alpha#30 family
def a30_daily(Dd, k=3, a=5, b=20, scale=True):
    C = Dd["C"]
    s = sum(sgn(C.shift(i) - C.shift(i + 1)) for i in range(k))
    rk = s.rank(axis=1, pct=True)
    f = 1 - rk
    if scale:
        V = Dd["V"]
        f = f * (V.rolling(a).sum() / V.rolling(b).sum())
    return f


def a30_roll(S, k=3, a=5, b=20, scale=True, step=24):
    C = S["close"]
    s = sum(sgn(C.shift(step * i) - C.shift(step * (i + 1))) for i in range(k))
    rk = s.rank(axis=1, pct=True)
    f = 1 - rk
    if scale:
        V = S["vol"]
        wa, wb = step * a, step * b
        f = f * (V.rolling(wa, min_periods=int(.9 * wa)).sum() / V.rolling(wb, min_periods=int(.9 * wb)).sum())
    return f


# ----------------------------------------------------------------- H2 : Alpha#54 family
def a54_daily(Dd, power=5):
    O, H, L, C = Dd["O"], Dd["H"], Dd["L"], Dd["C"]
    rng = (H - L).where((H - L) > 0)
    return ((C - L) / rng) * (O / C) ** power


def a54_roll(S, power=5, w=24):
    O = S["open"].shift(w - 1); C = S["close"]
    H = S["high"].rolling(w, min_periods=int(.9 * w)).max(); L = S["low"].rolling(w, min_periods=int(.9 * w)).min()
    rng = (H - L).where((H - L) > 0)
    return ((C - L) / rng) * (O / C) ** power


# ----------------------------------------------------------------- evaluation
def hl(h, mode):
    return (h + 5) if mode == "h" else (h // 24 + 3)


def sweep(variants, B, hs=HORIZONS, mode_of=None, response="primary", extra_cols=None):
    """variants: {name: (F, mode)} ; returns DataFrame rows = variant x horizon with per-slice mean IC / t and TRAIN."""
    rows, ics = [], {}
    for name, (F, mode) in variants.items():
        for h in hs:
            Rm = sample((B.R if response == "primary" else B.RB)[h], mode)
            ic = xs_ic(sample(F, mode), Rm)
            rep = slice_report(ic, hl(h, mode))
            row = dict(variant=name, mode=mode, h=h)
            for nm in ("EXPLORE", "C1", "C2", "C3", "TRAIN"):
                row[f"{nm}_ic"] = rep[nm]["mean"]; row[f"{nm}_t"] = rep[nm]["t"]
            row["n_train"] = rep["TRAIN"]["n"]
            rows.append(row); ics[(name, h)] = ic
    return pd.DataFrame(rows), ics


def show(df, cols=("EXPLORE", "C1", "C2", "C3", "TRAIN")):
    d = df.copy()
    out = d[["variant", "mode", "h"]].copy()
    for nm in cols:
        out[nm] = [f"{a:+.4f}({b:+.1f})" for a, b in zip(d[f"{nm}_ic"], d[f"{nm}_t"])]
    return out.to_string(index=False)


def verdict(df, delta=0.02, direction=1.0, V=None):
    """pre-committed decision on the pooled-TRAIN rows of a sweep: best variant by direction*IC.
    Returns dict(branch, best, tcrit, power, w_yes, w_no, weight_applied)."""
    V = V or len(df)
    tc = kit.tcrit_for(V)
    d = df.copy()
    d["score"] = direction * d["TRAIN_ic"]
    best = d.sort_values("score", ascending=False).iloc[0]
    c_key = f"{best['mode']}_{int(best['h'])}"
    se = NOISE[c_key]["c"] / np.sqrt(best["n_train"])
    pw = kit.power(se, delta, tc)
    ok = (best["score"] >= delta) and (direction * best["TRAIN_t"] >= tc)
    # wrong-sign significance counts as 'no'
    w = pw["w_yes"] if ok else pw["w_no"]
    wc, cap = kit.capped(w, "search")
    return dict(branch="supported" if ok else "not-supported", best=f"{best['variant']} h={int(best['h'])} {best['mode']}",
                best_ic=float(best["TRAIN_ic"]), best_t=float(best["TRAIN_t"]), tcrit=tc, se=float(se), power=pw["power"],
                w_yes=pw["w_yes"], w_no=pw["w_no"], weight_applied=wc, capped=cap, V=V)


def mkt_corr(F, B, h, mode):
    """market exposure of a feature: corr (TRAIN) of the cross-coin MEAN of its trailing-30d z-score with the EW-market forward return"""
    Fs = sample(F, mode)
    w = 30 if mode == "d" else 720
    z = (Fs - Fs.rolling(w, min_periods=w // 2).mean()) / Fs.rolling(w, min_periods=w // 2).std()
    m = z.mean(axis=1)
    x = pd.concat([m, sample(B.mkt[h], mode)], axis=1).dropna()
    x = x[train_mask(x.index)]
    return float(x.iloc[:, 0].corr(x.iloc[:, 1]))


N_TRAIN = {"h": 28000, "d": 1170}


def rule_power(V, delta=0.02):
    """text of the pre-run power simulation: se = measured c / sqrt(N), one line per sampling mode x horizon."""
    tc = kit.tcrit_for(V)
    lines = [f"Power simulation (measured noise, work/noise.json; delta = min_useful {delta}; Sidak critical |t| = {tc:.2f} for V = {V} variants; cap 3x):"]
    for mode in ("h", "d"):
        for h in HORIZONS:
            se = NOISE[f"{mode}_{h}"]["c"] / np.sqrt(N_TRAIN[mode])
            pw = kit.power(se, delta, tc)
            lines.append(f"  sampling {mode} h={h}: se {se:.4f}, power {pw['power']:.2f}, alpha(one-sided) {pw['alpha']:.4f}, "
                         f"w_yes {pw['w_yes']:.1f} -> {min(pw['w_yes'], 3):.2f}, w_no {pw['w_no']:.2f} -> {max(pw['w_no'], 1/3):.2f}")
    return "\n".join(lines)


def make_long(B, PR_close=None):
    """long hourly frame of the carded columns (TRAIN rows only, as the guard returned them) for features/f*.py"""
    S = B.S
    parts = []
    for c in COINS:
        d = pd.DataFrame({"t": S["close"].index, "coin": c})
        for k in ("open", "high", "low", "close", "vol", "quote_vol", "n", "buy_vol"):
            d[k] = S[k][c].values
        d["prem_close"] = PR_close[c].values if PR_close is not None else np.nan
        parts.append(d)
    out = pd.concat(parts, ignore_index=True)
    out = out.dropna(subset=["close"])
    return out[train_mask(pd.DatetimeIndex(out["t"]))].reset_index(drop=True)


def unstack_feature(s, idx):
    """features/*.compute output (Series indexed (t, coin)) -> wide frame on the given hourly index, columns COINS"""
    w = s.unstack("coin").reindex(idx)
    return w.reindex(columns=COINS)
