# Expected belief shift of a test with power pw at alpha a, given current probability p.
# Two-outcome approximation: "supported" (prob p*pw + (1-p)*a) or "not supported" (the rest, weighted as refuted).
# Weights capped to [0.1, 10] (guard b).
import sys, json

def post(p, w):
    o = p / (1 - p) * w
    return o / (1 + o)

def expected_shift(p, pw, a):
    ws = min(pw / a, 10.0); wr = max((1 - pw) / (1 - a), 0.1)
    ps = p * pw + (1 - p) * a
    return ps * abs(post(p, ws) - p) + (1 - ps) * abs(post(p, wr) - p), ws, wr, post(p, ws), post(p, wr)

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        name, p, pw, a = arg.split(":")
        es, ws, wr, pS, pR = expected_shift(float(p), float(pw), float(a))
        print(f"{name}: p={p} power={pw} alpha={a} -> w_sup={ws:.2f} w_ref={wr:.3f} post_sup={pS:.3f} post_ref={pR:.3f} E|shift|={es:.3f}")
