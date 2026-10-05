# OBSERVATIONS — Phase 0, all on EXPLORE (TRAIN start .. 2021-12-31)

Raw material for Phase 1 (mode E). Each entry: plot/table, slice, expected vs saw. Facts that are data identity/cleaning
(DATA_CARD.md) are listed separately at the bottom and are NOT observations to chase.

1. **Basis sawtooth on the funding clock.** `plots/00_6b_basis_cycle.png`, `tables/p0_6b_jump_by_funding.csv`,
   `tables/p0_6_hour_of_day.csv`. EXPLORE. Expected: the perp-spot basis has no structure at the settlement times beyond
   noise. Saw: the basis jumps +0.74 bp (SE 0.05) in the 30 min after each 00/08/16 UTC settlement vs -0.11 bp at a
   non-settlement placebo point, then decays -0.74 bp through the cycle. Both scale with the funding just paid (+1.48 /
   -2.12 bp when funding > 0.03%), and the within-cycle shape inverts under low/negative funding.
2. **Implied vol carries next-day realized-vol information beyond trailing RV.** `tables/p0_4b_partial_rv.csv`. EXPLORE
   (2021-04..12 only). Expected: DVOL adds a little beyond RV (it's an options-market forecast). Saw: raw Spearman with
   next-24h log RV 0.43, partial 0.17 after trailing 24h + 30d RV (n = 6,373, band 0.025).
3. **The half-spread series is mostly a volatility impostor.** `tables/p0_4b_partial_rv.csv`, `tables/p0_3_acf.csv`.
   EXPLORE. Expected: a spread measurement that is noisy and has an intraday shape. Saw: ACF1 0.995, flat by hour (1.06 ratio)
   while RV varies 1.48x, 0.66 correlated with trailing RV. Its 0.62 raw correlation with next-24h RV drops to 0.08
   partial after RV controls.
4. **Basis level predicts next-day realized vol beyond trailing RV.** `tables/p0_4_leadlag_screen.csv`,
   `tables/p0_4b_partial_rv.csv`. EXPLORE (2020-09..2021-12). Expected: nothing once RV is controlled. Saw: raw 0.29, partial
   0.15 after trailing 24h + 30d RV (n = 11,203, band 0.019). The basis is only 0.25 correlated with trailing RV itself.
5. **Basis and funding lean against next-day spot direction.** `tables/p0_4_leadlag_screen.csv`, `tables/p0_summary.json`
   (funding_spearman). EXPLORE. Expected: ~0. Saw: basis_bp vs next-24h r -0.058 (band 0.019); funding vs next-24h r -0.087
   (n = 1,433 overlapping 8h rows, so the effective n is ≈ 480 and this is inside the band ≈ 0.09). This is the crowd-positioning
   family (ALREADY TESTED list).
6. **Hourly spot return reversal, sign-unstable by era.** `tables/p0_3_acf.csv`, `tables/p0_5_eras.csv`. EXPLORE. Expected:
   ~0 at hourly after bounce. Saw: pooled ACF1 -0.053 (Spearman r vs next-1h r -0.078), but by era -0.084 / +0.005 / -0.076
   / +0.004: it alternates in sign, which is the noise signature.
7. **Lag-24 negative return autocorrelation.** `tables/p0_3_acf.csv`. EXPLORE. Expected: ~0. Saw: -0.046 (band 0.010).
   Same-hour-yesterday reversal. This is a time-of-day family (ALREADY TESTED: hour-of-day seasonality).
8. **DVOL level leans with next-day spot direction (positive).** `tables/p0_4_leadlag_screen.csv`, `tables/p0_extra.json`.
   EXPLORE, 9 months. Expected: ~0. Saw: +0.064 (band 0.025) pooled, positive in all three quarters (0.059, 0.087, 0.241),
   rising into the Q4-2021 top.
9. **Perp taker-buy ratio leans against next-day vol.** `tables/p0_4_leadlag_screen.csv`. EXPLORE. Expected ~0. Saw:
   log_taker vs next-24h log RV -0.20. Flow-imbalance family (ALREADY TESTED), and plausibly the leverage effect.
10. **The d_basis hourly change mean-reverts (ACF1 -0.23) and d_basis leans against next-hour spot return (-0.041).**
    `tables/p0_3_acf.csv`, `tables/p0_4_leadlag_screen.csv`. EXPLORE. Expected: a perp that leads spot would give a POSITIVE sign
    (spot catches up to perp). Saw: negative. The basis corrects by the perp leg, or it's the hourly-reversal impostor (#6).
11. **Weekend spread is LOWER than weekday** (half_bp 0.094 Sat vs 0.108 Mon) while volume is 0.72x. `tables/p0_6_day_of_week.csv`.
    EXPLORE. Expected wider on thin weekends. Saw the opposite, which is consistent with #3 (half_bp tracks vol, and vol is
    lower on weekends).
12. **Funding is pinned at the default 0.0100% on 46.8% of settlements**, with persistence ACF1 0.77. `tables/p0_1_distributions.csv`.
    EXPLORE. Descriptive: funding is a clamp of the premium index, so its information sits in departures from 0.01%.

Identity / data facts (DATA_CARD.md, not observations to chase): price files are SPOT; half_bp coverage 35-79% by year;
OI == 0 on one hour; 1m file has no VAL.
