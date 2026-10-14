weight_applied: 0.9000
variants: 72
suggests: H9; not pursued: mid-tercile peak of market-vol split (non-monotone, no mechanism), rev24s h24 sign flips by fold

# cell 07 result - H3 conditional split of the bounce-free reversal (TRAIN, hourly; 72 variants; cells/cell_07_table.csv, cells/cell_07_output.txt, plots/cell_07_conditions.png)
Pre-stated primary (rev3s, high-vs-low market-vol tercile, h1/h6, 'paired by day'): the paired design is INFEASIBLE (a day sits almost entirely in one volatility tercile: 1 shared day). Deviation recorded: independent-sample difference with se = sqrt(se_a^2 + se_b^2) from the two NW t's.
h1: high +0.0254 (t 6.3) vs low +0.0215 (t 4.6): diff +0.0039, t ~0.6. h6: high +0.0224 (t 3.9) vs low +0.0248 (t 3.6): diff -0.0024, t ~ -0.3. No difference >= +0.01, none <= 0 with t <= -1.65 -> INCONCLUSIVE (no-branch), weight_applied 0.90.
So market volatility does not modulate the reversal (the MIDDLE tercile is the strongest at h6, +0.038, t 8.0, probably noise). Own-volatility (high-vol vs low-vol half of the cross-section) also does not: rev3s h6 +0.021 vs +0.018 (diff +0.0007, t 0.09). Recent market move (down/flat/up): h6 +0.035/+0.029/+0.027, diff down-up +0.003 (t 0.3).
SESSION is the conditional that matters, at both features: rev3s h6 ASIA(21-01) +0.0589 (t 8.8; EXPLORE +0.061, C1 +0.046, C2 +0.059, C3 +0.064 - 4/4 and stable), other +0.040 (t 8.4), EU(07-11) +0.010 (t 1.5), US(13-16) -0.005 (t -0.7); paired ASIA - US = +0.064 (t 7.0, 1169 days) at h6, +0.040 (t 5.1) at h1.
rev3s h1: ASIA +0.035, other +0.035, EU +0.024, US -0.008. rev24s h6: ASIA +0.036 (t 4.2), other +0.026, EU +0.018, US -0.015 (C3 -0.064, t -3.1); rev24s h24 is flat to negative (US -0.003..-0.05), rev3s h24 ASIA +0.025.
Reading: the reversal is an overnight-hours effect: strongest when the signal is formed 21-06 UTC and absent for US-hours (13-16) signals, in line with cell 4. A feature that carries only the sign of the session is a gate, not a rank change; the library gets a session-gated variant of rev3s. This is H9 (child of H8): amplitude clock.
suggests: H9 (session-gated reversal). Not pursued: mvol middle-tercile peak (t 8.0 at h6; not monotone, no mechanism); rev24s h24 sign flips by fold (noise at the 24h horizon).
