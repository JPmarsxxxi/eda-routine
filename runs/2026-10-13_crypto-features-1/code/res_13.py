import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import kit
body = """# cell 13 result - H6 venue gaps and lead-lag (TRAIN, hourly, min_n 5; 33 variants; cells/cell_13_table.csv, cells/cell_13_output.txt, plots/cell_13_venue.png)
Pre-committed branch: SUPPORTED by the letter of the rule: best ub_gap_lvl at h1: IC +0.0431 (NW t +11.9; EXPLORE +0.026, C1 +0.064, C2 +0.034, C3 +0.042), Sidak bar 3.17, IC >= 0.02. weight_applied 3.0 (cap).
Others: ub_gap_lvl h6 +0.0356 (t 6.9); ub_retdiff_3 h1 +0.0332 (t 9.1), ub_retdiff_6 h1 +0.0325 (t 8.9), cb_gap_lvl h1 +0.0281 (t 10.1; C2 only +0.004), cb_retdiff_3 h1 +0.0222, cb_retdiff_6 h1 +0.0232; cb_retdiff_1 is IDENTICAL to cb_gap_chg_1 (and 3, 6): the return-difference and gap-change forms are the same numbers.
All venue features carry a positive sign (the venue that is up leads) at h1 and decay to ~0.005 at h24 (cb) / 0.01 (ub): a 1-6 hour effect, the same horizon as the bounce-free reversal.
HONEST CAVEAT, not resolved in this cell: every venue feature contains the Binance close with a MINUS sign: gap = log(other close) - log(Binance close), retdiff = other return - Binance return. A Binance print that closes away from its mid (the bid-ask bounce found in cells 5-6) lowers the Binance close and raises
the feature, and the same print is the start of the response. So these features overlap the base 1-hour reversal (IC +0.083) mechanically; cb gap std is 28 bp and Upbit 214 bp (KRW basis, cancelled by rank). The rule as written (no rival control) is met, so the belief moves; the rival (the Binance bounce / own-coin reversal) is controlled in the next H6 cell
with a one-bar entry delay and a residualisation on the Binance return ranks. Coverage: Coinbase 6.2 coins per hour on average, Upbit 4.8 (min_n 5 used).
"""
kit.result(13, 3.0, variants=33, suggests="none", body=body)
kit.attempt(13, "H6", "Coinbase and Upbit gap level, gap change, return difference x k x h", "ub_gap_lvl h1 +0.043 t 11.9 etc.; contains -Binance close: bounce rival pending")
kit.write_beliefs(); print(kit.posterior("H6"))
