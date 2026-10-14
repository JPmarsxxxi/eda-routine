| cell | hypothesis | what | outcome |
|---|---|---|---|
| 01 | H1 | seed #30 + streak-only, daily and rolling-24h anchors, 3 horizons (12 variants) | streak_daily h6 IC +0.043 t 3.6 supported; seed itself not; anchor-specific |
| 02 | H7 | streak-3 IC by anchor hour (24) x h (3), streak length sweep, residual on r24 | anchor 23 h6 IC +0.044, diff vs other anchors +0.038 t 3.0 supported; r24-only stronger (+0.074 t 6.3) |
| 03 | H1 | volume scale attribution + response-switch control, 4 features x 3 h x 2 responses | seed - streak -0.0105 (t -1.3) at h6: volume scale adds nothing; C3 fade is not the response switch; volratio flips sign by fold -> H4 |
| 04 | H8 | r24 reversal IC by anchor hour (24) x h (3) + session groups | ASIA h6 +0.055 t 6.35 but US side -0.004: sign flip not supported; amplitude clock inside general reversal -> H3 |
| 05 | H3 | reversal lookback (9) x transform (4) x horizon (3) | raw k2 h1 IC +0.084 t 35.6, decays with k and h; scaling hurts; bounce flag |
| 06 | H3 | reversal bounce control: base / skip1 / delay1 / delay2 x k(4) x h(3) + RB response | delay1 k3 h6 IC +0.030 t 9.3, C2+C3 +0.040: supported; ~50% of base IC is bounce/fast decay |
| 07 | H3 | bounce-free reversal x conditions (market vol, session, own vol, recent move) | session is the only conditional (ASIA h6 +0.059 vs US -0.005); vol regime/own vol/recent move do nothing |
| 08 | H4 | volume/trade count/size/taker surprises x w(1,6,24) x h(3) | pre-stated directions refuted; opposite-signed nsurp continuation at 24h (3/4 folds); taker_1 contrarian at h1 |
| 09 | H10 | nsurp/volsurp (w=1,6,24) residualised on same-window return and |return|; taker_1 on rev1 | nsurp_1 h24 residual IC +0.032 t 5.5, 4/4 folds positive: supported; taker_1 contrarian = rev1 |
| 10 | H5 | 13 positioning features x 3 horizons | premium/basis/funding/ls crowding sign holds in all folds: prem_lvl h1 -0.032 t -14; rivals (fixed effect, trailing return) pending |
| 11 | H5 | positioning survivors x {detrend, detrend+resid on r3s,r24} x h | prem_lvl detrended+resid h24 -0.025 t -5.0 4/4 folds; ls_acct dead (fixed effect); oi dead (price); funding weak |
| 12 | H5 | prem_dtr_resid x conditions (market premium regime, funding clock, session, funding floor) | robust to market premium regime (+0.024/+0.022 at h6); stronger in US hours and when funding is on the floor |
| 13 | H6 | Coinbase and Upbit gap level, gap change, return difference x k x h | ub_gap_lvl h1 +0.043 t 11.9 etc.; contains -Binance close: bounce rival pending |
| 14 | H6 | venue features: base / delay1 / delay1+resid(rev1,rev3) | bounce explains 60-90% of h1 IC; best residual ub_gap_lvl h6 +0.0137 t 2.6: not supported |
| 15 | H2 | f54 daily/rolling, clv, oc5, r24 x h(3) + residual on r24 | f54_roll h24 +0.029 t 4.7 supported but C1-driven; h1/h6 negative (reversal) |
| 16 | H2 | f54_roll h24 by trend state (up/down) and session; residual on r24 | down-state IC +0.026 t 2.95: not a bull impostor; US-anchor strongest |
| 17 | H3 | 7 feature modules: IC by horizon/fold, 12x12 correlation, incremental IC, cost line | f001 max corr 0.24; f006~f007 0.78 duplicate; f002 = lagged b_rev24; all COMBINE-ONLY |
| 18 | H3 | confirm f001 on C1-C3 (frozen) | C1=inconclusive, C2=supported, C3=supported; shown=True |
| 19 | H9 | confirm f002 on C1-C3 (frozen) | C1=supported, C2=supported, C3=inconclusive; shown=True |
| 20 | H10 | confirm f003 on C1-C3 (frozen) | C1=supported, C2=inconclusive, C3=supported; shown=True |
| 21 | H5 | confirm f004 on C1-C3 (frozen) | C1=inconclusive, C2=inconclusive, C3=supported; shown=False |
| 22 | H2 | confirm f005 on C1-C3 (frozen) | C1=supported, C2=inconclusive, C3=supported; shown=True |
| 23 | H7 | confirm f006 on C1-C3 (frozen) | C1=supported, C2=inconclusive, C3=inconclusive; shown=False |
| 24 | H1 | confirm f007 on C1-C3 (frozen) | C1=inconclusive, C2=inconclusive, C3=inconclusive; shown=False |
| 25 | H3 | VAL f001 (frozen F1) | IC +0.0141 t +1.99 -> inconclusive |
| 26 | H9 | VAL f002 (frozen F2) | IC +0.0284 t +1.93 -> inconclusive |
| 27 | H10 | VAL f003 (frozen F3) | IC +0.0201 t +1.38 -> inconclusive |
| 28 | H2 | VAL f005 (frozen F5) | IC +0.0164 t +1.14 -> inconclusive |
| 29 | H11 | 8 risk features x {level, detrended} x 3 h | levels IC -0.07..-0.09 at h24 are coin fixed effects; detrended |IC| <= 0.0144: not supported |
| 30 | H12 | beta x BTC / EW market move (k=1,3,6,24) x h(3) | all 24 variants NEGATIVE (refutes diffusion sign); fixed-effect vs reversal unresolved -> H13 |
| 31 | H13 | beta x market move by UP/DOWN state + detrended form | opposite signs in UP/DOWN at h6, h24: fixed effect, refuted |
| 32 | H14 | hour-of-day seasonality persistence N=20,60 x raw/demeaned/sign x h | season60_dm h1 +0.0223 t 9.2 supported; C3-heavy (+0.0445): FTMO-mid artifact suspected |
| 33 | H14 | season60_dm / season20_sign scored on primary vs Binance response, hour-of-day decomposition | Binance-response IC +0.0203 (t 9.4): not an FTMO-mid artifact |
| 34 | H14 | orthogonality/incremental/cost of f008 and f004-h1 | f008 max corr 0.024 but incremental leg mis-specified (sparse partners): inconclusive per rule; both COMBINE-ONLY |
| 35 | H5 | confirm F8 on C1-C3 (frozen) | C1=supported, C2=supported, C3=inconclusive; shown=True |
| 36 | H14 | confirm F9 on C1-C3 (frozen) | C1=inconclusive, C2=inconclusive, C3=supported; shown=False |
| 37 | H5 | VAL F8 (frozen F8) | IC +0.0210 t +4.73 -> supported |
| 38 | H15 | within-bar shape (7 features) x h x {undelayed, delay1} | delayed body h1 -0.0272 t -11 but corr -0.97 with rev1: an impostor; gap has no content |
| 39 | H15 | bar-shape features residualised on rev1, delayed and undelayed | delayed residual |IC| <= 0.007: refuted; vwap_dev undelayed -0.042 is pure bounce |
| 40 | H5 | basis/funding detrended, forms a/b/c (resid r3s, r24, f004) x h | funding_dtr|f004 h24 +0.0172 t 3.0: supported (incremental); basis = premium twin |
| 41 | H5 | confirm F10 on C1-C3 (frozen) | C1=inconclusive, C2=inconclusive, C3=supported; shown=False |
| 42 | H16 | range position/drawdown/rally/MA distance x 4 windows x level/detrended x 3 h | dd_72 detrended h6 score +0.032 t 6.5: supported by rule; reversal rival uncontrolled |
| 43 | H16 | dd/madev detrended, raw vs residual on r3s,r24,r72, h6/h24 | dd_336 h24 residual +0.0220 t 2.9: supported incremental; not frozen (power) |
| 44 | H4 | volsurp/nsurp/taker residualised x 8 conditions x h6,h24 | pre-stated signs absent in every regime (best +0.0243 t 3.2 < 3.36); ASIA/US sign flip leads to H10 |
| 45 | H10 | f003 IC by session / trend / market-vol conditions at h6, h24 | no session dependence (ASIA-other +0.0065 t 1.1); C2 is the weak fold |
| 46 | H6 | venue-gap residuals (delay1 + resid) in home sessions vs other | best home-session +0.0141 t 1.6: not supported; H6 closed |
| 47 | H13 | UP-state beta x market move: undelayed/delay1, level/detrended, k=1,3,6 | delayed+detrended UP-state h1 IC -0.0425 t -12.7, 4/4 folds; overlap with f001 to be tested |
| 48 | H13 | UP-state -beta feature raw vs residual on f001 + market-residual reversal, h1/h6 | residual h6 +0.035 t 7.1, 4/4 folds, corr with f001 <= 0.16; static component a ~0.038 flagged |
| 49 | H13 | -beta static vs -beta x sign(market) vs time-varying beta, raw and residual | g_rev residual +0.013 (h1,h6) under 0.015: static -beta (+0.023/+0.040) is the fixed effect |
| 50 | H17 | perp taker imbalance, perp-spot gap, perp share, perp count surprise x {detrended, residual} x h | best residual |IC| 0.0132 (pgap_6 h6): not supported; perp taker = bounce |
