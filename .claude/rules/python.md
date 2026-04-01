---
globs: "**/*.py"
---
# Python / FastAPI Rules

## Structure
- router → service → repository layer separation.
- Pydantic models for request/response type enforcement.
- Dependency injection via FastAPI Depends().

## Async
- Use async/await consistently. No mixing with sync functions.
- DB operations must be async (asyncpg / SQLAlchemy async).

## Error Handling
- Use HTTPException with explicit status codes.
- Define custom Exception classes for predictable errors.

## Types
- Type hints required on all functions.
- Use `X | None` instead of `Optional[X]` (Python 3.10+).

## General
- Manage env vars with pydantic-settings BaseSettings.
- n8n API calls only from service layer.
