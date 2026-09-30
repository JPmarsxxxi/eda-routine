# Step-1 pick arithmetic: expected |posterior - prior| for each OPEN hypothesis's next available test.
import sys, json
def post(p, w): o = p / (1 - p) * w; return o / (1 + o)
def cap(w): return min(max(w, 0.1), 10.0)
def expected_shift(p, power, alpha):
    if power is None or power < 0:   # no admissible test left (slice spent / produced it): nothing can move p
        return 0.0, 1.0, 1.0, 0.0
    ws, wr = cap(power / alpha), cap((1 - power) / (1 - alpha))
    ps = p * power + (1 - p) * alpha; pr = 1 - ps
    return ps * abs(post(p, ws) - p) + pr * abs(post(p, wr) - p), ws, wr, ps
if __name__ == "__main__":
    tests = json.loads(sys.argv[1])  # {id: [prior, power, alpha, label]}
    rows = []
    for k, (p, pw, a, lab) in tests.items():
        es, ws, wr, ps = expected_shift(p, pw, a)
        rows.append((es, k, p, pw, a, ws, wr, ps, lab))
    for es, k, p, pw, a, ws, wr, ps, lab in sorted(rows, reverse=True):
        if pw is None or pw < 0:
            print(f"{k}: posterior {p:.3f} -- no admissible test ({lab}) -> E|shift| 0.0 pp"); continue
        print(f"{k}: prior {p:.2f} power {pw:.3f} alpha {a:.3f} w_sup {ws:.2f} w_ref {wr:.3f} P(sup) {ps:.3f} -> post_sup {post(p, ws):.3f} post_ref {post(p, wr):.3f} E|shift| {100*es:.1f} pp  [{lab}]")
