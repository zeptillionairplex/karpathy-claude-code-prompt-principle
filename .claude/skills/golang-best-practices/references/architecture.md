# Architecture & Project Layout

## Clean Architecture Layers

Dependency direction — outer depends on inner, never reverse:
```
infrastructure → interfaces → use_cases → entities
```

| Layer | Folder | Role |
|-------|--------|------|
| entities | `internal/{domain}/entity/` | Pure domain types. Zero external imports. |
| use_cases | `internal/{domain}/service/` | Orchestrates entities. Receives repos via interface. |
| interfaces | `internal/{domain}/handler/` | HTTP/gRPC. Parses request, calls service, returns response. |
| infrastructure | `internal/{domain}/repository/` | DB, cache, external APIs. No business logic. |

## Standard Project Layout

```
cmd/
  server/main.go          # entry point only — wire deps, start server
internal/
  {domain}/
    CLAUDE.md             # layer, purpose, files, public API
    entity/               # domain types, value objects
    service/              # use cases, business logic
    handler/              # HTTP handlers
    repository/           # DB queries
shared/
  middleware/             # auth, logging, rate-limit
  infrastructure/         # DB pool, cache client, HTTP client
  errors/                 # shared error types
migrations/               # SQL migration files (up + down)
```

## Rules

**arch-clean-layers** — Imports flow inward only.
```go
// BAD: service imports repository directly
type OrderService struct {
    repo *PostgresOrderRepository  // concrete type
}

// GOOD: service depends on interface
type OrderService struct {
    repo OrderRepository  // interface defined in use_cases layer
}
type OrderRepository interface {
    FindByID(ctx context.Context, id OrderID) (*Order, error)
    Save(ctx context.Context, order *Order) error
}
```

**arch-domain-folder** — One folder per domain. All related code lives there.
A developer working on `orders` must not need to read the `payments` folder.
Each domain folder has a `CLAUDE.md` describing its layer and public API.

**arch-no-circular** — Sibling domains never import each other.
```go
// BAD: orders imports payments
import "myapp/internal/payments"

// GOOD: extract shared type to shared/
import "myapp/shared/money"
```

**arch-cmd-thin** — `main.go` only wires dependencies and starts the server.
No business logic, no DB queries, no HTTP routing in main.

## Dependency Injection

Wire deps manually in `main.go` or use a DI container (samber/do, google/wire).
Always inject via constructor, never use global vars for dependencies.

```go
// GOOD: constructor injection
func NewOrderService(repo OrderRepository, events EventPublisher) *OrderService {
    return &OrderService{repo: repo, events: events}
}
```
