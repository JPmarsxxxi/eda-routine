"""Write cells/cell_NN_result.md from tables/cell_NN.json, update BELIEFS.md (posterior, state, evidence line) and append the
ATTEMPTS.md row. Usage: python write_result.py NN HYP [NOTE...]
For test/val cells the weight applied is the branch's weight from the rule file (D10); redirects apply 1."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
import common as C

nn, hyp = int(sys.argv[1]), sys.argv[2]
note = " ".join(sys.argv[3:])
J = json.load(open(os.path.join(C.RUN, "tables", f"cell_{nn:02d}.json")))
rule = open(os.path.join(C.RUN, "cells", f"cell_{nn:02d}_rule.md")).read()
kind, sl = J["kind"], J["slice"]
if kind == "redirect":
    w, br = 1.0, J["branch"]
else:
    w_sup = float(re.search(r"weight\(supported\).*\*\*([0-9.]+)\*\*", rule).group(1))
    w_ref = float(re.search(r"weight\(refuted\).*\*\*([0-9.]+)\*\*", rule).group(1))
    br = J["branch"]
    w = {"supported": w_sup, "refuted": w_ref, "inconclusive": 1.0}[br]

n, raw, net, rv, sp = J["neutral"], J["raw"], J["net_of_rev1"], J["rev1_ic"], J["spread_bp"]
f = lambda d: f"{d['mean']:+.4f} (se {d['se']:.4f}, t {d['t']:+.2f}, n {d['n']})"
txt = f"""branch: {br}
weight_applied: {w:.4g}

# cell_{nn:02d} — RESULT ({kind}, {J['alpha']}{' x -1' if J['sign'] < 0 else ''}, {sl})

**Branch fired: {br.upper()}.** Deciding number: mean daily cross-sectional rank IC = {f(n)}, days {J['first_day']} ..
{J['last_day']}. Rule (D7): supported needs >= 0.02 and t >= 1.645; refuted needs mean + 1.645 se < 0.02
(here {n['mean'] + 1.645 * n['se']:+.4f}). Weight applied to {hyp}: **{w:.4g}**{' (redirect: never moves the parent)' if kind == 'redirect' else ''}.

Pre-registered descriptives (did not decide anything):
- raw version (own-return incl. market, trailing scaling): {f(raw)}
- net of 1-day reversal: {f(net)}; b_rev1's own IC on {sl}: {f(rv)}
- halves of {sl}: first {f(J['half1'])}; second {f(J['half2'])}
- top-half minus bottom-half spread: {sp['mean']:+.1f} bp/day (t {sp['t']:+.2f}); daily half-membership turnover {J['turnover']:.3f};
  implied cost {J['cost_bp_day']:.1f} bp/day at the median-coin 45 bp round trip (D11)
- market share: corr(signal cross-sectional mean, same-day panel return) {J['market_corr']:+.3f}; with BTC {J['btc_corr']:+.3f}

{note}
Plot: `plots/cell_{nn:02d}_{J['alpha'].lower()}_{sl.lower()}{'_flip' if J['sign'] < 0 else ''}.png`. Table: `tables/cell_{nn:02d}.json`, `tables/cell_{nn:02d}_daily_ic.csv`.
"""
open(os.path.join(C.RUN, "cells", f"cell_{nn:02d}_result.md"), "w").write(txt)

# BELIEFS.md update (posterior chain + state from the fold record)
B = open(os.path.join(C.RUN, "BELIEFS.md")).read()
m = re.search(rf"(?ms)^## {hyp}\b.*?(?=^## H\d+|\Z)", B)
blk = m.group(0)
post = float(re.search(r"(?m)^posterior:\s*([0-9.]+)", blk).group(1))
o = post / (1 - post) * w
newp = o / (1 + o)
ev = f"- cell_{nn:02d}: {sl} {br}{' (redirect)' if kind == 'redirect' else ''} weight={w:.4g} capped=no -> posterior {newp:.4f}"
# fold record for the state
import glob
recs = []
for p in sorted(glob.glob(os.path.join(C.RUN, "cells", "cell_*_result.md"))):
    k = int(re.search(r"cell_(\d+)_result", p).group(1))
    r = open(p.replace("_result", "_rule")).read()
    kv = dict(re.findall(r"(?m)^([a-z_]+):\s*(.*)$", r))
    if kv.get("hypothesis") != hyp:
        continue
    b = re.search(r"(?m)^branch:\s*(\w+)", open(p).read()).group(1)
    recs.append((kv["kind"], kv["slice"], b))
sup = sum(1 for k, s, b in recs if k == "test" and s.startswith("C") and b == "supported")
ref = sum(1 for k, s, b in recs if k == "test" and s.startswith("C") and b == "refuted")
opened = {s for k, s, b in recs if k == "test"}
born = re.search(r"(?m)^born_on:\s*(\S+)", blk).group(1)
seen_raw = re.search(r"(?m)^seen_on:\s*(.*)$", blk).group(1)
seen = set() if seen_raw.strip().lower() == "none" else {s.strip() for s in seen_raw.split(",")}
left = [f for f in ["C1", "C2", "C3"] if f not in opened | {born} | seen]
val_sup = any(k == "val" and b == "supported" for k, s, b in recs)
if newp < 0.05:
    state = "LOW"
elif newp <= 0.85:
    state = "OPEN"
elif sup >= 2 and ref == 0 and not left:
    state = "HIGH-VAL" if val_sup else "HIGH-CONFIRM"
else:
    state = "HIGH"
blk2 = re.sub(r"(?m)^posterior:.*$", f"posterior: {newp:.4f}", blk, count=1)
blk2 = re.sub(r"(?m)^state:.*$", f"state: {state}", blk2, count=1)
blk2 = blk2.rstrip("\n") + "\n" + ev + "\n\n"
B = B.replace(blk, blk2)
open(os.path.join(C.RUN, "BELIEFS.md"), "w").write(B)

with open(os.path.join(C.RUN, "ATTEMPTS.md"), "a") as fh:
    fh.write(f"| {nn} | {pd.Timestamp.now('UTC'):%Y-%m-%d %H:%M} | cell_{nn:02d} {kind} | {hyp} {J['alpha']}"
             f"{' x-1' if J['sign'] < 0 else ''} | {sl} | IC {n['mean']:+.4f} t {n['t']:+.2f} n {n['n']} -> {br} "
             f"(w {w:.3g}; {hyp} {post:.3f} -> {newp:.3f} {state}) |\n")
print(txt)
print(f"{hyp}: {post:.4f} -> {newp:.4f}  state {state}  (sup folds {sup}, ref folds {ref}, folds left {left})")
