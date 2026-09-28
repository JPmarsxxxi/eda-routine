"""Step 4c plot (BH) and Step 5 Bayes ranking. No data loaded: reads tables only."""
from lib import *
from scipy import stats

P = pd.read_csv(os.path.join(RUN, "tables", "15_bh_adjusted_pvals.csv"))
K = len(P)
fig, ax = plt.subplots(figsize=(10, 4))
ps = np.sort(P.p.clip(lower=1e-300).values)
ax.plot(np.arange(1, K + 1), -np.log10(ps), "o", color=PAL[0], label="sorted raw p")
ax.plot(np.arange(1, K + 1), -np.log10(0.05 * np.arange(1, K + 1) / K), color=GRAY, label="BH 5% line")
ax.set_xlabel("rank"); ax.set_ylabel("-log10 p"); ax.set_yscale("symlog", linthresh=10); ax.legend()
ax.set_title(f"15: {int(P.survives_bh_5pct.sum())} of K={K} sweep tests survive Benjamini-Hochberg at 5% (most are the 1-min null facts)", fontsize=10)
save(fig, 15, "bh_adjustment")

def lr_p(t, K):
    p = 2 * stats.norm.sf(abs(t)); pk = min(1.0, K * p)
    return (1.0 if pk >= 1 / np.e else 1 / (-np.e * pk * np.log(pk))), p, pk

def lr_era(s, m=7, q=0.8):
    return (q ** s * (1 - q) ** (m - s)) / (0.5 ** m)

leads = [
    # name, kind, prior, robust-check t (the (a) twin-controlled check), eras same sign (of 7)
    ("OBS5 |hourly r| by UTC hour (h00 > h05)", "size", 0.50, 13.286, 7),
    ("OBS6 weekend |daily r| lower", "size", 0.50, -8.051, 7),
    ("OBS1 trailing 5-min r -> fwd 5-min r (reversal)", "direction", 0.05, -8.666, 6),
    ("OBS4 21-23 UTC mean return (known prior)", "mean", 0.05, 2.641, 6),
]
rows = []
for n, kind, pr, t, s in leads:
    lp, p, pk = lr_p(t, K); le = lr_era(s); lr = min(lp, le)
    po = pr / (1 - pr) * lr
    rows.append(dict(lead=n, kind=kind, prior=pr, prior_odds=pr / (1 - pr), check_t=t, p=p, p_times_K=pk, LR_pvalue_bound=lp,
                     eras_same_sign=s, LR_eras=le, LR_used=lr, posterior_odds=po, posterior=po / (1 + po)))
B = pd.DataFrame(rows).sort_values("posterior", ascending=False); table(B.set_index("lead"), 23, "bayes_ranking"); print(B.round(4).to_string())
fig, ax = plt.subplots(figsize=(10, 3.6))
ax.barh(B.lead, B.prior, color=GRAY, label="prior"); ax.barh(B.lead, B.posterior, left=0, color=PAL[0], alpha=0.6, label="posterior")
ax.set_xlim(0, 1); ax.invert_yaxis(); ax.legend(); ax.tick_params(axis="y", labelsize=8); ax.set_xlabel("probability")
ax.set_title(f"23: size claims rank first ({B.posterior.iloc[0]:.2f}); reversal {B[B.lead.str.startswith('OBS1')].posterior.iloc[0]:.2f}; 21-23 UTC {B[B.lead.str.startswith('OBS4')].posterior.iloc[0]:.2f}", fontsize=10)
save(fig, 23, "bayes_ranking")
