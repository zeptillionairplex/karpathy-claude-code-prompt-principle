# 6. Late-Dependency Mitigation

The problem: deep into a session, AI or human realizes a missing library
("we need TanStack Query / zod / a state lib"). Retrofitting later is
expensive — code, tests, and prompts all need rework.

Layered defenses, ordered by cost.

## Defense 1 — Planning checklist (cheap, prevents most cases)
Use `04-planning-checklist.md` before kickoff. Most "late" libraries are
predictable; the checklist forces a decision or an explicit DEFER.

## Defense 2 — Tech-stack registry as gatekeeper
`contracts/STACK.md` is the only place a library lives. If an agent proposes
a library that isn't in STACK.md, the agent must stop and ask. The CLAUDE.md
rule: "Adding an import not listed in STACK.md is forbidden without an ADR."

## Defense 3 — ADR template for additions
Light template, ~5 minutes to fill:

```markdown
# ADR NNNN: Add <library>
Status: proposed
Date: YYYY-MM-DD

## Context
What problem does this solve? Why now and not deferred?

## Decision
Library, version, scope of use.

## Consequences
- Bundle / build impact
- Adjacent changes (does it replace something?)
- Test surface added
```

## Defense 4 — Triage routine when an agent proposes a new lib mid-task

```
1. STOP the agent. Don't let it install yet.
2. Ask: is this in STACK.md?
   - YES → check version constraint, proceed.
   - NO  → continue.
3. Can the existing stack do this? (90% of the time, yes.)
   - YES → reject, ask agent to use existing tools.
   - NO  → continue.
4. Does it need to land THIS sprint?
   - NO → defer; add to STACK.md "Deferred" row with date.
   - YES → write ADR, update STACK.md, then implement.
```

## Defense 5 — Spec-first contracts as a forcing function
A frozen `openapi.yaml` makes most "we need a new lib" surprises visible at
spec time, not at code time. Pagination, auth, errors, retries — all live in
the spec, so the libraries that implement them are decided when the spec is.

## Defense 6 — Capability inventory in CI
Add a CI step that diffs `package.json` / `go.mod` against
`contracts/STACK.md`. Any import that isn't registered fails the build. This
catches an ADR-skipping merge.

## Costs of skipping these
- Late TanStack adoption mid-project: rewrite of every fetch + cache
  invalidation, ~1–3 days plus regression risk.
- Late zod adoption: every form re-validated, double-paths during migration.
- Late state lib: prop drilling refactor across the tree.
- AI-introduced silent dep: no one knows it's there until prod build size
  jumps or a CVE hits.

The checklist + STACK.md + triage is the smallest discipline that absorbs
nearly all of these without rework.
