# Error Handling

## Core Rules

**err-wrap-context** — Always add context when wrapping errors.
```go
// BAD: loses context
return err

// GOOD: adds where it happened
return fmt.Errorf("fetching order %s: %w", id, err)
```

**err-log-once** — Log errors exactly once, at the top handler layer. Below that, just propagate.
```go
// BAD: logs at every layer
func (r *repo) Find(id string) (*Order, error) {
    if err != nil {
        log.Error("find failed", err)  // DON'T log here
        return nil, err
    }
}

// GOOD: propagate up, log only in handler
func (h *handler) GetOrder(w http.ResponseWriter, r *http.Request) {
    order, err := h.service.GetOrder(r.Context(), id)
    if err != nil {
        slog.Error("get order", "error", err, "id", id)
        http.Error(w, "internal error", 500)
        return
    }
}
```

**err-sentinel** — Define package-level sentinel errors for expected failures.
```go
// In the entity or service package
var (
    ErrNotFound   = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
)

// Caller checks with errors.Is
if errors.Is(err, order.ErrNotFound) {
    http.Error(w, "not found", 404)
}
```

**err-type-assert** — Use `errors.As` for typed errors, `errors.Is` for sentinel values.
```go
// BAD
if e, ok := err.(*ValidationError); ok { ... }

// GOOD
var ve *ValidationError
if errors.As(err, &ve) { ... }
```

**err-no-panic** — Never panic in library or service code.
```go
// OK: only in main/init for unrecoverable startup failures
func main() {
    db, err := sql.Open(...)
    if err != nil {
        log.Fatal("cannot open db", err)
    }
}

// NEVER in service/handler/repo
func (s *service) Process(ctx context.Context, id string) {
    // never panic here
}
```

## HTTP Error Responses

Always return structured JSON errors, never raw strings.
```go
type ErrorResponse struct {
    Error string `json:"error"`
    Code  string `json:"code"`
}

// Success: {"data": ..., "message": "ok"}
// Error:   {"error": "order not found", "code": "NOT_FOUND"}
```

Map domain errors to HTTP status codes in the handler layer only.
```go
func httpStatus(err error) int {
    switch {
    case errors.Is(err, ErrNotFound):     return 404
    case errors.Is(err, ErrUnauthorized): return 401
    case errors.Is(err, ErrValidation):   return 400
    default:                              return 500
    }
}
```
