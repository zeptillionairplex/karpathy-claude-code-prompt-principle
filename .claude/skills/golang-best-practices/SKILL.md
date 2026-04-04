---
name: golang-best-practices
description: Comprehensive Go best practices covering architecture, error handling, database, testing, security, observability, and concurrency. Use when writing, reviewing, or refactoring any Go code.
metadata:
  version: "1.0.0"
---

# Go Best Practices

Comprehensive guide for production-quality Go code. Contains rules across 8 categories,
prioritized by impact to guide implementation and code review.

## When to Apply

Reference these guidelines when:
- Writing new Go packages, handlers, services, or repositories
- Reviewing Go code for correctness and maintainability
- Refactoring existing Go code
- Designing Clean Architecture layers in Go
- Writing tests, handling errors, or adding observability

## Rule Categories by Priority

| Priority | Category | Impact | Reference |
|----------|----------|--------|-----------|
| 1 | Project Layout & Architecture | CRITICAL | `references/architecture.md` |
| 2 | Error Handling | CRITICAL | `references/error-handling.md` |
| 3 | Database & Transactions | CRITICAL | `references/database.md` |
| 4 | Gin HTTP Framework | HIGH | `references/gin.md` |
| 5 | Testing | HIGH | `references/testing.md` |
| 6 | Security | HIGH | `references/security.md` |
| 7 | Concurrency & Context | MEDIUM-HIGH | `references/concurrency.md` |
| 8 | Observability | MEDIUM | `references/observability.md` |
| 9 | Code Style & Naming | LOW-MEDIUM | `references/code-style.md` |

## Quick Reference

### 1. Project Layout & Architecture (CRITICAL)
- `arch-clean-layers` — entities → use_cases → interfaces → infrastructure. Never reverse.
- `arch-interface-injection` — use_cases receive repos as interface, never concrete type
- `arch-domain-folder` — one folder per domain; each has its own CLAUDE.md
- `arch-no-circular` — sibling domains never import each other; use shared/

### 2. Error Handling (CRITICAL)
- `err-wrap-context` — always `fmt.Errorf("doing X: %w", err)`
- `err-log-once` — log only at the top handler layer, propagate raw error below
- `err-sentinel` — define sentinel errors with `errors.New` in the package that owns them
- `err-no-panic` — never panic in library/service code; only in init or main
- `err-type-assert` — use `errors.As` / `errors.Is` not type assertions

### 3. Database & Transactions (CRITICAL)
- `db-parameterized` — never interpolate user input into SQL strings
- `db-transaction-wrap` — wrap multi-table mutations in a single transaction
- `db-no-tx-http` — never make HTTP calls inside a transaction
- `db-connection-pool` — configure `SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`
- `db-context-first` — always pass `context.Context` to every DB call

### 4. Gin HTTP Framework (HIGH)
- `gin-bind-should` — use `ShouldBindJSON`, never `BindJSON` (hijacks error handling)
- `gin-error-centralize` — one `handleError` helper per handler struct; no repeated `switch err`
- `gin-error-format` — always `{"error": "...", "code": "..."}` / `{"data": ..., "message": "ok"}`
- `gin-middleware-next` — call `c.Next()` to pass through, `c.Abort()` to stop chain
- `gin-ctx-request` — pass `c.Request.Context()` to services; never pass `*gin.Context` past handler
- `gin-no-global` — use `gin.New()` + explicit middleware; never `gin.Default()` in production
- `gin-router-group` — group routes by domain; apply auth middleware at group level

### 5. Testing (HIGH)
- `test-table-driven` — use table-driven tests for all non-trivial logic
- `test-real-db` — DB layer tests use a real DB; no mocks for SQL
- `test-testify` — use `github.com/stretchr/testify/assert` and `require`
- `test-parallel` — call `t.Parallel()` in unit tests for speed
- `test-helpers` — shared setup in `testutils/` package, never in `init()`

### 5. Security (HIGH)
- `sec-no-hardcoded-secrets` — secrets from env vars or secret manager only
- `sec-bcrypt-passwords` — always bcrypt (cost ≥ 12) or argon2id for passwords
- `sec-sql-injection` — parameterized queries only; never `fmt.Sprintf` into SQL
- `sec-tls-verify` — never set `InsecureSkipVerify: true` in production
- `sec-log-no-pii` — never log passwords, tokens, PII

### 6. Concurrency & Context (MEDIUM-HIGH)
- `ctx-first-arg` — `context.Context` is always the first argument
- `ctx-no-store` — never store context in a struct field
- `ctx-cancel-defer` — always `defer cancel()` immediately after `WithCancel/WithTimeout`
- `goroutine-exit` — every goroutine must have a documented exit condition
- `goroutine-waitgroup` — use `sync.WaitGroup` to wait; use `errgroup` for error propagation

### 7. Observability (MEDIUM)
- `obs-structured-log` — use `slog` (stdlib, Go 1.21+) with key-value pairs
- `obs-request-id` — propagate request ID through context and all log lines
- `obs-error-log` — log errors with full context at handler layer only
- `obs-metrics` — expose Prometheus metrics for latency, errors, throughput
- `obs-trace` — wrap external calls (DB, HTTP, gRPC) with OpenTelemetry spans

### 8. Code Style & Naming (LOW-MEDIUM)
- `style-receiver-short` — receiver name = 1-2 letter abbreviation of type name
- `style-no-stutter` — avoid package name in exported names (`user.UserService` → `user.Service`)
- `style-interface-small` — prefer small interfaces (1-3 methods); compose larger ones
- `style-comment-exported` — all exported symbols must have a doc comment
- `style-error-lowercase` — error strings lowercase, no period at end

## How to Use

Read individual reference files for detailed explanations and code examples:

```
references/architecture.md
references/error-handling.md
references/database.md
references/gin.md
references/testing.md
references/security.md
references/concurrency.md
references/observability.md
references/code-style.md
```

Each reference file contains:
- Why it matters
- Bad example with explanation
- Good example with explanation
- Edge cases and exceptions

## References

- https://go.dev/doc/effective_go
- https://google.github.io/styleguide/go/
- https://github.com/uber-go/guide
- https://pkg.go.dev/golang.org/x/tools
