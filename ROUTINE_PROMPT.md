# Routine prompt: paste this into the Instructions box

Desktop app -> Code tab -> Routines -> New routine -> **Local**.
Name: `eda-routine`. Working folder: `C:\Users\User\eda-routine`. Schedule: **Manual** (run it with "Run now").
Then click **Run now** once and approve each tool with "always allow": a run stalls on any permission prompt it has
not seen before. Note that a local task only runs while the app is open and the computer is awake.

Instructions (paste exactly):

```
Run the EDA routine. Read C:\Users\User\eda-routine\TARGET.md. If its STATUS line is not READY, do nothing and stop.
Otherwise read C:\Users\User\eda-routine\RUNBOOK_v3.md, then the JOB_<job>.md file named by TARGET.md's JOB: line,
and follow both exactly, writing everything into a new folder C:\Users\User\eda-routine\runs\<YYYY-MM-DD>_<target-name>\.
You are unattended: nobody will answer questions. Run gate.py on the run folder; only if it prints PASS, set TARGET.md
STATUS to DONE <run folder>. If you stop with a STOPPED.md instead, set STATUS to STOPPED <run folder>.
The method for a single claim is skill 14c-eda.md, as the runbook says; ignore RUNBOOK.md (v2) and RUNBOOK_v1_sweep.md.
```

The real instructions live in RUNBOOK_v3.md and the JOB_*.md files (edit them there, not in the app). The routine's saved
prompt is stored by the app at `~/.claude/scheduled-tasks/eda-routine/SKILL.md` — after changing this file, paste the new
prompt there too (until 2026-10-13 this file pointed at RUNBOOK.md v2).
