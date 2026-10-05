import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build
from daily import daily
from tests import nscore, nw_se
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("EXPLORE", "cell_07"); R, REL, V, QV = daily(P)
Z = nscore(R); prod = Z * Z.shift(-1); big = R.abs().ge(R.abs().quantile(.9)) & R.notna()
def ic(mask, sl=slice(None)):
    c = prod.where(mask).loc[sl].mean(axis=1).dropna(); se, n = nw_se(c.values); return c.mean(), se, c.mean() / se, n
rows = {"ALL": ic(R.notna()), "BIG10": ic(big), "OTHER": ic(~big & R.notna())}
for e, (a, b) in {"2017H2-18": ("2017", "2018"), "2019": ("2019", "2019"), "2020": ("2020", "2020"), "2021H1": ("2021", "2021")}.items():
    rows[f"BIG10_{e}"] = ic(big, slice(a, b)); rows[f"OTHER_{e}"] = ic(~big & R.notna(), slice(a, b))
D = pd.DataFrame(rows, index=["ic", "se", "z", "days"]).T; print(D.round(4).to_string())
zb, zo, za = D.loc["BIG10", "z"], D.loc["OTHER", "z"], D.loc["ALL", "z"]
if za > 1.645: branch = "opposite sign"
elif zb < -1.645 and zo < -1.645: branch = "everywhere"
elif zb < -1.645 and abs(zo) <= 1.645: branch = "extreme-days only"
else: branch = "absent everywhere"
# gross next-day move after big down / big up days (bp), descriptive
nx = R.shift(-1); dn = nx.where(big & (R < 0)).stack().mean() * 1e4; up = nx.where(big & (R > 0)).stack().mean() * 1e4
print(f"after big DOWN days next-day {dn:.1f} bp; after big UP days {up:.1f} bp")
print("REDIRECT BRANCH:", branch)
D.to_csv(os.path.join(TB, "cell_07_redirect_h1.csv"))
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ks = ["2017H2-18", "2019", "2020", "2021H1"]; x = np.arange(4); w = .38
ax.bar(x - w / 2, [D.loc[f"BIG10_{k}", "ic"] for k in ks], w, color=PAL[0], label="top-10% |r| days")
ax.bar(x + w / 2, [D.loc[f"OTHER_{k}", "ic"] for k in ks], w, color=GRAY, label="other days")
ax.set_xticks(x); ax.set_xticklabels(ks); ax.axhline(0, color=GRAY, lw=1); ax.set_ylabel("day->next-day normal-score IC"); ax.legend()
ax.set_title(f"Redirect (EXPLORE): big-day IC {D.loc['BIG10','ic']:.3f} (z {zb:.1f}) vs other {D.loc['OTHER','ic']:.3f} -> {branch}")
save(fig, "cell_07_redirect_h1")
