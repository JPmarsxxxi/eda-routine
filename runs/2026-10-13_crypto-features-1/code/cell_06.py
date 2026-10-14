import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_06"); C = B.S["close"]; lr = np.log(C)


def Rd(h, d, resp="primary"):
    # forward return from the END of bar t+d to the END of bar t+d+h; invalid if new_source in (t+d, t+d+h]
    R = B.R if resp == "primary" else B.RB
    return R[h].shift(-d)


rows = []; ics = {}
for k in (1, 2, 3, 6):
    base = -(lr - lr.shift(k)); skip1 = -(lr.shift(1) - lr.shift(1 + k))
    for h in HORIZONS:
        for name, F, d in (("base", base, 0), ("skip1", skip1, 0), ("delay1", base, 1), ("delay2", base, 2)):
            ic = xs_ic(F, Rd(h, d)); ics[(name, k, h)] = ic
            rep = slice_report(ic, h + 5 + d)
            rows.append(dict(c=name, k=k, h=h, **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}, tr=rep["TRAIN"]["mean"]))
for name, F, d in (("base", -(lr - lr.shift(2)), 0), ("delay1", -(lr - lr.shift(2)), 1)):
    for h in HORIZONS:
        ic = xs_ic(F, Rd(h, d, "binance")); rep = slice_report(ic, h + 5 + d)
        rows.append(dict(c=name + "_binResp", k=2, h=h, **{n: f"{rep[n]['mean']:+.4f}({rep[n]['t']:+.1f})" for n in rep}, tr=rep["TRAIN"]["mean"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250)
print(T.drop(columns="tr").to_string(index=False)); T.to_csv("cells/cell_06_table.csv", index=False)
print("\nBOUNCE SHARE: 1 - IC(delay1)/IC(base) at TRAIN:")
for k in (1, 2, 3, 6):
    for h in HORIZONS:
        b = T[(T.c == "base") & (T.k == k) & (T.h == h)].tr.iloc[0]; d1 = T[(T.c == "delay1") & (T.k == k) & (T.h == h)].tr.iloc[0]
        print(f"k{k} h{h}: base {b:+.4f} delay1 {d1:+.4f} share lost {1-d1/b:.0%}")
for k in (2, 3):
    ic = ics[("delay1", k, 6)]
    f = {n: nw(ic[in_slice(ic.index, n)], 12) for n in ("C1", "C2", "C3")}
    c23 = ic[in_slice(ic.index, "C2") | in_slice(ic.index, "C3")]
    print(f"PRIMARY k{k} h6 delay1: TRAIN {nw(ic[train_mask(ic.index)],12)['mean']:+.4f} (t {nw(ic[train_mask(ic.index)],12)['t']:.1f})  C1 {f['C1']['mean']:+.4f}(t{f['C1']['t']:.1f}) C2 {f['C2']['mean']:+.4f}(t{f['C2']['t']:.1f}) C3 {f['C3']['mean']:+.4f}(t{f['C3']['t']:.1f}) C2+C3 {nw(c23,12)['mean']:+.4f}")
fig, ax = plt.subplots(figsize=(8, 4))
for name in ("base", "skip1", "delay1", "delay2"):
    ic = ics[(name, 2, 1)]; rep = slice_report(ic, 6); ax.plot(["EXPLORE", "C1", "C2", "C3"], [rep[n]["mean"] for n in ("EXPLORE", "C1", "C2", "C3")], marker="o", label=name)
ax.axhline(0, color="#9b9a94", lw=.8); ax.legend(); ax.set_title("k=2 reversal IC at h1: base vs skip-1 vs entry delay, by fold")
fig.savefig("plots/cell_06_bounce.png", bbox_inches="tight")
