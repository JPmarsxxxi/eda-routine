"""Mandatory redirect cell (RUNBOOK_v3 step 8): "where does the data actually point?" for a refuted hypothesis.
Usage: cell_redirect.py write NN H SLICE   -> writes cells/cell_NN_rule.md then cells/cell_NN_announce.md (before any code)
       cell_redirect.py run   NN H SLICE   -> runs, writes cells/cell_NN_result.md (weight 1) + plot + ATTEMPTS row
SLICE must be EXPLORE or a slice H already opened. Pointers (pre-registered, same for every redirect):
  P1 sign flipped (bottom-minus-top), 1-day horizon
  P2 horizons 2, 3, 5 days (average per-day spread over d+1..d+h, paper sign and flipped)
  P3 one era only: each calendar year inside the slice, paper sign and flipped
  P4 a re-translation the formula's assumption check pointed to (scale-free variant), both signs
  P5 the named rival sort (plain 1-day return, or price level), both signs
Bar for a pointer to spawn a child: |mean| >= 20 bp/day AND |t| >= 2.5 (2.5 not 1.645: ~15 looks in one redirect).
At most one child (the largest |t| pointer that clears the bar; DECISIONS D13)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import run_lib as L
mode, NN, H, SL = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
ALPHA = {"H1": "A101", "H2": "A42", "H3": "A2", "H4": "A6", "H5": "A4", "H6": "A2RAWPOS"}[H]
VAR = {"A101": ("(close - open)/(high - low) without the +.001 price-unit term", lambda P: (P["close"] - P["open"]) / (P["high"] - P["low"])),
       "A42": ("rank(vwap/close - 1) / 1: the scale-free (return) form of vwap - close, no price-level denominator", lambda P: L.cs_rank(P["vwap"] / P["close"] - 1)),
       "A2": ("correlation on raw (unranked) delta(log volume, 2) and (close-open)/open", lambda P: -1 * L.ts_corr(L.delta(np.log(P["volume"]), 2), (P["close"] - P["open"]) / P["open"], 6)),
       "A6": ("-correlation(log(close/close.shift(1)), log volume, 10): returns instead of price level", lambda P: -1 * L.ts_corr(np.log(P["close"] / P["close"].shift(1)), np.log(P["volume"]), 10)),
       "A4": ("-ts_rank(close/mean_9(close), 9): own relative level, no cross-sectional price-level rank", lambda P: -1 * L.ts_rank(P["close"] / P["close"].rolling(9).mean(), 9)),
       "A2RAWPOS": ("Spearman (ranked-in-time) version: correlation of ts-ranks over 6 days", lambda P: L.ts_corr(L.ts_rank(L.delta(np.log(P["volume"]), 2), 6), L.ts_rank((P["close"] - P["open"]) / P["open"], 6), 6))}[ALPHA]
RIV = {"A101": ("plain 1-day return log(close/open)", lambda P: np.log(P["close"] / P["open"])),
       "A42": ("price level rank(vwap + close)", lambda P: L.cs_rank(P["vwap"] + P["close"])),
       "A2": ("plain 1-day return (close-open)/open", lambda P: (P["close"] - P["open"]) / P["open"]),
       "A6": ("10-day return log(close/close.shift(10))", lambda P: np.log(P["close"] / P["close"].shift(10))),
       "A4": ("9-day return log(close/close.shift(9))", lambda P: np.log(P["close"] / P["close"].shift(9))),
       "A2RAWPOS": ("6-day volatility (std of daily log returns)", lambda P: np.log(P["close"] / P["close"].shift(1)).rolling(6).std())}[ALPHA]
rp, ap = os.path.join(L.RUN, "cells", f"cell_{NN:02d}_rule.md"), os.path.join(L.RUN, "cells", f"cell_{NN:02d}_announce.md")
if mode == "write":
    open(rp, "w").write(f"""hypothesis: {H}
slice: {SL}
kind: redirect

# cell_{NN:02d} rule — mandatory redirect for {H} ({'Alpha#' + ALPHA[1:] if ALPHA != 'A2RAWPOS' else 'H6 signal'}) on {SL}

Trigger: {H}'s only sub-claim was refuted (RUNBOOK_v3 step 8). Question: where does the data actually point instead?
{SL} is {'EXPLORE' if SL == 'EXPLORE' else 'a slice ' + H + ' already opened'}; no unopened fold is looked at. Weight applied: 1 (a redirect moves no posterior).

Pointers (each = the same 2-bin top-minus-bottom next-day spread, mean bp/day with Newey-West(5) SE, on {SL}):
- P1 sign flipped (bottom-minus-top).
- P2 horizons h = 2, 3, 5 days: mean per-day spread of the average return over d+1..d+h (response windows overlap: NW(5) SE),
  paper sign and flipped.
- P3 one era only: each calendar year inside {SL}, both signs.
- P4 re-translation pointed to by the Phase-1 assumption check: {VAR[0]}, both signs.
- P5 the named rival: {RIV[0]}, both signs.
**Bar for a pointer:** |mean| >= 20 bp/day AND |t| >= 2.5 (stricter than 1.645 because ~15 looks are taken here).
**Outcome rule:** if one or more pointers clear the bar, the one with the largest |t| becomes ONE new child hypothesis in
BELIEFS.md (born_on {SL} cell_{NN:02d}; seen_on = none unless another slice was shown), with its own rule file before any
test; if none clears it, the finding is "absent everywhere looked" and no child is spawned (DECISIONS D13).
""")
    open(ap, "w").write(f"""### Cell {NN:02d} — EDA redirect: where does {H} ({'Alpha#' + ALPHA[1:] if ALPHA != 'A2RAWPOS' else 'H6 signal'}) point instead, on {SL}?

**Sub-claim being tested:** none (redirect, kind: redirect, weight 1) — see cell_{NN:02d}_rule.md for the five pointers.
**Why it matters:** RUNBOOK_v3 step 8 — a refuted hypothesis gets a mandatory "where does the data point" look before the
session moves on; any lead becomes a new child, never a rewrite.
**Test(s) used:** 2-bin quantile sorts, NW(5) SE; horizons 2/3/5; per-year; scale-free variant; rival sort.
**Decision rule before running:** a pointer counts if |mean| >= 20 bp/day and |t| >= 2.5; largest |t| -> one child.
**Data loaded:** {SL} only (signal inputs + 40-day lookback; responses inside {SL}); guard asserted (ACCESS_LOG.md).
**Decisions I need from you:** none (unattended; DECISIONS D13).
""")
    print("wrote redirect rule + announce", NN); sys.exit()

assert os.path.exists(rp) and os.path.exists(ap)
S = L.slices(); win = S[SL]
P = L.build_panel(f"cell_{NN:02d} {H} redirect on {SL}", win)
fwd = P["fwd"]
# multi-day responses: average daily return over d+1..d+h, valid if every day valid; must end inside the slice
def fwd_h(h):
    acc = sum(fwd.shift(-k) for k in range(h)) / h
    end_ok = acc.index + pd.Timedelta(days=h + 1) <= win[1]
    acc.loc[~end_ok] = np.nan
    return acc
sig = L.alpha(ALPHA, P)
rows = []
def add(name, s, f):
    sp = L.half_spread_series(s, f)
    if len(sp) < 30:
        rows.append([name, len(sp), np.nan, np.nan]); return
    m, se = sp.mean(), L.nw_se(sp.values); rows.append([name, len(sp), round(m, 1), round(m / se, 2)])
add("P0 paper sign, h=1 (the refuted test, for reference)", sig, fwd)
add("P1 sign flipped, h=1", -sig, fwd)
for h in (2, 3, 5):
    add(f"P2 paper sign, h={h}", sig, fwd_h(h)); add(f"P2 flipped, h={h}", -sig, fwd_h(h))
for y in sorted(set(fwd.index.year)):
    m = fwd.index.year == y
    if m.sum() > 60:
        f2 = fwd.copy(); f2.loc[~m] = np.nan
        add(f"P3 paper sign, {y} only", sig, f2); add(f"P3 flipped, {y} only", -sig, f2)
v = VAR[1](P); add("P4 variant, paper sign", v, fwd); add("P4 variant, flipped", -v, fwd)
r = RIV[1](P); add("P5 rival, high-minus-low", r, fwd); add("P5 rival, low-minus-high", -r, fwd)
t = pd.DataFrame(rows, columns=["pointer", "days", "mean_bp_day", "t"])
t["clears_bar"] = (t.mean_bp_day.abs() >= 20) & (t.t.abs() >= 2.5) & ~t.pointer.str.startswith("P0")
# only pointers whose sign is "the direction of the mean" count: a pointer with negative mean is the same as its flip
t.loc[t.mean_bp_day < 0, "clears_bar"] = False
best = t[t.clears_bar].sort_values("t", ascending=False).head(1)
plt = L.setup_mpl()
fig, ax = plt.subplots(figsize=(8, 0.28 * len(t) + 1.2))
cols = [L.PAL[1] if c else L.GRAY for c in t.clears_bar]
ax.barh(range(len(t)), t.t.fillna(0), color=cols); ax.set_yticks(range(len(t))); ax.set_yticklabels(t.pointer, fontsize=7)
ax.axvline(2.5, color=L.PAL[7], ls="--"); ax.axvline(-2.5, color=L.PAL[7], ls="--"); ax.invert_yaxis()
ax.set_xlabel("t of the mean spread (green = clears |mean|>=20 & |t|>=2.5)")
ax.set_title(f"cell {NN:02d} redirect {H} on {SL}: " + (f"points to '{best.pointer.iloc[0]}'" if len(best) else "absent everywhere looked"))
L.save(fig, f"cell_{NN:02d}_{H}_redirect_{SL}")
res = f"""branch: inconclusive
weight_applied: 1

# cell_{NN:02d} result — redirect for {H} ({'Alpha#' + ALPHA[1:] if ALPHA != 'A2RAWPOS' else 'H6 signal'}) on {SL}

Pointers (mean bp/day, NW(5) t). Bar: |mean| >= 20 and |t| >= 2.5, positive mean in the stated direction.

{L.md(t)}

**Finding:** {('points to: ' + best.pointer.iloc[0] + f' (mean {best.mean_bp_day.iloc[0]} bp/day, t {best.t.iloc[0]}) -> ONE child spawned in BELIEFS.md') if len(best) else 'absent everywhere looked (no pointer clears the bar) -> no child spawned (DECISIONS D13).'}
Redirect: weight 1, no posterior moves. `branch: inconclusive` is the gate.py-required placeholder for a redirect.

Plot: plots/cell_{NN:02d}_{H}_redirect_{SL}.png
"""
open(os.path.join(L.RUN, "cells", f"cell_{NN:02d}_result.md"), "w").write(res)
K = sum(1 for l in open(os.path.join(L.RUN, "ATTEMPTS.md")) if l.startswith("| ") and l[2:4].isdigit()) + 1
with open(os.path.join(L.RUN, "ATTEMPTS.md"), "a") as fh:
    fh.write(f"| {NN:02d} | {H} | {SL} | redirect | {len(t)} pointer sorts (see result) | "
             + (f"best: {best.pointer.iloc[0]} {best.mean_bp_day.iloc[0]} bp/day t {best.t.iloc[0]}" if len(best) else "none clears the bar")
             + f" | (redirect, weight 1) | {K} |\n")
print(res)
