---
globs: "**/*.test.ts, **/*.test.tsx, **/*.spec.ts, **/*_test.go, **/test_*.py, **/__tests__/**"
---
# Testing Rules

## General
- Test behavior, not implementation internals.
- Test name format: "should [action] when [condition]"
- One assertion per test.

## TypeScript (Vitest / Jest)
- Component tests: React Testing Library.
- Query by user-facing attributes (getByRole, getByText first).
- Mock API calls with msw.

## Go
- Use table-driven test pattern.
- DB tests use real DB. No mocks.
- Test helpers go in testutils/ package.

## Python (pytest)
- Use fixtures for shared setup.
- Isolate DB tests with transaction rollback.
- Use pytest-asyncio for async tests.
