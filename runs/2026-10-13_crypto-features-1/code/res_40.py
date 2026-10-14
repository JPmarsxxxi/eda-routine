import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 40 result - H5: do basis / funding add to the premium feature f004? (TRAIN, hourly; 18 variants; cells/cell_40_table.csv, cells/cell_40_output.txt, plots/cell_40_basis_funding.png)
Pre-committed branch: SUPPORTED. Best form-(c) variant: funding_dtr (funding minus the coin's trailing-720h mean) residualised on r3s, r24 AND f004, at h24: score (-IC) +0.0172 (NW t +3.04; EXPLORE +0.009, C1 +0.014, C2 +0.031, C3 +0.029), bars: score >= 0.015, t >= Sidak 2.64, same sign in C2 and C3. weight_applied 3.0 (cap).
(The cell's printed check line carried a sign slip on the t and C2/C3 conditions - it printed `supported: False` - the rule is applied as written in the rule file: score +0.0172 >= 0.015, t +3.04 >= 2.64, C2 and C3 positive in score = -IC. Recorded in DECISIONS.md D8.)
Basis does NOT add: basis_dtr form (c) is within +-0.011 at every horizon (h1 -0.0059, h6 +0.0022, h24 +0.0092 with C1/C2 ~0): the basis is the premium's twin (mean XS correlation 0.50 with f004). Funding adds a piece at h24 only: the form-(b) funding_dtr at h24 is +0.0199 (t 3.0), after f004 +0.0172 (t 3.0); at h1/h6 form (c) is <= 0.003 / negative.
Funding_dtr correlation with f004: 0.24; its per-fold form-(c) h24 profile +0.009/+0.014/+0.031/+0.029 (EXPLORE and C1 have funding only from 2020; 32-60% of EXPLORE hours). A candidate (F10) can be frozen at h24: expected folds C2 and C3 supported, C1 inconclusive.
"""
kit.result(40, 3.0, variants=18, suggests="none", body=body)
kit.attempt(40, "H5", "basis/funding detrended, forms a/b/c (resid r3s, r24, f004) x h", "funding_dtr|f004 h24 +0.0172 t 3.0: supported (incremental); basis = premium twin")
kit.write_beliefs(); print(kit.posterior("H5"))
