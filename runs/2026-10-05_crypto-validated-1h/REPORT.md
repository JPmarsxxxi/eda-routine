# REPORT — runs/2026-10-05_crypto-validated-1h (EDA routine v3.1, unattended, cloud)

**Source mode:** E (set in TARGET.md; autopick not run). No inbox item used. Data: crypto_panel_validated_2026-10-05,
target = primary/validated_<COIN> `price`, 10 coins, 1h -> daily decisions at 00:00 UTC. Splits (SPLITS.md, from
coverage counts): EXPLORE 2019-01-01..2021-07-01, C1 2021-07-08..2022-01-01, C2 2022-01-08..2022-07-01, C3
2022-07-08..2023-03-20, VAL unopened. Holdout guard asserted at every load (ACCESS_LOG.md: all PASS).

## Belief table
| H | claim | prior -> posterior | evidence chain (slice: branch, weight) | final state |
|---|---|---|---|---|
| H1 | XS perp premium -> 72h relative underperformance (crowded perp longs) | 0.49 -> **0.321** | C1 refuted 0.729; redirect C1 (1); C2 refuted 0.843; redirect C2 (1); C3 refuted 0.801; redirect C3 (1) | OPEN, no slice left |
| H2 | Fear & Greed level -> next-day panel return (sentiment momentum) | 0.12 -> **0.059** | C1 refuted 0.759; redirect C1 (1); C2 refuted 0.804; redirect C2 (1); C3 refuted 0.748; redirect C3 (1) | OPEN, no slice left |
| H3 | prior-session S&P 500 return -> next-day panel return (risk-on spillover) | 0.06 -> **0.049** | C1 refuted 0.814; redirect C1 (1) | LOW |

Stop: **S4** (slices exhausted) after 14 cells (7 tests, 7 redirects). No hypothesis reached HIGH, none reached
HIGH-CONFIRM, so **VAL was not opened** (VAL_NOTE therefore not needed beside any number).

## Fold table (decay-first shape) — effect = top-minus-bottom spread, bp; bar = cost-sized threshold
| H | EXPLORE (birth) | C1 | C2 | C3 |
|---|---|---|---|---|
| H1 (72h, bar -122/-117) | -170 (IC t -3.75) | -23, t -0.39, refuted | -118, t -1.56, refuted | -19, t -0.35, refuted |
| H2 (24h, bar +89/+84) | +84 (IC t +2.75) | +70, t +0.91, refuted | +41, t +0.41, refuted | -23, t -0.39, refuted |
| H3 (24h, bar +89) | +37 (IC t +2.18) | -146, t -1.77, refuted | — | — |

**Cost line:** nothing reached HIGH or VAL. For reference the bars were 2 x mean round-trip cost from TARGET.md's
measured FTMO costs (72h book: 117-122 bp; 24h panel timing: 84-89 bp). Only H1 on C2 had a point estimate at the bar
(-118 vs -117) and it was not significant (t -1.56).

**K (for downstream DSR deflation):** 77 looks = 29 EXPLORE screen ICs + 7 fold openings + 41 redirect looks (ATTEMPTS.md).
Power per fold was low (0.20-0.31 at the cost-sized effect), so every refuted weight was mild (0.73-0.84): the
posteriors fell slowly, not because evidence was mixed.

## 1b findings (part-0 form)
- **H1 — 1b finding:** a change in perp/perp_premium `close` (XS rank) did **not** predict 72h relative primary returns
  by a cost-sized margin on any of three folds; the sign held on all three (-23/-118/-19 bp) but EXPLORE's -170 bp shrank
  ~85% on two of them. Net: (c) refuted at tradeable size in this data; a small negative residual may exist (redirect
  leads below). Not a kill — the user decides.
- **H2 — 1b finding:** Fear & Greed level showed no cost-sized next-day timing effect on C1/C2/C3; the spread fell
  monotonically +70 -> +41 -> -23 bp. Consistent with its rival (price-momentum/bull-regime impostor, OBS #5/#11). Net: (c).
- **H3 — 1b finding:** prior-session S&P 500 return predicted the WRONG sign on C1 (-146 bp, t -1.77); LOW. Net: (c).

## Still open
H1 (0.321) and H2 (0.059) are OPEN with no admissible slice: further evidence needs a fresh sample (TEST is the user's
call; nothing here argues for opening it).

## Leads (not findings; not chased)
- Most- vs least-crowded single coin by premium: -161 (t -1.60) C1, -215 (t -1.74) C2, -33 (t -0.34) C3.
- High premium-dispersion blocks: -18 / -246 (t -1.99) / -81 bp — inconsistent across folds.
- Opposite-sign equity spillover on C1 (strong S&P days -> weak crypto next day; R5 BTC -144 bp t -2.11).
- Phase-0 observations not chased: coinbase/kimchi premium, active addresses, Deribit funding, VIX, GDELT (all |t| < 1.8
  on EXPLORE); EXPLORE primary prices are byte-identical to spot/binance closes (OBS #8); hourly reversal is not bid/ask
  bounce (Roll 13-48 bp vs < 1 bp real, OBS #9); daily reversal (already tested topic).
- NO-STORY entries: none were registered.

## Process notes
gate.py: see run log in the final message (must PASS before DONE). The eda-v3-judge agent could not be launched from
this session (no sub-agent tool available); a human should run it on this folder before relying on the result.
Defaults a human should confirm are in DECISIONS.md (D4 matplotlib instead of cellplot/seaborn; D5 FTMO Saturday
windows dropped, which cut C2/C3 72h blocks by ~45%; D6 day convention/lags; D8 power-sim sample counting; D9 the
interrupted session; D10 one redirect per fold refutation).
