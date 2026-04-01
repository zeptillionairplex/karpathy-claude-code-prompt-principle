---
globs: "**/*.go"
---
# Go / Gin Rules

## Architecture: Clean Architecture

Dependency direction — outer layers depend on inner, never reverse:
```
infrastructure → interfaces/adapters → use_cases → entities
```

| Layer | Maps to | Role |
|-------|---------|------|
| `entities/` | domain models | Pure business types and rules. Zero external deps. |
| `use_cases/` | service | Application logic orchestrating entities. No DB/HTTP deps. |
| `interfaces/` | handler | HTTP/gRPC/CLI — translate requests ↔ use cases. |
| `infrastructure/` | repository | DB, cache, external APIs, message queues. |

**Rules:**
- `entities/` must have zero imports from other internal layers.
- `use_cases/` receives dependencies via interface injection, never concrete types.
- `interfaces/` (handler): HTTP parsing, validation, response serialization only.
- `infrastructure/` (repository): DB queries only. No business logic.
- Each domain folder MUST have a `CLAUDE.md` listing its layer, purpose, and files.

## Error Handling
- Propagate errors upward. Log only at handler layer.
- Add context with fmt.Errorf("...: %w", err).
- No panic — except initialization code.

## API Response Format
```go
// Success
{"data": ..., "message": "ok"}
// Error
{"error": "...", "code": "ERROR_CODE"}
```

## General
- Always specify exit condition when spawning goroutines.
- context.Context is always the first argument.
- Struct field tag order: json, db, validate.

## Required Skills

When writing, reviewing, or refactoring Go code, **always apply these skills:**

| Situation | Skill |
|-----------|-------|
| Any Go code | `/golang-project-layout`, `/golang-error-handling`, `/golang-code-style` |
| DB / repository layer | `/golang-database` + `/supabase-postgres-best-practices` |
| Concurrency / goroutines | `/golang-concurrency`, `/golang-context` |
| Tests | `/golang-testing`, `/golang-stretchr-testify` |
| Security | `/golang-security` |
| Observability | `/golang-observability` |
| gRPC | `/golang-grpc` |
| Performance | `/golang-performance`, `/golang-benchmark` |

**If skills are not installed:**
```bash
npx skills add samber/cc-skills-golang --all -y -a claude-code
npx skills add supabase/agent-skills -y -a claude-code
```
