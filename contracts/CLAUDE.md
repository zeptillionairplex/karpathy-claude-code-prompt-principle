# contracts/ — API Contract Zone

This folder is the single source of truth for the API surface. Both backend
and frontend agents read from here; **only the main / orchestrator agent
writes here.**

## Files
- `openapi.yaml` — the contract. Single source of truth for paths, schemas,
  errors, auth.
- `STACK.md` — tech-stack registry. Locked decisions and explicit DEFERRED
  items. See `.claude/skills/parallel-dev/docs/05-tech-stack-registry.md`
  for the template.
- `examples/` — request/response samples.

## Rules
1. Every API change starts here. Edit `openapi.yaml` first; never adjust
   handler shape or TS types ahead of the spec.
2. After every spec change, regenerate both sides:
   - `cd ../backend && make generate`
   - `cd ../frontend && npm run generate:api`
3. Do not edit generated files (`backend/api/api.gen.go`, `frontend/src/types/api.ts`).
4. New libraries: ADR under `docs/adr/`, then update `STACK.md`. Do not add a
   library by importing it — see `.claude/skills/parallel-dev/docs/06-late-dependency.md`.
5. Lint before commit: `redocly lint openapi.yaml` (or equivalent).

## Subagents reading this
You are looking at the contract. Treat it as immutable for the duration of
your task unless the orchestrator explicitly asks you to draft a change.
Surface ambiguities back to the orchestrator instead of guessing.
