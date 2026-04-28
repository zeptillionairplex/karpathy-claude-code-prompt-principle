# 5. Tech Stack Registry — Template

Copy this file to `contracts/STACK.md` at project kickoff. It is the single
authoritative list of locked technology decisions. Both subagents read it.

---

# Tech Stack Registry

> Last updated: YYYY-MM-DD
> Owner: <human name / role>

## Locked decisions

| Layer | Choice | Version | Rationale (1 line) | ADR |
|---|---|---|---|---|
| Backend language | Go | 1.22 | team familiarity | docs/adr/0001 |
| Backend framework | Gin | v1.10 | minimal, fast, OpenAPI-friendly | docs/adr/0002 |
| Spec → Go codegen | oapi-codegen | latest | contract-first | docs/adr/0003 |
| Frontend | React + TS | 18.x / 5.x | | docs/adr/0004 |
| Spec → TS codegen | openapi-typescript | latest | | docs/adr/0005 |
| Server state | TanStack Query | v5 | dedup + cache | |
| HTTP client | fetch (native) | — | | |
| Form + validation | react-hook-form + zod | | | |
| DB | PostgreSQL | 16 | | |
| ORM / queries | sqlc | | typed SQL | |
| Migrations | atlas | | | |
| Auth | JWT (RS256) | — | stateless | docs/adr/0006 |
| Logging (BE) | zerolog | | | |
| Logging (FE) | console + Sentry | | | |
| Testing (BE) | go test + testcontainers | | | |
| Testing (FE) | vitest | | | |
| E2E | Playwright | | | |
| CI | GitHub Actions | | | |

## Deferred

| Capability | Defer until | Why deferring | Owner |
|---|---|---|---|
| Background jobs | Phase 2 | no async needs in MVP | |
| Feature flags | Phase 2 | hardcode for now | |

## Adding a library

1. Open an ADR under `docs/adr/NNNN-<slug>.md` (use template
   `docs/adr/_template.md`).
2. Update this table — moving from **Deferred** to **Locked decisions**.
3. Run a contract test if it touches the API surface (auth, errors,
   serialization).
4. Commit STACK.md and ADR together; reference both in the PR.

## Removing or replacing a library

Same flow — ADR with `Status: superseded` on the old, `Status: accepted` on
the new. STACK.md keeps history visible via git log; do not silently swap rows.
