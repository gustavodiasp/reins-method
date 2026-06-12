# Historic Mode

Optional, off by default. Turns each closed task into a short entry in a monthly
file, and compiles a summary on request — useful for self-assessment and
performance check-ins.

All data is **user-owned** and lives at `~/.paw/user/historic/` — never inside a
project repo, never touched by `paw update`.

---

## Enable / disable

```bash
paw historic on    # creates ~/.paw/user/historic/ and this month's file
paw historic off   # stops recording new entries; existing data is kept
```

---

## What happens when it's on

- `core/workflow/4_close_task.md` Step 8 records a short entry for every closed task:
  type, context, what was done, impact, and (optionally) a 0–10 difficulty rating
  across size/complexity/impact.
- Entries accumulate in `~/.paw/user/historic/YYYY-MM.md`, one file per month, created
  from `core/evaluation/templates/monthly.md`.
- On request ("generate monthly summary" / `paw historic summary`), the agent compiles
  the month's entries — optionally enriched with PR/commit metrics from available
  tooling — into a summary covering deliveries, progress against priorities, impact,
  skills demonstrated, and a one-line takeaway.

---

## Details

See `core/evaluation/README.md` for the full procedure (Mode A: recording an entry,
Mode B: generating a summary), the difficulty scale, and the rules (one file per
month, record at close not at month-end, no duplicates, enrichment is additive).

---

## Privacy

This is the one part of PAW that holds personal data by design. It is intentionally
kept:
- Outside any project repository
- Outside `~/.paw/core/` (so it's never confused with the updatable engine)
- Untouched by `paw update`

If you ever want to back it up or move it, it's just markdown files at
`~/.paw/user/historic/`.
