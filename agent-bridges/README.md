# Agent Bridge Files

The files in this directory (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`,
`copilot-instructions.md`) are **generated** by `reins install` / `reins update` from
`~/.reins/user/config.yaml` — do not edit them by hand, your changes will be
overwritten on the next `reins update`.

They all carry the same information — an import of `core/workflow/1_orchestrator.md`,
the user's standards, the active adapters, and the historic mode flag — but in one
of two forms depending on the agent (see the table below): import-capable agents
(Claude Code, Gemini CLI) get a short `@file` reference their runtime resolves
itself; every other agent gets the full content embedded literally, since they
have no equivalent import mechanism.

`reins install`/`reins update`/`reins sync` then wire **every agent you've
configured** (stored in `~/.reins/user/config.yaml`; you can select more than
one during setup, or change the list later with `reins agents`) to read the
corresponding bridge file, inside a clearly marked block. Only configured
agents are wired — an agent installed on the machine but never added to your
config is left untouched. If you install a new agent later, add it with
`reins agents`, then run `reins link-agents` to wire it in without a full
`reins update`.

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
| GitHub Copilot CLI | `copilot-instructions.md` | `~/.copilot/copilot-instructions.md` | full content inlined (no native import syntax) |
| Codex CLI | `AGENTS.md` | `~/.codex/AGENTS.md` | full content inlined |
| Other (generic) | `AGENTS.md` | `~/AGENTS.md` | full content inlined |

Cursor has no bridge — see the top-level `README.md`'s "Supported agents"
section for why. Aider and OpenCode aren't offered either, for similar
reasons; there's no dedicated code path for any of the three, only the
generic `other` fallback above.

For agents without a native "import another file" mechanism, the full bridge
content is embedded directly inside the managed block of their native config file
— no separate step needed to read it. `reins doctor` flags any agent whose native
file is missing the managed block entirely.

---

## Skill registration

Every bridge file ends with an **"Available skills"** section: a generated list of
every skill under `core/skills/`, `user/skills/`, and active adapters' `skills/`,
with their `name`, `description`, and path — built by `collect_skills` /
`skill_frontmatter` in `bin/reins`. This is how agents without a native skill-discovery
directory (Gemini CLI, Copilot CLI, Codex CLI, generic/other) find out what
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
