### Cell 09 — EDA: H4 redirect (where does the DVOL-return link actually point?)

**Sub-claim being tested:** none scored; a birth-slice redirect. Pieces: quarterly raw rho, relative-DVOL rho, 72h/168h horizon rho.

**Why it matters:** H4 was refuted pooled on CONFIRM while every CONFIRM quarter but the last was positive; this checks whether EXPLORE points to a variable that resolves that.

**Test(s) used:** Spearman + moving-block bootstrap SE.

**Decision rule before running:** `cells/cell_09_rule.md` (branches B1-B4, no weights).

**Engine/library APIs used:** `eda_guard.load` via `scripts/kit.hourly`, scipy.stats.spearmanr.

**Slice:** EXPLORE only (birth slice). CONFIRM not re-opened.

**Decisions I need from you:** none (unattended).
