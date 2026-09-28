# DECISIONS (unattended: each choice + reason; the conservative option where there was one)

- **D1 Forward returns skip one bar.** Y starts at the close of bar T+1, not T. The close of T is only knowable at T+60 s,
  and skipping one bar also removes the lag-1 bid-ask bounce from every predictive test. Stricter than necessary.
- **D2 Returns only where gap_min == 1**; forward and trailing windows are NaN if any minute is missing. Nothing is filled (data-hygiene rule 9).
- **D3 Bayesian random-walk coefficient (14c row 7) skipped.** It needs PyMC, which 14c marks "ask first". Nobody can be asked, so it was not installed.
  `arch` (Phillips-Perron) was already installed and was used; nothing was installed during this run.
- **D4 Plots** use matplotlib/seaborn styled by `cellplot.setup()` (palette only) and are saved as `plots/NN_slug.png`
  (runbook naming) instead of `cellplot()`'s `cell_NN_slug.png`. Titles carry computed numbers. Four titles that
  had wording written before the result were replaced with computed text and the scripts re-run (ATTEMPTS A2-A4).
- **D5 Eras = calendar years** (2017 Aug-Dec, 2018-2022, 2023Q1 to 03-19). 2017 is kept (a thin market, flagged
  in TARGET.md), and results ex-2017 are shown wherever 2017 could carry an effect.
- **D6 Candidate break for the Chow tests = 2020-01-01**, picked as mid-TRAIN before any Chow test ran. Step 0 had
  already shown the lag-1 autocorrelation sign changing between 2020 and 2021, so this date is NOT fully blind for OBS3.
- **D7 1-min ADF/KPSS use the first 40k bars of each era** (speed); the full-sample 1-min ADF rejects trivially.
- **D8 Hill CI for 1-min returns** uses a 10% subsample bootstrap rescaled by sqrt(0.1) (speed). The 60-min CI uses a daily block bootstrap.
- **D9 Priors for Step 5**: size 0.50, direction/mean 0.05 (from the runbook's base-rate statement). The era-replication
  parameter 0.8 is an assumption. The LR used is the MINIMUM of the p-value bound (p x K) and the era LR.
- **D10 OBS4 (21-23 UTC) is ranked but not taken to VAL.** It ranks 4th, and the VAL_NOTE says VAL overlaps the spent pooled row of that
  exact hypothesis, so a VAL look would add no clean evidence.
- **D11 Taker-side meaning of buy_vol** (taker buy base volume) is inferred from the Binance kline format from memory, not verified.
- **D12 No other file in data\ was read.** The cleaning log's perp and second-copy checks were not repeated.
  Nothing under backtest_engine2\data\ was opened or listed. `_SEALED_HOLDOUT.md`, `cellplot.py`, PROTOCOL.md and 14c were read (as the runbook requires).
