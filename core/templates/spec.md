# SPEC Template

A SPEC is written by the user, never by the agent (see `core/workflow/3_implement.md`
Permanent constraints). For each confirmed step in the breakdown, the SPEC is saved
to:

```
~/.paw/user/projects/<project-slug>/specs/<type>_<slug>/step-NN-spec.md
```

where `<type>_<slug>` matches the active context file's name (without `.md`), and
`NN` is the two-digit step number from `## Breakdown`.

---

```markdown
# SPEC: [Feature, refactor, or component name]

## Context
What exists today, where it lives, and what is wrong or missing.

## Goal
What changes and why.

## Expected behavior
### Main flow
### Secondary flows
### Edge cases / error states

## Guarantees
- [ ] Guarantee 1
- [ ] Guarantee 2
- [ ] Existing entry points / behavior outside this scope are unchanged

## Verification
- [ ] Automated tests: <files / framework, or "none — manual review">
- [ ] Manual review steps (if applicable)

## Architecture decision
Chosen approach and rationale (if an architecture decision was made prior to this SPEC).

## Out of scope
What explicitly does not change in this step.

## Files likely affected
- [ ] path/to/file
```

---

## PR section

When a PR is opened for this task, append to the **highest-numbered**
`step-NN-spec.md` for the task:

```markdown
## PR
<url>
```

Also record it in the context file's frontmatter (`prs`) — see
`core/workflow/4_close_task.md` Step 6.
