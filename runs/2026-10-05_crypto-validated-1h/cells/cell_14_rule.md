hypothesis: H3
slice: C1
kind: redirect

# cell_14 rule — mandatory redirect after H3's refutation on C1 (RUNBOOK_v3 Phase 2 step 8)

H3 was refuted on C1 (cell_13). This redirect looks only at C1 (already opened by H3), carries **weight_applied 1**, and
any finding becomes a NEW child born on C1 with its own rule file. Recorded as `branch: inconclusive`.

**Fixed menu for H3 redirects (same five shapes as H2, written now before H3's first redirect; DECISIONS D10):**
- R1 opposite sign: is the top-minus-bottom next-day spread significantly NEGATIVE (risk-on days followed by crypto weakness)? bar -2 x mean RT24.
- R2 horizon: 72h panel return on a non-overlapping 3-day grid, terciles of the prior-session S&P 500 return; bar 2 x mean RT72.
- R3 extremes: next-day panel return on days whose prior S&P session return >= +1% minus days <= -1%; bar 2 x mean RT24.
- R4 change: terciles of the prior 5-session S&P 500 return instead of the 1-session return; bar 2 x mean RT24.
- R5 BTC only: next-day BTC return by prior-session S&P tercile; bar 2 x RT24(BTC) = 37.8 bp.
(C1 bars: 2 x RT24 = 89.0 bp; 2 x RT72 = 121.8 bp.)

**Spawn rule:** a child only for |t| >= 2.5 in the stated direction AND an effect clearing that look's bar; otherwise
"absent everywhere on C1", no child.

H3 is LOW after cell_13 (closed to further tests); the redirect still runs because step 8 makes it mandatory after a
refutation. Note: R1 repeats cell_13's own statistic (its spread and t are already known: -146 bp, t -1.77), so R1 is
reported but adds nothing new; its spawn bar (|t| >= 2.5) is already known not to be met.
