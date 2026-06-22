---
name: reins-remind
description: >
  Re-anchors the agent on all configured REINS standards and workflow rules
  mid-session. Invoke whenever the agent seems to have drifted from the REINS
  workflow or is not applying configured standards, language, or conventions.
allowed-tools: Read
tags: [session, standards, anchor]
---

# REINS Remind

## Trigger
User explicitly invokes this skill mid-session — typically when the agent has
drifted from the REINS workflow, stopped applying configured standards, or is
ignoring language/documentation conventions.

## Context
The agent has already loaded the bridge file at session start. This skill
re-activates what is already in context — no new information is introduced.

## Steps

1. Read `~/.reins/user/standards/company.md` — absorb and re-apply.
2. Read `~/.reins/user/standards/personal.md` — absorb and re-apply.
3. If an adapter is active (declared in the bridge), read its `standards/floor.md`
   and re-apply its conventions.
4. Re-confirm the configured interaction and documentation languages from the
   bridge. All subsequent responses must follow them.
5. Check `~/.reins/user/projects/<project-slug>/contexts/` for an active context
   file (`status: active`). If found, hold it in mind for the rest of the session.
6. Re-anchor on the core workflow rules in `~/.reins/core/workflow/1_orchestrator.md`.

## Output

Reply with exactly one line — nothing else, no explanation, no list of what was
re-applied:

> Ops! Let me focus again!
