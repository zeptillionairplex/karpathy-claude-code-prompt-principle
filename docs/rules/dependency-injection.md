# Dependency Injection

## Principle

Dependencies flow inward. Outer layers receive inner layer interfaces via constructor injection — never instantiate concrete dependencies inside business logic.

```
main.go / dependencies.py
    │
    ├─ creates: Repository (concrete, infrastructure)
    ├─ creates: UseCase(repo interface)        ← receives interface, not concrete
    └─ creates: Handler(usecase interface)     ← receives interface, not concrete
```

---

## Go — Manual DI (small to medium projects)

Assemble all dependencies in `cmd/main.go`. No framework needed.

```go
func main() {
    db    := initDB()
    cache := initRedis()

    // Infrastructure layer — concrete implementations
    articleRepo := mysql.NewArticleRepository(db)
    cacheRepo   := redis.NewCacheRepository(cache)

    // Use case layer — receives domain interfaces
    articleUC := usecase.NewArticleUseCase(articleRepo, cacheRepo)

    // Handler layer — receives use case interfaces
    articleHandler := handler.NewArticleHandler(articleUC)

    r := setupRouter(articleHandler)
    r.Run(":8080")
}
```

Constructor signature pattern:

```go
// use case accepts repository interface (defined in domain layer)
func NewArticleUseCase(
    repo repository.ArticleRepository,   // interface, not *mysqlArticleRepository
    cache repository.CacheRepository,
    timeout time.Duration,
) ArticleUseCase {
    return &articleUseCase{repo: repo, cache: cache, timeout: timeout}
}
```

## Go — Google Wire (large projects)

Wire generates the wiring code at compile time from provider declarations.

```go
// wire.go  (build tag prevents compilation)
//go:build wireinject

func InitializeServer() (*http.Server, error) {
    wire.Build(
        initDB,
        mysql.NewArticleRepository,
        usecase.NewArticleUseCase,
        handler.NewArticleHandler,
        newServer,
    )
    return nil, nil
}
```

Group providers by layer in separate `ProviderSet` variables to keep wire files readable.

---

## Python — FastAPI `Depends()`

Chain dependency functions. FastAPI caches each function's result within a single request scope.

```python
# core/database.py
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session          # session closed automatically after request

# modules/article/presentation/dependencies.py
async def get_article_repo(
    session: AsyncSession = Depends(get_db_session),
) -> ArticleRepository:
    return ArticleRepository(session)

async def get_article_use_case(
    repo: ArticleRepository = Depends(get_article_repo),
) -> GetArticleUseCase:
    return GetArticleUseCase(repo)

# modules/article/presentation/routers.py
@router.get("/{article_id}")
async def get_article(
    article_id: int,
    use_case: GetArticleUseCase = Depends(get_article_use_case),
):
    return await use_case.execute(article_id)
```

## Python — Overriding for Tests

```python
# tests/conftest.py
def override_get_db_session():
    yield test_session

app.dependency_overrides[get_db_session] = override_get_db_session
```

---

## Rules

- Never call `SomeRepository()` inside a use case. Receive it via constructor.
- Never import concrete infrastructure types in use case or domain layers.
- Repository interfaces belong in the domain or application layer — not infrastructure.
- In Go: one `New*` constructor per type, always returning the interface.
- In Python: one `get_*` dependency function per injectable, chained via `Depends()`.
