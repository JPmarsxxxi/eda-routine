import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build
from daily import daily
from tests import fm_interaction
from plotstyle import plt, save, PAL, GRAY
TB = os.path.join(os.path.dirname(__file__), "..", "tables")
P = build("EXPLORE", "cell_05"); R, REL, V, QV = daily(P)
shock = np.log(V / V.shift(1).rolling(30, min_periods=20).median()); Y = REL.shift(-1)
rows = {}
rows["ALL"] = fm_interaction(Y, REL, shock, min_n=6)
rk = lambda X: X.rank(axis=1)
rows["ALL_rank"] = fm_interaction(Y, rk(REL.where(shock.notna())), rk(shock.where(REL.notna())), min_n=6)
for e, (a, b) in {"2018": ("2018", "2018"), "2019": ("2019", "2019"), "2020": ("2020", "2020"), "2021H1": ("2021", "2021")}.items():
    rows[e] = fm_interaction(Y.loc[a:b], REL.loc[a:b], shock.loc[a:b], min_n=6)
D = pd.DataFrame(rows, index=["b3", "se", "z", "days"]).T; D["b3_bp"] = D.b3 * 1e4
print(D[["b3_bp", "z", "days"]].round(2).to_string())
z0 = D.loc["ALL", "z"]; era_z = D.loc[["2018", "2019", "2020", "2021H1"], "z"]
if z0 < -1.645: branch = "opposite sign"
elif z0 > 1.645 or (abs(z0) <= 1.645 and (era_z.abs() > 2).sum() == 1): branch = "subset only"
else: branch = "absent everywhere"
print("REDIRECT BRANCH:", branch)
D.to_csv(os.path.join(TB, "cell_05_redirect_h4.csv"))
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ks = ["2018", "2019", "2020", "2021H1", "ALL"]
ax.bar(ks, D.loc[ks, "b3_bp"], color=[GRAY] * 4 + [PAL[0]])
ax.errorbar(range(5), D.loc[ks, "b3_bp"], yerr=1.645 * D.loc[ks, "se"] * 1e4, fmt="none", ecolor="#52514e")
ax.axhline(0, color=GRAY, lw=1); ax.axhline(-14.5, color=PAL[7], ls="--", lw=1, label="CONFIRM b3 (cell_04) -14.5 bp")
ax.set_ylabel("interaction b3, bp per 1sd x 1sd"); ax.legend(); ax.set_title(f"Redirect (EXPLORE): b3 {D.loc['ALL','b3_bp']:.1f} bp, z {z0:.2f} -> {branch}")
save(fig, "cell_05_redirect_h4")
