"""Run ONE pre-registered test cell: python cell_test.py <NN> <H#> <SLICE>.
The rule (cells/cell_NN_rule.md) and announcement (cells/cell_NN_announce.md) must already exist; this refuses otherwise.
Loads ONLY that slice (signal inputs with a 40-day lookback buffer; responses strictly inside the slice), computes the
hypothesis's alpha verbatim, the daily top-minus-bottom half spread of next-day primary returns, its mean, Newey-West(5)
SE, applies run_lib.decide, and writes cells/cell_NN_result.md + plots/cell_NN_<slug>.png + an ATTEMPTS.md row."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import run_lib as L
NN, H, SL = int(sys.argv[1]), sys.argv[2], sys.argv[3]
ALPHA = {"H1": "A101", "H2": "A42", "H3": "A2", "H4": "A6", "H5": "A4"}[H]
rule = os.path.join(L.RUN, "cells", f"cell_{NN:02d}_rule.md"); ann = os.path.join(L.RUN, "cells", f"cell_{NN:02d}_announce.md")
assert os.path.exists(rule) and os.path.exists(ann), "rule and announcement must be written before the cell runs"
head = open(rule).read()
assert f"hypothesis: {H}" in head and f"slice: {SL}" in head and "kind: test" in head, "rule header does not match"
w = json.load(open(os.path.join(L.RUN, "code", "power.json")))[SL]["weights"]
if H == "H5":
    w = json.load(open(os.path.join(L.RUN, "code", "power_h5.json")))[SL]["weights"]
S = L.slices(); win = S[SL]
P = L.build_panel(f"cell_{NN:02d} {H} {ALPHA} test on {SL}", win)
sig = L.alpha(ALPHA, P)
fwd = P["fwd"]
sp = L.half_spread_series(sig, fwd)
ic = L.daily_ic(sig, fwd)
m, se = sp.mean(), L.nw_se(sp.values)
t = m / se
branch = L.decide(m, se)
wt = {"supported": w["supported"], "refuted": w["refuted"], "inconclusive": 1.0}[branch]
capped = branch == "supported" and w["supported_raw"] > 10
# descriptive extras (same slice, reported, not decision inputs)
by_year = sp.groupby(sp.index.year).agg(["mean", "count"]).round(1)
plt = L.setup_mpl()
fig, ax = plt.subplots(figsize=(8, 3.4))
ax.plot(sp.index, sp.cumsum(), color=L.PAL[0], label=f"cumulative top-minus-bottom spread (mean {m:+.1f} bp/day)")
ax.plot(sp.index, np.arange(1, len(sp) + 1) * L.ECON_BP, color=L.GRAY, ls="--", label="20 bp/day economic bar")
ax.axhline(0, color=L.TEXT2, lw=.8)
ax.set_title(f"cell {NN:02d} — {H} {ALPHA} on {SL}: {branch} (mean {m:+.1f} bp/day, t {t:+.2f}, n {len(sp)})")
ax.set_ylabel("bp (sum of daily spreads)"); ax.legend(fontsize=7)
L.save(fig, f"cell_{NN:02d}_{H}_{ALPHA}_{SL}")
res = f"""branch: {branch}
weight_applied: {wt}

# cell_{NN:02d} result — {H} ({ALPHA}) on {SL}

Deciding numbers: mean top-minus-bottom half spread = **{m:+.2f} bp/day**, Newey-West(5) SE = {se:.2f} bp, t = {t:+.2f},
n = {len(sp)} days (one-sided 95% upper bound {m + 1.645*se:+.1f} bp vs the 20 bp/day bar).
Rule (from cell_{NN:02d}_rule.md): supported if mean >= 20 and t >= 1.645; refuted if mean + 1.645 SE < 20 and t < 1.645;
else inconclusive. -> **{branch}**.
Weight from the rule file: supported {w['supported']} / refuted {w['refuted']} / inconclusive 1 -> applied {wt}
{'(supported weight capped at 10x, guard b)' if capped else '(no cap needed; within 10x)'}.
Secondary (descriptive, not a decision input): mean daily Spearman IC {ic.mean():+.4f} (n {len(ic)} days,
t {ic.mean()/L.nw_se(ic.values):+.2f}); realised spread SD {sp.std():.1f} bp/day.
By calendar year inside the slice (mean bp/day, days):
{L.md(by_year, index=True)}

Plot: plots/cell_{NN:02d}_{H}_{ALPHA}_{SL}.png
"""
out = os.path.join(L.RUN, "cells", f"cell_{NN:02d}_result.md")
assert not os.path.exists(out), "result already exists — a cell runs once"
open(out, "w").write(res)
K = sum(1 for l in open(os.path.join(L.RUN, "ATTEMPTS.md")) if l.startswith("| ") and l[2:4].isdigit()) + 1
with open(os.path.join(L.RUN, "ATTEMPTS.md"), "a") as fh:
    fh.write(f"| {NN:02d} | {H} | {SL} | test | {ALPHA} top-minus-bottom half spread | {m:+.1f} bp/day, t {t:+.2f}, n {len(sp)} | {branch} | {K} |\n")
print(res)
json.dump({"mean": m, "se": se, "t": t, "n": len(sp), "branch": branch, "weight": wt},
          open(os.path.join(L.RUN, "code", f"cell_{NN:02d}.json"), "w"))
