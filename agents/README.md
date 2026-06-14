# Agent Bridge Files

The files in this directory (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`,
`copilot-instructions.md`) are **generated** by `reins install` / `reins update` from
`~/.reins/user/config.yaml` — do not edit them by hand, your changes will be
overwritten on the next `reins update`.

They all carry the same content: an import of `core/workflow/1_orchestrator.md`,
the user's standards, the active adapters, and the historic mode flag.

`reins install`/`reins update`/`reins sync` then wire **every agent detected on this
machine** (its config directory already exists) to read the corresponding bridge
file, inside a clearly marked block — not just the one agent picked during `reins
install`. The generic `~/AGENTS.md` fallback is always wired. If you install a
new AI agent later, run `reins link-agents` to wire it in without a full `reins
update`.

```
<!-- REINS:BEGIN -->
... managed content ...
<!-- REINS:END -->
```

Only the content between these markers is touched — everything else in your native
config file (e.g. `~/.claude/CLAUDE.md`) is left alone.

| Agent | Bridge file | Native target | Mechanism |
|---|---|---|---|
| Claude Code | `CLAUDE.md` | `~/.claude/CLAUDE.md` | `@~/.reins/agents/CLAUDE.md` import |
| Gemini CLI | `GEMINI.md` | `~/.gemini/GEMINI.md` | `@~/.reins/agents/GEMINI.md` import |
| GitHub Copilot CLI | `copilot-instructions.md` | `~/.copilot/instructions.md` | reference note (no native import syntax) |
| Codex CLI | `AGENTS.md` | `~/.codex/AGENTS.md` | reference note |
| Aider / OpenCode / Cursor / other | `AGENTS.md` | `~/AGENTS.md` | reference note |

For agents without a native "import another file" mechanism, the managed block is a
short pointer to the bridge file. Until that agent supports imports, open the bridge
file directly (e.g. `cat ~/.reins/agents/AGENTS.md`) or paste its content where needed —
`reins doctor` will flag this so you know it needs attention.

---

## Skill registration

Every bridge file ends with an **"Available skills"** section: a generated list of
every skill under `core/skills/`, `user/skills/`, and active adapters' `skills/`,
with their `name`, `description`, and path — built by `collect_skills` /
`skill_frontmatter` in `bin/reins`. This is how agents without a native skill-discovery
directory (Gemini CLI, Copilot CLI, Codex CLI, Aider/OpenCode/other) find out what
skills exist and when to use them.

**Claude Code** additionally has a native Agent Skills directory at
`~/.claude/skills/`. `reins install` / `reins update` / `reins new-skill` / `reins sync` all
call `sync_skills`, which (when `~/.claude/` exists, regardless of which agent is
configured as primary) maintains a symlink per REINS skill at
`~/.claude/skills/reins-<name>` (or
`~/.claude/skills/reins-<adapter>-<name>` for adapter skills) pointing at the skill's
directory in `~/.reins/`. These symlinks are namespaced with the `reins-` prefix so they
can be safely added/removed without touching any of your own Claude Code skills.

`reins uninstall` removes all `reins-*` symlinks from `~/.claude/skills/` (in addition to
removing the managed block from your agent's native config).
