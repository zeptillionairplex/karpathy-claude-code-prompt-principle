# Testing

## Core Rules

**test-table-driven** — Use table-driven tests for all non-trivial logic.
```go
func TestCalculateDiscount(t *testing.T) {
    tests := []struct {
        name     string
        price    float64
        quantity int
        want     float64
    }{
        {"no discount under 10", 100.0, 5, 0.0},
        {"10% discount at 10", 100.0, 10, 10.0},
        {"20% discount at 20", 100.0, 20, 20.0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := CalculateDiscount(tt.price, tt.quantity)
            assert.Equal(t, tt.want, got)
        })
    }
}
```

**test-real-db** — Repository tests use a real DB (test container or local). No SQL mocks.
Mocked SQL lets wrong queries pass. Use `github.com/testcontainers/testcontainers-go` or
a local test DB set up in `TestMain`.

**test-testify** — Use `require` for fatal assertions, `assert` for non-fatal.
```go
import (
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestCreateOrder(t *testing.T) {
    order, err := service.CreateOrder(ctx, input)
    require.NoError(t, err)           // stops test if fails
    assert.Equal(t, "pending", order.Status)  // continues on fail
    assert.NotEmpty(t, order.ID)
}
```

**test-parallel** — Call `t.Parallel()` at the top of all unit tests.
```go
func TestSomething(t *testing.T) {
    t.Parallel()
    // ...
}
```

**test-helpers** — Shared test setup goes in `internal/testutils/` package.
```go
// internal/testutils/db.go
func NewTestDB(t *testing.T) *sql.DB {
    t.Helper()
    db := setupTestDB()
    t.Cleanup(func() { db.Close() })
    return db
}
```

## Test Structure

```
internal/{domain}/
  service/
    order_service.go
    order_service_test.go       # unit test (mock repo)
  repository/
    order_repository.go
    order_repository_test.go    # integration test (real DB)
internal/testutils/
  db.go                         # shared DB setup
  fixtures.go                   # test data builders
```

## Naming

Test function names describe behavior:
```go
// BAD
func TestOrder(t *testing.T) {}

// GOOD
func TestCreateOrder_ShouldReturnErrorWhenStockIsEmpty(t *testing.T) {}
func TestGetOrder_ShouldReturn404WhenNotFound(t *testing.T) {}
```

## HTTP Handler Testing

Test handlers through `httptest` without starting a real server.
```go
func TestGetOrderHandler(t *testing.T) {
    t.Parallel()
    svc := &mockOrderService{order: &Order{ID: "123"}}
    h := NewOrderHandler(svc)

    req := httptest.NewRequest(http.MethodGet, "/orders/123", nil)
    w := httptest.NewRecorder()
    h.GetOrder(w, req)

    assert.Equal(t, 200, w.Code)
    var resp OrderResponse
    require.NoError(t, json.NewDecoder(w.Body).Decode(&resp))
    assert.Equal(t, "123", resp.ID)
}
```
