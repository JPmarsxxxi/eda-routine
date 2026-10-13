"""Phase 2 step 1: for every pickable hypothesis, its next admissible test and the expected belief shift (D10 weights,
tables/power.csv). Writes tables/pick_NN.txt. Usage: python pick.py NN
Reads the live BELIEFS.md and cells/ headers, so the arithmetic always uses the current posteriors and slice record."""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
import common as C

nn = int(sys.argv[1])
power = pd.read_csv(os.path.join(C.RUN, "tables", "power.csv"))
text = open(os.path.join(C.RUN, "BELIEFS.md")).read()
blocks = re.split(r"(?m)^##\s*(H\d+)\b", text)
H = {}
for i in range(1, len(blocks), 2):
    kv = dict(re.findall(r"(?m)^([a-z_]+):\s*(.*)$", blocks[i + 1]))
    H[blocks[i]] = kv
opened = {h: [] for h in H}
for p in sorted(glob.glob(os.path.join(C.RUN, "cells", "cell_*_rule.md"))):
    kv = dict(re.findall(r"(?m)^([a-z_]+):\s*(.*)$", open(p).read()))
    if kv.get("kind") == "test" and kv.get("hypothesis") in opened:
        opened[kv["hypothesis"]].append(kv["slice"])
ALPHA = {"H1": "A30", "H2": "A35", "H3": "A38", "H4": "A53", "H5": "A54"}
lines = [f"pick_{nn:02d}: E|shift| = sum over supported/refuted of P(branch) x |posterior(branch) - current|,"
         f" P(branch) = p x P(b|IC=0.02) + (1-p) x P(b|IC=0); weights capped [0.1, 10] (D10, tables/power.csv)"]
cands = []
for h, kv in H.items():
    if kv["state"] not in ("OPEN", "HIGH"):
        continue
    born = kv["born_on"].split()[0]
    seen = set() if kv["seen_on"].strip().lower() == "none" else {s.strip() for s in kv["seen_on"].split(",")}
    closed = {born} | seen | set(opened[h])
    nxt = [s for s in ["EXPLORE"] if s not in closed]
    folds = [f for f in ["C1", "C2", "C3"] if f not in closed]
    if folds:
        nxt.append(folds[0])
    a = kv.get("alpha_code") or ALPHA.get(h)
    for s in nxt:
        row = power[(power.alpha == a) & (power.slice == s)].iloc[0]
        sim = {"P_H1": {"supported": row.power, "refuted": row.P_ref_H1},
               "P_H0": {"supported": row.alpha_size, "refuted": row.P_ref_H0},
               "w_sup": row.w_sup, "w_ref": row.w_ref}
        p = float(kv["posterior"])
        e = C.expected_shift(p, sim)
        cands.append((e, h, s, p, row.w_sup, row.w_ref))
cands.sort(key=lambda x: (-x[0], x[2] != "EXPLORE"))
for e, h, s, p, ws, wr in cands:
    lines.append(f"  {h} {ALPHA.get(h, H[h].get('alpha_code'))} next={s:7s} p={p:.3f} w_sup={ws:.2f} w_ref={wr:.3f} -> E|shift| {e*100:.2f} pp")
lines.append(f"PICK: {cands[0][1]} on {cands[0][2]} (largest expected shift {cands[0][0]*100:.2f} pp)" if cands else "PICK: none")
open(os.path.join(C.RUN, "tables", f"pick_{nn:02d}.txt"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
