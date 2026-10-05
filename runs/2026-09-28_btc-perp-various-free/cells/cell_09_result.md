# cell_09 RESULT — H4 redirect (EXPLORE only, birth slice, no weight)

Script `scripts/cell_09_h4_redirect.py`; tables `tables/09_result.json`, `tables/09_by_quarter.csv`; plot `plots/09_h4_redirect.png`.

**Branch fired: B1 (one era, leaning to the latest quarter).** EXPLORE raw DVOL vs next-24h return by quarter: 2021Q2 +0.056, 2021Q3 +0.103, 2021Q4 +0.215 (best).
Others pooled +0.037 < 0.0669, best >= 0.15, so B1's condition holds. B2/B3 did not fire: relative DVOL 24h +0.109 (SE 0.071, z 1.54, below the 2-SE bar);
raw 72h +0.030 (SE 0.085); raw 168h -0.001 (SE 0.108). Raw pooled +0.057 (SE 0.050).

**Spawn:** none. B1 is an era-conditional claim (one quarter of EXPLORE, and the same quarters that CONFIRM's own quarter table had already shown), so it is recorded
as a lead, not a hypothesis. The relative-DVOL variable came within reach (rho 0.109) but not the 2-SE bar; it is a lead with a stated number (0.109, z 1.54), not tested on CONFIRM.
The trend in EXPLORE quarters (0.06 -> 0.10 -> 0.21) then the CONFIRM quarters (0.21, 0.09, 0.18, 0.06, -0.02) is a fade-over-time shape.

Not chased (stated): H4's nine-month DVOL history is too short for a relative-level test with this SE; it would need the years that are not available before CONFIRM.
