import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc = kit.tcrit_for(33)
rule = f"""# cell 13 rule - H6: cross-venue gaps and lead-lag (Coinbase USD and Upbit KRW vs Binance); controls: none this cell; conditional: none
Features (hourly, all knowable at the bar end; cross-sectional ranks cancel the common USDT/USD and KRW/USD basis):
 Coinbase (9 coins; BNB absent; XRP absent after 2021H1): gap_lvl = log(CB close / BN close) minus its trailing-720h mean; gap_chg_1, gap_chg_3, gap_chg_6 = change of the log gap; retdiff_k = (CB k-hour return) - (BN k-hour return), k = 1, 3, 6.
 Upbit (BTC ETH XRP ADA DOGE SOL; the common KRW/USD move cancels in rank): ub_retdiff_k = (UB KRW k-hour return) - (BN k-hour return), k = 1, 3, 6, and ub_gap_lvl = log(UB close / BN close) minus its trailing-720h mean.
 7 + 4 = 11 features x h = 1, 6, 24 = 33 variants (V = 33). min_n for the cross-section: 5 coins (EXPLORE has only 4-5 Coinbase coins, Upbit 5-6), stated deviation from the default 6.
Pre-stated direction: POSITIVE IC for every feature (the venue that moved up more / trades at a premium leads, Binance catches up).
Pass rule: SUPPORTED if the best variant has pooled-TRAIN IC >= +0.02 and NW t >= Sidak {tc:.2f}. Wrong-signed significant results count as 'no'. Not supported otherwise.
{fx.rule_power(33)}
Note: with 5-8 coins per cross-section the se is a little above the table (fewer coins per timestamp); the cap makes w_yes 3.0 and w_no is shown.
"""
ann = """### Cell 13 - EDA: H6 do other venues lead Binance?
**Sub-claim:** (C5) a venue return gap predicts Binance/primary returns; (Q2 assumption) the venues differ enough (same-hour return corr 0.994).
**Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(13, "H6", "TRAIN", "search", "none", "none", rule, ann)
