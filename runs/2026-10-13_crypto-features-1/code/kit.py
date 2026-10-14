"""kit.py - cell bookkeeping: rule/announce/result files, power + evidence weights, BELIEFS.md regenerated from
state.json + the cells' own result files (so the posterior chain can never drift from weight_applied)."""
import os, re, json, math, glob
from scipy import stats

RUN = r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1"
CELLS = os.path.join(RUN, "cells")
STATE = os.path.join(RUN, "work", "state.json")
CAP = {"search": 3.0, "confirm": 10.0, "val": 10.0}


def _w(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def power(se, delta, tcrit=1.96, alpha=0.05):
    """power to see mean IC >= tcrit*se when the true mean IC is delta, given the measured se of the mean IC.
    Two-sided alpha: the 'effect there' outcome has likelihood ratio power/alpha; absent: (1-power)/(1-alpha)."""
    z = delta / se
    pw = float(1 - stats.norm.cdf(tcrit - z))
    # alpha = size of the test at tcrit (two-sided in the direction we look)
    a = float(2 * (1 - stats.norm.cdf(tcrit))) / 2
    w_yes = pw / a if a > 0 else 3.0
    w_no = (1 - pw) / (1 - a)
    return dict(power=pw, alpha=a, w_yes=w_yes, w_no=w_no)


def capped(w, kind):
    c = CAP[kind]
    wc = min(max(w, 1 / c), c)
    return wc, (abs(wc - w) > 1e-9)


def tcrit_for(V):
    """Sidak-style critical |t| for the best of V variants."""
    return float(stats.norm.ppf(1 - 0.025 / max(V, 1)))


def begin(nn, hyp, slice_, kind, controls, conditional, rule_body, announce_body, candidate=None, sha=None, method=None):
    head = f"hypothesis: {hyp}\nslice: {slice_}\nkind: {kind}\ncontrols: {controls}\nconditional: {conditional}\n"
    if candidate:
        head += f"candidate: {candidate}\n"
    if sha:
        head += f"spec_sha256: {sha}\n"
    if method:
        head += f"method: {method}\n"
    _w(os.path.join(CELLS, f"cell_{nn:02d}_announce.md"), announce_body)
    _w(os.path.join(CELLS, f"cell_{nn:02d}_rule.md"), head + "\n" + rule_body)


def result(nn, weight, variants=None, suggests=None, branch=None, folds=None, body=""):
    head = f"weight_applied: {weight:.4f}\n"
    if variants is not None:
        head += f"variants: {variants}\n"
    if suggests is not None:
        head += f"suggests: {suggests}\n"
    if branch is not None:
        head += f"branch: {branch}\n"
    if folds is not None:
        head += f"folds: {folds}\n"
    _w(os.path.join(CELLS, f"cell_{nn:02d}_result.md"), head + "\n" + body)


def attempt(nn, hyp, what, outcome):
    p = os.path.join(RUN, "ATTEMPTS.md")
    new = not os.path.exists(p)
    with open(p, "a", encoding="utf-8") as fh:
        if new:
            fh.write("| cell | hypothesis | what | outcome |\n|---|---|---|---|\n")
        fh.write(f"| {nn:02d} | {hyp} | {what} | {outcome} |\n")


# ------------------------------------------------------------------ beliefs
def load_state():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def save_state(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(s, fh, indent=1)


def add_h(hid, title, parent, source, question, hypothesis, forbids, rivals, born_on, prior, anchor):
    s = load_state()
    s[hid] = dict(title=title, parent=parent, source=source, question=question, hypothesis=hypothesis, forbids=forbids,
                  rivals=rivals, born_on=born_on, prior=prior, anchor=anchor, state="OPEN")
    save_state(s)


def set_state(hid, state):
    s = load_state(); s[hid]["state"] = state; save_state(s)


def _cell_heads():
    out = []
    for p in sorted(glob.glob(os.path.join(CELLS, "cell_*_rule.md"))):
        nn = int(re.search(r"cell_(\d+)_rule", p).group(1))
        head = {}
        with open(p, encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"^([a-z_0-9]+):\s*(.*)$", line.strip())
                if m and m.group(1) not in head:
                    head[m.group(1)] = m.group(2).strip()
        rp = os.path.join(CELLS, f"cell_{nn:02d}_result.md")
        w = None; cands = None
        if os.path.exists(rp):
            with open(rp, encoding="utf-8") as fh:
                for line in fh:
                    m = re.match(r"^weight_applied:\s*(\S+)", line.strip())
                    if m:
                        w = float(m.group(1)); break
        out.append((nn, head, w))
    return out


def write_beliefs():
    s = load_state()
    heads = _cell_heads()
    fcands = {}
    for p in glob.glob(os.path.join(RUN, "candidates", "F*.md")):
        t = open(p, encoding="utf-8").read()
        m = re.search(r"(?m)^hypothesis:\s*(H\d+)", t)
        if m:
            fcands.setdefault(m.group(1), []).append(re.search(r"(F\d+)\.md", p).group(1))
    parts = ["# BELIEFS - hypotheses (generated from work/state.json + the cells' weight_applied lines)\n"]
    for hid in sorted(s, key=lambda x: int(x[1:])):
        h = s[hid]
        odds = h["prior"] / (1 - h["prior"])
        ev = []
        for nn, head, w in heads:
            if head.get("hypothesis") != hid or w is None:
                continue
            kind = head.get("kind", "search")
            wc, _ = capped(w, kind)
            odds *= w
            post = odds / (1 + odds)
            ev.append(f"- cell_{nn:02d}: {kind} {head.get('slice')} weight={w:.3f} capped={'yes' if abs(wc - w) < 1e-9 and (abs(w - CAP[kind]) < 1e-3 or abs(w - 1 / CAP[kind]) < 1e-3) else 'no'} -> posterior {post:.3f}")
        post = odds / (1 + odds)
        cl = ", ".join(sorted(fcands.get(hid, []), key=lambda f: int(f[1:]))) or "none"
        parts.append(f"## {hid} - {h['title']}\nparent: {h['parent']}\nsource: {h['source']}\nquestion: {h['question']}\n"
                     f"hypothesis: {h['hypothesis']}\nforbids: {h['forbids']}\nrivals: {h['rivals']}\nborn_on: {h['born_on']}\n"
                     f"prior: {h['prior']:.2f}\nanchor: {h['anchor']}\nposterior: {post:.3f}\nstate: {h['state']}\n"
                     f"candidates: {cl}\nevidence:\n" + ("\n".join(ev) if ev else "- (none yet)") + "\n")
    _w(os.path.join(RUN, "BELIEFS.md"), "\n".join(parts))
    return {hid: None for hid in s}


def posterior(hid):
    s = load_state()[hid]
    odds = s["prior"] / (1 - s["prior"])
    for nn, head, w in _cell_heads():
        if head.get("hypothesis") == hid and w is not None:
            odds *= w
    return odds / (1 + odds)
