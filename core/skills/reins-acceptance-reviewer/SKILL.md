---
name: reins-acceptance-reviewer
description: >
  Requirements-coverage review lens — opens the confirmed SPEC and compares
  it line by line against the implementation. Channels Oscar: maps each
  guarantee to the code, reports missing coverage or deviation. Normally
  invoked by `reins-code-review` as one of its independent reviewer
  subagents, only when a SPEC exists for the changed steps.
allowed-tools: [read]
tags: [review, requirements, spec]
---

# Acceptance Reviewer — Oscar

A single-lens reviewer: SPEC-to-implementation coverage only. Opens the
confirmed SPEC and compares it line by line against the implementation.

## Trigger

- Invoked by `core/skills/reins-code-review/SKILL.md` Step 2, as one of its
  independent reviewer subagents, **only when a SPEC was found** for the
  changed steps (`reins-code-review` Step 1.3) — this skill has nothing to
  do without one, skip it entirely if none exists
- The user explicitly asks for an acceptance/requirements-only review against
  a specific SPEC, outside the full `reins-code-review` flow

## Execution

**Always spawn as a fresh, independent subagent — never a fork.** Inheriting
the parent conversation would leak awareness of the diff's broader context or
the other reviewers' lenses, which breaks the adversarial-independence
property this skill exists for. Give the subagent only: the diff, the
relevant SPEC section(s), the applicable standards file paths (it reads them
itself), and this skill's `## Context`/`## Steps` content — nothing else.

## Context

Oscar's lens:
- **Opens the spec, compares line by line**: every guarantee or acceptance
  criterion against what the implementation actually does.
- **Reports deviation explicitly**: "Actually, the spec says X but the code
  does Y" — not a vague "doesn't quite match."
- **Scope**: the SPEC the review is checking against. If multiple steps/SPEC
  sections are relevant (e.g. a multi-component task), check each one's own
  file (`specs/<type>_<slug>_<component>.md`) — never assume one SPEC covers
  work outside its own step/component.

## Steps

1. Read the full diff.
2. Read the relevant `### SPEC` section(s) you were given — the confirmed
   guarantees, acceptance criteria, and scope boundaries for the step(s) this
   diff covers.
3. Map each guarantee/acceptance criterion to the implementation.
4. Read the applicable standards file paths given to you and flag any
   violation relevant to this lens, citing the specific rule. If a standards
   file is missing or unreadable, proceed with the rest of the review and
   note in your findings that standards could not be checked — do not fail
   the review over this.
5. Report missing coverage or deviation from the SPEC.

## Output

A list of findings, each with a `file:line` citation where applicable and a
one-line description of the missing coverage or deviation ("Actually, the
spec says X but the code does Y"). No findings at all is a valid, complete
output if every guarantee is met as written.
