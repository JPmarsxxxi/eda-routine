# OBSERVATIONS — Phase 0, all on EXPLORE (2019-01-01 -> 2021-07-01)

Raw material for Phase 1 (mode E: every hypothesis must trace to one of these). "Expected vs saw" is one line each.

1. **XS perp premium predicts 72h relative returns, negatively** (tables/00_4_explanatory_screen.csv row 7;
   plots/00_explanatory_screen.png). Slice EXPLORE. Expected: |IC| < 0.03 like most features. Saw: IC -0.112, t -3.75,
   top-third minus bottom-third premium coins -170 bp per 72h (n=166 non-overlapping 3-day blocks).
2. **The premium effect is not a reversal proxy** (tables/00_4_impostor_premium.csv). EXPLORE. Expected: high premium
   = recent winners, so premium would be a twin of past returns. Saw: rank corr with past-3d return -0.01; IC after
   removing past-3d rank -0.111 (t -3.85); past-3d return's own XS IC +0.02.
3. **Funding is a twin of premium** (same table). EXPLORE. Expected: related. Saw: XS rank corr 0.70; funding's own XS 72h
   IC -0.076 (t -2.43, -128 bp): one lead, not two.
4. **The premium effect is weak at 24h** (screen row 5). EXPLORE. Expected: if real at 72h, about a third of it at 24h.
   Saw: IC -0.045, t -2.61, -24 bp per 24h, below the ~45 bp average 24h round-trip cost.
5. **Fear & Greed level predicts the next-day panel return, positively** (screen row 22). EXPLORE. Expected: ~0. Saw: IC
   +0.092, t +2.75, top-minus-bottom tercile days +84 bp/day; at 72h t +1.77. Fear&Greed is built partly from price and
   volatility (MANIFEST), so it may be a momentum or regime impostor; EXPLORE is a bull-heavy sample.
6. **S&P 500 prior-session return predicts the next-day panel return, positively** (screen row 24). EXPLORE. Expected: ~0
   after a full extra session of lag. Saw: IC +0.088, t +2.18, +37 bp/day tercile spread; nothing at 72h (t 0.01).
7. **Most explanatory families show nothing** (screen rows 8-21, 26-29): coinbase premium, kimchi premium, active
   addresses, Deribit funding, VIX change, GDELT attention all |t| < 1.8. 5 flags out of 29 looks vs ~1.3 expected by chance.
8. **Primary = raw Binance spot in EXPLORE** (tables/00_4_twin_primary_vs_binance_spot.csv). Expected: near-identical.
   Saw: identical on 100% of rows (price and quote volume): spot/binance close is a twin of the target before 2022.
9. **Hourly reversal is not bounce** (tables/00_7_roll.csv). Expected: Roll half-spread ~ real half-spread (< 1 bp).
   Saw: 13-48 bp: the negative lag-1 covariance is reversal. (Short-horizon reversal is ALREADY TESTED: not chased.)
10. **Volatility and volume cluster strongly with a 24h cycle** (tables/00_3_acf.csv, 00_6_intraday.csv). Expected:
    yes. Saw: |r| ACF 0.25-0.44 at 1h, still 0.03-0.13 at 168h; volume share peaks 16 UTC, troughs 21 UTC (1.87x).
    Not a return claim; context for rivals (vol, time of day).
11. **Regime breaks at 2020H1 and 2021H1** (tables/00_5_regimes.csv). Expected: some. Saw: median daily vol 3.8% ->
    6.2% -> 4.7% -> 9.1%; pairwise corr 0.91 in 2020H1, 0.54 in 2021H1. Any EXPLORE effect may be a bull/alt-season effect.
12. **Daily returns reverse** (tables/00_3_acf.csv): daily ACF(1) negative for all 10 coins (6 significant). ALREADY
    TESTED topic (daily TS reversal): recorded, not chased.
