import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
kit.add_h("H14", "Hour-of-day seasonality persistence: a coin's mean return at the upcoming hour of day over the last 20-60 days predicts its next-bar rank", "none",
  "TARGET.md FAMILIES (time-of-day / day-of-week interactions); OBSERVATIONS #6; MEMORY same-hour-yesterday 1h reversal (NO-STORY lead, CONFIRM lag-24 IC -0.035)",
  "Does the cross-sectional rank of a coin's own average return at the upcoming UTC hour of day (last 20/60 days, drift removed) persist into the next 1h/6h/24h?",
  "a change in a coin's trailing 20-day or 60-day mean return at the same hour of day as the next bar (net of its own drift) predicts the cross-sectional rank of its next 1h/6h/24h primary return positively because intraday flow patterns (regional sessions, funding/settlement flows, scheduled liquidity) recur for each coin",
  "no season_N form shows a positive IC beyond min_useful after removing the coin drift; MEMORY says the same-hour-yesterday return has a NEGATIVE sign (-0.035), which would refute persistence in favour of reversal",
  "same-hour-yesterday reversal (MEMORY NO-STORY lead, a 1-observation version of the same statistic); coin fixed effect (the average return of the coin itself); volatility clock (hours with big moves)",
  "EXPLORE #6", 0.20,
  "MEMORY: same-hour-yesterday 1h reversal CONFIRM lag-24 IC -0.035 with no story (sign opposite to persistence); tracker base 0.30 x0.67 for the opposing sign -> 0.20")
kit.write_beliefs(); print("ok")
