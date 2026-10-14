import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
w, cap = kit.capped(0.0, "search")   # no-branch with power ~1.0: (1-power)/(1-alpha) ~ 0 -> floor 1/3
body = """# cell 34 result - H14 / H5 orthogonality, incremental IC and cost line (TRAIN; 6 variants; cells/cell_34_output.txt, work/cell34_stats.json, plots/cell_34_f008_corr.png)
Pre-committed branch: NOT SUPPORTED (inconclusive), on a measurement artifact that the pre-stated rule did not foresee, reported as it happened. Leg 1 passes: max |corr| of f008 with any other candidate or baseline = 0.024 (f006); the seasonality feature is orthogonal to everything
(f001 +0.01, f002 0.00, f003 0.00, f004 0.00, f005 -0.01, f007 -0.01, b_rev1 -0.01, b_rev24 0.00, b_mom168 0.00, b_lowvol 0.00, b_liq -0.01). Leg 2 fails as computed: the 'two most correlated others' were f006 and f007, which exist only at the 23:00 bar, so the residualised series had 969 rows (IC +0.0187, t +1.61, not >= 1.96).
With correlations of ~0.00-0.02 the partialling is a no-op; the incremental IC with dense partners is reported separately in work/supp_f008_inc.json (supplementary, not a cell; see DECISIONS.md D7). The rule is applied as written: weight_applied 0.333 (the power-1.0 no-branch floor).
f008 IC by horizon (TRAIN): h1 +0.0222 (t 8.3; EXPLORE +0.017, C1 +0.017, C2 +0.009, C3 +0.045), h6 +0.0095 (t 3.7), h24 +0.0009 (t 0.4): a one-hour effect. Per fold only C3 reaches the 0.02 bar; the freeze rule is applied unchanged.
f004 at h1 (the variant under preparation): max |corr| 0.05 (b_rev1); residual IC after b_rev1/f005 = +0.0248 (t +11.4; folds +0.023/+0.023/+0.032/+0.025) - larger than the h24 IC (+0.0249) with per-fold t of 4.4-6.9 at h1.
Cost line at h1: f008 gross top-3 minus bottom-3 +2.13 bp (n 20,510), f004 +2.12 bp (n 25,971) vs ~88 bp round trip: both COMBINE-ONLY.
"""
kit.result(34, w, variants=6, suggests="none", body=body)
kit.attempt(34, "H14", "orthogonality/incremental/cost of f008 and f004-h1", "f008 max corr 0.024 but incremental leg mis-specified (sparse partners): inconclusive per rule; both COMBINE-ONLY")
kit.write_beliefs(); print(kit.posterior("H14"))
