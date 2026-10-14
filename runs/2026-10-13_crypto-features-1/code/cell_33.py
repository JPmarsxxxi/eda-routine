import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from fx import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = Base("cell_33"); S = B.S; C = S["close"]; lr = np.log(C); ix = C.index; tr = train_mask(ix)
r = lr.diff()
def season(N):
    acc = sum(r.shift(24 * j - 1) for j in range(1, N + 1)); cnt = sum(r.shift(24 * j - 1).notna().astype(int) for j in range(1, N + 1))
    return (acc / cnt).where(cnt >= int(0.8 * N))
s60 = season(60); s20 = season(20)
V = {"season60_dm": s60 - r.rolling(24 * 60, min_periods=864).mean(), "season20_sign": np.sign(s20 - r.rolling(24 * 20, min_periods=288).mean())}
rows = []; ics = {}
for name, x in V.items():
    for h in (1, 6):
        for resp, RR in (("primary", B.R), ("binance", B.RB)):
            ic = xs_ic(x[tr], RR[h][tr]); ics[(name, h, resp)] = ic; rep = slice_report(ic, h + 5)
            c23 = ic[in_slice(ic.index, "C2") | in_slice(ic.index, "C3")]; m23 = nw(c23, h + 5)
            rows.append(dict(variant=name, h=h, resp=resp, **{k: f"{rep[k]['mean']:+.4f}({rep[k]['t']:+.1f})" for k in rep}, c23=f"{m23['mean']:+.4f}({m23['t']:+.1f})", tr=rep["TRAIN"]["mean"], t=rep["TRAIN"]["t"], c23m=m23["mean"]))
T = pd.DataFrame(rows); pd.set_option("display.width", 250); T.to_csv("cells/cell_33_table.csv", index=False)
print(T.drop(columns=["tr", "t", "c23m"]).to_string(index=False))
# hour-of-day decomposition, season60_dm h1, C2+C3, both responses (signal hour u = hour of next bar)
dec = {}
for resp in ("primary", "binance"):
    ic = ics[("season60_dm", 1, resp)]; ic = ic[in_slice(ic.index, "C2") | in_slice(ic.index, "C3")]
    u = (ic.index.hour + 1) % 24; dec[resp] = ic.groupby(u).mean()
D_ = pd.DataFrame(dec).round(4); print("\nIC by upcoming-hour u (C2+C3), season60_dm h1:"); print(D_.T.to_string())
p = T[(T.variant == "season60_dm") & (T.h == 1) & (T.resp == "binance")].iloc[0]
print("\nPRIMARY (Binance response, h1): TRAIN", round(p.tr, 4), round(p.t, 2), " C2+C3", round(p.c23m, 4))
print("supported:", bool(p.tr >= .02 and p.t >= 1.96 and p.c23m >= .015), " refuted:", bool(p.tr <= .01))
fig, ax = plt.subplots(figsize=(10, 4)); D_.plot.bar(ax=ax); ax.axhline(0, color="#9b9a94"); ax.set_title("season60_dm h1 IC by upcoming hour of day, C2+C3")
fig.savefig("plots/cell_33_hours.png", bbox_inches="tight")
