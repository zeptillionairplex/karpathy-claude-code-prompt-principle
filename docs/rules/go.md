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
→ See `docs/rules/error-handling.md` for full patterns (domain errors, central middleware, wrapping rules).

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

## Layer Code Patterns

### Domain entity
```go
// internal/domain/entity/article.go
type Article struct {
    ID        int64     `json:"id"`
    Title     string    `json:"title"    validate:"required"`
    Content   string    `json:"content"  validate:"required"`
    AuthorID  int64     `json:"author_id"`
    CreatedAt time.Time `json:"created_at"`
    UpdatedAt time.Time `json:"updated_at"`
}
```

### Repository interface (defined in domain, implemented in infrastructure)
```go
// internal/domain/repository/article_repository.go
type ArticleRepository interface {
    GetByID(ctx context.Context, id int64) (entity.Article, error)
    Store(ctx context.Context, a *entity.Article) error
    Update(ctx context.Context, a *entity.Article) error
    Delete(ctx context.Context, id int64) error
}
```

### UseCase
```go
// internal/usecase/article_usecase.go
type ArticleUseCase interface {
    GetByID(ctx context.Context, id int64) (entity.Article, error)
}

type articleUseCase struct {
    repo    repository.ArticleRepository
    timeout time.Duration
}

func NewArticleUseCase(repo repository.ArticleRepository, timeout time.Duration) ArticleUseCase {
    return &articleUseCase{repo: repo, timeout: timeout}
}

func (uc *articleUseCase) GetByID(ctx context.Context, id int64) (entity.Article, error) {
    ctx, cancel := context.WithTimeout(ctx, uc.timeout)
    defer cancel()
    article, err := uc.repo.GetByID(ctx, id)
    if err != nil {
        return entity.Article{}, fmt.Errorf("articleUseCase.GetByID: %w", err)
    }
    return article, nil
}
```

### Handler (delivery)
```go
// internal/delivery/http/handler/article_handler.go
type ArticleHandler struct{ useCase usecase.ArticleUseCase }

func NewArticleHandler(uc usecase.ArticleUseCase) *ArticleHandler {
    return &ArticleHandler{useCase: uc}
}

func (h *ArticleHandler) GetByID(c *gin.Context) {
    id, err := strconv.ParseInt(c.Param("id"), 10, 64)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "invalid id"})
        return
    }
    article, err := h.useCase.GetByID(c.Request.Context(), id)
    if err != nil {
        c.Error(err) // central error middleware handles response
        return
    }
    c.JSON(http.StatusOK, gin.H{"data": article})
}
```

### DI assembly (main.go)
```go
func main() {
    db         := initDB()
    articleRepo := postgres.NewArticleRepository(db)
    articleUC   := usecase.NewArticleUseCase(articleRepo, 5*time.Second)
    articleH    := handler.NewArticleHandler(articleUC)

    r := gin.Default()
    r.Use(middleware.ErrorHandler())
    r.GET("/articles/:id", articleH.GetByID)
    r.Run(":8080")
}
```

→ See `docs/rules/dependency-injection.md` for Wire setup.
→ See `docs/rules/error-handling.md` for central error middleware.

## Required Skills

When writing, reviewing, or refactoring Go code, **always apply these skills:**

| Situation | Skill |
|-----------|-------|
| Any Go code | `/golang-best-practices` |
| DB / repository layer | `/golang-best-practices` + `/supabase-postgres-best-practices` |

**If skills are not installed:**
```bash
npx skills add supabase/agent-skills -y -a claude-code
```
(`golang-best-practices` is a local skill in `.claude/skills/` — no install needed.)
