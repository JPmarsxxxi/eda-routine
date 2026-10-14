import os, re, itertools
from scipy import stats

RUN = r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1"


def confirm_weights(ses, delta=0.02, tcrit=1.96, need=2, cap=10.0):
    """weights for a confirm cell: outcome 'CONFIRM-SHOWN' (>= need of n folds supported). Per-fold power from each fold's own se;
    null: each fold 'supported' with the one-sided alpha at tcrit."""
    a = float(1 - stats.norm.cdf(tcrit))
    ps = [float(1 - stats.norm.cdf(tcrit - delta / se)) for se in ses]

    def p_at_least(pl):
        tot = 0.0
        for combo in itertools.product([0, 1], repeat=len(pl)):
            if sum(combo) >= need:
                pr = 1.0
                for c, p in zip(combo, pl):
                    pr *= p if c else (1 - p)
                tot += pr
        return tot
    PH, P0 = p_at_least(ps), p_at_least([a] * len(ps))
    wy, wn = PH / P0, (1 - PH) / (1 - P0)
    return dict(P_H=PH, P_0=P0, fold_power=ps, w_yes=wy, w_no=wn, applied_yes=min(wy, cap), applied_no=max(wn, 1 / cap))


def hyp_of(fid):
    t = open(os.path.join(RUN, "candidates", f"{fid}.md"), encoding="utf-8").read()
    return re.search(r"(?m)^hypothesis:\s*(H\d+)", t).group(1)


def pass_rule_of(fid):
    t = open(os.path.join(RUN, "candidates", f"{fid}.md"), encoding="utf-8").read()
    return re.search(r"(?m)^pass_rule:\s*(.*)$", t).group(1)
