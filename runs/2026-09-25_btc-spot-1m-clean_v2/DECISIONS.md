# DECISIONS (unattended: question, conservative default taken)

1. **Run folder name.** `runs/2026-09-25_btc-spot-1m-clean` already exists (the v1 sweep, same date and name). The routine
   says "a new folder", so this run writes to `runs/2026-09-25_btc-spot-1m-clean_v2`. The v1 folder was listed (file names
   only) and NOT opened: it holds results on this same data and would contaminate this run.
2. **Earlier hunts named in files I was told to read.** TARGET.md names "arc #047", "the 21:00-23:00 UTC seasonality EDA",
   "flow-imbalance / positioning", "dislocation propagation", "reversal after taker imbalance" (names only). PROTOCOL / 14c /
   part-0 / data-hygiene mention past arcs (#016, #024, #027, #029e, #036c, #037, #039, #042, #045, A02) as teaching examples.
   Listing `backtest_engine2\` to find `cellplot.py` also showed file names such as `intraday_tsm_btc.ipynb`, `x043_signed_flow.py`,
   `x047_impact_decay.py`; none was opened. `_SEALED_HOLDOUT.md` was NOT read. None of these steers which tests are run: the
   hypothesis is taken from the SSRN/Substack search below, filtered only by TARGET.md's ALREADY TESTED line as the runbook requires.
   `backtest_engine2\data\` was not opened or listed.
3. **Plot helper.** PROTOCOL 5.1 asks for `cellplot.py` styling. Its `cellplot()` saves as `plots/cell_NN_slug.png`; the runbook asks
   for `plots/NN_slug.png`. Default taken: import `setup`, `PAL`, `GRAY` from cellplot (the palette/style) and save to the runbook's
   name `plots/NN_slug.png` with matplotlib/seaborn (plotly+kaleido static export not needed).
4. **No installs.** PRE-APPROVED INSTALLS: none. Only numpy/pandas/scipy/statsmodels/matplotlib/seaborn already present are used.
5. **Mid rule.** No quotes in this file, so returns cannot be taken from a mid. Default: close-to-close trade-price returns, with
   bounce risk stated wherever horizons are short (DATA_CARD.md).

## Step 1: hypothesis search (TARGET.md HYPOTHESIS = SEARCH). Written BEFORE the first page load.
6. **Source pick.** Site: **SSRN** (papers.ssrn.com) first; Substack only if SSRN yields no usable claim. Why SSRN: part-0's source
   table says SSRN hands over "a single narrow claim, usually one table", which fits a one-hypothesis EDA. Search terms, in order:
   (1) `bitcoin intraday return predictability`; (2) if needed `bitcoin price overreaction` / `bitcoin round number price barriers`.
   Why these: the carded columns are 1-minute trade-price OHLCV + volume + aggressor split for ONE asset, no book, options, on-chain
   or other coins, so the claim must be a single-asset price/volume predictability claim. TAP corner (part-0 Step 0): dataset frozen
   (BTC spot 1m), vary the idea away from the ALREADY TESTED corners (hour-of-day seasonality at 21-23 UTC, flow imbalance /
   positioning, cross-coin propagation, reversal after taker imbalance). Budget: <= 12 page loads, logged below.

### Page log (Claude-in-Chrome, own tab 1224920620, read-only, closed afterwards). 5 of 12 loads used.
| # | URL | why | source sample period |
|---|---|---|---|
| 1 | papers.ssrn.com/sol3/results.cfm?txtKey_Words=bitcoin+intraday+return+predictability | search term (1). An automatic "security verification" interstitial showed and cleared by itself on re-read; nothing was clicked or solved | - |
| 2 | papers.ssrn.com/sol3/papers.cfm?abstract_id=4080253 | abstract of the only hit: Wen, Bouri, Xu & Zhao (2022) "Intraday Return Predictability in the Cryptocurrency Markets: Momentum, Reversal, or Both" | BTC 2013-03-03 to 2020-05-31 |
| 3 | papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID4135239_code2537556.pdf?abstractid=4080253&mirid=1&type=2 | "Open PDF in Browser", to read the exact predictor definitions. It bounced back to the abstract page; no text obtained. Downloads folder checked: no file was saved by this run | - |
| 4 | papers.ssrn.com/sol3/results.cfm?txtKey_Words=market+intraday+momentum+Gao+Han+Li+Zhou | purpose (3): the definition of the method Wen et al. build on | - |
| 5 | papers.ssrn.com/sol3/papers.cfm?abstract_id=2440866 | abstract of Gao, Han, Li & Zhou "Market Intraday Momentum" (JFE 2018): definition "the first half-hour return on the market since the previous day's close predicts the last half-hour return"; stronger on more volatile and higher-volume days; mechanisms: infrequent rebalancing (Bogousslavsky 2016) and late-informed trading near the close | SPY 1993-2013 |

7. **Candidates.** One candidate considered, one picked: Wen et al. (2022). Not in ALREADY TESTED (it is a CONDITIONAL
   predictability claim, first half-hour return -> last half-hour return, not an unconditional hour-of-day mean; the
   window 23:30-24:00 is outside 21:00-23:00). Testable with `close` only. Economic reason given by the source.
   Rejected parts of the same source: ETH/LTC/XRP replication (other assets, not given), FOMC days (external calendar, not
   given), COVID break (single event), the "reversal" leg (abstract does not say WHICH intraday return reverses, and the
   PDF could not be read; guessing a definition would be inventing the claim). Only the momentum leg is taken.
8. **Operational definitions (my choice, because the paper's text was unreadable).** Crypto has no close, so the day is the
   UTC calendar day (Binance's own daily-candle boundary). r_first(d) = ln(close of 00:29 bar of d / close of 23:59 bar of
   d-1) ("since the previous day's close", Gao et al.). r_last(d) = ln(close of 23:59 bar of d / close of 23:29 bar of d).
   r_first is knowable at 00:30, r_last starts at 23:30: no overlap, no look-ahead. A day is used only if all four
   anchor bars exist (no filling). Half-hour length is the source's; no other window lengths are searched.
9. **Source results are not used.** Wen et al.'s sample (to 2020-05-31) lies inside TRAIN; Gao et al. is SPY. Neither overlaps
   VAL, so VAL is not additionally soft-clean for this claim from the source (it remains SOFT-clean for the reasons in
   TARGET.md's VAL_NOTE). No coefficient, R^2 or sign from either paper is copied into any rule; the abstracts give no numbers.

10. **C6b uses buy_vol/sell_vol.** Question: does a mechanism check on last-half-hour aggressor flow overlap the ALREADY TESTED "flow-imbalance" topic? Default: it is kept as a side-bet check only (flow is the OUTCOME the mechanism implies, never a predictor), and no flow-based predictor is tested. If a human reads it as overlap, drop C6b; nothing else depends on it.
