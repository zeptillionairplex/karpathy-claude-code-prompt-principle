# Observability

## Logging

**obs-structured-log** — Use `slog` (Go 1.21+ stdlib) with key-value pairs. Never `fmt.Println` or `log.Printf` in production code.
```go
import "log/slog"

// BAD
log.Printf("user %s created order %s", userID, orderID)

// GOOD
slog.Info("order created",
    "user_id", userID,
    "order_id", orderID,
    "amount", amount,
)
```

**obs-request-id** — Generate a request ID at ingress, store in context, include in every log line.
```go
// Middleware
func RequestID(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        id := uuid.New().String()
        ctx := context.WithValue(r.Context(), ctxKeyRequestID, id)
        w.Header().Set("X-Request-ID", id)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// In any handler/service
requestID := ctx.Value(ctxKeyRequestID).(string)
slog.Info("processing", "request_id", requestID, "order_id", orderID)
```

**obs-log-levels** — Use the right level:
- `Debug`: detailed flow, only in development
- `Info`: normal operations, key business events
- `Warn`: recoverable issues, degraded behavior
- `Error`: failures that need attention; always include `"error", err`

```go
slog.Error("failed to send notification",
    "error", err,
    "order_id", orderID,
    "user_id", userID,
)
```

## Metrics

**obs-metrics** — Expose Prometheus metrics for the four golden signals.
```go
import "github.com/prometheus/client_golang/prometheus"

var (
    httpRequestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{Name: "http_requests_total"},
        []string{"method", "path", "status"},
    )
    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "path"},
    )
)
```

Track at minimum: request rate, error rate, latency (p50/p95/p99), and saturation.

## Tracing

**obs-trace** — Wrap external calls with OpenTelemetry spans.
```go
import "go.opentelemetry.io/otel"

func (s *OrderService) GetOrder(ctx context.Context, id string) (*Order, error) {
    ctx, span := otel.Tracer("order-service").Start(ctx, "GetOrder")
    defer span.End()

    order, err := s.repo.FindByID(ctx, id)
    if err != nil {
        span.RecordError(err)
        return nil, fmt.Errorf("get order: %w", err)
    }
    return order, nil
}
```

## Health Checks

Expose `/healthz` (liveness) and `/readyz` (readiness) endpoints.
```go
// Liveness: is the process running?
mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(200)
})

// Readiness: can it serve traffic? (check DB, cache, etc.)
mux.HandleFunc("/readyz", func(w http.ResponseWriter, r *http.Request) {
    if err := db.PingContext(r.Context()); err != nil {
        http.Error(w, "db not ready", 503)
        return
    }
    w.WriteHeader(200)
})
```
