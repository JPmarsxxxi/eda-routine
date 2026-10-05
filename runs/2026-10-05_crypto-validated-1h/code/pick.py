"""Phase 2 step 1: expected belief shift of the next admissible test per pickable hypothesis.
usage: pick.py H1=0.49:C1 H2=0.12:C1 ...  (current posterior : next admissible slice). Uses tables/power.csv."""
import sys, os
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from hyp import weights, cap, post
P = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "tables", "power.csv"), dtype={"truth": str}, keep_default_na=False)
out = []
for arg in sys.argv[1:]:
    h, rest = arg.split("="); p, s = rest.split(":"); p = float(p)
    row = P[(P.hyp == h) & (P.slice == s)].set_index("truth")
    pw = row.loc["true", "p_sup"]
    W = weights(pw)
    E = 0; parts = []
    for b, col in (("supported", "p_sup"), ("inconclusive", "p_inc"), ("refuted", "p_ref")):
        pb = p * row.loc["true", col] + (1 - p) * row.loc["null", col]
        w, _ = cap(W[b]); pp = post(p, w); E += pb * abs(pp - p)
        parts.append(f"P({b})={p:.3f}x{row.loc['true', col]:.3f}+{1-p:.3f}x{row.loc['null', col]:.3f}={pb:.3f}, w={w:.3f} -> post {pp:.3f}, |shift| {abs(pp-p):.3f}")
    out.append((h, s, p, pw, E, parts))
for h, s, p, pw, E, parts in sorted(out, key=lambda x: -x[4]):
    print(f"{h} on {s}: prior {p:.3f}, power {pw:.3f}, expected |shift| = {E*100:.1f} pp")
    for x in parts: print("    " + x)
