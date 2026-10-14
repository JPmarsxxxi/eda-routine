import sys, os, json, re, glob, datetime
sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code"); sys.path.insert(0, r"C:\Users\User\eda-routine")
import kit, gate

RUN = kit.RUN; RN = os.path.basename(RUN)
W = lambda p, t: open(p, "w", encoding="utf-8").write(t)
st = kit.load_state()
start = datetime.datetime.strptime(open(os.path.join(RUN, "START.txt")).read().strip(), "%Y-%m-%dT%H:%M:%SZ")
now = datetime.datetime.utcnow()
minutes = round((now - start).total_seconds() / 60)

# ---------------- stop reason
rep = gate.GateReport(RUN)
folds = gate.check_splits(RUN, rep)
cells = gate.check_cells(RUN, folds, rep)
kt, kv = gate.k_counts(cells)
nopen = sum(1 for h in st.values() if h["state"] == "OPEN"); ndrop = sum(1 for h in st.values() if h["state"] == "DROPPED")
nfroz = len(glob.glob(os.path.join(RUN, "candidates", "F*.md")))
W(os.path.join(RUN, "STOP_REASON.md"), f"""rule: S2
open_count: {nopen}
dropped_count: {ndrop}
frozen_count: {nfroz}
val_pass_count: 1
minutes: {minutes}
detail: S2 (dry): the last 8 cells (43-50) are search cells (H16 rival control, H4, H10, H6, H13 x3, H17) and none led to a frozen candidate (F10, the last freeze, precedes cell 41). Cells used {len(cells)} of the 60 cap, {minutes} of 180 minutes. All 10 frozen specs have their confirm cell; the 5 CONFIRM-SHOWN (F1, F2, F3, F5, F8) have their VAL cell. S1 does not apply ({nopen} hypotheses still OPEN).
""")

# ---------------- belief table
by_cell = {}
for nn, head, w in kit._cell_heads():
    by_cell.setdefault(head.get("hypothesis"), []).append((nn, head.get("kind"), head.get("slice"), w))
fc = {}
for p in glob.glob(os.path.join(RUN, "candidates", "F*.md")):
    t = open(p, encoding="utf-8").read(); fc.setdefault(re.search(r"(?m)^hypothesis:\s*(H\d+)", t).group(1), []).append(re.search(r"(F\d+)\.md", p).group(1))
children = {}
for h, v in st.items():
    if v["parent"] != "none": children.setdefault(v["parent"], []).append(h)
tbl = "| H | title | prior -> posterior | state | evidence chain (cell: kind slice weight) | children | candidates |\n|---|---|---|---|---|---|---|\n"
for h in sorted(st, key=lambda x: int(x[1:])):
    v = st[h]; ev = "; ".join(f"{nn}: {k} {sl} x{w:.2f}" for nn, k, sl, w in by_cell.get(h, []) if w is not None)
    tbl += f"| {h} | {v['title'][:70]} | {v['prior']:.2f} -> {kit.posterior(h):.3f} | {v['state']} | {ev} | {', '.join(children.get(h, [])) or '-'} | {', '.join(sorted(fc.get(h, []), key=lambda x: int(x[1:]))) or '-'} |\n"

cj = {}
for f in glob.glob(os.path.join(RUN, "work", "confirm_*.json")):
    o = json.load(open(f)); cj[os.path.basename(f)[8:-5]] = o
vj = {}
for f in glob.glob(os.path.join(RUN, "work", "val_*.json")):
    o = json.load(open(f)); vj[os.path.basename(f)[4:-5]] = o
CAND = [("F1", "H3", "none", "f001", "f001", "f001"), ("F2", "H9", "none", "f002", "f002", "f002"), ("F3", "H10", "none", "f003", "f003", "f003"),
        ("F4", "H5", "none", "f004 h24", "f004", None), ("F5", "H2", "none", "f005", "f005", "f005"), ("F6", "H7", "none", "f006", "f006", None),
        ("F7", "H1", "none", "f007", "f007", None), ("F8", "H5", "F4", "f004 h1", "F8", "F8"), ("F9", "H14", "none", "f008", "F9", None), ("F10", "H5", "none", "f009", "F10", None)]
ct = "| F | hypothesis | variant_of | feature (primary h) | C1 | C2 | C3 | CONFIRM | VAL (2023-03-25..2023-11-30) |\n|---|---|---|---|---|---|---|---|---|\n"
for F, h, vo, ft, ck, vk in CAND:
    o = cj[ck]; f = o["folds"]
    cells3 = " | ".join(f"{f[n]['mean']:+.4f} (t {f[n]['t']:+.1f}) {f[n]['branch'][:5]}" for n in ("C1", "C2", "C3"))
    val = "not run" if vk is None else f"{vj[vk]['val']['mean']:+.4f} (t {vj[vk]['val']['t']:+.2f}) {vj[vk]['val']['branch']}"
    ct += f"| {F} | {h} | {vo} | {ft} (h{o['primary_h']}) | {cells3} | {'SHOWN' if o['shown'] else 'FAIL'} | {val} |\n"

W(os.path.join(RUN, "REPORT.md"), f"""# REPORT - run {RN} (job: features; mode E, data-only; target: forward return of the 10-coin primary panel at 1h / 6h / 24h)

**Source mode and item:** E (Phase 0 observations plus the two TARGET.md seeds, Alpha#30 and minus Alpha#54); no INBOX item used. **Data:** crypto_panel_validated_2026-10-05 (guard-bounded at TRAIN <= 2023-03-19 in every search cell; VAL opened only by the 5 `val` cells). **Stop:** S2 at {len(cells)} cells, {minutes} minutes. K_train {kt}, K_val {kv}; K_cum_train {124 + kt}, K_cum_val {1 + kv} for this dataset.

## What the run found, in one paragraph
Ten specs were frozen from TRAIN searches; five were CONFIRM-SHOWN and reached VAL, five failed CONFIRM (F4, F6, F7, F9, F10). **One passed VAL: F8, the detrended perp premium-index crowding feature (f004) at h1** (VAL IC +0.0210, NW t 4.7; CONFIRM folds +0.021 / +0.034 / +0.020), and its same-code h24 spec F4 failed CONFIRM by a hair (+0.0186, +0.0190, +0.0253). Four reached VAL and came back **inconclusive** (right sign, under the 0.02 bar): the bounce-free 3-hour reversal f001 (+0.0141, t 1.99), the session-gated 24h reversal f002 (+0.0284, t 1.93), the trade-count surprise f003 (+0.0201, t 1.38), closing strength f005 (+0.0164, t 1.14).
The seeds: **Alpha#30's content is the sign-streak fade, not the volume scale** (volume scale subtracts: -0.0105 at h6, t -1.3), it lives at the UTC day boundary / Asia-hour window, and as written (f007) it fades in C2/C3; **the C3 fade is NOT the response switch** (scoring against the Binance close instead of the FTMO mid does not recover the seed's C3 IC). **Minus Alpha#54** (f005) is a 24h continuation concentrated in 2021H2 with an opposite-signed 1-6h reversal; it survives a trend split but not VAL.
Two methodological findings matter more than any single feature: (1) **about half of every 1-6h Binance-print reversal IC is the bid-ask bounce** (a one-bar entry delay removes 41-69%; cells 6, 14, 38-39); (2) **every slowly moving level feature (volatility, long/short ratio, beta, open interest) shows a large in-sample IC that is a coin fixed effect on 10 coins** and disappears when the coin's own mean is removed (cells 11, 29, 31, 49).

## Beliefs (prior -> posterior, with the evidence chain)
{tbl}
Weights are capped at 3x for search cells and 10x for confirm / VAL cells. Priors and anchors are in BELIEFS.md. OPEN hypotheses at the stop are listed in STOP_REASON.md; H6 and H14 were DROPPED (DECISIONS.md).

## Candidates (all frozen before their confirm cell; sha256 in each VAL cell)
{ct}
CONFIRM-SHOWN = at least 2 of 3 folds supported (IC >= 0.02 and NW t >= 1.96) and none refuted. A fold can be 'inconclusive' simply because its standard error (about 0.007-0.017 for hourly sampling, 0.035 for daily) is large relative to 0.02.

## Cost line (TRAIN, top-3 minus bottom-3 forward return per signal at the primary horizon vs 2 x the mean round trip of the traded names)
Every feature is COMBINE-ONLY: gross spreads of -4.6 to +23.5 bp (f001 -0.75 at h6, f002 -4.59 at h6, f003 +23.5 at h24, f004 +6.0 at h24 / +2.1 at h1, f005 +20.8 at h24, f006 +2.2, f007 +18.5, f008 +2.1 at h1, f009 +4.7 at h24) against about 87 bp round trip. Rank IC 0.02-0.04 with a near-zero extreme-quantile spread means the effects sit in the middle of the ranks and in the lower-volatility coins, not in the tails dominated by DOGE and SOL.

## K (counted, never capped)
K_train = {kt} (sum of `variants:` over the search cells plus one per confirm cell), K_val = {kv} (F1, F2, F3, F5, F8). K_cum_train = {124 + kt}, K_cum_val = {1 + kv} for crypto_panel_validated_2026-10-05 (previous runs: 124 and 1).

## Part-0 finding blocks (one per candidate that reached VAL)
**F8 / f004 - perp premium crowding, h1 (VAL-PASS).** 1b finding: *a change in a coin's perp premium-index close relative to its own trailing-720h mean, net of its trailing 3-hour and 24-hour returns, predicts a LOWER cross-sectional rank of its next-1h primary return because leveraged long crowding is unwound through the premium/funding mechanism.* Supported on CONFIRM folds C1 +0.0213 (t 4.1), C2 +0.0336 (t 6.0), C3 +0.0195 (t 4.3, just under 0.02) and on VAL +0.0210 (t 4.7; monthly IC -0.025 in March, +0.014..+0.042 from April to October, -0.004 in November). It survives the coin fixed-effect control (66-88% of the raw IC kept), the trailing-return reversal control, the market-premium regime split (both states +0.022..+0.024 at h6) and has max |corr| 0.05 with every other candidate and baseline. VAL is weak evidence (note in TARGET.md).
**F1 / f001 - bounce-free 3-hour reversal, h6 (VAL-FAIL, inconclusive).** 1b finding: *a change in a coin's trailing return over bars t-3..t-1 predicts the opposite sign for the cross-sectional rank of its return over the next 6 hours because overnight order-flow overshoots revert.* CONFIRM C1 +0.0174 (t 2.3, under the bar) / C2 +0.0445 / C3 +0.0372; VAL +0.0141 (t 1.99). The unlagged version (IC +0.058) is the Binance last-print bounce and was not frozen. Strong in 21-06 UTC signals (+0.059 at h6), absent at 13-16 UTC.
**F2 / f002 - 24h reversal in 21-06 UTC signals, h6 (VAL-FAIL, inconclusive).** CONFIRM +0.0433 / +0.0361 / +0.0191; VAL +0.0284 (t 1.93, a hair under the 1.96 bar); incremental IC against the plain trailing-24h reversal baseline is negative (it is that baseline, gated).
**F3 / f003 - 1h trade-count surprise net of the move, h24 (VAL-FAIL, inconclusive).** CONFIRM +0.0319 / +0.0113 / +0.0512; VAL +0.0201 (t 1.38, 4,884 hours: IC at the bar, t short of the bar); session-independent (cell 45); C2 (2022H1 bear) is its weak fold.
**F5 / f005 - closing strength, h24 (VAL-FAIL, inconclusive).** CONFIRM +0.0766 / +0.0262 / +0.0279; VAL +0.0164 (t 1.14); the 1-6h IC has the opposite sign (-0.035 / -0.021); the C1 fold (2021H2) carries most of the h24 TRAIN IC.

## Leads and observations not chased
- dd_336 incremental piece (H16): the 14-day drawdown, detrended and net of r3s / r24 / r72, has IC +0.0220 at h24 (t 2.9; folds +0.010 / +0.030 / +0.020) and +0.0161 at h6; not frozen because per-fold se (0.017) makes a fold test uninformative; a pooled-sample feature for a combiner.
- Static low-beta ranking (H13): IC +0.0234 (h1), +0.0400 (h6) in all folds, +0.041/+0.059 in market-up states; a coin attribute (BTC/ETH vs DOGE/SOL), not registered. Time-varying beta carries nothing.
- Hour-of-day seasonality persistence (H14, f008): IC +0.0222 at h1 (t 8.3) but only C3 passes (+0.0451); DROPPED as a feature, COMBINE-only lead.
- Funding beyond the premium (H5, f009): +0.0171 at h24 (t 3.0), C2 t 1.96 and C3 +0.0281; CONFIRM-FAIL.
- Taker-buy imbalance in US-hour signals at h24: +0.0243 (t 3.2, under Sidak 3.36; C1 +0.002). Upbit premium residual at h6: +0.0137 (t 2.6). rng_24 detrended h6: wrong-signed +0.0180.
- The 60-day same-hour return mean beats the single same-hour-yesterday return (-0.0057): persistence needs averaging.
- NO-STORY entries: none flagged; all hypotheses had a mechanism sentence.

## Judge verdict
(appended after the eda-v3-judge run)
""")
print("stop+report written; K", kt, kv, "minutes", minutes, "open", nopen)
