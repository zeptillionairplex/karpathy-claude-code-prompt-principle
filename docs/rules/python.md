---
globs: "**/*.py"
---
# Python / FastAPI Rules

## Architecture: Clean Architecture

Dependency direction — outer depends on inner, never reverse:
```
infrastructure → interfaces/adapters → use_cases → entities
```

| Layer | Maps to | Role |
|-------|---------|------|
| `entities/` | Pydantic models | Pure domain types and business rules. Zero framework deps. |
| `use_cases/` | service | Application logic. Receives deps via constructor injection. |
| `interfaces/` | router | FastAPI routes — parse request, call use case, return response. |
| `infrastructure/` | repository | DB, external APIs. Implements interfaces defined in use_cases/. |

**Rules:**
- `entities/` models: Pydantic BaseModel only. No SQLAlchemy, no FastAPI imports.
- `use_cases/` accepts repository as an injected interface (ABC), never concrete class.
- `interfaces/` (router): no business logic. Validation via Pydantic, DI via `Depends()`.
- Each domain folder MUST have a `CLAUDE.md` listing its layer, purpose, and files.

## Async
- Use async/await consistently. No mixing with sync functions.
- DB operations must be async (asyncpg / SQLAlchemy async).

## Error Handling
→ See `docs/rules/error-handling.md` for full patterns (domain exceptions, FastAPI handlers, response format).

## Types
- Type hints required on all functions.
- Use `X | None` instead of `Optional[X]` (Python 3.10+).

## General
- Manage env vars with pydantic-settings BaseSettings.
- n8n API calls only from service layer.
