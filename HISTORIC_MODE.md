# Historic Mode

Optional, off by default. Records a short entry for every closed task and stores
it locally under `~/.reins/user/historic/`. What you do with that data is entirely
up to you.

All data is **user-owned** and lives on your machine — never inside a project repo,
never touched by `reins update`.

---

## Enable / disable

```bash
reins historic on    # creates ~/.reins/user/historic/ and this month's file
reins historic off   # stops recording new entries; existing data is kept
```

---

## What happens when it's on

- `core/workflow/4_close_task.md` Step 8 fires at every task close and records an entry
  in `~/.reins/user/historic/` using whatever structure you have defined there.
- If no structure exists yet, the agent asks how you want to organize the entry before
  proceeding — file layout, naming, and format are entirely your choice.
- On request (`reins historic summary`), the agent reads what you have stored and
  produces a summary in the same terms you use.

---

## Details

See `core/evaluation/README.md` for the full procedure (Mode A: recording an entry,
Mode B: generating a summary), the difficulty scale, and the rules (one file per
month, record at close not at month-end, no duplicates, enrichment is additive).

---

## Privacy

This is the one part of REINS that holds personal data by design. It is intentionally
kept:
- Outside any project repository
- Outside `~/.reins/core/` (so it's never confused with the updatable engine)
- Untouched by `reins update`

If you ever want to back it up or move it, it's just markdown files at
`~/.reins/user/historic/`.
