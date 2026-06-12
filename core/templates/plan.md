# PLAN Template

The PLAN is written by the agent, after reading the SPEC for a step, as part of
Step 2 of `core/workflow/3_implement.md`. It is saved to:

```
~/.paw/user/projects/<project-slug>/specs/<type>_<slug>/step-NN-plan.md
```

matching the `step-NN-spec.md` it responds to.

---

```markdown
# PLAN: [Same name as the SPEC]

## Guarantees covered
Restate each guarantee from the SPEC and confirm it will be addressed.

## Verification approach
- Automated tests: <files to add/change, or "none — manual review">
- Manual review steps (if applicable): what the user should see and check

## Open questions / risks
Anything in the SPEC that conflicts with existing code, or any assumption that needs
confirmation before implementation starts. Empty if none.
```

---

Once the user approves the PLAN, proceed to Step 3 (Implement) of
`3_implement.md`.
