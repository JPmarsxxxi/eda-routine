"""Phase 2 step 1: expected belief shift of every admissible test, from BELIEFS.md + cell headers + power sims.
E|dp| = P(sup)|p_sup - p| + P(ref)|p_ref - p|, P(sup) = p*power + (1-p)*alpha, P(ref) = p*ref_alt + (1-p)*ref_null
(all from the x1.5-noise simulation at the slice's own size; weights capped at 10x)."""
import sys, os, re, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import run_lib as L
B = open(os.path.join(L.RUN, "BELIEFS.md")).read()
blocks = re.split(r"(?m)^##\s*(H\d+)\b", B)
E = {}
for i in range(1, len(blocks), 2):
    kv = dict(re.findall(r"(?m)^([a-z_]+):\s*(.*)$", blocks[i + 1]))
    E[blocks[i]] = kv
opened = {h: [] for h in E}
for f in sorted(glob.glob(os.path.join(L.RUN, "cells", "cell_*_rule.md"))):
    kv = dict(re.findall(r"(?m)^([a-z_]+):\s*(.*)$", open(f).read()))
    if kv.get("kind") == "test" and kv.get("hypothesis") in opened:
        opened[kv["hypothesis"]].append(kv["slice"])
PW = json.load(open(os.path.join(L.RUN, "code", "power.json")))
PW5 = json.load(open(os.path.join(L.RUN, "code", "power_h5.json")))
rows = []
for h, kv in E.items():
    if kv["state"] not in ("OPEN", "HIGH"):
        continue
    closed = {kv["born_on"].split()[0]} | ({s.strip() for s in kv["seen_on"].split(",")} if kv["seen_on"] != "none" else set()) | set(opened[h])
    cands = []
    if "EXPLORE" not in closed:
        cands.append("EXPLORE")
    nxt = next((f for f in ["C1", "C2", "C3"] if f not in closed), None)
    if nxt:
        cands.append(nxt)
    p = float(kv["posterior"])
    for s in cands:
        src = PW5 if h == "H5" else PW
        x = src[s]["x1.5"]; w = src[s]["weights"]
        ps = L.prob(L.odds(p) * w["supported"]); pr = L.prob(L.odds(p) * w["refuted"])
        Ps = p * x["power"] + (1 - p) * w["alpha_used"]; Pr = p * x["ref_alt"] + (1 - p) * x["ref_null"]
        sh = Ps * abs(ps - p) + Pr * abs(pr - p)
        rows.append((round(sh * 100, 2), h, s, p, round(Ps, 3), round(Pr, 3), round(ps, 3), round(pr, 3)))
rows.sort(key=lambda r: -r[0])
print("| expected shift (pp) | hyp | slice | p now | P(sup) | P(ref) | p if sup | p if ref |")
print("|---:|---|---|---:|---:|---:|---:|---:|")
for r in rows:
    print("| " + " | ".join(str(v) for v in r) + " |")
