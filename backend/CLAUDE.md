# backend/ — Backend agent scope

You are operating in the backend tree. The contract lives at
`../contracts/openapi.yaml`. Conventions and rationale are inherited from the
root `CLAUDE.md`; this file adds backend-specific rules.

## Codegen
- Source: `../contracts/openapi.yaml`.
- Generator: `oapi-codegen` (Go) or equivalent.
- Output: `api/api.gen.*` — **read-only**. Generated files carry a header
  warning; do not edit by hand.
- Trigger: `make generate` after any spec change.

## Architecture
- Handlers implement the generated `ServerInterface`. Signature is fixed by
  the spec.
- Business logic lives under `service/`, not in handlers.
- Persistence layer: SQL via `sqlc` (queries in `db/queries/*.sql`), or the
  ORM listed in `../contracts/STACK.md`.
- Cross-cutting concerns (auth middleware, request id, logging) sit in
  `middleware/`.

## Testing
- Unit: `go test ./...` (or language equivalent).
- Integration: `make test-integration` — uses testcontainers if listed in
  STACK.md.
- Contract test: validate handler responses against `../contracts/openapi.yaml`
  before merging.

## Hard rules (from root)
- The contract is sacred. Spec changes go through the orchestrator, not here.
- New imports must be in `../contracts/STACK.md`. If you find a library not
  registered, stop and surface it.
- Don't touch `frontend/`, `contracts/`, or root config.

## Reference skills (load only when the task needs them)
- `.claude/skills/optional/golang/` — Go conventions (if linked by `/setup`)
- `.claude/skills/parallel-dev/` — overall workflow and triage routines
