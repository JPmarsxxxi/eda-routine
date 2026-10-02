import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from panel import build, COINS
from plotstyle import plt, save, PAL
P = build("EXPLORE", "p0_02"); cl = P["close"]
rows = []; miss_month = {}
for c in COINS:
    s = cl[c]; life = s.loc[s.first_valid_index():s.last_valid_index()]
    m = life.isna(); miss_month[c] = m.groupby(m.index.strftime("%Y-%m")).sum()
    # gap runs
    runs = (m != m.shift()).cumsum()[m]; lens = runs.value_counts() if m.any() else pd.Series(dtype=int)
    top_month = miss_month[c].idxmax() if m.any() else None
    top_share = miss_month[c].max() / m.sum() if m.any() else 0
    # whole-exchange? other coins live at those hours also missing?
    others = [o for o in COINS if o != c]
    live_o = cl[others].loc[m[m].index].notna().sum(1) if m.any() else pd.Series(dtype=float)
    frac_exch = (live_o == 0).mean() if m.any() else np.nan
    v = P["vol"][c].loc[life.index]
    rows.append(dict(coin=c, life_start=life.index[0], life_hours=len(life), missing=int(m.sum()), n_gaps=len(lens),
                     longest_gap_h=int(lens.max()) if len(lens) else 0, top_month=top_month, top_month_share=round(top_share, 3),
                     share_missing_when_all_others_missing=round(frac_exch, 3), zero_vol_bars=int((v == 0).sum()),
                     zero_vol_pct=round(100 * (v == 0).mean(), 4)))
T = pd.DataFrame(rows).set_index("coin")
T["finding_i_gt128"] = T.missing > 128
T["finding_ii_month"] = (T.top_month_share > 0.5) & (T.share_missing_when_all_others_missing < 0.5)
T["finding_iii_zero_vol"] = T.zero_vol_pct > 0.5
T.to_csv(os.path.join(os.path.dirname(__file__), "..", "tables", "p0_02_missing.csv"))
print(T.to_string())
MM = pd.DataFrame(miss_month).fillna(0)
print(MM[MM.sum(1) > 0].to_string())
fig, ax = plt.subplots(figsize=(9, 3.6))
ax.bar(range(len(MM)), MM.sum(1).values, color=PAL[0])
ticks = [i for i, k in enumerate(MM.index) if k.endswith("-01")]
ax.set_xticks(ticks); ax.set_xticklabels([MM.index[i][:4] for i in ticks])
ax.set_ylabel("missing coin-hours in month"); ax.set_title("Missing hours are exchange-wide outage clusters, total %d-%d per coin (EXPLORE)" % (T.missing.min(), T.missing.max()))
save(fig, "00_missingness")
