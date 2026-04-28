# 2. Spec-First Workflow

The contract drives both sides. Code that disagrees with the spec must fail
at compile/typecheck — never at runtime in production.

## Pipeline

```
contracts/openapi.yaml
     ├─→ oapi-codegen          → backend/api/api.gen.go
     └─→ openapi-typescript    → frontend/src/types/api.ts
```

## Backend (Go example)

```bash
# inside backend/
oapi-codegen -package api -generate types,gin -o api/api.gen.go ../contracts/openapi.yaml
```

Wire this into `Makefile`:

```make
generate:
	oapi-codegen -package api -generate types,gin -o api/api.gen.go ../contracts/openapi.yaml
```

Handlers must implement the generated `ServerInterface`. If the spec and
handlers diverge, compilation fails — that's the safety net.

## Frontend (TS example)

```bash
# inside frontend/
npx openapi-typescript ../contracts/openapi.yaml -o src/types/api.ts
```

Wire into `package.json`:

```json
{ "scripts": { "generate:api": "openapi-typescript ../contracts/openapi.yaml -o src/types/api.ts" } }
```

Wrap fetches in TanStack Query (or chosen client) and let the generated types
drive request/response typing.

## Mock for parallel work

While backend is in flight, the frontend agent can hit a spec-driven mock:

```bash
npx @stoplight/prism-cli mock contracts/openapi.yaml
```

This unblocks parallel iteration — the frontend agent never has to wait.

## Spec-change protocol
1. Edit `contracts/openapi.yaml` (and bump `info.version` if breaking).
2. Re-run codegen on both sides: `cd backend && make generate`, `cd frontend && npm run generate:api`.
3. Both agents adapt to the new types simultaneously.
4. CI runs `redocly lint contracts/openapi.yaml` plus a contract test.

## Common pitfalls
- **Hand-editing generated files.** Mark them read-only in CLAUDE.md and add
  an auto-generated header.
- **Spec drift during a sprint.** Freeze the spec at sprint start; treat
  changes as their own ticket with explicit human review.
- **Two agents both editing `openapi.yaml`.** Only the lead/main agent edits
  the spec; subagents read it.
