---
type: feature # feature | hotfix | bugfix | chore | spike
stack: # detected stack(s), e.g. ruby, node, python, ruby+node
status: active # active | paused
branches: {} # map of component -> branch name, e.g. { backend: feature/123-x, frontend: feature/123-y }
                 # component key: single lowercase word, letters/digits/- only (see 2_new_task.md Step 3) — it's used in spec file paths
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
<!-- Single-component task: one unchanged line, e.g. "03 — add pagination". -->
<!-- Multi-component task (branches has >1 entry): one line per component with -->
<!-- an active step, labeled like Breakdown, e.g.: -->
<!--   (backend) 03 — add pagination endpoint -->
<!--   (frontend) 02 — wire pagination controls -->
<!-- A session updates only its own component's line — never the whole field,
     and never the whole file. Always a targeted edit, re-read fresh first —
     see 3_implement.md "After confirmation — update the context file". -->

## Decisions made
<!-- Added by the agent only after I explicitly confirm an architecture or approach decision. One line per decision. -->

## Open questions / blockers
<!-- Added by the agent when something is unclear or blocked. -->

## SPEC status
<!-- Updated by the agent. Format: Step N — [not written / approved / implemented] -->
<!-- Multi-component: label like Breakdown/Current step, e.g. "(backend) Step 03 — implemented" -->
<!-- Single-component: SPEC/PLAN sections live in specs/<type>_<slug>.md (one "## Step NN" section per step) -->
<!-- Multi-component: each component has its own specs/<type>_<slug>_<component>.md -->

## My notes
<!-- Written by me only. The agent never modifies this field. -->
