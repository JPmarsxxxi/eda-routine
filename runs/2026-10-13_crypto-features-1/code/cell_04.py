import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_04"); C = B.S["close"]; tr = train_mask(C.index)
r24 = -np.log(C / C.shift(24))
prof = {}; ics = {}
for h in HORIZONS:
    ic = xs_ic(r24, B.R[h]); ics[h] = ic
    g = ic[tr].groupby(ic[tr].index.hour)
    prof[h] = {a: nw(g.get_group(a), h // 24 + 3) for a in range(24)}
tab = pd.DataFrame({h: [prof[h][a]["mean"] for a in range(24)] for h in HORIZONS}).round(4)
tabt = pd.DataFrame({h: [prof[h][a]["t"] for a in range(24)] for h in HORIZONS}).round(1).add_prefix("t")
print("r24 reversal IC by anchor hour:"); print(pd.concat([tab, tabt], axis=1).to_string())
def group(ic, hours, h):
    x = ic[ic.index.hour.isin(hours)]
    d = x.groupby(x.index.floor("D")).mean(); d.index = d.index + pd.Timedelta(hours=23)  # stamp
    return d
groups = {"ASIA(21,22,23,0,1)": [21, 22, 23, 0, 1], "US(13-16)": [13, 14, 15, 16], "EU(7-11)": [7, 8, 9, 10, 11], "other": [2, 3, 4, 5, 6, 12, 17, 18, 19, 20]}
for h in HORIZONS:
    print(f"\nh={h} session groups (daily-collapsed):")
    for gname, hrs in groups.items():
        d = group(ics[h], hrs, h); rep = slice_report(d, h // 24 + 3)
        print(f"  {gname:20s}", fmt_rep(rep))
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
for i, h in enumerate(HORIZONS):
    ax[i].bar(range(24), tab[h].values, color=["#e34948" if a in (21,22,23,0,1) else ("#008300" if a in (13,14,15,16) else "#2a78d6") for a in range(24)]); ax[i].axhline(0, color="#9b9a94", lw=.8); ax[i].set_title(f"r24 reversal IC by anchor hour, h={h}")
fig.savefig("plots/cell_04_r24_session.png", bbox_inches="tight")
a = group(ics[6], groups["ASIA(21,22,23,0,1)"], 6); u = group(ics[6], groups["US(13-16)"], 6)
ra, ru = nw(a[train_mask(a.index)], 3), nw(u[train_mask(u.index)], 3)
print("\nPRIMARY h6: ASIA", round(ra["mean"], 4), round(ra["t"], 2), " US", round(ru["mean"], 4), round(ru["t"], 2))
