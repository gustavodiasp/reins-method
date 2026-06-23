# Historic Mode — Reference

This directory contains **example** templates for organizing historic task entries.
They are not mandatory. The structure of `~/.reins/user/historic/` is entirely
user-defined — REINS does not impose any file layout, naming convention, or format.

---

## What historic mode does

When `historic_mode: on`, a hook fires at the end of every closed task (`4_close_task.md`
Step 8). The agent records an entry based on whatever structure the user has defined in
`~/.reins/user/historic/`. If no structure exists yet, the agent asks the user how they
want to organize the entry before proceeding.

---

## Example templates (optional)

`templates/monthly.md` and `templates/task-entry.md` are one possible way to organize
entries — by month, with task metadata and an optional retro section. Use them, adapt
them, or ignore them entirely.

To use an example template as your starting point, copy it to
`~/.reins/user/historic/` and adjust it to your needs. Once a structure exists there,
the agent will follow it on every subsequent task close.

---

## `reins historic summary`

On request, the agent reads whatever is in `~/.reins/user/historic/` and produces a
summary. The content and format of the summary follow what the user has stored there —
no fixed schema is assumed.
