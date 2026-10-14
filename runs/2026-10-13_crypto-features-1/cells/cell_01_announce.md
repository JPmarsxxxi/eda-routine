### Cell 01 - EDA: does the Alpha#30 seed predict at 1h/6h/24h on TRAIN, and is the volume scale doing the work?
**Sub-claim:** H1 / C5 (effect) and C4 (attribution: streak-only vs volume-scaled) of the decomposition; decomposition floor Q1 existence (coverage), Q3 impostor (volume ratio alone is cell 2), Q8 stability (per slice).
**Why it matters:** if neither anchor shows a pooled-TRAIN IC >= 0.02 the seed is a regime effect (C1/C2 only, per MEMORY) and cells 2-3 must find which regime.
**Tests:** xs_ic (Spearman per timestamp, cross-section of the coins available, >= 6), NW t. **Decision rule before running:** see rule file. **APIs:** pandas rank/rolling, scipy.stats; eda_guard via code/panel.py.
**Decisions needed:** none (defaults in DECISIONS.md D5/D6).
