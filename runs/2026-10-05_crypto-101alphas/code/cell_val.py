"""Phase 3 VAL cell for a HIGH-CONFIRM hypothesis. write: rule (first) + announce; run: the one VAL opening.
Same statistic and three-branch rule as every test cell. Power: normal sampling of the mean spread with
SE = (EXPLORE-pool simulated SE of C3, the most similar fold: 9 coins, FTMO-mid era) x sqrt(N_C3 / N_VAL) x 3.83
(the LARGEST measured fold null-noise ratio; VAL's own noise is unmeasured and is not looked at before the test)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import run_lib as L
mode, NN, H = sys.argv[1], int(sys.argv[2]), sys.argv[3]
ALPHA = {"H1": "A101"}[H]
S = L.slices(); win = S["VAL"]
VAL_NOTE = ("VAL is weak evidence. (1) BTC VAL was crossed twice by earlier work and overlaps a spent pooled row of an earlier "
            "BTC seasonality EDA. (2) VAL has since been opened ONCE more, on all 10 coins, for a pre-registered test of the "
            "crash-day rebound topic (see ALREADY TESTED): SOFT-clean for every coin for that topic. (3) VAL may be a DIFFERENT "
            "REGIME from TRAIN (2023 was calm; from 2023-04 BTC's 1-minute trade counts fell ~8x, cause not established).")
rp, ap, outp = [os.path.join(L.RUN, "cells", f"cell_{NN:02d}_{x}.md") for x in ("rule", "announce", "result")]
if mode == "write":
    cov = {}
    for c in L.COINS:
        p = L.load_primary(c, f"cell_{NN:02d} VAL power: coverage counts only (t, new_source; price not used)", win)[["t", "new_source"]]
        if not len(p): continue
        day = p.t.dt.floor("D"); g = pd.DataFrame({"n": p.groupby(day).size(), "ns": p.new_source.groupby(day).sum()})
        cov[c] = ((g.n == 24) & (g.ns == 0))
    C = pd.DataFrame(cov).asfreq("D").fillna(False).astype(bool)
    n = C.sum(axis=1).shift(-1)
    n = n[(n.index >= win[0]) & (n.index + pd.Timedelta(days=2) <= win[1])]
    Nval = int((n >= L.MIN_COINS).sum())
    se1 = json.load(open(os.path.join(L.RUN, "code", "sim_se.json")))["C3"]["sim_se_x1"]
    P1 = json.load(open(os.path.join(L.RUN, "code", "power.json")))["C3"]["N"]
    scale = json.load(open(os.path.join(L.RUN, "code", "noise_c1.json")))["ratio"]
    se = se1 * np.sqrt(P1 / Nval) * scale
    rng = np.random.default_rng(28)
    def probs(d):
        m = rng.normal(d, se, 200000); t = m / se
        return ((m >= 20) & (t >= 1.645)).mean(), ((m + 1.645 * se < 20) & (t < 1.645)).mean()
    a, r0 = probs(0.0); pw, r1 = probs(20.0); al = max(a, 0.005)
    ws, wr = L.capped(pw / al), (1 - pw) / (1 - al)
    json.dump({"N": Nval, "se": se, "alpha": a, "power": pw, "ref_null": r0, "ref_alt": r1, "w_sup": ws, "w_ref": wr},
              open(os.path.join(L.RUN, "code", f"val_{NN:02d}.json"), "w"))
    open(rp, "w").write(f"""hypothesis: {H}
slice: VAL
kind: val

# cell_{NN:02d} rule — VAL pass for {H} (Alpha#101), the only HIGH-CONFIRM hypothesis

> **VAL_NOTE (TARGET.md, quoted beside every VAL number):** {VAL_NOTE}

Why VAL: {H} is HIGH-CONFIRM (posterior 0.863 > 0.85, supported on C1 and C2, refuted on none). RUNBOOK_v3 Phase 3: open VAL
ONCE, rule first, report even a failure; never described as out-of-sample proof. **Caveat written before the test:** the
0.863 rests on cell_01's overstated weight (DECISIONS D14); at the honest weight H1 would be ~0.67 (OPEN).

Sub-claim: on VAL ({win[0].date()} .. {win[1].date()} excl.), the top half of coins by verbatim Alpha#101 (Binance UTC daily bar of day d)
out-earns the bottom half over end of d -> end of d+1 (primary `price`; FTMO mid for 7 coins in 2023) by >= 20 bp/day.
Tool: the same 2-bin quantile sort, mean spread, Newey-West(5) SE; IC descriptive.
Decision rule: **supported** if mean >= 20 bp/day AND t >= 1.645; **refuted** if mean + 1.645 SE < 20 AND t < 1.645;
**inconclusive** otherwise.
Power (normal sampling, 200,000 draws): N = {Nval} usable VAL signal days (coverage flags only), SE assumed {se:.1f} bp
(= C3's EXPLORE-pool simulated SE {se1:.2f} x sqrt({P1}/{Nval}) x the largest measured fold null-noise ratio {scale:.2f};
conservative). Result: power {pw:.3f} at 20 bp/day, alpha {a:.3f} (P(ref|20) {r1:.3f}, P(ref|0) {r0:.3f}).
Weights: supported = power/alpha = {pw/al:.3f}{' -> capped 10' if pw/al > 10 else ''} -> {ws:.3f}; refuted = (1-power)/(1-alpha) = {wr:.3f}; inconclusive 1.
Guard (a): first VAL look for {H}. Guard (b): within 10x.
Cost line to report alongside (TARGET.md): round trip BTC 18.9, ETH 25.4, LTC 36.5, ADA/DOGE/DOT/BNB/SOL ~45-47, XRP 68.6 bp.
""")
    open(ap, "w").write(f"""### Cell {NN:02d} — VAL: does {H} (Alpha#101) hold on VAL?

**Sub-claim being tested:** {H} top-minus-bottom next-day spread >= 20 bp/day on VAL (cell_{NN:02d}_rule.md).
**Why it matters:** the last look RUNBOOK_v3 allows this session; HIGH-CONFIRM -> HIGH-VAL only if supported.
**Test(s) used:** 2-bin quantile sort, NW(5) SE.
**Decision rule before running:** supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645; else
inconclusive. Weights {ws:.3f} / {wr:.3f} / 1.
**VAL_NOTE:** quoted in the rule file and the result file.
**Data loaded:** VAL only (signal inputs + 40-day lookback buffer that lies in the embargo/C3 tail; responses inside VAL).
**Decisions I need from you:** none (unattended; RUNBOOK Phase 3 authorises one VAL opening for HIGH-CONFIRM).
""")
    print("wrote VAL rule + announce; N", Nval, "se", round(se, 1), "power", pw, "alpha", a); sys.exit()

assert os.path.exists(rp) and os.path.exists(ap) and not os.path.exists(outp)
v = json.load(open(os.path.join(L.RUN, "code", f"val_{NN:02d}.json")))
P = L.build_panel(f"cell_{NN:02d} {H} VAL (the one VAL opening)", win)
sig = L.alpha(ALPHA, P); sp = L.half_spread_series(sig, P["fwd"]); ic = L.daily_ic(sig, P["fwd"])
m, se = sp.mean(), L.nw_se(sp.values); t = m / se; br = L.decide(m, se)
w = {"supported": round(v["w_sup"], 3), "refuted": round(v["w_ref"], 3), "inconclusive": 1.0}[br]
plt = L.setup_mpl()
fig, ax = plt.subplots(figsize=(8, 3.4))
ax.plot(sp.index, sp.cumsum(), color=L.PAL[0], label=f"cumulative spread (mean {m:+.1f} bp/day)")
ax.plot(sp.index, np.arange(1, len(sp) + 1) * 20, color=L.GRAY, ls="--", label="20 bp/day economic bar"); ax.axhline(0, color=L.TEXT2, lw=.8)
ax.set_title(f"cell {NN:02d} VAL — {H} Alpha#101: {br} (mean {m:+.1f} bp/day, t {t:+.2f}, n {len(sp)}); VAL is weak evidence")
ax.legend(fontsize=7); L.save(fig, f"cell_{NN:02d}_{H}_A101_VAL")
open(outp, "w").write(f"""branch: {br}
weight_applied: {w}

# cell_{NN:02d} result — VAL pass for {H} (Alpha#101)

> **VAL_NOTE (TARGET.md):** {VAL_NOTE}

Deciding numbers: mean top-minus-bottom half spread = **{m:+.2f} bp/day**, NW(5) SE {se:.2f} bp, t = {t:+.2f}, n = {len(sp)} days
(one-sided 95% upper bound {m + 1.645*se:+.1f} bp vs the 20 bp/day bar). -> **{br}**, weight {w} (rule file: supported
{round(v['w_sup'],3)} / refuted {round(v['w_ref'],3)} / inconclusive 1).
Descriptive: mean daily Spearman IC {ic.mean():+.4f} (t {ic.mean()/L.nw_se(ic.values):+.2f}, n {len(ic)}); realised SE {se:.1f} vs assumed {v['se']:.1f}.
This VAL number is weak evidence (VAL_NOTE) and is not out-of-sample proof.

Plot: plots/cell_{NN:02d}_{H}_A101_VAL.png
""")
K = sum(1 for l in open(os.path.join(L.RUN, "ATTEMPTS.md")) if l.startswith("| ") and l[2:4].isdigit()) + 1
with open(os.path.join(L.RUN, "ATTEMPTS.md"), "a") as fh:
    fh.write(f"| {NN:02d} | {H} | VAL | val | A101 top-minus-bottom half spread | {m:+.1f} bp/day, t {t:+.2f}, n {len(sp)} | {br} | {K} |\n")
print(open(outp).read())
