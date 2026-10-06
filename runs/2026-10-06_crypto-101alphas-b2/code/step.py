"""One loop iteration: pick (pick.py) -> rule -> run -> result. Usage: python step.py NN [forced HYP SLICE]"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
P = "/home/user/eda-routine/.venv/bin/python"
D = os.path.dirname(__file__)
nn = int(sys.argv[1])
out = subprocess.run([P, f"{D}/pick.py", str(nn)], capture_output=True, text=True).stdout
print(out)
m = re.search(r"PICK: (H\d+) on (\w+)", out)
if not m:
    sys.exit("no pick")
hyp, sl = m.group(1), m.group(2)
B = open(os.path.join(os.path.dirname(D), "BELIEFS.md")).read()
blk = re.search(rf"(?ms)^## {hyp}\b.*?(?=^## H\d+|\Z)", B).group(0)
ac = re.search(r"(?m)^alpha_code:\s*(\S+)", blk)
sg = re.search(r"(?m)^sign:\s*(\S+)", blk)
alpha = ac.group(1) if ac else {"H1": "A30", "H2": "A35", "H3": "A38", "H4": "A53", "H5": "A54"}[hyp]
sign = sg.group(1) if sg else "1"
subprocess.run([P, f"{D}/write_rule.py", str(nn), hyp, alpha, sl, "test", sign,
                f"Picked by pick_{nn:02d} (largest expected shift)."], check=True)
subprocess.run([P, f"{D}/cell_run.py", str(nn), "test", alpha, sl, sign], check=True, capture_output=True)
r = subprocess.run([P, f"{D}/write_result.py", str(nn), hyp], capture_output=True, text=True, check=True).stdout
print("\n".join(l for l in r.splitlines() if l.startswith(("**Branch", "- ", "H", "  implied"))))
