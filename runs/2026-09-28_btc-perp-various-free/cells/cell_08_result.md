# cell_08 RESULT — H4 CONFIRM opening

Script `scripts/cell_08_h4_confirm.py`; tables `tables/08_result.json`, `tables/08_by_quarter.csv`, `tables/08_tercile_means.csv`; plot `plots/08_h4_confirm.png`. CONFIRM, n = 10,559.

**Branch fired: REFUTED.** Deciding number: Spearman(dvol_t, next-24h spot return) = **+0.0194** (block-bootstrap SE 0.0439), below the +0.025 refute bar
and well below the +0.0669 support bar. EXPLORE was 0.057 (SE 0.05 on 9 months).

**Weight applied:** (1-power)/(1-alpha) = 0.637/0.95 = **0.671** (inside the cap). Odds 0.25/0.75 = 0.3333 x 0.671 = 0.2237 -> **posterior 0.183**. State OPEN.
Note the SE is larger than the effect: this test has low power (0.363), so a refutation here is a weak one and moves belief only modestly, as the weight shows.

Unweighted (reported, not scored):
- Partial on trailing 24h return: +0.0175 (unchanged).
- By quarter (decay-first): +0.213, +0.094, +0.182, +0.062, -0.017 (2022Q1..2023Q1): positive in 4 of 5 but fading, while the pooled is ~0. Best quarter removed
  (2022Q1): pooled -0.015. Within-quarter positive and pooled zero means DVOL level drifted across quarters against the returns of those quarters (between-quarter
  variation cancels the within-quarter link); this is the point the redirect cell examines on EXPLORE.
- Tercile mean next-24h returns (bp): low -2.3 / mid -42.8 / high +7.9. Not monotone.
- Economics: N/A (not a rule).

**Redirect (step 8):** cell_09 (mandatory).
