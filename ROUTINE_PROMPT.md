# Routine prompt: paste this into the Instructions box

Desktop app -> Code tab -> Routines -> New routine -> **Local**.
Name: `eda-routine`. Working folder: `C:\Users\User\eda-routine`. Schedule: **Manual** (run it with "Run now").
Then click **Run now** once and approve each tool with "always allow": a run stalls on any permission prompt it has
not seen before. Note that a local task only runs while the app is open and the computer is awake.

Instructions (paste exactly):

```
Run the EDA routine. Read C:\Users\User\eda-routine\TARGET.md. If its STATUS line is not READY, do nothing and stop.
Otherwise read C:\Users\User\eda-routine\RUNBOOK.md and follow it exactly, writing everything into a new folder
C:\Users\User\eda-routine\runs\<YYYY-MM-DD>_<target-name>\. You are unattended: nobody will answer questions.
When done, set TARGET.md STATUS to DONE <run folder>. If you stop with a STOPPED.md instead, set STATUS to STOPPED <run folder>.
The method is skill 14c-eda.md, exactly as the runbook says; ignore RUNBOOK_v1_sweep.md.
```

The real instructions live in RUNBOOK.md (edit it there, not in the app). The routine's saved prompt is stored by
the app at `~/.claude/scheduled-tasks/eda-routine/SKILL.md`.
