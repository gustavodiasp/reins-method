---
type: feature # feature | hotfix | bugfix | chore | spike
stack: # detected stack(s), e.g. ruby, node, python, ruby+node
status: active # active | paused
branches: {} # map of component -> branch name, e.g. { backend: feature/123-x, frontend: feature/123-y }
prs: {} # map of component -> PR URL (empty/null until opened)
title: # human-readable title
updated_at: # YYYY-MM-DD
---

# Context — {{title}}

---

## Task
<!-- Filled by the agent at task start. Do not modify. -->

## Epic
<!-- Filled by the agent at task start. Do not modify. -->

## Objective (in one sentence)
<!-- Written by me only. The agent never modifies this field. -->

## Breakdown
<!-- Updated by the agent after each confirmed step. Format: checked = done, unchecked = pending. -->
<!-- For multi-stack tasks, prefix each step with its component, e.g. "(backend) ..." -->

## Current step
<!-- Updated by the agent at the start of each step. -->

## Decisions made
<!-- Added by the agent only after I explicitly confirm an architecture or approach decision. One line per decision. -->

## Open questions / blockers
<!-- Added by the agent when something is unclear or blocked. -->

## SPEC status
<!-- Updated by the agent. Format: Step N — [not written / approved / implemented] -->
<!-- SPEC/PLAN files live in ~/.paw/user/projects/<project-slug>/specs/<type>_<slug>/step-NN-{spec,plan}.md -->

## My notes
<!-- Written by me only. The agent never modifies this field. -->
