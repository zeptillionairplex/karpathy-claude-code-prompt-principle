# Error Handling

## Principle

Define errors in the domain layer. Propagate upward. Map to HTTP codes only at the delivery layer.

```
Domain defines:   ErrNotFound, ErrConflict, ErrForbidden
UseCase returns:  domain errors (wrapped with context)
Handler maps:     domain error → HTTP status code
```

Never log the same error twice. Log once at the boundary where it's handled.

---

## Go

### Domain errors

```go
// internal/domain/errors.go
var (
    ErrNotFound  = errors.New("not found")
    ErrConflict  = errors.New("conflict")
    ErrForbidden = errors.New("forbidden")
)
```

### UseCase — wrap with context

```go
func (uc *articleUseCase) GetByID(ctx context.Context, id int64) (entity.Article, error) {
    article, err := uc.repo.GetByID(ctx, id)
    if err != nil {
        return entity.Article{}, fmt.Errorf("articleUseCase.GetByID: %w", err)
    }
    return article, nil
}
```

### Handler — central error middleware

```go
// internal/delivery/http/middleware/error_handler.go
func ErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()
        for _, err := range c.Errors {
            switch {
            case errors.Is(err.Err, domain.ErrNotFound):
                c.JSON(http.StatusNotFound, errorResponse(err.Error()))
            case errors.Is(err.Err, domain.ErrConflict):
                c.JSON(http.StatusConflict, errorResponse(err.Error()))
            case errors.Is(err.Err, domain.ErrForbidden):
                c.JSON(http.StatusForbidden, errorResponse(err.Error()))
            default:
                log.Error(err.Err)
                c.JSON(http.StatusInternalServerError, errorResponse("internal server error"))
            }
            return
        }
    }
}

// Handler — push error into gin, don't respond directly
func (h *ArticleHandler) GetByID(c *gin.Context) {
    article, err := h.useCase.GetByID(c.Request.Context(), id)
    if err != nil {
        c.Error(err)   // middleware handles response
        return
    }
    c.JSON(http.StatusOK, response.Success(article))
}
```

### Rules (Go)
- Use `fmt.Errorf("context: %w", err)` to wrap, `errors.Is()` / `errors.As()` to unwrap.
- No `panic` outside initialization code.
- Log only in the middleware, not in use cases or repositories.

---

## Python

### Domain exceptions

```python
# app/core/exceptions.py
class DomainError(Exception):
    pass

class NotFoundError(DomainError):
    def __init__(self, resource: str, id: int):
        super().__init__(f"{resource} with id {id} not found")

class ConflictError(DomainError):
    pass

class ForbiddenError(DomainError):
    pass
```

### UseCase — raise domain exceptions

```python
async def execute(self, article_id: int) -> Article:
    article = await self._repo.get_by_id(article_id)
    if article is None:
        raise NotFoundError("Article", article_id)
    return article
```

### FastAPI — central exception handler

```python
# app/core/middleware.py
from fastapi import Request
from fastapi.responses import JSONResponse

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content=error_body(str(exc)))

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError):
        return JSONResponse(status_code=409, content=error_body(str(exc)))

    @app.exception_handler(ForbiddenError)
    async def forbidden_handler(request: Request, exc: ForbiddenError):
        return JSONResponse(status_code=403, content=error_body(str(exc)))
```

### Rules (Python)
- Use `HTTPException` only for framework-level errors (auth, validation). Business errors use domain exceptions.
- Type-hint all exception classes. Register handlers in `app/core/middleware.py`.
- Never catch and swallow exceptions silently.

---

## Unified Error Response Format

Both Go and Python APIs return this shape:

```json
{
  "error": {
    "code": "ARTICLE_NOT_FOUND",
    "message": "Article with id 123 not found"
  }
}
```

`code` is UPPER_SNAKE_CASE. `message` is human-readable. No stack traces in production responses.
