import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
tc = kit.tcrit_for(39)
rule = f"""# cell 08 rule - H4: volume, trade-count, trade-size and taker-flow surprises (controls: none this cell; conditional: none)
Features (hourly, Binance spot, trailing-only normalisation; w = window in hours of the numerator):
 volsurp_w = log( sum(quote_vol, w) / (w * mean(quote_vol over the trailing 720h ending at t-w)) ), w = 1, 6, 24;
 nsurp_w = same with the trade count n; sizesurp_w = log(quote_vol/n over w) minus its trailing-720h mean (average trade size surprise); taker_w = sum(buy_vol, w)/sum(vol, w) - 0.5 (taker-buy imbalance), w = 1, 6, 24;
 volratio_d = log( sum(quote_vol, 120) / sum(quote_vol, 480) ) (the Alpha#30 volume ratio at hourly anchors).
13 features x h = 1, 6, 24 = 39 variants (V = 39). Hourly sampling, cross-sectional Spearman IC, NW t (lags h+5), TRAIN with per-slice report.
Pre-stated directions (from cell 3 and the story): surprises in volume / trade count / size: NEGATIVE IC for the surprise (high-attention coin underperforms), score = -IC; taker imbalance: POSITIVE (buy-heavy flow continues).
Pass rule: SUPPORTED if the best variant in its pre-stated direction has pooled-TRAIN score >= 0.02 and NW t >= Sidak {tc:.2f}; the wrong-signed significant ones count as 'no'. Per-slice sign stability is reported (4 slices).
{fx.rule_power(39)}
"""
ann = """### Cell 08 - EDA: H4 do volume / trade-count / size / taker-imbalance surprises predict the cross-section?
**Sub-claim:** C5 effect of order-flow surprises at 1/6/24h; decomposition Q1 existence (n regime shift in C3 handled by trailing normalisation), Q7 shape reported by slice.
**Why it matters:** these are the only inputs in the library with no price transform; if none works H4 is a candidate for drop after controls. **Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(8, "H4", "TRAIN", "search", "none", "none", rule, ann)
