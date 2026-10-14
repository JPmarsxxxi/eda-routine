"""confirm.py - run a frozen candidate unchanged on every CONFIRM fold, or on VAL. Uses features/<fid>.py exactly as registered."""
import sys, importlib, json, hashlib, functools
sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code"); sys.path.insert(0, r"C:\Users\User\eda-routine")
from fx import *
import panel
import kit_confirm as kc

PRIM = {"f009": (24, "h"), "f001": (6, "h"), "f002": (6, "h"), "f003": (24, "h"), "f004": (24, "h"), "f005": (24, "h"), "f006": (6, "d"), "f007": (24, "d"), "f008": (1, "h")}
CAND = {"F1": "f001", "F2": "f002", "F3": "f003", "F4": "f004", "F5": "f005", "F6": "f006", "F7": "f007", "F8": "f004", "F9": "f008", "F10": "f009"}
CAND_H = {"F8": 1}   # candidates whose primary horizon differs from PRIM[feature]

FOLD_N = {"C1": 4242, "C2": 4046, "C3": 6023}
VAL_LO, VAL_HI = pd.Timestamp("2023-03-25"), pd.Timestamp("2023-12-01")


def _resolve(x):
    if x[0] == 'F':
        return CAND[x], x[1:], x
    return x, x[-1], 'F' + x[-1]


def _h(x):
    feat, n, cand = _resolve(x)
    return CAND_H.get(cand, PRIM[feat][0]), PRIM[feat][1]


def fold_se(fid):
    h, mode = _h(fid)
    fid = _resolve(fid)[0]
    f = {"f002": 10 / 24}.get(fid, 1.0)
    out = []
    for nm in ("C1", "C2", "C3"):
        n = FOLD_N[nm] * f / (24 if mode == "d" else 1)
        out.append(NOISE[f"{mode}_{h}"]["c"] / np.sqrt(n))
    return out


def val_se(fid):
    h, mode = _h(fid)
    fid = _resolve(fid)[0]
    f = {"f002": 10 / 24}.get(fid, 1.0)
    n = 6400 * f / (24 if mode == "d" else 1)   # ~250 days with 6+ coins
    return NOISE[f"{mode}_{h}"]["c"] / np.sqrt(n)


def branch(m):
    if m["mean"] >= 0.02 and m["t"] >= 1.96:
        return "supported"
    if m["mean"] < 0 and m["t"] <= -1.65:
        return "refuted"
    return "inconclusive"


def build(cell, fid, val=False):
    if val:
        panel.GRID = pd.date_range("2018-01-01", "2023-11-30 23:00", freq="h")
        G.load = functools.partial(G.load, train_lo=pd.Timestamp("2022-12-01"), train_hi=pd.Timestamp("2023-11-30 23:59:59"), allow_empty=True)
    B = Base(cell)
    PR = perp_hourly(cell, "premium") if fid in ("f004", "f009") else None
    FU = funding(cell)[0] if fid == "f009" else None
    S = B.S
    parts = []
    for c in COINS:
        d = pd.DataFrame({"t": S["close"].index, "coin": c})
        for k in ("open", "high", "low", "close", "vol", "quote_vol", "n", "buy_vol"):
            d[k] = S[k][c].values
        d["prem_close"] = PR["close"][c].values if PR is not None else np.nan
        d["funding"] = FU[c].values if FU is not None else np.nan
        parts.append(d)
    L = pd.concat(parts, ignore_index=True).dropna(subset=["close"])
    if not val:
        L = L[train_mask(pd.DatetimeIndex(L["t"]))]
    L = L.reset_index(drop=True)
    mod = importlib.import_module(f"features.{fid}")
    X = unstack_feature(mod.compute(L), S["close"].index)
    return B, X


def pooled_pearson(X, R, mask):
    rk = X.rank(axis=1)
    z = rk.sub(rk.mean(axis=1), axis=0).div(rk.std(axis=1), axis=0)
    j = pd.concat([z[mask].stack(), R[mask].stack()], axis=1).dropna()
    return float(j.iloc[:, 0].corr(j.iloc[:, 1]))


def run_confirm(nn, fid):
    h0, mode = _h(fid)
    B, X = build(f"cell_{nn:02d}", _resolve(fid)[0])
    out = {"fid": fid, "primary_h": h0, "mode": mode, "folds": {}, "by_h": {}}
    for h in HORIZONS:
        Fs, Rs = sample(X, mode), sample(B.R[h], mode)
        ic = xs_ic(Fs, Rs)
        L = hl(h, mode)
        out["by_h"][h] = {nm: nw(ic[in_slice(ic.index, nm)], L) for nm in ("C1", "C2", "C3")}
        if h == h0:
            for nm in ("C1", "C2", "C3"):
                m = out["by_h"][h][nm]; out["folds"][nm] = dict(m, branch=branch(m))
            out["raw_pearson"] = {nm: pooled_pearson(Fs, Rs, in_slice(Fs.index, nm)) for nm in ("C1", "C2", "C3")}
            out["mkt_corr"] = mkt_corr(X, B, h, mode)
    br = [out["folds"][n]["branch"] for n in ("C1", "C2", "C3")]
    out["shown"] = br.count("supported") >= 2 and br.count("refuted") == 0
    w = kc.confirm_weights(fold_se(fid))
    out["weights"] = w
    out["weight_applied"] = w["applied_yes"] if out["shown"] else w["applied_no"]
    json.dump(out, open(os.path.join(RUN, "work", f"confirm_{fid}.json"), "w"), indent=1, default=float)
    print(f"{fid} primary h{h0} ({mode}) folds:")
    for nm in ("C1", "C2", "C3"):
        f = out["folds"][nm]; print(f"  {nm}: IC {f['mean']:+.4f} t {f['t']:+.2f} n {f['n']} -> {f['branch']}")
    print("other horizons:", {h: {nm: round(v['mean'], 4) for nm, v in d.items()} for h, d in out["by_h"].items()})
    print("raw pooled Pearson (rank-z vs return):", {k: round(v, 4) for k, v in out["raw_pearson"].items()}, " market corr:", round(out["mkt_corr"], 3))
    print("CONFIRM-SHOWN:", out["shown"], " P_H %.3f P_0 %.4f w_yes %.1f w_no %.2f applied %.4f" % (w["P_H"], w["P_0"], w["w_yes"], w["w_no"], out["weight_applied"]), "fold power:", [round(p, 2) for p in w["fold_power"]])
    return out


def write_confirm_result(nn, fid, extra=""):
    o = json.load(open(os.path.join(RUN, "work", f"confirm_{fid}.json")))
    folds = ", ".join(f"{n}={o['folds'][n]['branch']}" for n in ("C1", "C2", "C3"))
    h0 = o["primary_h"]
    body = f"# cell {nn:02d} result - confirm of candidates/F{_resolve(fid)[1]}.md ({_resolve(fid)[0]}), frozen spec run unchanged on C1, C2, C3 (primary h{h0}, {o['mode']} sampling; work/confirm_{fid}.json)\n"
    for n in ("C1", "C2", "C3"):
        f = o["folds"][n]
        body += f"{n}: mean rank IC {f['mean']:+.4f}, NW t {f['t']:+.2f}, n {f['n']} -> {f['branch']}\n"
    body += "Other horizons (IC by fold, reported only): " + "; ".join(f"h{h}: " + " ".join(f"{n} {v['mean']:+.4f}" for n, v in d.items()) for h, d in o["by_h"].items()) + "\n"
    body += f"Raw (pooled panel Pearson of the feature rank-z with the next-{h0}h return): " + ", ".join(f"{k} {v:+.4f}" for k, v in o["raw_pearson"].items()) + f". Market correlation (cross-coin mean standardised feature vs EW market forward return): {o['mkt_corr']:+.3f}.\n"
    w = o["weights"]
    body += f"CONFIRM-SHOWN = {o['shown']}. Fold powers at min_useful {[round(p, 2) for p in w['fold_power']]}: P(>=2 of 3 supported | effect) {w['P_H']:.3f}, under the null {w['P_0']:.4f} -> w_yes {w['w_yes']:.1f} (capped {w['applied_yes']:.1f}), w_no {w['w_no']:.2f}; weight_applied {o['weight_applied']:.4f}.\n"
    body += extra
    kit.result(nn, o["weight_applied"], folds=folds, body=body)
    kit.attempt(nn, kc.hyp_of(f"F{_resolve(fid)[1]}"), f"confirm {fid} on C1-C3 (frozen)", f"{folds}; shown={o['shown']}")


def begin_confirm(nn, fid):
    n = _resolve(fid)[1]
    h0, mode = _h(fid)
    hyp = kc.hyp_of(f"F{n}")
    w = kc.confirm_weights(fold_se(fid))
    rule = f"""# cell {nn:02d} rule - confirm of candidates/F{n}.md ({fid}), frozen before this cell, run unchanged on C1, C2 and C3
The frozen spec is candidates/F{n}.md (not edited after its freeze; this cell's code is code/confirm.py importing features/{fid}.py). Primary horizon h = {h0} ({mode} sampling). Slice CONFIRM = each of C1, C2, C3 separately.
pass_rule (copied from the candidate file, per fold): {kc.pass_rule_of(f'F{n}')}
min_useful: 0.02.
Evidence weights (cap 10x): outcome CONFIRM-SHOWN (>= 2 of 3 folds supported, none refuted). Per-fold power at delta = 0.02 from the measured noise (work/noise.json: se = c/sqrt(N), fold powers {[round(p, 2) for p in w['fold_power']]});
P(CONFIRM-SHOWN | effect at min_useful in every fold) = {w['P_H']:.3f}; under the null each fold is 'supported' with probability 0.025, P(CONFIRM-SHOWN | null) = {w['P_0']:.4f};
w_yes = {w['w_yes']:.1f} -> capped {w['applied_yes']:.1f}; w_no = {w['w_no']:.2f} (floor 0.1). weight_applied = w_yes if CONFIRM-SHOWN else w_no.
"""
    ann = f"""### Cell {nn:02d} - CONFIRM: candidate F{n} ({fid}) on C1, C2, C3
**Claim:** the frozen spec holds fold by fold (decomposition floor Q8 stability, Q10 replication). **Why it matters:** CONFIRM-SHOWN is required before VAL. The spec, threshold and universe are not changed by what this shows.
**Decision rule:** pass_rule above. **Decisions needed:** none.
"""
    kit.begin(nn, hyp, "CONFIRM", "confirm", "none", "none", rule, ann, candidate=f"F{n}")


def run_val(nn, fid):
    h0, mode = _h(fid)
    B, X = build(f"cell_{nn:02d}", _resolve(fid)[0], val=True)
    out = {"fid": fid, "primary_h": h0, "mode": mode, "by_h": {}}
    Fs0 = sample(X, mode)
    vm = lambda idx: (idx >= VAL_LO) & (idx < VAL_HI)
    for h in HORIZONS:
        Rs = sample(B.R[h], mode)
        ic = xs_ic(Fs0, Rs)
        L = hl(h, mode)
        out["by_h"][h] = nw(ic[vm(ic.index)], L)
        if h == h0:
            m = out["by_h"][h]; out["val"] = dict(m, branch=branch(m))
            out["raw_pearson"] = pooled_pearson(Fs0, Rs, vm(Fs0.index))
            z = X.rank(axis=1); z = z.sub(z.mean(axis=1), axis=0).div(z.std(axis=1), axis=0)
            fz = z.mean(axis=1)    # cross-coin mean of rank-z is ~0 by construction; use trailing-30d z of the raw feature instead
            w = 30 if mode == "d" else 720
            Xs = sample(X, mode); zz = (Xs - Xs.rolling(w, min_periods=w // 2).mean()) / Xs.rolling(w, min_periods=w // 2).std()
            xx = pd.concat([zz.mean(axis=1), sample(B.mkt[h], mode)], axis=1).dropna(); xx = xx[vm(xx.index)]
            out["mkt_corr"] = float(xx.iloc[:, 0].corr(xx.iloc[:, 1])) if len(xx) > 30 else float("nan")
            monthly = ic[vm(ic.index)].groupby(ic[vm(ic.index)].index.to_period("M")).mean()
            out["monthly"] = {str(k): float(v) for k, v in monthly.items()}
            out["n_coins_mean"] = float(X[vm(X.index)].notna().sum(axis=1).mean())
    se = val_se(fid)
    pw = kit.power(se, 0.02, 1.96)
    out["se"] = se; out["power"] = pw
    ok = out["val"]["branch"] == "supported"
    w = pw["w_yes"] if ok else pw["w_no"]
    out["weight_applied"], _ = kit.capped(w, "val")
    json.dump(out, open(os.path.join(RUN, "work", f"val_{fid}.json"), "w"), indent=1, default=float)
    v = out["val"]
    print(f"{fid} VAL primary h{h0}: IC {v['mean']:+.4f} t {v['t']:+.2f} n {v['n']} -> {v['branch']}; weight {out['weight_applied']:.3f}")
    print("other horizons:", {h: round(m["mean"], 4) for h, m in out["by_h"].items()}, " raw pearson", round(out["raw_pearson"], 4), " mkt corr", round(out["mkt_corr"], 3), " coins/hour", round(out["n_coins_mean"], 1))
    print("monthly IC:", {k: round(v, 4) for k, v in out["monthly"].items()})
    return out


def begin_val(nn, fid):
    n = _resolve(fid)[1]
    h0, mode = _h(fid)
    hyp = kc.hyp_of(f"F{n}")
    p = os.path.join(RUN, "candidates", f"F{n}.md")
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
    se = val_se(fid); pw = kit.power(se, 0.02, 1.96)
    rule = f"""# cell {nn:02d} rule - VAL check of candidates/F{n}.md ({fid}); the spec is frozen, its sha256 is in the header
VAL_NOTE (TARGET.md, quoted): "VAL is weak evidence. (1) BTC VAL was crossed twice by earlier work. (2) VAL was opened once more, on all 10 coins, for the crash-day rebound topic, and once by runs/2026-10-05_crypto-101alphas (#101): SOFT-clean. (3) VAL may be a DIFFERENT REGIME from TRAIN (2023 was calm; from 2023-04 BTC's 1-minute trade counts fell ~8x)."
The cell runs features/{fid}.py unchanged on 2023-03-25 .. 2023-11-30 (code/confirm.py run_val); nothing is tuned on what it shows. History before 2023-03-25 (from 2022-12-01) is loaded only to fill trailing windows.
pass_rule (copied verbatim from candidates/F{n}.md): {kc.pass_rule_of(f'F{n}')}
min_useful: 0.02. One VAL check per frozen spec.
Evidence weights (cap 10x): VAL-sample se = c/sqrt(N) = {se:.4f} (c from work/noise.json, N ~ 6,400 signal hours x coin share); power at delta 0.02 and tcrit 1.96 = {pw['power']:.2f}, alpha(one-sided) {pw['alpha']:.4f};
w_yes = {pw['w_yes']:.1f} -> capped 10; w_no = {pw['w_no']:.2f}. weight_applied = w_yes if branch supported else w_no.
"""
    ann = f"""### Cell {nn:02d} - VAL: candidate F{n} ({fid})
**Claim:** the frozen spec's primary-horizon IC holds on VAL (2023-03-25..2023-11-30). **Why it matters:** the only check of this spec on data it was not searched on; a pass is handed to the user in TEST_REQUESTS.md, never called out-of-sample proof.
**Decision rule:** pass_rule above. **Decisions needed:** none.
"""
    kit.begin(nn, hyp, "VAL", "val", "none", "none", rule, ann, candidate=f"F{n}", sha=sha)


def write_val_result(nn, fid, extra=""):
    o = json.load(open(os.path.join(RUN, "work", f"val_{fid}.json")))
    v = o["val"]
    body = f"# cell {nn:02d} result - VAL of candidates/F{_resolve(fid)[1]}.md ({_resolve(fid)[0]}), primary h{o['primary_h']} ({o['mode']} sampling; work/val_{fid}.json)\n"
    body += f"VAL 2023-03-25..2023-11-30: mean rank IC {v['mean']:+.4f}, NW t {v['t']:+.2f}, n {v['n']} -> {v['branch']} (rule: supported if IC >= +0.02 and t >= 1.96; refuted if IC < 0 and t <= -1.65).\n"
    body += "Other horizons (reported only): " + ", ".join(f"h{h} {m['mean']:+.4f} (t {m['t']:+.1f})" for h, m in o["by_h"].items()) + f". Raw pooled Pearson {o['raw_pearson']:+.4f}; market corr {o['mkt_corr']:+.3f}; coins per signal {o['n_coins_mean']:.1f}.\n"
    body += "Monthly mean IC: " + ", ".join(f"{k} {m:+.4f}" for k, m in o["monthly"].items()) + "\n"
    body += f"Power at delta 0.02: se {o['se']:.4f}, power {o['power']['power']:.2f}; weight_applied {o['weight_applied']:.4f}.\nVAL_NOTE applies: weak evidence, regime may differ (calm 2023; trade counts fell after 2023-04), earlier work opened VAL on this panel.\n"
    body += extra
    kit.result(nn, o["weight_applied"], branch=v["branch"], body=body)
    kit.attempt(nn, kc.hyp_of(f"F{_resolve(fid)[1]}"), f"VAL {fid} (frozen F{_resolve(fid)[1]})", f"IC {v['mean']:+.4f} t {v['t']:+.2f} -> {v['branch']}")
