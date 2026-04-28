# 3. Subagent Orchestration

Two subagents (backend, frontend) work in parallel; the main agent owns the
spec and integration.

## Roles

| Agent | CWD | Reads | Writes |
|---|---|---|---|
| Main / orchestrator | repo root | everything | `contracts/`, integration glue |
| Backend subagent | `backend/` | root + `backend/` + `contracts/openapi.yaml` (read-only) | `backend/**` (excl. `*.gen.*`) |
| Frontend subagent | `frontend/` | root + `frontend/` + `contracts/openapi.yaml` (read-only) | `frontend/**` (excl. generated types) |

CLAUDE.md auto-load makes this enforceable without prompt repetition: each
subagent only sees the contexts attached to its CWD.

## Spawn pattern (Claude Code Agent tool)

```
Agent({
  description: "Backend implementation",
  subagent_type: "executor",
  prompt: "CWD: backend/. Implement handlers per backend/CLAUDE.md against
           the frozen contracts/openapi.yaml. Do not edit api/api.gen.go.
           Stop and surface any spec ambiguity instead of guessing."
})

Agent({
  description: "Frontend implementation",
  subagent_type: "executor",
  prompt: "CWD: frontend/. Implement views/hooks per frontend/CLAUDE.md
           using src/types/api.ts. Do not edit generated types. Use the
           Prism mock at http://127.0.0.1:4010 until backend is ready."
})
```

Run both in parallel (single message, two Agent calls).

## Conflict prevention
- **Spec ownership.** Only main edits `contracts/openapi.yaml`. Subagents
  request changes by surfacing the question, not by editing.
- **Generated files.** `.gen.*` and `src/types/api.ts` are read-only for
  subagents — enforced by CLAUDE.md note + a generated-file header.
- **Cross-cutting changes** (e.g. auth header rename). Flow: spec change →
  re-gen → both subagents adapt. Never modify request shape on one side only.

## Human checkpoints (must)
- Requirements → spec translation (domain knowledge).
- Major spec changes (resources, auth, pagination, error model).
- Security decisions (JWT vs session, CORS, input validation).
- Performance tradeoffs (N+1, caching, pagination size).

## Daily cadence example
```
AM 30m   human: requirements / spec freeze
AM 2-3h  agents: parallel implementation
Noon 15m human: PR-style midpoint review
PM 2-3h  agents: integration + tests
EOD 30m  human: smoke check, queue tomorrow's priorities
```

## Verification before merge
- `redocly lint contracts/openapi.yaml`
- backend: `go build ./... && go test ./...`
- frontend: `npm run typecheck && npm run test`
- contract test: backend stub vs frontend mock-call (e.g. `dredd`).
- e2e: Playwright happy-path on the integrated stack.
