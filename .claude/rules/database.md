---
globs: "**/migrations/**, **/repository*, **/*_repository*, **/db/**, **/*.sql"
---
# Database / PostgreSQL / MinIO Rules

## PostgreSQL
- Always write up/down migration pairs.
- Require user confirmation before DROP, TRUNCATE, or DELETE without WHERE.
- Add indexes only after running EXPLAIN ANALYZE on the query.
- No N+1 queries — use JOIN or batch loading.

## Transactions
- Wrap multi-table changes in a transaction.
- No external API calls inside a transaction.

## MinIO
- Use presigned URLs for file uploads.
- Bucket names via env vars only. No hardcoding.
- Check object existence before deletion.

## General
- Never log sensitive data (PII, passwords).
- Always hash passwords with bcrypt or argon2.
