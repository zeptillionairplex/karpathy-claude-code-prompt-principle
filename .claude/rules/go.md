---
globs: "**/*.go"
---
# Go / Gin Rules

## Layer Structure
- handler → service → repository. No reverse direction.
- handler: HTTP parsing, validation, response serialization only.
- service: business logic only. No direct DB access.
- repository: DB queries only. No business logic.

## Error Handling
- Propagate errors upward. Log only at handler layer.
- Add context with fmt.Errorf("...: %w", err).
- No panic — except initialization code.

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
