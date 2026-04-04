# Code Style & Naming

## Naming

**style-no-stutter** — Don't repeat the package name in exported identifiers.
```go
// BAD: called as user.UserService, user.UserID
package user
type UserService struct{}
type UserID string

// GOOD: called as user.Service, user.ID
package user
type Service struct{}
type ID string
```

**style-receiver-short** — Receiver name = 1-2 letter abbreviation of the type, consistent throughout.
```go
// BAD
func (orderService *OrderService) GetOrder(...) {}
func (self *OrderService) CreateOrder(...) {}

// GOOD
func (s *OrderService) GetOrder(...) {}
func (s *OrderService) CreateOrder(...) {}
```

**style-interface-small** — Prefer single-method or small interfaces. Compose larger ones.
```go
// BAD: hard to mock, hard to implement
type Repository interface {
    FindByID(ctx context.Context, id string) (*Order, error)
    Save(ctx context.Context, order *Order) error
    Delete(ctx context.Context, id string) error
    List(ctx context.Context, filter Filter) ([]Order, error)
    Count(ctx context.Context, filter Filter) (int, error)
}

// GOOD: compose what you need at the call site
type OrderReader interface {
    FindByID(ctx context.Context, id string) (*Order, error)
    List(ctx context.Context, filter Filter) ([]Order, error)
}
type OrderWriter interface {
    Save(ctx context.Context, order *Order) error
    Delete(ctx context.Context, id string) error
}
```

**style-error-lowercase** — Error strings are lowercase, no punctuation at end.
```go
// BAD
errors.New("Order not found.")
fmt.Errorf("Failed to connect to database: %w", err)

// GOOD
errors.New("order not found")
fmt.Errorf("connect to database: %w", err)
```

## Comments

**style-comment-exported** — Every exported symbol needs a doc comment starting with the name.
```go
// BAD
type OrderService struct{}

// GOOD
// OrderService handles the business logic for order management.
type OrderService struct{}

// GetOrder retrieves an order by its ID.
// Returns ErrNotFound if the order does not exist.
func (s *OrderService) GetOrder(ctx context.Context, id string) (*Order, error) {}
```

**style-comment-why** — Comments explain *why*, not *what*. Code explains itself.
```go
// BAD
// increment counter
counter++

// GOOD
// rate limiter uses token bucket; refill happens in background goroutine
counter++
```

## Structure

- Max function length: ~30 lines. Split if longer.
- Max file length: ~300 lines. Split by responsibility if longer.
- One struct per file for domain entities. Handlers can be grouped by resource.
- `internal/` for code not meant to be imported by external packages.
- Group imports: stdlib | external | internal (goimports does this automatically).

```go
import (
    "context"
    "fmt"

    "github.com/lib/pq"
    "go.uber.org/zap"

    "myapp/internal/order"
    "myapp/shared/errors"
)
```

## Struct Tags

Always use this order: `json`, `db`, `validate`.
```go
type Order struct {
    ID     string  `json:"id"     db:"id"     validate:"required,uuid"`
    Amount float64 `json:"amount" db:"amount" validate:"required,gt=0"`
}
```
