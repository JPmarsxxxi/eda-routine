import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import fx, kit
kit.add_h("H17", "Perp aggressive flow and derivatives intensity: perp taker imbalance, perp-versus-spot taker gap, perp share of volume, perp trade-count surprise", "none",
  "TARGET.md FAMILIES (funding rate and basis, OI/positioning); OBSERVATIONS #7, #8, #13; cells 8-12 (spot taker = bounce; premium crowding is real)",
  "Do the aggressor imbalance of Binance USD-M perpetual trades, its gap to spot, the perp share of dollar volume and the perp trade-count surprise rank the next 1h/6h/24h returns beyond the same-window return?",
  "a change in a coin's perp taker-buy imbalance (or in the perp-minus-spot taker gap, the perp share of volume, or the perp trade-count surprise) predicts the cross-sectional rank of its next 1h/6h/24h primary return because leveraged flow adds pressure that spot flow does not (crowding sign like the premium) or reveals information earlier",
  "no perp-flow feature has an IC beyond min_useful after residualising on the same-window return and |return| and removing the coin's own mean; the spot taker contrarian IC was the bounce (cell 9), so a perp taker IC that vanishes under the same control is the same bounce",
  "bid-ask bounce / own-window return (cell 9: taker_1 residual on rev1 = 0); the premium feature f004 (leveraged longs pay the premium); the coin fixed effect in perp share of volume",
  "EXPLORE #7 #8 #13", 0.25,
  "no earlier run on this panel used perp aggressor flow; tracker base 0.30 x0.85 because the spot taker analogue was only the bounce and the premium already carries the crowding story -> 0.25")
tc = kit.tcrit_for(48)
rule = f"""# cell 50 rule - H17: perp aggressive flow and derivatives intensity (controls: same-window return and |return|; coin fixed effect via within-coin detrending; conditional: none)
Features (hourly, Binance USD-M perp klines + spot; w = window hours): ptaker_w = sum(perp taker_buy_volume, w)/sum(perp volume, w) - 0.5, w = 1, 6, 24; pgap_w = ptaker_w - staker_w (spot buy_vol/vol - 0.5 over w), w = 6, 24; pshare = log(perp quote_volume_24h / spot quote_volume_24h) minus its coin's trailing-2160h mean;
 pnsurp_w = log(perp trade count over w / (w x trailing-720h mean per hour)), w = 1, 6. 8 features. Forms: (a) rank of the feature detrended within coin (minus its trailing 2160h mean ending t-1, except pshare/pnsurp already scaled); (b) (a) residualised on the cross-sectional ranks of the same-window signed return and |return|.
Horizons 1, 6, 24. 8 features x 2 forms x 3 h = 48 (V = 48). Direction two-sided (exploratory family; the sign found is a finding, not a pre-stated claim): score = |IC| with its sign reported.
Pre-stated primary: SUPPORTED if the best form-(b) variant has |pooled-TRAIN IC| >= 0.02 and NW |t| >= Sidak {tc:.2f}, with the same sign in C2 and C3. Not supported otherwise.
{fx.rule_power(48)}
"""
ann = """### Cell 50 - EDA: H17 do perp aggressive flow / derivatives intensity features rank the cross-section?
**Sub-claim:** (C5) perp-side flow carries information the spot side and the premium do not; (Q3 impostor) same-window return and the coin fixed effect are controlled in the form (b)/(a) design. **Decision rule:** see rule file. **Decisions needed:** none.
"""
kit.begin(50, "H17", "TRAIN", "search", "same-window signed return and |return|; coin fixed effect (detrending)", "none", rule, ann)
