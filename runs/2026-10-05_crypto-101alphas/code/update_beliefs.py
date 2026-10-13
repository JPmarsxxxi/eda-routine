"""Phase 2 step 6: append the cell's evidence line to its hypothesis and recompute posterior/state from the chain.
Usage: update_beliefs.py NN"""
import sys, os, re, glob
sys.path.insert(0, os.path.dirname(__file__))
import run_lib as L
NN = int(sys.argv[1])
rule = dict(re.findall(r"(?m)^([a-z_]+):\s*(.*)$", open(os.path.join(L.RUN, "cells", f"cell_{NN:02d}_rule.md")).read()))
res = dict(re.findall(r"(?m)^([a-z_]+):\s*(.*)$", open(os.path.join(L.RUN, "cells", f"cell_{NN:02d}_result.md")).read()))
H, SL, kind = rule["hypothesis"], rule["slice"], rule["kind"]
w = float(res["weight_applied"]); br = res["branch"]
path = os.path.join(L.RUN, "BELIEFS.md"); B = open(path).read()
parts = re.split(r"(?m)^(##\s*H\d+\b.*)$", B)
for i in range(1, len(parts), 2):
    if re.match(rf"##\s*{H}\b", parts[i]):
        body = parts[i + 1]
        prior = float(re.search(r"(?m)^prior:\s*(\S+)", body).group(1))
        ws = [float(x) for x in re.findall(r"weight=([0-9.]+)", body)] + [w]
        post = L.prob(L.odds(prior) * __import__("math").prod(ws))
        # fold record from result files
        sup = ref = 0
        for f in glob.glob(os.path.join(L.RUN, "cells", "cell_*_rule.md")):
            kv = dict(re.findall(r"(?m)^([a-z_]+):\s*(.*)$", open(f).read()))
            rf = f.replace("_rule.md", "_result.md")
            if kv.get("hypothesis") == H and kv.get("kind") == "test" and kv.get("slice", "").startswith("C") and os.path.exists(rf):
                b = dict(re.findall(r"(?m)^([a-z_]+):\s*(.*)$", open(rf).read())).get("branch")
                sup += b == "supported"; ref += b == "refuted"
        if post < 0.05: st = "LOW"
        elif post <= 0.85: st = "OPEN"
        else: st = "HIGH-CONFIRM" if (sup >= 2 and ref == 0) else "HIGH"
        capped = "yes" if (br == "supported" and "CAPPED" in open(os.path.join(L.RUN, "cells", f"cell_{NN:02d}_rule.md")).read()) else "no"
        line = f"- cell_{NN:02d}: {SL} {br} weight={w} capped={capped} -> posterior {post:.3f}"
        if kind == "redirect":
            line = f"- cell_{NN:02d}: {SL} redirect weight=1.0 capped=no -> posterior {post:.3f}"
        body = re.sub(r"(?m)^posterior:.*$", f"posterior: {post:.3f}", body, count=1)
        body = re.sub(r"(?m)^state:.*$", f"state: {st}", body, count=1)
        body = body.rstrip("\n") + "\n" + line + "\n\n"
        parts[i + 1] = body
        print(H, "->", f"{post:.3f}", st, "| folds sup/ref", sup, ref)
open(path, "w").write("".join(parts))
