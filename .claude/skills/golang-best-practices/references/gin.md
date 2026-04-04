# Gin HTTP Framework

## Handler Structure

Every handler receives `*gin.Context` and belongs in the `interfaces/handler/` layer.
No business logic in handlers — call the service, return the response.

```go
// BAD: business logic in handler
func (h *OrderHandler) CreateOrder(c *gin.Context) {
    var req CreateOrderRequest
    c.ShouldBindJSON(&req)
    // validating, calculating totals, saving... all here
}

// GOOD: handler delegates to service
func (h *OrderHandler) CreateOrder(c *gin.Context) {
    var req CreateOrderRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error(), "code": "INVALID_REQUEST"})
        return
    }
    order, err := h.service.CreateOrder(c.Request.Context(), req.ToDTO())
    if err != nil {
        h.handleError(c, err)
        return
    }
    c.JSON(http.StatusCreated, gin.H{"data": order, "message": "ok"})
}
```

## Request Binding

**gin-bind-should** — Use `ShouldBindJSON` (not `BindJSON`). `BindJSON` calls `c.AbortWithError` internally, which fights with your own error handling.

```go
// BAD: BindJSON hijacks error response
if err := c.BindJSON(&req); err != nil { ... }

// GOOD: ShouldBindJSON returns error, you control the response
if err := c.ShouldBindJSON(&req); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error(), "code": "INVALID_REQUEST"})
    return
}
```

**gin-bind-validate** — Add `validate` struct tags and run `go-playground/validator` at the service boundary, not just in the handler.

```go
type CreateOrderRequest struct {
    UserID string  `json:"user_id" binding:"required,uuid"`
    Amount float64 `json:"amount"  binding:"required,gt=0"`
}
```

## Error Responses

**gin-error-format** — Always return the standard error envelope. Never `c.String()` for errors.

```go
// Standard error response
c.JSON(statusCode, gin.H{
    "error": "human-readable message",
    "code":  "MACHINE_READABLE_CODE",
})

// Standard success response
c.JSON(statusCode, gin.H{
    "data":    result,
    "message": "ok",
})
```

**gin-error-centralize** — Add a `handleError` helper on the handler struct to map domain errors to HTTP status codes. Don't repeat `switch err` blocks in every handler.

```go
func (h *OrderHandler) handleError(c *gin.Context, err error) {
    var notFound *domain.NotFoundError
    switch {
    case errors.As(err, &notFound):
        c.JSON(http.StatusNotFound, gin.H{"error": notFound.Error(), "code": "NOT_FOUND"})
    case errors.Is(err, domain.ErrUnauthorized):
        c.JSON(http.StatusUnauthorized, gin.H{"error": "unauthorized", "code": "UNAUTHORIZED"})
    default:
        h.logger.ErrorContext(c.Request.Context(), "unhandled error", "err", err)
        c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error", "code": "INTERNAL_ERROR"})
    }
}
```

## Middleware

**gin-middleware-next** — Always call `c.Next()` at the end of middleware that passes through. Call `c.Abort()` or `c.AbortWithStatus()` to stop the chain.

```go
func AuthMiddleware(svc AuthService) gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        claims, err := svc.ValidateToken(token)
        if err != nil {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
                "error": "invalid token",
                "code":  "UNAUTHORIZED",
            })
            return
        }
        c.Set("user_id", claims.UserID)
        c.Next()
    }
}
```

**gin-middleware-context** — Pass values downstream via `c.Set` / `c.Get`. Extract into typed helpers to avoid stringly-typed access.

```go
// helpers in shared/middleware/context.go
func SetUserID(c *gin.Context, id string) { c.Set("user_id", id) }
func GetUserID(c *gin.Context) (string, bool) {
    v, ok := c.Get("user_id")
    if !ok {
        return "", false
    }
    id, ok := v.(string)
    return id, ok
}
```

## Router Setup

**gin-router-group** — Group routes by domain and apply middleware at the group level.

```go
func SetupRouter(orderHandler *OrderHandler, authMW gin.HandlerFunc) *gin.Engine {
    r := gin.New()
    r.Use(gin.Recovery())
    r.Use(RequestIDMiddleware())
    r.Use(LoggerMiddleware())

    r.GET("/healthz", HealthHandler)
    r.GET("/readyz", ReadyHandler)

    v1 := r.Group("/api/v1")
    {
        orders := v1.Group("/orders", authMW)
        orders.POST("", orderHandler.CreateOrder)
        orders.GET("/:id", orderHandler.GetOrder)
        orders.PUT("/:id", orderHandler.UpdateOrder)
    }

    return r
}
```

**gin-no-global** — Never use `gin.Default()` in production. Build the engine with `gin.New()` and add only the middleware you control.

```go
// BAD: gin.Default() adds its own logger/recovery you can't configure
r := gin.Default()

// GOOD: explicit middleware stack
r := gin.New()
r.Use(gin.Recovery())
r.Use(yourStructuredLogger())
```

## Context Propagation

**gin-ctx-request** — Always use `c.Request.Context()` when passing context to services or DB calls. Never pass `c` itself past the handler boundary.

```go
// BAD: gin.Context leaks into service layer
func (s *OrderService) Create(c *gin.Context, ...) {}

// GOOD: standard context.Context
order, err := h.service.CreateOrder(c.Request.Context(), dto)
```

## Path & Query Parameters

**gin-param-validate** — Validate path params before use. `c.Param` always returns a string; parse and validate explicitly.

```go
func (h *OrderHandler) GetOrder(c *gin.Context) {
    id := c.Param("id")
    if _, err := uuid.Parse(id); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "invalid order id", "code": "INVALID_PARAM"})
        return
    }
    // proceed
}
```
