import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc = kit.tcrit_for(2)
rule = f"""# cell 10 rule - H5: perp positioning (funding, premium index, perp-spot basis, open interest change, long/short ratio) as cross-sectional predictors (controls: none this cell; conditional: none)
Features (hourly, point-in-time; funding = last settled rate with stamp <= bar open; premium index = premium-klines close of bar t; basis = perp kline close / spot close - 1 of bar t; OI and ratios = last 5m snapshot <= open+55min; OI == 0 -> NaN):
 funding_lvl; funding_chg_24 (funding minus funding 24h earlier); prem_lvl (premium index close, bp); prem_chg_6 (change over 6h); basis_lvl; basis_chg_6; oi_chg_6, oi_chg_24 (log change of open interest in coin units); oi_val_chg_24 (log change of OI notional);
 ls_acct_lvl (count_long_short_ratio) and ls_chg_24; ls_top_lvl (top-trader count ratio); taker_ls_lvl (sum_taker_long_short_vol_ratio, log). 13 features x h = 1, 6, 24 = 39 variants (V = 39).
Cross-section: coins with the input available; coverage by fold is reported (OI/ls: BTC only before 2021-12 -> cross-section < 6 coins -> NaN IC until C1 end; EXPLORE and most of C1 are empty for those, so their folds are 'n/a').
Pre-stated directions (crowding story): higher funding / premium / basis / OI growth / long-short ratio -> LOWER return (score = -IC); taker_ls (aggressive buying) -> HIGHER (score = +IC).
Pass rule: SUPPORTED if the best variant in its pre-stated direction has pooled score >= +0.02 and NW t >= Sidak {kit.tcrit_for(39):.2f} (pooled over the folds where it exists) AND the same sign in BOTH C2 and C3 (the only folds with all coins). Not supported otherwise.
{fx.rule_power(39)}
Note on N: pooled sample is smaller for OI/ls features (C2+C3 + part of C1, ~11,000 hours, se ~0.009 at h24): power at delta 0.02 is lower than the table above; the cap makes w_yes 3.0 and w_no stays near 0.75-0.9 for them.
"""
ann = """### Cell 10 - EDA: H5 does leverage crowding rank the coins' next 1-24h returns?
**Sub-claim:** (C5) rank of funding/premium/basis/OI growth/long-short predicts negatively; (Q1 existence) coverage by fold, (Q2 assumption) the pinned funding floor makes funding a clipped variable (OBSERVATIONS #7).
**Why it matters:** the only inputs in the panel that describe positioning; MEMORY says the XS perp premium had a negative sign on three folds but low power.
**Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(10, "H5", "TRAIN", "search", "none", "none", rule, ann)
