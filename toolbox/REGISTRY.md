# TOOLBOX — methods validated for use by any job (JOB_METHODS.md). gate.py parses the table.

One row per method and version. `validation` points at `toolbox/<id>_validation.md`: the planted-answer test and its result.
`result: FAIL` rows stay, so no run retries the same method the same way. `beats`: the baseline it beat on real data and by
how much (or `-`). `runs`: every run that used it.

| id | what | package | version | source | validation | result | beats | runs |
|---|---|---|---|---|---|---|---|---|
