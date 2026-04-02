# Database & Transactions

## Core Rules

**db-parameterized** — Never interpolate user input into SQL. Always use placeholders.
```go
// BAD: SQL injection risk
query := fmt.Sprintf("SELECT * FROM orders WHERE id = '%s'", userInput)

// GOOD: parameterized
row := db.QueryRowContext(ctx, "SELECT * FROM orders WHERE id = $1", id)
```

**db-context-first** — Pass `context.Context` to every DB call. Never use context-less variants.
```go
// BAD
db.Query("SELECT ...")
db.Exec("INSERT ...")

// GOOD
db.QueryContext(ctx, "SELECT ...")
db.ExecContext(ctx, "INSERT ...")
```

**db-transaction-wrap** — Wrap all multi-table mutations in a single transaction.
```go
tx, err := db.BeginTx(ctx, nil)
if err != nil {
    return fmt.Errorf("begin tx: %w", err)
}
defer func() {
    if p := recover(); p != nil {
        _ = tx.Rollback()
        panic(p)
    } else if err != nil {
        _ = tx.Rollback()
    } else {
        err = tx.Commit()
    }
}()

// all mutations use tx, not db
_, err = tx.ExecContext(ctx, "UPDATE orders SET ...", ...)
_, err = tx.ExecContext(ctx, "INSERT INTO events ...", ...)
```

**db-no-tx-http** — Never make HTTP or external API calls inside a transaction.
Transactions hold DB locks. External calls can be slow or fail, causing lock contention.

**db-connection-pool** — Always configure pool limits. Never use zero-value `sql.DB`.
```go
db.SetMaxOpenConns(25)
db.SetMaxIdleConns(10)
db.SetConnMaxLifetime(5 * time.Minute)
db.SetConnMaxIdleTime(2 * time.Minute)
```

## Scanning Rows

Always close rows and check for iteration errors.
```go
rows, err := db.QueryContext(ctx, "SELECT id, name FROM orders WHERE user_id = $1", userID)
if err != nil {
    return fmt.Errorf("query orders: %w", err)
}
defer rows.Close()

var orders []Order
for rows.Next() {
    var o Order
    if err := rows.Scan(&o.ID, &o.Name); err != nil {
        return fmt.Errorf("scan order: %w", err)
    }
    orders = append(orders, o)
}
if err := rows.Err(); err != nil {
    return fmt.Errorf("rows error: %w", err)
}
```

## Migrations

- Always write up AND down migrations.
- One migration file per schema change.
- Never modify an already-applied migration.
- Run migrations at startup or via CI, not manually in production.

```
migrations/
  001_create_orders.up.sql
  001_create_orders.down.sql
  002_add_status_index.up.sql
  002_add_status_index.down.sql
```

## Repository Pattern

Repository implements an interface defined in the use_cases layer.
```go
// defined in service layer (use_cases)
type OrderRepository interface {
    FindByID(ctx context.Context, id string) (*Order, error)
    Save(ctx context.Context, order *Order) error
    ListByUser(ctx context.Context, userID string) ([]Order, error)
}

// implemented in infrastructure layer
type postgresOrderRepository struct {
    db *sql.DB
}

func (r *postgresOrderRepository) FindByID(ctx context.Context, id string) (*Order, error) {
    // SQL only — no business logic here
}
```
